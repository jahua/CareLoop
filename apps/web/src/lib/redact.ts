/**
 * Phase 3 P1-4: Redaction for logs (Spec §5, §17.4).
 * Use before writing any user-generated or PII-bearing text to logs or analytics.
 * Audit and feedback payloads do not include raw user message content; this helper
 * is for any future code that might log free text.
 */

const EMAIL_RE = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const SWISS_PHONE_RE = /(\+41|0041|0)\s*[1-9]\d{1,2}\s*\d{3}\s*\d{2}\s*\d{2}/g;
const GENERIC_PHONE_RE = /\+\d{1,3}[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{0,4}/g;

/**
 * Redact common PII patterns from a string before logging.
 * Returns a string safe for persistent logs (no raw email, phone numbers).
 */
export function redactForLog(text: string): string {
  if (typeof text !== "string") return "[invalid]";
  return text
    .replace(EMAIL_RE, "[REDACTED_EMAIL]")
    .replace(SWISS_PHONE_RE, "[REDACTED_PHONE]")
    .replace(GENERIC_PHONE_RE, "[REDACTED_PHONE]");
}

/**
 * Policy: Audit and feedback logs use only pseudonymous identifiers.
 * - session_id, request_id: UUIDs (no direct link to user identity).
 * - We do not log user message content in audit or feedback payloads.
 * - If any code path logs free text (e.g. error messages containing input), use redactForLog first.
 */
