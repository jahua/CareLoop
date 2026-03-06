#!/usr/bin/env node
/**
 * P2-7 Gateway canary gate checker.
 *
 * Inputs:
 * - GATEWAY_SHADOW_LOG (required): JSONL from gateway shadow logger
 * - BASELINE_P95_MS (required): baseline p95 latency (ms) without gateway
 * - BASELINE_5XX_RATE (required): baseline 5xx rate (0..1) without gateway
 * - Optional:
 *   - CANARY_WINDOW_MINUTES (default 60)
 *   - MIN_REQUESTS (default 20)
 *   - MAX_5XX_ABS_INCREASE (default 0.01)
 *   - MAX_P95_INCREASE_MS (default 200)
 *   - MAX_429_RATE (default 0.05)
 *   - MAX_ERROR_ENVELOPE_RATE (default 0.05)
 *   - BASELINE_AUDIT_LOG_PATH, CANARY_AUDIT_LOG_PATH, MAX_POLICY_CITATION_DROP (default 0.05)
 *
 * Exit code:
 * - 0 when all canary gates pass
 * - 1 when any gate fails
 */

const fs = require("fs");
const path = require("path");

const SHADOW_LOG = process.env.GATEWAY_SHADOW_LOG || "";
const BASELINE_P95_MS = Number.parseFloat(process.env.BASELINE_P95_MS || "NaN");
const BASELINE_5XX_RATE = Number.parseFloat(process.env.BASELINE_5XX_RATE || "NaN");

const WINDOW_MINUTES = Number.parseInt(process.env.CANARY_WINDOW_MINUTES || "60", 10);
const MIN_REQUESTS = Number.parseInt(process.env.MIN_REQUESTS || "20", 10);
const MAX_5XX_ABS_INCREASE = Number.parseFloat(process.env.MAX_5XX_ABS_INCREASE || "0.01");
const MAX_P95_INCREASE_MS = Number.parseInt(process.env.MAX_P95_INCREASE_MS || "200", 10);
const MAX_429_RATE = Number.parseFloat(process.env.MAX_429_RATE || "0.05");
const MAX_ERROR_ENVELOPE_RATE = Number.parseFloat(process.env.MAX_ERROR_ENVELOPE_RATE || "0.05");

const BASELINE_AUDIT_LOG_PATH = process.env.BASELINE_AUDIT_LOG_PATH || "";
const CANARY_AUDIT_LOG_PATH = process.env.CANARY_AUDIT_LOG_PATH || "";
const MAX_POLICY_CITATION_DROP = Number.parseFloat(process.env.MAX_POLICY_CITATION_DROP || "0.05");

function percentile(values, p) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.max(0, Math.min(sorted.length - 1, idx))];
}

function safeJson(line) {
  try {
    return JSON.parse(line);
  } catch {
    return null;
  }
}

function readJsonl(filePath) {
  if (!filePath) return [];
  if (!fs.existsSync(filePath)) return [];
  const raw = fs.readFileSync(filePath, "utf8");
  return raw
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean)
    .map(safeJson)
    .filter(Boolean);
}

function withinWindow(iso, nowMs, windowMs) {
  const t = Date.parse(String(iso || ""));
  if (!Number.isFinite(t)) return false;
  return nowMs - t <= windowMs;
}

function policyCitationCoverage(auditRows) {
  const policyRows = auditRows.filter((r) =>
    ["policy_navigation", "mixed"].includes(String(r?.coaching_mode || ""))
  );
  if (!policyRows.length) return null;
  const withCitation = policyRows.filter((r) => Number(r?.citation_count || 0) > 0).length;
  return withCitation / policyRows.length;
}

function fail(checks, id, detail) {
  checks.push({ id, status: "fail", detail });
}

function pass(checks, id, detail) {
  checks.push({ id, status: "pass", detail });
}

