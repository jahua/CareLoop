# Privacy and Redaction (Phase 3 P1-4)

Aligned with Technical Specification §5, §17.4 and Swiss FADP considerations. See also [SECURITY-AND-PRIVACY.md](SECURITY-AND-PRIVACY.md) for the full security and privacy posture.

## Logging policy

- **Pseudonymous identifiers only:** In audit and feedback logs we store only `session_id` and `request_id` (UUIDs). These do not directly identify a natural person and support correlation for debugging and compliance without exposing identity.
- **No user message content:** Audit JSONL (`AUDIT_LOG_PATH`) and feedback JSONL (`FEEDBACK_LOG_PATH`) do **not** include the user’s message text or any free-form input. Only structured fields (mode, pipeline status, citation counts, thumbs/score, timestamps) are written.
- **No raw PII in analytics:** Personal names, email addresses, and phone numbers must not appear in persistent logs or analytics exports. If any future code logs free text (e.g. error details that might contain user input), it must use the redaction helper first.

## Redaction helper

- **Location:** `apps/web/src/lib/redact.ts`
- **`redactForLog(text: string): string`** – Replaces common PII patterns (email, Swiss and generic phone numbers) with placeholders before writing to logs. Use this whenever logging content that might contain user input or contact details.

## Compliance notes

- Retention and deletion of audit/feedback files should follow your data governance policy (e.g. Swiss FADP).
- User consent for personality profiling is required before enabling that feature (Spec §17.4).
- Data export/delete controls for profile-related data should be implemented as required for production.
