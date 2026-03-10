#!/usr/bin/env node
/**
 * Load translated English policy documents into policy_chunks.
 *
 * For each translated document, this script:
 * 1. Chunks the English content (same parameters as chunk-and-load-policy.js)
 * 2. Inserts chunks with source_id suffixed "_en" to avoid overwriting originals
 * 3. Adds metadata.language = "en" and metadata.language_original
 *
 * Usage:
 *   DATABASE_URL=... node scripts/load-translated-policies.js [path-to-translated.json]
 *
 * Default input: data/documents/translated/translated_policies.json
 */

const { Client } = require("pg");
const fs = require("fs");
const path = require("path");

const TARGET_CHUNK_TOKENS = 300;
const OVERLAP_RATIO = 0.15;
const CHARS_PER_TOKEN = 4;

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

async function run() {
  const inputPath =
    process.argv[2] ||
    path.resolve(__dirname, "../data/documents/translated/translated_policies.json");

  if (!fs.existsSync(inputPath)) {
    console.error(`Input not found: ${inputPath}`);
    console.error("Run translate-policies-gemini.js first.");
    process.exit(1);
  }

  const documents = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  if (!Array.isArray(documents) || documents.length === 0) {
    console.error("Input must be a non-empty JSON array.");
    process.exit(1);
  }

  const allChunks = [];
  for (const doc of documents) {
    const sourceId = `${doc.source_id}_en`;
    const title = doc.title_en || `${doc.title} (English)`;
    const url = doc.url || null;
    const content = doc.content_en || "";
    const metadata = {
      ...(doc.metadata || {}),
      language: "en",
      language_original: doc.metadata?.language_original || "unknown",
      original_source_id: doc.source_id,
    };

    const chunks = splitIntoChunks(content, sourceId, title, url, metadata);
    allChunks.push(...chunks);
  }

  console.log(`Chunked ${documents.length} translated document(s) into ${allChunks.length} chunks.`);

  const client = new Client({
    connectionString:
      process.env.DATABASE_URL || "postgresql://big5loop:changeme@localhost:5432/big5loop",
  });

  try {
    await client.connect();

    for (const row of allChunks) {
      await client.query(
        `INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata)
         VALUES ($1, $2, $3, $4, $5, $6)
         ON CONFLICT (source_id, chunk_id) DO UPDATE SET
           content = EXCLUDED.content, title = EXCLUDED.title,
           url = EXCLUDED.url, metadata = EXCLUDED.metadata`,
        [row.source_id, row.chunk_id, row.title, row.content, row.url, JSON.stringify(row.metadata)]
      );
    }

    console.log(`Inserted/updated ${allChunks.length} English chunks in policy_chunks.`);
    console.log(
      `English chunks use source_id pattern: <original>_en (e.g. zh_iv_rente_en)`
    );
  } catch (err) {
    console.error("Error:", err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

run();
