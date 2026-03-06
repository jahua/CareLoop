#!/usr/bin/env node
/**
 * Chunk, embed (NVIDIA API), and load translated policy documents into policy_chunks.
 *
 * Handles both:
 *   - Cantonal translations (JSON): data/documents/translated/translated_policies.json
 *   - Fedlex translations (Markdown): data/documents/translated_fedlex/*.md
 *
 * Usage:
 *   NVIDIA_API_KEY=<key> DATABASE_URL=<url> node scripts/embed-and-load-policies.js
 *
 * Options:
 *   --dry-run         Preview chunks without API calls or DB writes
 *   --skip-embed      Load chunks without embeddings (FTS only)
 *   --single <id>     Process only one source_id
 *   --fedlex-only     Process only Fedlex documents
 *   --cantonal-only   Process only cantonal documents
 */

const fs = require("fs");
const path = require("path");
const https = require("https");

const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY;
const NVIDIA_EMBED_URL = "https://integrate.api.nvidia.com/v1/embeddings";
const NVIDIA_EMBED_MODEL = process.env.NVIDIA_EMBED_MODEL || "nvidia/nv-embedqa-e5-v5";
const DB_CONFIG = process.env.DATABASE_URL
  ? { connectionString: process.env.DATABASE_URL }
  : { host: "::1", port: 5432, user: "careloop", password: "changeme", database: "careloop" };

const CANTONAL_PATH = path.resolve(
  __dirname,
  "../data/documents/translated/translated_policies.json"
);
const FEDLEX_DIR = path.resolve(__dirname, "../data/documents/translated_fedlex");

const TARGET_CHUNK_TOKENS = 300;
const OVERLAP_RATIO = 0.15;
const CHARS_PER_TOKEN = 4;
const EMBED_BATCH_SIZE = 5;
const EMBED_DELAY_MS = 500;

const DRY_RUN = process.argv.includes("--dry-run");
const SKIP_EMBED = process.argv.includes("--skip-embed");
const SINGLE_ID = getArg("--single");
const FEDLEX_ONLY = process.argv.includes("--fedlex-only");
const CANTONAL_ONLY = process.argv.includes("--cantonal-only");

function getArg(flag) {
  const idx = process.argv.indexOf(flag);
  return idx !== -1 && process.argv[idx + 1] ? process.argv[idx + 1] : null;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// --- Chunking ---

function splitIntoChunks(content, sourceId, title, url, metadata) {
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
        embedding: null,
      });
    }
    index += 1;
    if (end >= text.length) break;
    start = end - overlapChars;
  }
  return chunks;
}

// --- Embedding via NVIDIA API ---

