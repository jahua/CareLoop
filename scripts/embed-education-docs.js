#!/usr/bin/env node
/**
 * Chunk, embed (NVIDIA API), and load education documents into policy_chunks.
 *
 * Reads markdown files from: data/documents/home_care_education/extracted/*.md
 *
 * Usage:
 *   # Step 1: Extract PDFs to markdown first (see instructions below)
 *   # Step 2: Run this script
 *   NVIDIA_API_KEY=<key> node scripts/embed-education-docs.js
 *
 * Options:
 *   --dry-run         Preview chunks without API calls or DB writes
 *   --skip-embed      Load chunks without embeddings (FTS only)
 *   --single <id>     Process only one source_id
 *
 * PDF extraction (do this first):
 *   pip install pymupdf4llm
 *   python3 -c "
 *     import pymupdf4llm, sys
 *     text = pymupdf4llm.to_markdown(sys.argv[1])
 *     with open(sys.argv[2], 'w') as f: f.write(text)
 *   " input.pdf output.md
 */

const fs = require("fs");
const path = require("path");
const https = require("https");

const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY;
const NVIDIA_EMBED_URL = "https://integrate.api.nvidia.com/v1/embeddings";
const NVIDIA_EMBED_MODEL = process.env.NVIDIA_EMBED_MODEL || "nvidia/nv-embedqa-e5-v5";

// DB config: prefer explicit host/port for IPv6 to avoid URL parsing issues
const EXPLICIT_DB_CONFIG = { host: "::1", port: 5432, user: "big5loop", password: "changeme", database: "big5loop" };
const DB_CONFIG = (process.env.DATABASE_URL && !process.env.DATABASE_URL.includes("[::1]"))
  ? { connectionString: process.env.DATABASE_URL }
  : EXPLICIT_DB_CONFIG;

const EDUCATION_DIR = path.resolve(__dirname, "../data/documents/home_care_education/extracted");

const TARGET_CHUNK_TOKENS = 300;
const OVERLAP_RATIO = 0.15;
const CHARS_PER_TOKEN = 4;
const EMBED_BATCH_SIZE = 5;
const EMBED_DELAY_MS = 500;

const DRY_RUN = process.argv.includes("--dry-run");
const SKIP_EMBED = process.argv.includes("--skip-embed");
const SINGLE_ID = getArg("--single");

// Map filename stems to source IDs and titles
const EDUCATION_DOC_MAP = [
  {
    prefix: "edu_caregiver_training_manual",
    title: "Caregiver Training Manual — Basic Care of People with Disabilities",
    url: null,
  },
  {
    prefix: "edu_aarp_prepare_to_care",
    title: "AARP Prepare to Care Guide",
    url: "https://www.aarp.org/caregiving/prepare-to-care-planning-guide/",
  },
  {
    prefix: "edu_caregiving_seniors_guide",
    title: "Caregiving for Seniors — A Practical Guide (2nd Edition)",
    url: null,
  },
  {
    prefix: "edu_family_caregiver_guide",
    title: "Family Caregiver Guide",
    url: null,
  },
];

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

// --- Database ---

async function loadToDatabase(chunks, client) {
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
}

// --- Main ---

