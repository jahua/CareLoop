#!/usr/bin/env node
/**
 * P2-9 Stale citation detector (background job).
 * - Reads distinct URLs from policy_chunks
 * - Probes each URL (HEAD then optional GET fallback)
 * - Emits one JSONL telemetry line to BACKGROUND_JOB_LOG_PATH or stdout
 * - Exits 1 when failures exceed threshold (STALE_CITATION_FAIL_THRESHOLD)
 */

const { Client } = require("pg");
const { appendFile } = require("fs").promises;

const DATABASE_URL =
  process.env.DATABASE_URL ||
  process.env.AUDIT_DATABASE_URL ||
  "postgresql://careloop:changeme@localhost:5432/careloop";
const LOG_PATH = process.env.BACKGROUND_JOB_LOG_PATH || "";
const MAX_URLS = Number.parseInt(process.env.STALE_CITATION_MAX_URLS || "100", 10);
const TIMEOUT_MS = Number.parseInt(process.env.STALE_CITATION_TIMEOUT_MS || "5000", 10);
const FAIL_THRESHOLD = Number.parseFloat(process.env.STALE_CITATION_FAIL_THRESHOLD || "0.1"); // 10%
const ALLOW_GET_FALLBACK = process.env.STALE_CITATION_ALLOW_GET_FALLBACK !== "0";

function telemetryLine(payload) {
  return JSON.stringify({ ...payload, created_at: new Date().toISOString() }) + "\n";
}

async function appendTelemetry(line) {
  if (!LOG_PATH) {
    process.stdout.write(line);
    return;
  }
  await appendFile(LOG_PATH, line).catch(() => process.stdout.write(line));
}

async function fetchWithTimeout(url, method) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const response = await fetch(url, {
      method,
      redirect: "follow",
      signal: controller.signal,
    });
    return { ok: response.ok, status: response.status, error: null };
  } catch (e) {
    return {
      ok: false,
      status: null,
      error: e && e.name === "AbortError" ? "timeout" : String(e?.message || "fetch_failed"),
    };
  } finally {
    clearTimeout(timer);
  }
}

async function checkUrl(url) {
  const head = await fetchWithTimeout(url, "HEAD");
  if (head.ok) return { status: "ok", method: "HEAD", http_status: head.status };

  const shouldFallback =
    ALLOW_GET_FALLBACK &&
    (head.status === 405 || head.status === 403 || head.status === 400 || head.status === null);
  if (shouldFallback) {
    const getRes = await fetchWithTimeout(url, "GET");
    if (getRes.ok) return { status: "ok", method: "GET", http_status: getRes.status };
    return {
      status: "stale",
      method: "GET",
      http_status: getRes.status,
      error: getRes.error || `http_${getRes.status || "unknown"}`,
    };
  }

  return {
    status: "stale",
    method: "HEAD",
    http_status: head.status,
    error: head.error || `http_${head.status || "unknown"}`,
  };
}

async function run() {
  const job_id = `stale-citation-${Date.now()}`;
  const startedAt = Date.now();
  let status = "ok";
  let error_code;
  let checked_count = 0;
  let stale_count = 0;
  let stale_ratio = 0;
  const stale_samples = [];

  const client = new Client({ connectionString: DATABASE_URL });
  try {
    await client.connect();
    const sql = `
      SELECT DISTINCT url
      FROM policy_chunks
      WHERE url IS NOT NULL AND TRIM(url) <> ''
      ORDER BY url
      LIMIT $1
    `;
    const result = await client.query(sql, [MAX_URLS]);
    const urls = result.rows.map((r) => String(r.url || "").trim()).filter(Boolean);
    checked_count = urls.length;

    for (const url of urls) {
      const probe = await checkUrl(url);
      if (probe.status === "stale") {
        stale_count += 1;
        if (stale_samples.length < 20) {
          stale_samples.push({
            url,
            method: probe.method,
            http_status: probe.http_status,
            error: probe.error,
          });
        }
      }
    }

    stale_ratio = checked_count > 0 ? stale_count / checked_count : 0;
    if (checked_count === 0) {
      status = "fail";
      error_code = "empty_url_set";
    } else if (stale_ratio > FAIL_THRESHOLD) {
      status = "fail";
      error_code = "stale_ratio_exceeded";
    }
  } catch (e) {
    status = "fail";
    error_code = `db_or_probe_error:${String(e?.message || "unknown")}`;
  } finally {
    await client.end().catch(() => {});
  }

  const payload = {
    job_id,
    job_type: "stale_citation_detector",
    stage: "background_job",
    status,
    duration_ms: Date.now() - startedAt,
    error_code,
    checked_count,
    stale_count,
    stale_ratio: Number(stale_ratio.toFixed(4)),
    threshold: FAIL_THRESHOLD,
    timeout_ms: TIMEOUT_MS,
    stale_samples,
  };

  await appendTelemetry(telemetryLine(payload));
  process.exit(status === "ok" ? 0 : 1);
}

run().catch(async (e) => {
  const payload = {
    job_id: `stale-citation-${Date.now()}`,
    job_type: "stale_citation_detector",
    stage: "background_job",
    status: "fail",
    duration_ms: 0,
    error_code: String(e?.message || "unknown"),
  };
  await appendTelemetry(telemetryLine(payload));
  process.exit(1);
});

