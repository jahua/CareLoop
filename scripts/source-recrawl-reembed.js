#!/usr/bin/env node
/**
 * P2-9 Source recrawl / re-embedding job (safe baseline).
 *
 * Current implementation focuses on changed-source detection + chunk upsert:
 * - Reads source registry (sources.config.json)
 * - Reads latest fetched documents JSON (same shape used by chunk-and-load)
 * - Compares content hash against DB metadata.content_hash
 * - In dry-run mode reports changes only
 * - In apply mode replaces chunks for changed sources
 *
 * Telemetry is written as one JSONL record to BACKGROUND_JOB_LOG_PATH or stdout.
 */

const { Client } = require("pg");
const { appendFile, readFile } = require("fs").promises;
const { createHash } = require("crypto");
const path = require("path");

const DATABASE_URL =
  process.env.DATABASE_URL ||
  process.env.AUDIT_DATABASE_URL ||
  "postgresql://big5loop:changeme@localhost:5432/big5loop";
const LOG_PATH = process.env.BACKGROUND_JOB_LOG_PATH || "";
const DRY_RUN = process.env.SOURCE_RECRAWL_DRY_RUN !== "0"; // default true
const MAX_SOURCES = Number.parseInt(process.env.SOURCE_RECRAWL_MAX_SOURCES || "100", 10);
const TARGET_CHUNK_TOKENS = 300;
const OVERLAP_RATIO = 0.15;
const CHARS_PER_TOKEN = 4;

const SOURCES_CONFIG_PATH =
  process.env.SOURCE_CONFIG_PATH ||
  path.resolve(process.cwd(), "data/sources/cantonal/sources.config.json");
const DOCUMENTS_PATH =
  process.env.SOURCE_DOCUMENTS_PATH ||
  path.resolve(process.cwd(), "data/documents/cantonal/documents.json");

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

function splitIntoChunks(content, sourceId, title, url, metadata = {}) {
  const chunks = [];
  if (!content || typeof content !== "string") return chunks;
  const targetChars = TARGET_CHUNK_TOKENS * CHARS_PER_TOKEN;
  const overlapChars = Math.floor(targetChars * OVERLAP_RATIO);
  const text = content.replace(/\s+/g, " ").trim();
  let start = 0;
  let index = 0;

  while (start < text.length) {
    let end = start + targetChars;
    if (end < text.length) {
      const nextSpace = text.lastIndexOf(" ", end);
      if (nextSpace > start) end = nextSpace + 1;
    } else {
      end = text.length;
    }
    const chunkContent = text.slice(start, end).trim();
    if (chunkContent) {
      chunks.push({
        source_id: sourceId,
        chunk_id: `${sourceId}_chunk_${index}`,
        title: index === 0 ? title : `${title} (part ${index + 1})`,
        content: chunkContent,
        url: url || null,
        metadata: { ...metadata },
      });
    }
    index += 1;
    start = end - overlapChars;
    if (start >= text.length) break;
  }
  return chunks;
}

function hashContent(text) {
  return createHash("sha256").update(String(text || ""), "utf8").digest("hex").slice(0, 24);
}

async function readJson(filePath) {
  const raw = await readFile(filePath, "utf8");
  return JSON.parse(raw);
}

async function run() {
  const job_id = `source-recrawl-${Date.now()}`;
  const startedAt = Date.now();
  let status = "ok";
  let error_code;

  let sources_checked = 0;
  let sources_changed = 0;
  let sources_unchanged = 0;
  let sources_missing_content = 0;
  let chunks_upserted = 0;
  let chunks_deleted = 0;
  const changed_sources = [];

  const client = new Client({ connectionString: DATABASE_URL });

  try {
    const sourceCfg = await readJson(SOURCES_CONFIG_PATH);
    const docs = await readJson(DOCUMENTS_PATH);
    const sourceList = Array.isArray(sourceCfg?.sources) ? sourceCfg.sources : [];
    const docsBySource = new Map(
      (Array.isArray(docs) ? docs : []).map((d) => [String(d.source_id || ""), d])
    );
    const effectiveSources = sourceList.slice(0, Math.max(0, MAX_SOURCES));

    await client.connect();

    for (const src of effectiveSources) {
      const source_id = String(src?.source_id || "").trim();
      if (!source_id) continue;
      sources_checked += 1;

      const doc = docsBySource.get(source_id);
      const content = String(doc?.content || "");
      if (!content.trim()) {
        sources_missing_content += 1;
        continue;
      }

      const content_hash = hashContent(content);
      const hashResult = await client.query(
        `SELECT metadata->>'content_hash' AS content_hash
         FROM policy_chunks
         WHERE source_id = $1
         ORDER BY created_at DESC
         LIMIT 1`,
        [source_id]
      );
      const previousHash = hashResult.rows[0]?.content_hash || null;
      const changed = previousHash !== content_hash;

      if (!changed) {
        sources_unchanged += 1;
        continue;
      }

      sources_changed += 1;
      changed_sources.push(source_id);

      if (DRY_RUN) continue;

      const title = String(doc?.title || src?.title || source_id);
      const url = String(doc?.url || src?.url || "");
      const metadata = {
        ...(doc?.metadata && typeof doc.metadata === "object" ? doc.metadata : {}),
        recrawled_at: new Date().toISOString(),
        content_hash,
      };
      const chunks = splitIntoChunks(content, source_id, title, url, metadata);

      const delRes = await client.query("DELETE FROM policy_chunks WHERE source_id = $1", [source_id]);
      chunks_deleted += delRes.rowCount || 0;

      for (const row of chunks) {
        await client.query(
          `INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [row.source_id, row.chunk_id, row.title, row.content, row.url, JSON.stringify(row.metadata)]
        );
      }
      chunks_upserted += chunks.length;
    }

    if (sources_checked === 0) {
      status = "fail";
      error_code = "empty_source_config";
    }
  } catch (e) {
    status = "fail";
    error_code = `source_recrawl_error:${String(e?.message || "unknown")}`;
  } finally {
    await client.end().catch(() => {});
  }

  const payload = {
    job_id,
    job_type: "source_recrawl_reembed",
    stage: "background_job",
    status,
    duration_ms: Date.now() - startedAt,
    error_code,
    dry_run: DRY_RUN,
    source_config_path: SOURCES_CONFIG_PATH,
    source_documents_path: DOCUMENTS_PATH,
    sources_checked,
    sources_changed,
    sources_unchanged,
    sources_missing_content,
    chunks_upserted,
    chunks_deleted,
    changed_sources: changed_sources.slice(0, 50),
  };

  await appendTelemetry(telemetryLine(payload));
  process.exit(status === "ok" ? 0 : 1);
}

run().catch(async (e) => {
  await appendTelemetry(
    telemetryLine({
      job_id: `source-recrawl-${Date.now()}`,
      job_type: "source_recrawl_reembed",
      stage: "background_job",
      status: "fail",
      duration_ms: 0,
      error_code: String(e?.message || "unknown"),
    })
  );
  process.exit(1);
});

