#!/usr/bin/env node
/**
 * P2-9 Corpus freshness check (background job).
 * Connects to DB, counts policy_chunks, optionally gets min(created_at).
 * Emits one JSONL telemetry line to BACKGROUND_JOB_LOG_PATH or stdout.
 * Exit 0 on success, 1 on failure (DB unreachable or empty corpus when expected).
 * See docs/BACKGROUND-JOBS-DESIGN.md.
 */

const { Client } = require("pg");
const { appendFile } = require("fs").promises;

const DATABASE_URL =
  process.env.DATABASE_URL ||
  process.env.AUDIT_DATABASE_URL ||
  "postgresql://careloop:changeme@localhost:5432/careloop";
const LOG_PATH = process.env.BACKGROUND_JOB_LOG_PATH || "";
const FAIL_ON_EMPTY = process.env.CORPUS_FAIL_ON_EMPTY !== "0"; // default: fail if 0 chunks

function telemetryLine(payload) {
  return JSON.stringify({ ...payload, created_at: new Date().toISOString() }) + "\n";
}

async function run() {
  const job_id = `corpus-freshness-${Date.now()}`;
  const startedAt = Date.now();
  let status = "ok";
  let error_code = null;
  let chunk_count = 0;
  let min_created_at = null;

  const client = new Client({ connectionString: DATABASE_URL });
  try {
    await client.connect();
    const countResult = await client.query("SELECT COUNT(*)::int AS n FROM policy_chunks");
    chunk_count = countResult.rows[0]?.n ?? 0;
    const minResult = await client.query("SELECT MIN(created_at) AS min_at FROM policy_chunks");
    const minRow = minResult.rows[0];
    if (minRow?.min_at) min_created_at = minRow.min_at.toISOString();

    if (FAIL_ON_EMPTY && chunk_count === 0) {
      status = "fail";
      error_code = "empty_corpus";
    }
  } catch (e) {
    status = "fail";
    error_code = "db_error";
    if (e && typeof e.message === "string") error_code += `: ${e.message}`;
  } finally {
    await client.end().catch(() => {});
  }

  const duration_ms = Date.now() - startedAt;
  const payload = {
    job_id,
    job_type: "corpus_freshness",
    stage: "background_job",
    status,
    duration_ms,
    error_code: error_code || undefined,
    chunk_count,
    min_created_at,
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
  const payload = {
    job_id: `corpus-freshness-${Date.now()}`,
    job_type: "corpus_freshness",
    stage: "background_job",
    status: "fail",
    duration_ms: 0,
    error_code: e && e.message ? String(e.message) : "unknown",
    created_at: new Date().toISOString(),
  };
  process.stdout.write(JSON.stringify(payload) + "\n");
  process.exit(1);
});
