#!/usr/bin/env node
/**
 * Phase 4 load test runner.
 * Sends TOTAL requests with CONCURRENCY parallelism to /api/gateway/chat
 * and prints a JSON summary for pilot checklist evidence.
 */

const BASE_URL = process.env.BASE_URL || "http://127.0.0.1:3003";
const TOTAL = Number.parseInt(process.env.LOAD_TOTAL || "100", 10);
const CONCURRENCY = Number.parseInt(process.env.LOAD_CONCURRENCY || "100", 10);
const TIMEOUT_MS = Number.parseInt(process.env.LOAD_TIMEOUT_MS || "30000", 10);
const MODEL_TIER = process.env.LOAD_MODEL_TIER || "medium";
const WORKFLOW = process.env.LOAD_WORKFLOW || "standard";
const CANTON = process.env.LOAD_CANTON || "ZH";
const LANGUAGE = process.env.LOAD_LANGUAGE || "en";

const PROMPTS = [
  "I feel overwhelmed today and need emotional support.",
  "Can you give me a step-by-step caregiving plan for today?",
  "What are Zurich IV application steps and required documents with official sources?",
  "I am stressed and also need Zurich EL eligibility guidance with citations.",
];

function percentile(values, p) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.max(0, Math.min(sorted.length - 1, Math.ceil((p / 100) * sorted.length) - 1));
  return sorted[idx];
}

async function requestOnce(i) {
  const started = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const body = {
    request_id: crypto.randomUUID(),
    session_id: `00000000-0000-4000-8000-${(1200000 + i).toString(16).padStart(12, "0")}`,
    user_id: `phase4-load-${i}`,
    message: PROMPTS[i % PROMPTS.length],
    context: { language: LANGUAGE, canton: CANTON },
    routing_hints: {
      model_tier: MODEL_TIER,
      ...(WORKFLOW === "simple" ? { workflow: "simple" } : {}),
    },
  };

  try {
    const res = await fetch(`${BASE_URL}/api/gateway/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const latencyMs = Date.now() - started;
    const data = await res.json().catch(() => ({}));
    return {
      ok: res.ok,
      status: res.status,
      latency_ms: latencyMs,
      error_envelope: Boolean(data && data.success === false && data.error),
      mode: data?.coaching_mode || "none",
    };
  } catch (e) {
    return {
      ok: false,
      status: 599,
      latency_ms: Date.now() - started,
      error_envelope: true,
      mode: "none",
      error: String(e?.name || e),
    };
  } finally {
    clearTimeout(timer);
  }
}

async function runPool(total, concurrency) {
  const results = [];
  let next = 0;
  async function worker() {
    while (next < total) {
      const i = next++;
      // eslint-disable-next-line no-await-in-loop
      results.push(await requestOnce(i));
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, total) }, () => worker()));
  return results;
}

async function main() {
  const started = Date.now();
  const results = await runPool(TOTAL, CONCURRENCY);
  const elapsedMs = Date.now() - started;
  const total = results.length;
  const ok = results.filter((r) => r.ok).length;
  const fail = total - ok;
  const rate5xx = results.filter((r) => r.status >= 500).length / (total || 1);
  const rate429 = results.filter((r) => r.status === 429).length / (total || 1);
  const errorEnvelopeRate = results.filter((r) => r.error_envelope).length / (total || 1);
  const latencies = results.map((r) => r.latency_ms);
  const modeCounts = results.reduce((acc, r) => {
    acc[r.mode] = (acc[r.mode] || 0) + 1;
    return acc;
  }, {});

  const summary = {
    job_id: `phase4-load-${Date.now()}`,
    stage: "phase4_load_test",
    base_url: BASE_URL,
    total,
    concurrency: CONCURRENCY,
    timeout_ms: TIMEOUT_MS,
    workflow: WORKFLOW,
    model_tier: MODEL_TIER,
    elapsed_ms: elapsedMs,
    ok,
    fail,
    rate_ok: Number((ok / (total || 1)).toFixed(4)),
    rate_5xx: Number(rate5xx.toFixed(4)),
    rate_429: Number(rate429.toFixed(4)),
    error_envelope_rate: Number(errorEnvelopeRate.toFixed(4)),
    p50_ms: percentile(latencies, 50),
    p95_ms: percentile(latencies, 95),
    p99_ms: percentile(latencies, 99),
    modes: modeCounts,
    created_at: new Date().toISOString(),
  };

  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
  process.exit(0);
}

main().catch((e) => {
  process.stderr.write(`load test failed: ${String(e?.message || e)}\n`);
  process.exit(1);
});
