#!/usr/bin/env node
/**
 * P2-7 Gateway canary baseline capture (without gateway path).
 *
 * Sends synthetic requests to /api/chat and computes:
 * - BASELINE_P95_MS
 * - BASELINE_5XX_RATE
 * - error envelope rate
 *
 * Exit 0 on success; 1 on insufficient samples or request failures beyond tolerance.
 */

const crypto = require("crypto");

const BASE_URL = process.env.BASELINE_BASE_URL || "http://localhost:3003";
const REQUESTS = Number.parseInt(process.env.BASELINE_REQUESTS || "30", 10);
const CONCURRENCY = Math.max(1, Number.parseInt(process.env.BASELINE_CONCURRENCY || "3", 10));
const TIMEOUT_MS = Number.parseInt(process.env.BASELINE_TIMEOUT_MS || "20000", 10);
const ACCEPT_FAIL_RATE = Number.parseFloat(process.env.BASELINE_ACCEPT_FAIL_RATE || "0.2");
const SESSION_PREFIX = process.env.BASELINE_SESSION_PREFIX || "00000000-0000-4000-8000-";

function percentile(values, p) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.max(0, Math.min(sorted.length - 1, idx))];
}

function randomSessionId(i) {
  const suffix = crypto.createHash("sha1").update(String(i)).digest("hex").slice(0, 12);
  return `${SESSION_PREFIX}${suffix}`;
}

async function requestOnce(i) {
  const started = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const payload = {
    session_id: randomSessionId(i),
    turn_index: 1,
    message: i % 2 === 0
      ? "I need help understanding IV eligibility in Zurich."
      : "I feel stressed and need practical next steps to cope today.",
    context: { language: "en", canton: "ZH" },
  };

  try {
    const res = await fetch(`${BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    const latency_ms = Date.now() - started;
    const data = await res.json().catch(() => ({}));
    const has_error_envelope =
      data && typeof data === "object" && data.success === false && typeof data.error === "object";
    const error_code = has_error_envelope && typeof data.error?.error_code === "string"
      ? data.error.error_code
      : undefined;

    return {
      ok: res.ok,
      status: res.status,
      latency_ms,
      has_error_envelope,
      error_code,
    };
  } catch (e) {
    return {
      ok: false,
      status: 599,
      latency_ms: Date.now() - started,
      has_error_envelope: true,
      error_code: e?.name === "AbortError" ? "timeout" : "request_failed",
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
  if (!Number.isFinite(REQUESTS) || REQUESTS <= 0) {
    console.error("BASELINE_REQUESTS must be > 0");
    process.exit(1);
  }
  const started = Date.now();
  const results = await runPool(REQUESTS, CONCURRENCY);
  const elapsed_ms = Date.now() - started;

  const total = results.length;
  const latencies = results.map((r) => r.latency_ms);
  const p95 = percentile(latencies, 95);
  const p50 = percentile(latencies, 50);
  const status5xx = results.filter((r) => r.status >= 500).length;
  const envelopeErrors = results.filter((r) => r.has_error_envelope).length;
  const failed = results.filter((r) => !r.ok).length;
  const failRate = total > 0 ? failed / total : 1;
  const rate5xx = total > 0 ? status5xx / total : 1;
  const envelopeRate = total > 0 ? envelopeErrors / total : 1;

  const summary = {
    job_id: `gateway-baseline-${Date.now()}`,
    job_type: "gateway_baseline_capture",
    stage: "background_job",
    status: failRate <= ACCEPT_FAIL_RATE ? "ok" : "fail",
    base_url: BASE_URL,
    requests: total,
    concurrency: CONCURRENCY,
    timeout_ms: TIMEOUT_MS,
    elapsed_ms,
    metrics: {
      p50_ms: p50,
      p95_ms: p95,
      rate_5xx: Number(rate5xx.toFixed(4)),
      error_envelope_rate: Number(envelopeRate.toFixed(4)),
      fail_rate: Number(failRate.toFixed(4)),
    },
    baseline_env: {
      BASELINE_P95_MS: p95,
      BASELINE_5XX_RATE: Number(rate5xx.toFixed(4)),
    },
    created_at: new Date().toISOString(),
  };

  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
  process.exit(summary.status === "ok" ? 0 : 1);
}

main().catch((e) => {
  process.stderr.write(`baseline capture failed: ${String(e?.message || e)}\n`);
  process.exit(1);
});

