#!/usr/bin/env node
/**
 * P2-9 Retrieval regression: run multiple policy cases from a JSON file (or default list).
 * Usage: node scripts/retrieval-regression-runner.js [path-to-cases.json]
 * Cases format:
 * [ { case_id, message, context?, require_policy_mode?, expected_coaching_mode?, min_citations? } ].
 * Each case gets a new session; we assert content + citations and optional routing expectations.
 * Emits one JSONL telemetry line (job_type retrieval_regression) to BACKGROUND_JOB_LOG_PATH or stdout.
 * Exit 0 if all pass, 1 if any fail. See docs/BACKGROUND-JOBS-DESIGN.md, PILLAR-TEST-MATRIX-EXECUTION.md.
 */

const BASE_URL = process.env.BASE_URL || process.env.CARELOOP_BASE_URL || "http://localhost:3003";
const LOG_PATH = process.env.BACKGROUND_JOB_LOG_PATH || "";
const fs = require("fs");
const path = require("path");
const { appendFile } = require("fs").promises;

const DEFAULT_CASES = [
  {
    case_id: "pn-smoke-1",
    message: "What are the eligibility conditions for IV (Invalidity Insurance) in Switzerland?",
    context: { language: "en", canton: "ZH" },
    require_policy_mode: true,
    min_citations: 1,
  },
  {
    case_id: "pn-smoke-2",
    message: "How do I register for IV?",
    context: { language: "en", canton: "ZH" },
    require_policy_mode: true,
    min_citations: 1,
  },
];

function uuid() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

function loadCases(filePath) {
  if (!filePath) return DEFAULT_CASES;
  const raw = fs.readFileSync(path.resolve(filePath), "utf8");
  const arr = JSON.parse(raw);
  if (!Array.isArray(arr)) return DEFAULT_CASES;
  return arr
    .filter((c) => c && typeof c.case_id === "string" && typeof c.message === "string")
    .map((c) => ({
      case_id: c.case_id,
      message: c.message,
      context: c.context,
      require_policy_mode: c.require_policy_mode === true,
      expected_coaching_mode: typeof c.expected_coaching_mode === "string" ? c.expected_coaching_mode : undefined,
      min_citations: Number.isInteger(c.min_citations) ? c.min_citations : undefined,
    }));
}

function isPolicyMode(mode) {
  return mode === "policy_navigation" || mode === "mixed";
}

async function runOneCase(baseUrl, { case_id, message, context, require_policy_mode, expected_coaching_mode, min_citations }) {
  const sessionId = uuid();
  const body = { session_id: sessionId, turn_index: 1, message, context: context || { language: "en", canton: "ZH" } };
  let has_content = false;
  let has_citations = false;
  let error_code = null;
  let http_status = null;
  let coaching_mode = null;
  let citation_count = 0;

  try {
    const res = await fetch(`${baseUrl}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    http_status = res.status;
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      error_code = `http_${res.status}`;
      return { case_id, pass: false, error_code, http_status };
    }
    if (data && data.success === false && data.error) {
      error_code = data.error.error_code || "pipeline_error";
      return { case_id, pass: false, error_code, http_status };
    }

    const content = data?.message?.content ?? data?.reply ?? "";
    has_content = typeof content === "string" && content.length > 0;
    const citations =
      data?.citations ??
      data?.policy_evidence ??
      data?.policy_navigation?.citations ??
      data?.message?.citations ??
      [];
    citation_count = Array.isArray(citations) ? citations.length : 0;
    const requiredCitations = Number.isInteger(min_citations) ? min_citations : 1;
    has_citations = citation_count >= requiredCitations;
    coaching_mode = typeof data?.coaching_mode === "string" ? data.coaching_mode : typeof data?.message?.coaching_mode === "string" ? data.message.coaching_mode : null;
    const policyModeRequired = require_policy_mode || expected_coaching_mode === "policy_navigation" || expected_coaching_mode === "mixed";
    const mode_ok = expected_coaching_mode
      ? coaching_mode === expected_coaching_mode
      : policyModeRequired
        ? isPolicyMode(coaching_mode)
        : true;

    if (!has_content) error_code = "no_content";
    else if (!has_citations) error_code = "no_citations";
    else if (!mode_ok) error_code = "unexpected_coaching_mode";

    return {
      case_id,
      pass: has_content && has_citations && mode_ok,
      error_code: error_code || undefined,
      http_status,
      coaching_mode: coaching_mode || undefined,
      citation_count,
    };
  } catch (e) {
    return { case_id, pass: false, error_code: "request_failed", http_status: null };
  }
}

async function run() {
  const casesPath = process.argv[2];
  const cases = loadCases(casesPath);
  const job_id = `retrieval-regression-${Date.now()}`;
  const startedAt = Date.now();

  const results = [];
  for (const c of cases) {
    const r = await runOneCase(BASE_URL, c);
    results.push(r);
  }

  const duration_ms = Date.now() - startedAt;
  const pass_count = results.filter((r) => r.pass).length;
  const fail_count = results.length - pass_count;
  const status = fail_count === 0 ? "ok" : "fail";
  const failures = results
    .filter((r) => !r.pass)
    .map((r) => ({ case_id: r.case_id, error_code: r.error_code, coaching_mode: r.coaching_mode, citation_count: r.citation_count }));

  const payload = {
    job_id,
    job_type: "retrieval_regression",
    stage: "background_job",
    status,
    duration_ms,
    total: cases.length,
    pass_count,
    fail_count,
    failures: failures.length ? failures : undefined,
    created_at: new Date().toISOString(),
  };

  const line = JSON.stringify(payload) + "\n";
  if (LOG_PATH) {
    await appendFile(LOG_PATH, line).catch(() => process.stdout.write(line));
  } else {
    process.stdout.write(line);
  }

  if (fail_count > 0) {
    process.stderr.write(`retrieval-regression: ${pass_count}/${cases.length} passed; failures: ${JSON.stringify(failures)}\n`);
  }

  process.exit(status === "ok" ? 0 : 1);
}

run().catch((e) => {
  process.stderr.write(String(e));
  process.exit(1);
});
