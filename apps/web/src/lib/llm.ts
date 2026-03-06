/**
 * Direct LLM generation via NVIDIA API.
 * Used as fallback when N8N generation returns heuristic responses,
 * and for all cases where we want conversation-context-aware responses.
 */

const NVIDIA_API_URL =
  process.env.NVIDIA_API_URL ||
  "https://integrate.api.nvidia.com/v1/chat/completions";
const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY || "";
const NVIDIA_MODEL = process.env.NVIDIA_MODEL || "google/gemma-3n-e4b-it";

export interface LLMMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface LLMOptions {
  temperature?: number;
  max_tokens?: number;
  model?: string;
  timeoutMs?: number;
}

export interface LLMResult {
  content: string;
  model: string;
  duration_ms: number;
}

export function isLLMAvailable(): boolean {
  return NVIDIA_API_KEY.length > 10;
}

/**
 * Call the NVIDIA LLM API with multi-turn messages.
 * Returns null on failure (caller should keep existing response).
 */
export async function generateLLMResponse(
  messages: LLMMessage[],
  options?: LLMOptions
): Promise<LLMResult | null> {
  if (!isLLMAvailable()) return null;

  const model = options?.model || NVIDIA_MODEL;
  const t0 = Date.now();

  try {
    const res = await fetch(NVIDIA_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${NVIDIA_API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: options?.temperature ?? 0.6,
        max_tokens: options?.max_tokens ?? 400,
      }),
      signal: AbortSignal.timeout(options?.timeoutMs ?? 25000),
    });

    if (!res.ok) {
      console.error(
        `[llm] NVIDIA API returned ${res.status}: ${await res.text().catch(() => "")}`
      );
      return null;
    }

    const data = await res.json();
    const content = data?.choices?.[0]?.message?.content;
    if (!content || content.trim().length < 10) {
      console.error("[llm] NVIDIA API returned empty/short content");
      return null;
    }

    return {
      content: content.trim(),
      model,
      duration_ms: Date.now() - t0,
    };
  } catch (err) {
    console.error("[llm] NVIDIA API call failed:", err);
    return null;
  }
}

export interface PolicyEvidence {
  source_id: string;
  title: string;
  content: string;
  url?: string;
}

/**
 * Build the system prompt for CareLoop, incorporating evidence and directives.
 */
export function buildSystemPrompt(
  coachingMode: string,
  evidence?: PolicyEvidence[],
  directives?: string[]
): string {
  let prompt =
    "You are CareLoop, a supportive, personality-aware caregiver coaching assistant " +
    "for informal caregivers in Switzerland.\n\n";

  if (coachingMode === "policy_navigation" || coachingMode === "mixed") {
    prompt += "ROLE: You are helping the user navigate Swiss social policy and benefits.\n";
    prompt +=
      "Provide clear, accurate, actionable information based on the official sources provided.\n\n";
  } else if (coachingMode === "practical_education") {
    prompt += "ROLE: You are a practical coaching advisor.\n";
    prompt +=
      "Give structured, actionable advice with concrete steps the user can take.\n\n";
  } else {
    prompt += "ROLE: You are an empathetic emotional support companion.\n";
    prompt +=
      "Listen actively, validate feelings, and gently guide the user toward small actionable steps.\n\n";
  }

  if (evidence && evidence.length > 0) {
    prompt += "OFFICIAL POLICY CONTEXT (base your answer on these sources):\n";
    evidence.forEach((e, i) => {
      prompt += `[Source ${i + 1}] ${e.title}: ${e.content}\n\n`;
    });
    prompt +=
      "INSTRUCTIONS: Answer using the provided context. Cite sources when stating policy facts. " +
      "If the answer is not in the context, say so honestly.\n\n";
  }

  if (directives && directives.length > 0) {
    prompt += "Style directives:\n";
    directives.forEach((d, i) => {
      prompt += `${i + 1}. ${d}\n`;
    });
    prompt += "\n";
  }

  prompt +=
    "Rules:\n" +
    "- Keep responses 2-5 sentences unless the user asks for details.\n" +
    "- Reference what the user said to show you listened.\n" +
    "- Be genuine and warm but not saccharine.\n" +
    "- Ask one follow-up question when appropriate.\n" +
    "- Never start with 'I appreciate you sharing'.";

  return prompt;
}
