import { NextRequest, NextResponse } from "next/server";
import type { ErrorCode, ErrorStage } from "@careloop/contracts";
import { ERROR_CODES } from "@careloop/contracts";
import { auditTurn, buildAuditPayload } from "@/lib/audit";
import { writeAuditToDb } from "@/lib/audit-db";
import { writeStageTimingsToDb } from "@/lib/performance-metrics";
import { retrievePolicyEvidence } from "@/lib/retrieval";
import type { RetrievalResult } from "@/lib/retrieval";
import {
  generateLLMResponse,
  buildSystemPrompt,
  isLLMAvailable,
} from "@/lib/llm";
import type { LLMMessage } from "@/lib/llm";

const VALID_ERROR_CODES = new Set<string>(ERROR_CODES);
function isErrorCode(s: unknown): s is ErrorCode {
  return typeof s === "string" && VALID_ERROR_CODES.has(s);
}

export const dynamic = "force-dynamic";

function errorResponse(
  error_code: ErrorCode,
  message: string,
  status: number,
  options?: { stage?: ErrorStage; retryable?: boolean; session_id?: string; request_id?: string; fallback_content?: string }
): NextResponse {
  const envelope = {
    success: false as const,
    error: {
      error_code,
      message,
      stage: options?.stage ?? "unknown",
      retryable: options?.retryable ?? false,
      session_id: options?.session_id,
      request_id: options?.request_id,
    },
    fallback_content: options?.fallback_content,
    timestamp: new Date().toISOString(),
  };
  return NextResponse.json(envelope, { status });
}

const WEBHOOK_URL =
  process.env.N8N_WEBHOOK_URL || process.env.NEXT_PUBLIC_N8N_WEBHOOK_URL || "http://localhost:5678";
const N8N_TIMEOUT_MS = Number.parseInt(process.env.N8N_TIMEOUT_MS ?? "60000", 10);

const POLICY_KEYWORDS = [
  "benefit", "benefits", "eligibility", "eligible", "procedure", "policy",
  "official", "form", "forms", "document", "documents", "source", "sources",
  "deadline", "deadlines", "allowance", "invalidenversicherung", "iv", "el",
  "zurich", "canton", "spitex", "ahv", "supplementary", "social",
  "insurance", "registration", "disability", "caregiver", "care",
];
const EDUCATION_KEYWORDS = [
  "how to", "steps", "step-by-step", "plan", "routine", "practice",
  "technique", "guide", "learn", "checklist", "method", "prioritize",
  "actionable", "next steps", "manage", "organize", "tips",
];
const EMOTIONAL_KEYWORDS = [
  "feel", "feeling", "stressed", "anxious", "anxiety", "overwhelmed",
  "sad", "worried", "burned out", "panic", "lonely", "lost", "support",
  "reassurance", "cope", "help me",
];

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function hasKeyword(lowerText: string, keyword: string): boolean {
  const kw = keyword.toLowerCase();
  if (/^[a-z0-9]+$/.test(kw) && kw.length <= 3) {
    const re = new RegExp(`\\b${escapeRegExp(kw)}\\b`, "i");
    return re.test(lowerText);
  }
  return lowerText.includes(kw);
}

function scoreByKeywords(text: string, keywords: string[]): number {
  const lower = text.toLowerCase();
  return keywords.reduce((score, keyword) => (hasKeyword(lower, keyword) ? score + 1 : score), 0);
}

/**
 * Fallback intent inference for the current message alone.
 */
function inferCoachingModeFallback(message: string): "emotional_support" | "practical_education" | "policy_navigation" | "mixed" {
  const policyScore = scoreByKeywords(message, POLICY_KEYWORDS);
  const educationScore = scoreByKeywords(message, EDUCATION_KEYWORDS);
  const emotionalScore = scoreByKeywords(message, EMOTIONAL_KEYWORDS);

  if (policyScore > 0 && emotionalScore > 0) return "mixed";
  if (policyScore >= Math.max(educationScore, emotionalScore) && policyScore > 0) return "policy_navigation";
  if (educationScore >= emotionalScore && educationScore > 0) return "practical_education";
  return "emotional_support";
}

