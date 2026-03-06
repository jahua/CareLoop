# Data Export and Deletion (Phase 3 P1-11)

Aligned with Technical Specification §17.4 and Swiss FADP (right to access, right to erasure).

## Scope

- **Profile-related data:** Personality states (OCEAN, confidence, stability), session-level summaries.
- **Session data:** Chat sessions, conversation turns, policy evidence, feedback logs, audit logs (when persisted).
- **Identifiers:** `session_id` is the primary pseudonymous key; no raw PII in DB (user message content may exist in `conversation_turns.user_msg` for operational need—see retention below).

## Retention (recommended defaults)

| Data | Retention | Notes |
|------|-----------|--------|
| `chat_sessions` | Until user requests deletion or 24 months inactive | Align with your governance. |
| `conversation_turns` | Same as sessions | Consider anonymising `user_msg` after 90 days if not needed for support. |
| `personality_states` | Same as sessions | Required for continuity; delete with session. |
| `policy_evidence` | Same as sessions | Citation audit; delete with session. |
| `audit_log` (file or DB) | Per compliance (e.g. 12–24 months) | No PII in audit payload; retain for debugging and compliance. |
| `feedback` (file) | Per product (e.g. 12 months) | Aggregate only for quality; no raw messages. |

Define exact retention in your privacy policy and document in `SECURITY-AND-PRIVACY.md` when fixed.

## Export (right to access)

**Goal:** Allow a user (identified by `session_id` or a stable pseudonymous ID) to receive a copy of their data.

**Implementation options:**

1. **API:** `GET /api/data/export?session_id=<uuid>` (optional: set `DATA_API_KEY` and send `x-api-key` or `Authorization: Bearer <key>`) returns a JSON bundle when `DATABASE_URL` or `AUDIT_DATABASE_URL` is set:
   - Session metadata (`chat_sessions` row).
   - Turns (`conversation_turns`: turn_index, mode, timestamps; optionally redacted `user_msg`/`assistant_msg`).
   - Personality states (`personality_states`: ocean, confidence, stable, turn_index).
   - Policy evidence references (`policy_evidence`: source_id, chunk_id, title, url).
   - No audit/feedback content (or only high-level stats if allowed by policy).

2. **Admin/script:** Export by `session_id` via SQL or a small script that queries the tables above and outputs JSON/CSV. Document the script and access path.

**Security:** Export must be restricted (auth, rate limit). Do not expose other users’ data. When `DATA_API_KEY` is set, the API requires the `x-api-key` header or `Authorization: Bearer <key>` to match.

## Deletion (right to erasure)

**Goal:** Permanently delete or anonymise all data linked to a user/session when requested.

**Implementation options:**

1. **API:** `POST /api/data/delete` with body `{ "session_id": "<uuid>" }` (optional: set `DATA_API_KEY` and send `x-api-key` or `Authorization: Bearer <key>`). When `DATABASE_URL` or `AUDIT_DATABASE_URL` is set, performs deletion:
   - Delete in order: `policy_evidence` → `personality_states` → `performance_metrics` → `conversation_turns` → `chat_sessions`. If `audit_log` is in DB, delete or anonymise by `session_id`. If using file audit/feedback, optionally scrub lines by session_id (or document that file logs are not per-session deletable and retain only for retention period).

2. **Admin/script:** Same ordering; run as one-off or scheduled job. Document in runbook.

**Verification:** After deletion, no row in any of the above tables should reference the `session_id`; optionally log the deletion (e.g. “session_id X deleted at timestamp”) for compliance proof.

## Consent for personality profiling

- Before storing or using OCEAN/personality state for adaptation, obtain explicit consent (e.g. in-app toggle or first-turn confirmation).
- If the user withdraws consent, stop updating personality state and optionally clear existing personality data for that session (or user) via the deletion flow above.

## References

- [SECURITY-AND-PRIVACY.md](SECURITY-AND-PRIVACY.md) – Overview and access paths
- [PRIVACY-AND-REDACTION.md](PRIVACY-AND-REDACTION.md) – Logging and redaction
- Technical Specification §17.4 (Security and Privacy Standards)