function callNvidiaEmbed(texts) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      input: texts,
      model: NVIDIA_EMBED_MODEL,
      input_type: "passage",
    });

    const parsed = new URL(NVIDIA_EMBED_URL);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname,
      method: "POST",
      headers: {
        Authorization: `Bearer ${NVIDIA_API_KEY}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(`NVIDIA API error: ${JSON.stringify(json.error)}`));
            return;
          }
          const embeddings = json.data.map((d) => d.embedding);
          resolve(embeddings);
        } catch (e) {
          reject(new Error(`Failed to parse NVIDIA response: ${e.message}`));
        }
      });
    });

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function embedChunks(chunks) {
  if (SKIP_EMBED || DRY_RUN) return;

  console.log(`  Embedding ${chunks.length} chunks (batch size ${EMBED_BATCH_SIZE})...`);

  for (let i = 0; i < chunks.length; i += EMBED_BATCH_SIZE) {
    const batch = chunks.slice(i, i + EMBED_BATCH_SIZE);
    const texts = batch.map((c) => c.content.slice(0, 2048));

    try {
      const embeddings = await callNvidiaEmbed(texts);
      for (let j = 0; j < batch.length; j++) {
        batch[j].embedding = embeddings[j];
      }
      const pct = Math.min(100, Math.round(((i + batch.length) / chunks.length) * 100));
      process.stdout.write(`\r  Embedded ${i + batch.length}/${chunks.length} (${pct}%)`);
    } catch (err) {
      console.error(`\n  Embed error at batch ${i}: ${err.message}`);
      console.error("  Continuing without embeddings for this batch...");
    }

    if (i + EMBED_BATCH_SIZE < chunks.length) await sleep(EMBED_DELAY_MS);
  }
  console.log();
}

// --- Document loaders ---

function loadCantonalDocs() {
  if (!fs.existsSync(CANTONAL_PATH)) {
    console.log("Cantonal translations not found, skipping.");
    return [];
  }
  const documents = JSON.parse(fs.readFileSync(CANTONAL_PATH, "utf8"));
  const allChunks = [];

  for (const doc of documents) {
    const sourceId = `${doc.source_id}_en`;
    if (SINGLE_ID && sourceId !== SINGLE_ID && doc.source_id !== SINGLE_ID) continue;

    const title = doc.title_en || `${doc.title} (English)`;
    const content = doc.content_en || "";
    const metadata = {
      ...(doc.metadata || {}),
      language: "en",
      language_original: doc.metadata?.language_original || "unknown",
      original_source_id: doc.source_id,
      source_type: "cantonal",
    };

    const chunks = splitIntoChunks(content, sourceId, title, doc.url, metadata);
    allChunks.push(...chunks);
  }

  return allChunks;
}

const FEDLEX_SR_MAP = [
  { prefix: "policy_830_1_", sr: "830.1", title: "ATSG — General Part of Social Insurance Law" },
  { prefix: "policy_831_10_", sr: "831.10", title: "IVG — Federal Act on Disability Insurance" },
  { prefix: "policy_831_201_", sr: "831.201", title: "IVV Annexes — Disability Insurance Ordinance Details" },
  { prefix: "policy_831_232_21_", sr: "831.232.21", title: "HVI — Assistive Devices Ordinance" },
  { prefix: "policy_831_20_", sr: "831.20", title: "IVV — Disability Insurance Ordinance" },
  { prefix: "policy_831_301_", sr: "831.301", title: "ELV — Supplementary Benefits Ordinance" },
  { prefix: "policy_831_30_", sr: "831.30", title: "ELG — Federal Act on Supplementary Benefits" },
  { prefix: "policy_834_1_", sr: "834.1", title: "EOG — Earnings Compensation Act" },
  { prefix: "policy_836_1_", sr: "836.1", title: "FamZG — Federal Act on Family Allowances" },
];

function loadFedlexDocs() {
  if (!fs.existsSync(FEDLEX_DIR)) {
    console.log("Fedlex translations not found, skipping.");
    return [];
  }

  const mdFiles = fs.readdirSync(FEDLEX_DIR).filter((f) => f.endsWith(".md"));
  const allChunks = [];

  for (const file of mdFiles) {
    const stem = file.replace(".md", "");
    const srKey = Object.keys(FEDLEX_SR_MAP).find((k) => stem.startsWith(k));
    const info = srKey ? FEDLEX_SR_MAP[srKey] : null;

    const sourceId = `fedlex_${(info?.sr || stem).replace(/\s+/g, "_").replace(/SR_?/g, "").toLowerCase()}_en`;
    if (SINGLE_ID && sourceId !== SINGLE_ID) continue;

    const content = fs.readFileSync(path.join(FEDLEX_DIR, file), "utf8");
    const title = info ? `${info.title} (${info.sr})` : stem;
    const url = `https://www.fedlex.admin.ch/eli/cc/${stem.replace(/policy_/, "").replace(/_/g, "/")}`;

    const metadata = {
      authority_tier: info?.authority_tier || 1,
      jurisdiction: "Federal",
      canton: "Federal",
      language: "en",
      language_original: "de",
      sr_number: info?.sr || stem,
      source_type: "fedlex",
      translated_at: new Date().toISOString(),
    };

    const chunks = splitIntoChunks(content, sourceId, title, url, metadata);
    allChunks.push(...chunks);
  }

  return allChunks;
}

// --- Database ---

async function loadToDatabase(chunks, client) {
  const hasEmbedding = chunks.some((c) => c.embedding !== null);

  for (const row of chunks) {
    if (row.embedding) {
      const vecStr = `[${row.embedding.join(",")}]`;
      await client.query(
        `INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata, embedding)
         VALUES ($1, $2, $3, $4, $5, $6, $7::vector)
         ON CONFLICT (source_id, chunk_id) DO UPDATE SET
           content = EXCLUDED.content, title = EXCLUDED.title,
           url = EXCLUDED.url, metadata = EXCLUDED.metadata,
           embedding = EXCLUDED.embedding`,
        [row.source_id, row.chunk_id, row.title, row.content, row.url, JSON.stringify(row.metadata), vecStr]
      );
    } else {
      await client.query(
        `INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata)
         VALUES ($1, $2, $3, $4, $5, $6)
         ON CONFLICT (source_id, chunk_id) DO UPDATE SET
           content = EXCLUDED.content, title = EXCLUDED.title,
           url = EXCLUDED.url, metadata = EXCLUDED.metadata`,
        [row.source_id, row.chunk_id, row.title, row.content, row.url, JSON.stringify(row.metadata)]
      );
    }
  }

  return hasEmbedding;
}

// --- Process one document at a time to avoid OOM ---

async function processAndLoad(chunks, client, stats) {
  if (!DRY_RUN) {
    await embedChunks(chunks);
    await loadToDatabase(chunks, client);
  }
  const withEmbed = chunks.filter((c) => c.embedding !== null).length;
  stats.total += chunks.length;
  stats.embedded += withEmbed;
  chunks.length = 0; // free memory
}

// --- Main ---