interface ConversationMessage {
  role: string;
  content: string;
}

/**
 * Context-aware intent inference: for short follow-up messages (e.g. "tell me more"),
 * look at the recent conversation to maintain topic continuity.
 */
function inferIntentWithHistory(
  currentMessage: string,
  conversationHistory: ConversationMessage[]
): "emotional_support" | "practical_education" | "policy_navigation" | "mixed" {
  const directIntent = inferCoachingModeFallback(currentMessage);

  // If the current message has clear keywords, trust them
  if (directIntent !== "emotional_support") return directIntent;

  // For short / ambiguous follow-ups, inherit topic from recent conversation
  const wordCount = currentMessage.trim().split(/\s+/).length;
  const isShortFollowUp = wordCount <= 10;
  if (!isShortFollowUp || conversationHistory.length === 0) return directIntent;

  // Check if recent conversation was about policy or education
  const recentText = conversationHistory
    .slice(-6)
    .map((m) => m.content)
    .join(" ");
  const recentPolicyScore = scoreByKeywords(recentText, POLICY_KEYWORDS);
  const recentEducationScore = scoreByKeywords(recentText, EDUCATION_KEYWORDS);

  if (recentPolicyScore >= 3) return "policy_navigation";
  if (recentEducationScore >= 3) return "practical_education";

  return directIntent;
}

/**
 * Extract the last user message about policy from conversation history.
 * Used as the retrieval query when the current message is a vague follow-up.
 */
function getRetrievalQuery(
  currentMessage: string,
  conversationHistory: ConversationMessage[]
): string {
  const directPolicyScore = scoreByKeywords(currentMessage, POLICY_KEYWORDS);
  if (directPolicyScore >= 2 || currentMessage.trim().split(/\s+/).length > 10) {
    return currentMessage;
  }

  // For short follow-ups, find the last substantive user message about policy
  for (let i = conversationHistory.length - 1; i >= 0; i--) {
    const msg = conversationHistory[i];
    if (msg.role !== "user") continue;
    const score = scoreByKeywords(msg.content, POLICY_KEYWORDS);
    if (score >= 1 && msg.content.trim().split(/\s+/).length > 5) {
      return msg.content;
    }
  }

  return currentMessage;
}

export function GET() {
  return NextResponse.json({
    ok: true,
    endpoint: "/api/chat",
    method: "POST",
    hint: "Send POST with body: { session_id, turn_index, message, context }.",
  });
}