function main() {
  const checks = [];
  const nowMs = Date.now();
  const windowMs = WINDOW_MINUTES * 60 * 1000;

  if (!SHADOW_LOG) {
    console.error("GATEWAY_SHADOW_LOG is required.");
    process.exit(1);
  }
  if (!Number.isFinite(BASELINE_P95_MS) || !Number.isFinite(BASELINE_5XX_RATE)) {
    console.error("BASELINE_P95_MS and BASELINE_5XX_RATE are required.");
    process.exit(1);
  }

  const rows = readJsonl(path.resolve(SHADOW_LOG)).filter((r) =>
    withinWindow(r?._logged_at, nowMs, windowMs)
  );
  const reqRows = rows.filter((r) => r?._event === "gateway_request");
  const resRows = rows.filter((r) => r?._event === "gateway_response");

  const invalidReq = reqRows.filter((r) => {
    const sid = String(r?.session_id || "");
    const msg = String(r?.message || "");
    const isUuid =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(sid);
    return !isUuid || msg.length === 0;
  }).length;

  const responseCount = resRows.length;
  const statusCodes = resRows.map((r) => Number(r?.status_code || 0));
  const latencies = resRows.map((r) => Number(r?.latency_ms || 0)).filter((n) => Number.isFinite(n));
  const fiveXX = statusCodes.filter((s) => s >= 500).length;
  const tooMany = statusCodes.filter((s) => s === 429).length;
  const errorEnvelope = resRows.filter((r) => Boolean(r?.has_error_envelope)).length;

  const canary5xxRate = responseCount > 0 ? fiveXX / responseCount : 1;
  const canary429Rate = responseCount > 0 ? tooMany / responseCount : 1;
  const canaryEnvelopeRate = responseCount > 0 ? errorEnvelope / responseCount : 1;
  const canaryP95 = percentile(latencies, 95);

  if (reqRows.length >= MIN_REQUESTS && responseCount >= MIN_REQUESTS) {
    pass(checks, "traffic_volume", `req=${reqRows.length}, resp=${responseCount}`);
  } else {
    fail(checks, "traffic_volume", `insufficient samples req=${reqRows.length}, resp=${responseCount}, min=${MIN_REQUESTS}`);
  }

  if (invalidReq === 0) {
    pass(checks, "envelope_shape", "all gateway request envelopes valid");
  } else {
    fail(checks, "envelope_shape", `invalid_envelopes=${invalidReq}`);
  }

  if (canary5xxRate <= BASELINE_5XX_RATE + MAX_5XX_ABS_INCREASE) {
    pass(
      checks,
      "error_rate_5xx",
      `canary=${canary5xxRate.toFixed(4)} baseline=${BASELINE_5XX_RATE.toFixed(4)} allowed_increase=${MAX_5XX_ABS_INCREASE}`
    );
  } else {
    fail(
      checks,
      "error_rate_5xx",
      `canary=${canary5xxRate.toFixed(4)} baseline=${BASELINE_5XX_RATE.toFixed(4)} exceeds allowed increase`
    );
  }

  if (canaryP95 != null && canaryP95 <= BASELINE_P95_MS + MAX_P95_INCREASE_MS) {
    pass(
      checks,
      "latency_p95",
      `canary_p95=${canaryP95}ms baseline_p95=${BASELINE_P95_MS}ms allowed_increase=${MAX_P95_INCREASE_MS}ms`
    );
  } else {
    fail(
      checks,
      "latency_p95",
      `canary_p95=${canaryP95}ms baseline_p95=${BASELINE_P95_MS}ms exceeds allowed increase`
    );
  }

  if (canary429Rate <= MAX_429_RATE) {
    pass(checks, "rate_limit_429", `rate=${canary429Rate.toFixed(4)} threshold=${MAX_429_RATE}`);
  } else {
    fail(checks, "rate_limit_429", `rate=${canary429Rate.toFixed(4)} threshold=${MAX_429_RATE}`);
  }

  if (canaryEnvelopeRate <= MAX_ERROR_ENVELOPE_RATE) {
    pass(
      checks,
      "error_envelope_rate",
      `rate=${canaryEnvelopeRate.toFixed(4)} threshold=${MAX_ERROR_ENVELOPE_RATE}`
    );
  } else {
    fail(
      checks,
      "error_envelope_rate",
      `rate=${canaryEnvelopeRate.toFixed(4)} threshold=${MAX_ERROR_ENVELOPE_RATE}`
    );
  }

  if (BASELINE_AUDIT_LOG_PATH && CANARY_AUDIT_LOG_PATH) {
    const baselineAudit = readJsonl(path.resolve(BASELINE_AUDIT_LOG_PATH));
    const canaryAudit = readJsonl(path.resolve(CANARY_AUDIT_LOG_PATH));
    const baselineCoverage = policyCitationCoverage(baselineAudit);
    const canaryCoverage = policyCitationCoverage(canaryAudit);
    if (baselineCoverage == null || canaryCoverage == null) {
      fail(checks, "policy_citation_coverage", "insufficient policy rows in audit logs");
    } else if (canaryCoverage + MAX_POLICY_CITATION_DROP >= baselineCoverage) {
      pass(
        checks,
        "policy_citation_coverage",
        `baseline=${baselineCoverage.toFixed(4)} canary=${canaryCoverage.toFixed(4)} max_drop=${MAX_POLICY_CITATION_DROP}`
      );
    } else {
      fail(
        checks,
        "policy_citation_coverage",
        `baseline=${baselineCoverage.toFixed(4)} canary=${canaryCoverage.toFixed(4)} drop_exceeds=${MAX_POLICY_CITATION_DROP}`
      );
    }
  }

  const failed = checks.filter((c) => c.status === "fail");
  const summary = {
    job_id: `gateway-canary-${Date.now()}`,
    job_type: "gateway_canary_gate",
    stage: "background_job",
    status: failed.length === 0 ? "ok" : "fail",
    window_minutes: WINDOW_MINUTES,
    baseline: {
      p95_ms: BASELINE_P95_MS,
      error_rate_5xx: BASELINE_5XX_RATE,
    },
    canary: {
      request_count: reqRows.length,
      response_count: responseCount,
      p95_ms: canaryP95,
      error_rate_5xx: canary5xxRate,
      rate_429: canary429Rate,
      error_envelope_rate: canaryEnvelopeRate,
      invalid_envelopes: invalidReq,
    },
    checks,
    created_at: new Date().toISOString(),
  };

  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
  process.exit(failed.length === 0 ? 0 : 1);
}

main();

