/**
 * Data deletion by session_id – Phase 3 P1-11.
 * Deletes in order: policy_evidence → personality_states → performance_metrics → conversation_turns → audit_log → chat_sessions.
 * See docs/DATA-EXPORT-AND-DELETION.md.
 */

import type { Client } from "pg";

export type DeleteResult = {
  deleted: {
    policy_evidence: number;
    personality_states: number;
    performance_metrics: number;
    conversation_turns: number;
    audit_log: number;
    chat_sessions: number;
  };
};

export async function deleteSessionData(client: Client, sessionId: string): Promise<DeleteResult> {
  const result = { policy_evidence: 0, personality_states: 0, performance_metrics: 0, conversation_turns: 0, audit_log: 0, chat_sessions: 0 };

  const r1 = await client.query("DELETE FROM policy_evidence WHERE session_id = $1::uuid", [sessionId]);
  result.policy_evidence = r1.rowCount ?? 0;

  const r2 = await client.query("DELETE FROM personality_states WHERE session_id = $1::uuid", [sessionId]);
  result.personality_states = r2.rowCount ?? 0;

  const r3 = await client.query("DELETE FROM performance_metrics WHERE session_id = $1::uuid", [sessionId]);
  result.performance_metrics = r3.rowCount ?? 0;

  const r4 = await client.query("DELETE FROM conversation_turns WHERE session_id = $1::uuid", [sessionId]);
  result.conversation_turns = r4.rowCount ?? 0;

  const r5 = await client.query("DELETE FROM audit_log WHERE session_id = $1::uuid", [sessionId]);
  result.audit_log = r5.rowCount ?? 0;

  const r6 = await client.query("DELETE FROM chat_sessions WHERE session_id = $1::uuid", [sessionId]);
  result.chat_sessions = r6.rowCount ?? 0;

  return { deleted: result };
}
