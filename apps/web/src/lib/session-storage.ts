const KEY = "big5loop_recent_sessions";
const MAX = 20;

export type RecentSession = {
  id: string;
  /** Display label: first user message preview or fallback */
  label: string;
  messageCount: number;
  lastUsed: string;
};

function getStored(): RecentSession[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (x): x is RecentSession =>
        x != null &&
        typeof x === "object" &&
        typeof (x as RecentSession).id === "string" &&
        typeof (x as RecentSession).label === "string"
    );
  } catch {
    return [];
  }
}

function setStored(list: RecentSession[]): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(KEY, JSON.stringify(list.slice(0, MAX)));
  } catch {
    /* quota exceeded */
  }
}

export function touchRecentSession(
  sessionId: string,
  messageCount: number,
  firstUserMessage?: string
): void {
  const list = getStored();
  const existing = list.find((s) => s.id === sessionId);
  const filtered = list.filter((s) => s.id !== sessionId);

  const label =
    firstUserMessage?.trim().slice(0, 60) ||
    existing?.label ||
    "New conversation";

  filtered.unshift({
    id: sessionId,
    label,
    messageCount,
    lastUsed: new Date().toISOString(),
  });
  setStored(filtered);
}

export function getRecentSessions(): RecentSession[] {
  return getStored();
}

export function removeRecentSession(sessionId: string): void {
  setStored(getStored().filter((s) => s.id !== sessionId));
}
