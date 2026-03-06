/**
 * Data export by session_id – Phase 3 P1-11.
 * Returns session, turns, personality_states, policy_evidence. No audit/feedback content.
 * See docs/DATA-EXPORT-AND-DELETION.md.
 */

import type { Client } from "pg";

export type ExportBundle = {
  session: { session_id: string; created_at: string; status: string; locale: string | null; canton: string | null } | null;
  turns: Array<{ turn_index: number; mode: string | null; created_at: string; user_msg: string; assistant_msg: string | null; latency_ms: number | null }>;
  personality_states: Array<{ turn_index: number; ocean_json: unknown; confidence_json: unknown; stable: boolean; created_at: string }>;
  policy_evidence: Array<{ turn_index: number; source_id: string; chunk_id: string; title: string | null; url: string | null }>;
};

export async function exportSessionData(client: Client, sessionId: string): Promise<ExportBundle> {
  const sessionResult = await client.query(
    "SELECT session_id, created_at, status, locale, canton FROM chat_sessions WHERE session_id = $1::uuid",
    [sessionId]
  );
  const turnsResult = await client.query(
    "SELECT turn_index, mode, created_at, user_msg, assistant_msg, latency_ms FROM conversation_turns WHERE session_id = $1::uuid ORDER BY turn_index",
    [sessionId]
  );
  const personalityResult = await client.query(
    "SELECT turn_index, ocean_json, confidence_json, stable, created_at FROM personality_states WHERE session_id = $1::uuid ORDER BY turn_index",
    [sessionId]
  );
  const evidenceResult = await client.query(
    "SELECT turn_index, source_id, chunk_id, title, url FROM policy_evidence WHERE session_id = $1::uuid ORDER BY turn_index, source_id, chunk_id",
    [sessionId]
  );

  const sessionRow = sessionResult.rows[0];
  return {
    session: sessionRow
      ? {
          session_id: sessionRow.session_id,
          created_at: sessionRow.created_at,
          status: sessionRow.status,
          locale: sessionRow.locale ?? null,
          canton: sessionRow.canton ?? null,
        }
      : null,
    turns: turnsResult.rows.map((r) => ({
      turn_index: r.turn_index,
      mode: r.mode ?? null,
      created_at: r.created_at,
      user_msg: r.user_msg,
      assistant_msg: r.assistant_msg ?? null,
      latency_ms: r.latency_ms ?? null,
    })),
    personality_states: personalityResult.rows.map((r) => ({
      turn_index: r.turn_index,
      ocean_json: r.ocean_json,
      confidence_json: r.confidence_json,
      stable: r.stable,
      created_at: r.created_at,
    })),
    policy_evidence: evidenceResult.rows.map((r) => ({
      turn_index: r.turn_index,
      source_id: r.source_id,
      chunk_id: r.chunk_id,
      title: r.title ?? null,
      url: r.url ?? null,
    })),
  };
}