async function run() {
  if (!DRY_RUN && !SKIP_EMBED && !NVIDIA_API_KEY) {
    console.error("ERROR: NVIDIA_API_KEY is required for embeddings.");
    console.error("Set it via: export NVIDIA_API_KEY=nvapi-...");
    console.error("Or use --skip-embed to load without embeddings.");
    process.exit(1);
  }

  console.log("=== CareLoop: Embed & Load Policy Documents ===\n");
  console.log(`Embedding model: ${NVIDIA_EMBED_MODEL}`);
  const dbLabel = DB_CONFIG.connectionString
    ? DB_CONFIG.connectionString.replace(/:[^:@]+@/, ":***@")
    : `${DB_CONFIG.host}:${DB_CONFIG.port}/${DB_CONFIG.database}`;
  console.log(`Database:        ${dbLabel}`);
  console.log(`Mode:            ${DRY_RUN ? "DRY RUN" : SKIP_EMBED ? "FTS only (no embeddings)" : "FTS + Vector embeddings"}`);
  console.log();

  const stats = { total: 0, embedded: 0, sources: [] };
  let client = null;

  if (!DRY_RUN) {
    const { Client } = require("pg");
    client = new Client(DB_CONFIG);
    await client.connect();
    console.log("Connected to database.\n");
  }

  try {
    // --- Cantonal: process one doc at a time ---
    if (!FEDLEX_ONLY && fs.existsSync(CANTONAL_PATH)) {
      console.log("--- Cantonal translations ---");
      const documents = JSON.parse(fs.readFileSync(CANTONAL_PATH, "utf8"));

      for (const doc of documents) {
        const sourceId = `${doc.source_id}_en`;
        if (SINGLE_ID && sourceId !== SINGLE_ID && doc.source_id !== SINGLE_ID) continue;

        const title = doc.title_en || `${doc.title} (English)`;
        const content = doc.content_en || "";
        const metadata = {
          ...(doc.metadata || {}),
          language: "en",
          language_original: doc.metadata?.language_original || "unknown",
          original_source_id: doc.source_id,
          source_type: "cantonal",
        };

        const chunks = splitIntoChunks(content, sourceId, title, doc.url, metadata);
        stats.sources.push({ id: sourceId, chunks: chunks.length });

        if (DRY_RUN) {
          console.log(`  ${sourceId}: ${chunks.length} chunks`);
        } else {
          process.stdout.write(`  ${sourceId} (${chunks.length} chunks)...`);
          await processAndLoad(chunks, client, stats);
          console.log(" done");
        }
      }
    }

    // --- Fedlex: process one file at a time ---
    if (!CANTONAL_ONLY && fs.existsSync(FEDLEX_DIR)) {
      console.log("\n--- Fedlex translations ---");
      const mdFiles = fs.readdirSync(FEDLEX_DIR).filter((f) => f.endsWith(".md"));

      for (const file of mdFiles) {
        const stem = file.replace(".md", "");
        const info = FEDLEX_SR_MAP.find((entry) => stem.startsWith(entry.prefix));

        const sourceId = `fedlex_${(info?.sr || stem).replace(/\s+/g, "_").toLowerCase()}_en`;
        if (SINGLE_ID && sourceId !== SINGLE_ID) continue;

        const content = fs.readFileSync(path.join(FEDLEX_DIR, file), "utf8");
        const title = info ? `${info.title} (SR ${info.sr})` : stem;
        const url = `https://www.fedlex.admin.ch/eli/cc/${stem.replace(/policy_/, "").replace(/_/g, "/")}`;

        const metadata = {
          authority_tier: 1,
          jurisdiction: "Federal",
          canton: "Federal",
          language: "en",
          language_original: "de",
          sr_number: info?.sr || stem,
          source_type: "fedlex",
          translated_at: new Date().toISOString(),
        };

        const chunks = splitIntoChunks(content, sourceId, title, url, metadata);
        stats.sources.push({ id: sourceId, chunks: chunks.length });

        if (DRY_RUN) {
          console.log(`  ${sourceId}: ${chunks.length} chunks`);
        } else {
          process.stdout.write(`  ${sourceId} (${chunks.length} chunks)...`);
          await processAndLoad(chunks, client, stats);
          console.log(" done");
        }
      }
    }

    // --- Summary ---
    console.log(`\nTotal: ${stats.total} chunks processed`);
    console.log(`  With embeddings: ${stats.embedded}`);
    console.log(`  Sources: ${stats.sources.length}`);

    if (DRY_RUN) {
      console.log("\nDRY RUN complete — no database writes.");
      return;
    }

    if (stats.embedded > 0) {
      console.log("\nCreating HNSW vector index (if not exists)...");
      await client.query(`
        CREATE INDEX IF NOT EXISTS idx_policy_chunks_embedding_hnsw
        ON policy_chunks USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
      `);
      console.log("  HNSW index ready.");
    }

    const dbStats = await client.query(`
      SELECT
        count(*) AS total,
        count(embedding) AS with_embedding,
        count(*) - count(embedding) AS without_embedding,
        count(DISTINCT source_id) AS sources
      FROM policy_chunks
    `);
    const s = dbStats.rows[0];
    console.log(`\nDatabase totals: ${s.total} chunks, ${s.with_embedding} with embeddings, ${s.sources} sources`);

  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  } finally {
    if (client) await client.end();
  }

  console.log("\n=== Done ===");
}

run().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
