/**
 * CareLoop frontend API client (FRONTEND-IMPROVEMENTS-TODO §6.3).
 * Chat, feedback, health, data export/delete.
 */

export type ExportBundle = {
  session: {
    session_id: string;
    created_at: string;
    status: string;
    locale: string | null;
    canton: string | null;
  } | null;
  turns: Array<{
    turn_index: number;
    mode: string | null;
    created_at: string;
    user_msg: string;
    assistant_msg: string | null;
    latency_ms: number | null;
  }>;
  personality_states: Array<{
    turn_index: number;
    ocean_json: unknown;
    confidence_json: unknown;
    stable: boolean;
    created_at: string;
  }>;
  policy_evidence: Array<{
    turn_index: number;
    source_id: string;
    chunk_id: string;
    title: string | null;
    url: string | null;
  }>;
};

export type ExportResponse =
  | { success: true; data: ExportBundle }
  | { success: false; error?: string; message?: string };

export type DeleteResponse =
  | { success: true; deleted?: Record<string, number> }
  | { success: false; error?: string; message?: string };

/**
 * Fetch session data for history restore. Uses GET /api/data/export.
 * Returns null if export not configured (501) or unauthorized (401).
 */
export async function fetchSessionHistory(
  sessionId: string,
  apiKey?: string
): Promise<ExportBundle | null> {
  const headers: Record<string, string> = {};
  if (apiKey) headers["x-api-key"] = apiKey;
  const res = await fetch(
    `/api/data/export?session_id=${encodeURIComponent(sessionId)}`,
    { headers }
  );
  if (res.status === 401 || res.status === 501) return null;
  if (!res.ok) return null;
  const json = (await res.json()) as ExportResponse;
  if (!json.success || !("data" in json)) return null;
  return json.data;
}

/**
 * Export session data and return the bundle (for download or display).
 */
export async function exportSessionData(
  sessionId: string,
  apiKey?: string
): Promise<ExportBundle | { error: string }> {
  const headers: Record<string, string> = {};
  if (apiKey) headers["x-api-key"] = apiKey;
  const res = await fetch(
    `/api/data/export?session_id=${encodeURIComponent(sessionId)}`,
    { headers }
  );
  const json = (await res.json()) as ExportResponse & { message?: string };
  if (!res.ok) {
    const msg =
      (typeof (json as { error?: string }).error === "string"
        ? (json as { error: string }).error
        : (json as { message?: string }).message) ?? `HTTP ${res.status}`;
    return { error: msg };
  }
  if (!("data" in json) || !json.success) {
    return { error: "Invalid export response" };
  }
  return json.data;
}

/**
 * Delete all data for a session. Uses POST /api/data/delete.
 */
export async function deleteSessionData(
  sessionId: string,
  apiKey?: string
): Promise<{ ok: true } | { error: string }> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (apiKey) headers["x-api-key"] = apiKey;
  const res = await fetch("/api/data/delete", {
    method: "POST",
    headers,
    body: JSON.stringify({ session_id: sessionId }),
  });
  const json = (await res.json()) as DeleteResponse & { message?: string };
  if (!res.ok) {
    const msg =
      (typeof (json as { error?: string }).error === "string"
        ? (json as { error: string }).error
        : (json as { message?: string }).message) ?? `HTTP ${res.status}`;
    return { error: msg };
  }
  if (!("success" in json) || !json.success) {
    return { error: (json as { error?: string }).error ?? "Delete failed" };
  }
  return { ok: true };
}
