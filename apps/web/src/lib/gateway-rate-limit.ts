/**
 * In-memory rate limiter for the gateway (P2).
 * Key = user_id (from envelope) or client IP. Window = 1 minute.
 * When GATEWAY_RATE_LIMIT_PER_MINUTE is set and > 0, requests over the limit get 429.
 * Not shared across instances; for multi-instance use Redis or similar (future).
 * See docs/GATEWAY-SHADOW-DESIGN.md.
 */

const WINDOW_MS = 60_000; // 1 minute

type Entry = { windowStart: number; count: number };
const store = new Map<string, Entry>();

function currentWindowStart(): number {
  return Math.floor(Date.now() / WINDOW_MS) * WINDOW_MS;
}

/**
 * @param key - Identifier (e.g. user_id or IP string).
 * @param limit - Max requests per minute; 0 = no limit.
 * @returns true if allowed, false if over limit.
 */
export function checkRateLimit(key: string, limit: number): boolean {
  if (limit <= 0) return true;
  const now = currentWindowStart();
  const entry = store.get(key);
  if (!entry) {
    store.set(key, { windowStart: now, count: 1 });
    return true;
  }
  if (entry.windowStart !== now) {
    entry.windowStart = now;
    entry.count = 1;
    return true;
  }
  entry.count += 1;
  return entry.count <= limit;
}

/**
 * Get remaining requests in current window (for optional X-RateLimit-* headers).
 * Returns undefined if limit is 0 (no limit).
 */
export function getRemaining(key: string, limit: number): number | undefined {
  if (limit <= 0) return undefined;
  const now = currentWindowStart();
  const entry = store.get(key);
  if (!entry || entry.windowStart !== now) return limit;
  return Math.max(0, limit - entry.count);
}

/**
 * Parse client IP from request (x-forwarded-for, x-real-ip, or connection).
 */
export function getClientIp(request: Request): string {
  const forwarded = request.headers.get("x-forwarded-for");
  if (forwarded) {
    const first = forwarded.split(",")[0]?.trim();
    if (first) return first;
  }
  const realIp = request.headers.get("x-real-ip");
  if (realIp) return realIp.trim();
  return "unknown";
}
