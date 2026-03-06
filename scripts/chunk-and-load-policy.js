#!/usr/bin/env node
/**
 * Chunk documents from a JSON file and insert into policy_chunks.
 * Use for open resources: scrape or paste content into sources JSON, then run this.
 *
 * Usage: DATABASE_URL=... node scripts/chunk-and-load-policy.js <path-to-sources.json>
 *
 * sources.json: array of { source_id, title, url, content [, metadata ] }
 * Spec §7.1: 200-400 tokens per chunk, 15-20% overlap. We use ~chars/4 as token proxy.
 */

const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

const TARGET_CHUNK_TOKENS = 300;
const OVERLAP_RATIO = 0.15;
const CHARS_PER_TOKEN = 4;

function approximateTokens(text) {
  return Math.ceil((text || '').length / CHARS_PER_TOKEN);
}

function splitIntoChunks(content, sourceId, title, url, metadata = {}) {
  const chunks = [];
  if (!content || typeof content !== 'string') return chunks;

  const targetChars = TARGET_CHUNK_TOKENS * CHARS_PER_TOKEN;
  const overlapChars = Math.floor(targetChars * OVERLAP_RATIO);

  let start = 0;
  let index = 0;
  const text = content.replace(/\s+/g, ' ').trim();

  while (start < text.length) {
    let end = start + targetChars;
    if (end < text.length) {
      const nextSpace = text.lastIndexOf(' ', end);
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
    index++;
    start = end - overlapChars;
    if (start >= text.length) break;
  }
  return chunks;
}

const SCHEMA_SQL = `
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS policy_chunks (
  id SERIAL PRIMARY KEY,
  source_id TEXT NOT NULL,
  chunk_id TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  url TEXT,
  embedding VECTOR(1024),
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(source_id, chunk_id)
);
CREATE INDEX IF NOT EXISTS idx_policy_chunks_content_trgm ON policy_chunks USING gin (to_tsvector('english', content));
`;

async function run() {
  const jsonPath = process.argv[2];
  if (!jsonPath) {
    console.error('Usage: node scripts/chunk-and-load-policy.js <sources.json>');
    console.error('  sources.json: [ { source_id, title, url, content [, metadata ] }, ... ]');
    process.exit(1);
  }
  const fullPath = path.isAbsolute(jsonPath) ? jsonPath : path.join(process.cwd(), jsonPath);
  if (!fs.existsSync(fullPath)) {
    console.error('File not found:', fullPath);
    process.exit(1);
  }

  let documents;
  try {
    documents = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
  } catch (e) {
    console.error('Invalid JSON:', e.message);
    process.exit(1);
  }
  if (!Array.isArray(documents) || documents.length === 0) {
    console.error('JSON must be a non-empty array of documents.');
    process.exit(1);
  }

  const allChunks = [];
  for (const doc of documents) {
    const sourceId = doc.source_id || 'unknown_source';
    const title = doc.title || sourceId;
    const url = doc.url || null;
    const content = doc.content || '';
    const metadata = doc.metadata && typeof doc.metadata === 'object' ? doc.metadata : {};
    const chunks = splitIntoChunks(content, sourceId, title, url, metadata);
    allChunks.push(...chunks);
  }

  console.log(`Chunked ${documents.length} document(s) into ${allChunks.length} chunks.`);

  const client = new Client({
    connectionString: process.env.DATABASE_URL || 'postgresql://careloop:changeme@localhost:5432/careloop',
  });

  try {
    await client.connect();
    await client.query(SCHEMA_SQL);

    for (const row of allChunks) {
      await client.query(
        `INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata)
         VALUES ($1, $2, $3, $4, $5, $6)
         ON CONFLICT (source_id, chunk_id) DO UPDATE SET
           content = EXCLUDED.content, title = EXCLUDED.title, url = EXCLUDED.url, metadata = EXCLUDED.metadata`,
        [row.source_id, row.chunk_id, row.title, row.content, row.url, JSON.stringify(row.metadata)]
      );
    }
    console.log(`Inserted/updated ${allChunks.length} rows in policy_chunks.`);
  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

run();
