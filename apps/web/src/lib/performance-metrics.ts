/**
 * P1-10: Write stage timings from workflow response to performance_metrics.
 * When N8N returns stage_timings in the response, the chat route calls this to persist.
 * Fire-and-forget; does not block the response. Table has FK to conversation_turns.
 * See docs/SLO-AND-MONITORING.md and Technical Spec §15.1.F.
 */

import { hasDatabase, withDb } from "@/lib/db";

export type StageTiming = {
  stage: string;
  status: string;
  duration_ms?: number;
  error_code?: string;
};

const INSERT_SQL = `
  INSERT INTO performance_metrics (session_id, turn_index, stage, status, duration_ms, error_code)
  VALUES ($1::uuid, $2::int, $3, $4, $5, $6)
`;

function isValidTiming(t: unknown): t is StageTiming {
  if (!t || typeof t !== "object") return false;
  const o = t as Record<string, unknown>;
  return (
    typeof o.stage === "string" &&
    o.stage.length > 0 &&
    typeof o.status === "string" &&
    o.status.length > 0
  );
}

/**
 * Persist stage_timings to performance_metrics. Call from chat route when workflow returns stage_timings.
 * Runs asynchronously; errors are ignored so the response is not blocked.
 */
export function writeStageTimingsToDb(
  sessionId: string,
  turnIndex: number,
  timings: unknown
): void {
  if (!hasDatabase()) return;
  const arr = Array.isArray(timings) ? timings : [];
  const valid = arr.filter(isValidTiming);
  if (valid.length === 0) return;

  setImmediate(() => {
    withDb(async (client) => {
      for (const t of valid) {
        await client.query(INSERT_SQL, [
          sessionId,
          turnIndex,
          t.stage,
          t.status,
          t.duration_ms ?? null,
          t.error_code ?? null,
        ]);
      }
    }).catch(() => {});
  });
}