function generateRequestId(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

export async function POST(request: NextRequest) {
  let request_id: string = generateRequestId();
  const startedAt = Date.now();
  try {
    const body = await request.json();
    request_id = body?.request_id ?? request.headers.get("x-request-id") ?? generateRequestId();
    const bodyWithRequestId = { ...body, request_id };
    const userMessage = String(body?.message ?? "");

    // Conversation history from the frontend (last N messages)
    const conversationHistory: ConversationMessage[] = Array.isArray(body?.messages)
      ? (body.messages as ConversationMessage[]).filter(
          (m) => typeof m.role === "string" && typeof m.content === "string"
        )
      : [];

    // Context-aware intent inference using conversation history
    const fallbackMode = inferIntentWithHistory(userMessage, conversationHistory);

    // Vector retrieval for policy AND education intents
    let retrieval: RetrievalResult | null = null;
    const needsRetrieval =
      fallbackMode === "policy_navigation" ||
      fallbackMode === "mixed" ||
      fallbackMode === "practical_education";
    if (needsRetrieval && userMessage.trim().length > 0) {
      try {
        const retrievalQuery = getRetrievalQuery(userMessage, conversationHistory);
        retrieval = await retrievePolicyEvidence(retrievalQuery);
      } catch (err) {
        console.error("[chat] Retrieval error (continuing without evidence):", err);
      }
    }

    const n8nPayload = {
      ...bodyWithRequestId,
      ...(retrieval && retrieval.evidence.length > 0
        ? {
            prefetched_evidence: retrieval.evidence,
            retrieval_meta: {
              method: retrieval.method,
              query_embedding_ms: retrieval.query_embedding_ms,
              search_ms: retrieval.search_ms,
              total_ms: retrieval.total_ms,
              count: retrieval.evidence.length,
            },
          }
        : {}),
    };

    const workflowPath =
      body?.workflow === "simple" ? "careloop-turn-simple" : "careloop-turn";
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), N8N_TIMEOUT_MS);
    const res = await fetch(`${WEBHOOK_URL}/webhook/${workflowPath}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(n8nPayload),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    const raw = await res.json().catch(() => ({}));
    const data = Array.isArray(raw) ? raw[0] : raw;

    if (!res.ok) {
      const message =
        res.status === 404
          ? "N8N webhook not found. Import and activate careloop-simplified.json in N8N (http://localhost:5678)."
          : (data?.error?.message ?? data?.error ?? data?.message ?? `Upstream ${res.status}`);
      return errorResponse(
        "internal_error",
        message,
        res.status,
        { stage: "generation", retryable: res.status >= 500, session_id: body?.session_id, request_id }
      );
    }

    // N8N returned 200 but body is error envelope
    if (data && typeof data === "object" && data.success === false && data.error && typeof data.error === "object") {
      const err = data.error as { error_code?: string; message?: string; stage?: string };
      const code = isErrorCode(err.error_code) ? err.error_code : "internal_error";
      const message = typeof err.message === "string" ? err.message : "Workflow returned an error.";
      return errorResponse(code, message, 503, {
        stage: "generation",
        retryable: true,
        session_id: body?.session_id,
        request_id: (data as { request_id?: string }).request_id ?? request_id,
        fallback_content: (data as { fallback_content?: string }).fallback_content,
      });
    }

    // Malformed or empty response
    if (!data || typeof data !== "object") {
      return errorResponse(
        "internal_error",
        "Invalid response from workflow (no data).",
        503,
        { stage: "generation", retryable: true, session_id: body?.session_id, request_id }
      );
    }
    const hasMessage = data.message && typeof data.message === "object" && typeof (data.message as { content?: unknown }).content === "string";
    if (!data.session_id || !hasMessage) {
      return errorResponse(
        "verifier_fallback",
        "Workflow response missing required fields (session_id or message.content).",
        503,
        { stage: "verification", retryable: true, session_id: body?.session_id, request_id }
      );
    }

    if (!data.coaching_mode) {
      data.coaching_mode = fallbackMode;
    }

    // Override N8N's mode when our context-aware inference disagrees and we have evidence.
    // N8N has no conversation history, so short follow-ups like "tell me more" get
    // mis-classified as emotional_support even when the conversation is about policy/education.
    if (
      retrieval &&
      retrieval.evidence.length > 0 &&
      (fallbackMode === "policy_navigation" || fallbackMode === "mixed" || fallbackMode === "practical_education") &&
      data.coaching_mode !== fallbackMode
    ) {
      data.coaching_mode = fallbackMode;
    }

    // ── LLM regeneration: replace heuristic responses with real LLM output ──
    // The N8N format node flattens generator status into pipeline_status/debug.
    const pipelineStatus = data.pipeline_status as Record<string, unknown> | undefined;
    const debugInfo = data.debug as Record<string, unknown> | undefined;
    const regulation = data.regulation as { directives?: string[] } | undefined;
    const isHeuristic =
      pipelineStatus?.generator === "heuristic" ||
      pipelineStatus?.generator === "fallback" ||
      typeof debugInfo?.generation_error === "string";

    if (isHeuristic && isLLMAvailable()) {
      const coachingMode = String(data.coaching_mode || "emotional_support");
      const evidence = retrieval?.evidence?.map((e) => ({
        source_id: e.source_id,
        title: e.title,
        content: e.content,
        url: e.url,
      }));

      const systemPrompt = buildSystemPrompt(
        coachingMode,
        evidence,
        Array.isArray(regulation?.directives) ? regulation.directives : undefined
      );

      const llmMessages: LLMMessage[] = [
        { role: "system", content: systemPrompt },
      ];

      // Include conversation history for multi-turn context
      const historySlice = conversationHistory.slice(-8);
      for (const m of historySlice) {
        if (m.role === "user" || m.role === "assistant") {
          llmMessages.push({
            role: m.role as "user" | "assistant",
            content: m.content,
          });
        }
      }

      // Current user message (may already be in historySlice, avoid duplication)
      const lastInHistory = historySlice[historySlice.length - 1];
      if (!lastInHistory || lastInHistory.role !== "user" || lastInHistory.content !== userMessage) {
        llmMessages.push({ role: "user", content: userMessage });
      }

      try {
        const llmResult = await generateLLMResponse(llmMessages);
        if (llmResult) {
          const msg = data.message as { content?: string };
          msg.content = llmResult.content;
          data.reply = llmResult.content;

          // Update pipeline status to reflect LLM regeneration
          if (pipelineStatus) {
            pipelineStatus.generator = "nvidia";
            pipelineStatus.generation_source = "api-route";
          }
          if (debugInfo) {
            debugInfo.generation_error = null;
            debugInfo.regeneration_ms = llmResult.duration_ms;
            debugInfo.regeneration_model = llmResult.model;
          }

          console.log(
            `[chat] LLM regeneration replaced heuristic (${llmResult.duration_ms}ms, ${llmResult.model})`
          );
        }
      } catch (err) {
        console.error("[chat] LLM regeneration failed, keeping N8N response:", err);
      }
    }

    // Overlay vector retrieval citations onto response
    if (retrieval && retrieval.evidence.length > 0) {
      const mode = data.coaching_mode as string;
      if (mode === "policy_navigation" || mode === "mixed" || mode === "practical_education") {
        const pn = (data.policy_navigation ?? {}) as Record<string, unknown>;
        pn.citations = retrieval.evidence.map((e) => ({
          source_id: e.source_id,
          title: e.title,
          url: e.url,
          similarity: e.similarity,
          retrieval_method: e.retrieval_method,
        }));
        data.policy_navigation = pn;

        const ps = (data.pipeline_status ?? {}) as Record<string, unknown>;
        ps.retrieval = "ok";
        ps.retrieval_method = retrieval.method;
        data.pipeline_status = ps;

        (data as Record<string, unknown>).retrieval_timing = {
          method: retrieval.method,
          query_embedding_ms: retrieval.query_embedding_ms,
          search_ms: retrieval.search_ms,
          total_ms: retrieval.total_ms,
          evidence_count: retrieval.evidence.length,
        };
      }
    }

    if (request_id && !data.request_id) {
      data.request_id = request_id;
    }

    // Audit
    const latencyMs = Date.now() - startedAt;
    const auditPayload = buildAuditPayload(
      data as Record<string, unknown>,
      body as { session_id?: string; turn_index?: number; message?: string },
      {
        messageForHash: typeof body?.message === "string" ? body.message : undefined,
        latencyMs,
      }
    );
    auditTurn(auditPayload);
    writeAuditToDb(auditPayload);
    if (Array.isArray((data as { stage_timings?: unknown }).stage_timings)) {
      const sid = body?.session_id;
      const tid = body?.turn_index;
      if (typeof sid === "string" && typeof tid === "number") {
        writeStageTimingsToDb(sid, tid, (data as { stage_timings: unknown }).stage_timings);
      }
    }
    return NextResponse.json(data);
  } catch (e) {
    const isTimeout = e instanceof Error && e.name === "AbortError";
    const message = isTimeout
      ? "Request to N8N timed out. Check that N8N is running and the workflow is active."
      : e instanceof Error
        ? e.message
        : "Request failed";
    return errorResponse(
      isTimeout ? "timeout_fallback" : "internal_error",
      message,
      500,
      { stage: "generation", retryable: isTimeout, request_id }
    );
  }
}
