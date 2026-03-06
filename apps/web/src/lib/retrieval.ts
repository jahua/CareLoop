/**
 * Policy retrieval service — hybrid vector + FTS search.
 *
 * Called from the API route before forwarding to N8N.
 * Embeds the user query via NVIDIA API, then runs cosine-similarity
 * search against policy_chunks. Falls back to PostgreSQL FTS when
 * vector results are below threshold.
 */

import { Client } from "pg";

const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY || "";
const NVIDIA_EMBED_URL = "https://integrate.api.nvidia.com/v1/embeddings";
const NVIDIA_EMBED_MODEL = process.env.NVIDIA_EMBED_MODEL || "nvidia/nv-embedqa-e5-v5";
const DB_URL = process.env.DATABASE_URL || "";

const VECTOR_TOP_K = 5;
const FTS_TOP_K = 5;
const SIMILARITY_THRESHOLD = 0.30;

export interface PolicyEvidence {
  source_id: string;
  chunk_id: string;
  title: string;
  content: string;
  url: string | null;
  similarity?: number;
  retrieval_method: "vector" | "fts";
}

export interface RetrievalResult {
  evidence: PolicyEvidence[];
  method: "vector" | "fts" | "hybrid" | "none";
  query_embedding_ms: number;
  search_ms: number;
  total_ms: number;
}

async function embedQuery(text: string): Promise<number[]> {
  const body = JSON.stringify({
    input: [text.slice(0, 2048)],
    model: NVIDIA_EMBED_MODEL,
    input_type: "query",
  });

  const res = await fetch(NVIDIA_EMBED_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${NVIDIA_API_KEY}`,
      "Content-Type": "application/json",
    },
    body,
  });

  if (!res.ok) {
    const err = await res.text().catch(() => "");
    throw new Error(`NVIDIA embed API ${res.status}: ${err.slice(0, 200)}`);
  }

  const json = await res.json();
  return json.data[0].embedding;
}

async function vectorSearch(
  client: Client,
  embedding: number[],
  topK: number
): Promise<PolicyEvidence[]> {
  const vecStr = `[${embedding.join(",")}]`;
  const result = await client.query(
    `SELECT source_id, chunk_id, title, content, url,
            1 - (embedding <=> $1::vector) AS similarity
     FROM policy_chunks
     WHERE embedding IS NOT NULL
     ORDER BY embedding <=> $1::vector
     LIMIT $2`,
    [vecStr, topK]
  );

  return result.rows
    .filter((r: { similarity: number }) => r.similarity >= SIMILARITY_THRESHOLD)
    .map((r: { source_id: string; chunk_id: string; title: string; content: string; url: string | null; similarity: number }) => ({
      source_id: r.source_id,
      chunk_id: r.chunk_id,
      title: r.title,
      content: r.content,
      url: r.url,
      similarity: Math.round(r.similarity * 1000) / 1000,
      retrieval_method: "vector" as const,
    }));
}

async function ftsSearch(
  client: Client,
  query: string,
  topK: number
): Promise<PolicyEvidence[]> {
  const result = await client.query(
    `SELECT source_id, chunk_id, title, content, url,
            ts_rank(to_tsvector('english', content || ' ' || title),
                    websearch_to_tsquery('english', $1)) AS rank
     FROM policy_chunks
     WHERE to_tsvector('english', content || ' ' || title)
           @@ websearch_to_tsquery('english', $1)
     ORDER BY rank DESC
     LIMIT $2`,
    [query, topK]
  );

  return result.rows.map((r: { source_id: string; chunk_id: string; title: string; content: string; url: string | null }) => ({
    source_id: r.source_id,
    chunk_id: r.chunk_id,
    title: r.title,
    content: r.content,
    url: r.url,
    retrieval_method: "fts" as const,
  }));
}

function deduplicateEvidence(items: PolicyEvidence[]): PolicyEvidence[] {
  const seen = new Set<string>();
  return items.filter((e) => {
    const key = `${e.source_id}::${e.chunk_id}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export async function retrievePolicyEvidence(
  userMessage: string
): Promise<RetrievalResult> {
  const t0 = Date.now();

  if (!DB_URL) {
    return { evidence: [], method: "none", query_embedding_ms: 0, search_ms: 0, total_ms: 0 };
  }

  const client = new Client({ connectionString: DB_URL });
  try {
    await client.connect();

    let evidence: PolicyEvidence[] = [];
    let method: RetrievalResult["method"] = "none";
    let embeddingMs = 0;

    if (NVIDIA_API_KEY) {
      const embStart = Date.now();
      try {
        const embedding = await embedQuery(userMessage);
        embeddingMs = Date.now() - embStart;

        const searchStart = Date.now();
        evidence = await vectorSearch(client, embedding, VECTOR_TOP_K);
        const searchMs = Date.now() - searchStart;

        if (evidence.length >= 2) {
          method = "vector";
          return {
            evidence,
            method,
            query_embedding_ms: embeddingMs,
            search_ms: searchMs,
            total_ms: Date.now() - t0,
          };
        }

        const ftsResults = await ftsSearch(client, userMessage, FTS_TOP_K);
        const combined = deduplicateEvidence([...evidence, ...ftsResults]).slice(0, VECTOR_TOP_K);
        return {
          evidence: combined,
          method: combined.length > 0 ? "hybrid" : "none",
          query_embedding_ms: embeddingMs,
          search_ms: Date.now() - searchStart,
          total_ms: Date.now() - t0,
        };
      } catch (embedErr) {
        console.error("[retrieval] Embedding failed, falling back to FTS:", embedErr);
      }
    }

    const searchStart = Date.now();
    evidence = await ftsSearch(client, userMessage, FTS_TOP_K);
    method = evidence.length > 0 ? "fts" : "none";

    return {
      evidence,
      method,
      query_embedding_ms: embeddingMs,
      search_ms: Date.now() - searchStart,
      total_ms: Date.now() - t0,
    };
  } finally {
    await client.end();
  }
}