async function run() {
  if (!DRY_RUN && !SKIP_EMBED && !NVIDIA_API_KEY) {
    console.error("ERROR: NVIDIA_API_KEY is required for embeddings.");
    console.error("Set it via: export NVIDIA_API_KEY=nvapi-...");
    console.error("Or use --dry-run to preview chunks.");
    process.exit(1);
  }

  if (!fs.existsSync(EDUCATION_DIR)) {
    console.error(`ERROR: Extracted markdown directory not found: ${EDUCATION_DIR}`);
    console.error("");
    console.error("Please extract PDFs to markdown first:");
    console.error("  mkdir -p data/documents/home_care_education/extracted");
    console.error("  pip install pymupdf4llm");
    console.error("  python3 scripts/extract-education-pdfs.py");
    process.exit(1);
  }

  console.log("=== Big5Loop: Embed & Load Education Documents ===\n");
  console.log(`Embedding model: ${NVIDIA_EMBED_MODEL}`);
  // For display only — mask password if using connection string
  const dbDisplay = process.env.DATABASE_URL
    ? process.env.DATABASE_URL.replace(/:[^:@]+@/, ":***@")
    : `${DB_CONFIG.host}:${DB_CONFIG.port}/${DB_CONFIG.database}`;
  console.log(`Database:        ${dbDisplay}`);
  console.log(`Mode:            ${DRY_RUN ? "DRY RUN" : SKIP_EMBED ? "FTS only" : "FTS + Vector embeddings"}`);
  console.log(`Source dir:      ${EDUCATION_DIR}`);
  console.log();

  const mdFiles = fs.readdirSync(EDUCATION_DIR).filter((f) => f.endsWith(".md"));
  if (mdFiles.length === 0) {
    console.error("No .md files found in extracted directory.");
    console.error("Extract PDFs first, then save as .md files with these names:");
    for (const doc of EDUCATION_DOC_MAP) {
      console.error(`  ${doc.prefix}.md`);
    }
    process.exit(1);
  }

  console.log(`Found ${mdFiles.length} markdown files:\n`);

  const stats = { total: 0, embedded: 0, sources: [] };
  let client = null;

  if (!DRY_RUN) {
    const { Client } = require("pg");
    client = new Client(DB_CONFIG);
    await client.connect();
    console.log("Connected to database.\n");
  }

  try {
    for (const file of mdFiles) {
      const stem = file.replace(".md", "");
      const docInfo = EDUCATION_DOC_MAP.find((d) => d.prefix === stem);

      const sourceId = stem;
      if (SINGLE_ID && sourceId !== SINGLE_ID) continue;

      const content = fs.readFileSync(path.join(EDUCATION_DIR, file), "utf8");
      const title = docInfo ? docInfo.title : stem.replace(/_/g, " ");
      const url = docInfo?.url || null;

      const metadata = {
        source_type: "education",
        language: "en",
        document_format: "pdf_extracted",
        original_file: file,
      };

      const chunks = splitIntoChunks(content, sourceId, title, url, metadata);
      stats.sources.push({ id: sourceId, title, chunks: chunks.length });

      if (DRY_RUN) {
        console.log(`  ${sourceId}: ${chunks.length} chunks — "${title}"`);
        if (chunks.length > 0) {
          console.log(`    First chunk (${chunks[0].content.length} chars): "${chunks[0].content.slice(0, 80)}..."`);
        }
      } else {
        process.stdout.write(`  ${sourceId} (${chunks.length} chunks)...`);
        await embedChunks(chunks);
        await loadToDatabase(chunks, client);
        const withEmbed = chunks.filter((c) => c.embedding !== null).length;
        stats.total += chunks.length;
        stats.embedded += withEmbed;
        chunks.length = 0; // free memory
        console.log(" done");
      }
    }

    // --- Summary ---
    console.log(`\n=== Summary ===`);
    console.log(`Sources: ${stats.sources.length}`);
    for (const s of stats.sources) {
      console.log(`  ${s.id}: ${s.chunks} chunks — "${s.title}"`);
    }

    if (DRY_RUN) {
      const totalChunks = stats.sources.reduce((sum, s) => sum + s.chunks, 0);
      console.log(`\nTotal: ${totalChunks} chunks (DRY RUN — no writes)`);
      return;
    }

    console.log(`\nTotal: ${stats.total} chunks loaded, ${stats.embedded} with embeddings`);

    if (stats.embedded > 0) {
      console.log("\nEnsuring HNSW vector index exists...");
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
        count(DISTINCT source_id) AS sources,
        count(*) FILTER (WHERE metadata->>'source_type' = 'education') AS education_chunks,
        count(*) FILTER (WHERE metadata->>'source_type' != 'education' OR metadata->>'source_type' IS NULL) AS policy_chunks
      FROM policy_chunks
    `);
    const s = dbStats.rows[0];
    console.log(`\nDatabase totals:`);
    console.log(`  ${s.total} total chunks (${s.with_embedding} with embeddings)`);
    console.log(`  ${s.education_chunks} education chunks`);
    console.log(`  ${s.policy_chunks} policy chunks`);
    console.log(`  ${s.sources} distinct sources`);

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
