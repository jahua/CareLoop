#!/usr/bin/env node
/**
 * P2-9 Retrieval regression smoke: one policy question → POST /api/chat, assert reply + citations.
 * Emits one JSONL telemetry line to BACKGROUND_JOB_LOG_PATH or stdout (same shape as corpus-freshness).
 * Exit 0 if response has content and (when required) citations; 1 otherwise.
 * See docs/BACKGROUND-JOBS-DESIGN.md and docs/PILLAR-TEST-MATRIX-EXECUTION.md.
 */

const BASE_URL = process.env.BASE_URL || process.env.BIG5LOOP_BASE_URL || "http://localhost:3003";
const LOG_PATH = process.env.BACKGROUND_JOB_LOG_PATH || "";
const { appendFile } = require("fs").promises;

function uuid() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

function telemetryLine(payload) {
  return JSON.stringify({ ...payload, created_at: new Date().toISOString() }) + "\n";
}

async function run() {
  const job_id = `retrieval-regression-smoke-${Date.now()}`;
  const startedAt = Date.now();
  let status = "ok";
  let error_code = null;
  let has_content = false;
  let has_citations = false;
  let http_status = null;

  const sessionId = uuid();
  const body = {
    session_id: sessionId,
    turn_index: 1,
    message: "What are the eligibility conditions for IV (Invalidity Insurance) in Switzerland?",
    context: { language: "en", canton: "ZH" },
  };

  try {
    const res = await fetch(`${BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    http_status = res.status;
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      status = "fail";
      error_code = `http_${res.status}`;
    } else if (data && data.success === false && data.error) {
      status = "fail";
      error_code = data.error.error_code || "pipeline_error";
    } else {
      const content = data?.message?.content ?? data?.reply ?? "";
      has_content = typeof content === "string" && content.length > 0;
      const citations =
        data?.citations ??
        data?.policy_evidence ??
        data?.message?.citations ??
        [];
      has_citations = Array.isArray(citations) && citations.length > 0;
      if (!has_content) {
        status = "fail";
        error_code = "no_content";
      } else if (!has_citations) {
        status = "fail";
        error_code = "no_citations";
      }
    }
  } catch (e) {
    status = "fail";
    error_code = "request_failed";
    if (e && e.message) error_code += `: ${e.message}`;
  }

  const duration_ms = Date.now() - startedAt;
  const payload = {
    job_id,
    job_type: "retrieval_regression_smoke",
    stage: "background_job",
    status,
    duration_ms,
    error_code: error_code || undefined,
    http_status,
    has_content,
    has_citations,
  };

  const line = telemetryLine(payload);
  if (LOG_PATH) {
    await appendFile(LOG_PATH, line).catch(() => process.stdout.write(line));
  } else {
    process.stdout.write(line);
  }

  process.exit(status === "ok" ? 0 : 1);
}

run().catch((e) => {
  process.stderr.write(String(e));
  process.exit(1);
});
