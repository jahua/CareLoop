# Security and Privacy (Phase 3 P1-11)

Aligned with Technical Specification §17.4 and Swiss FADP considerations.

## Security

- **Secrets:** Stored only in environment variables or a secret manager; never in code or Git. See [SECRETS-AND-CREDENTIALS.md](SECRETS-AND-CREDENTIALS.md).
- **Least privilege:** Service accounts and data access paths should use minimal required permissions; document access patterns for production.
- **No raw errors to clients:** All failure paths return structured envelopes (no stack traces). See Phase 3 error contract in `packages/contracts` and chat API.

### Access paths (deployed services)

| Component | Accesses | Purpose |
|-----------|----------|---------|
| **Next.js (apps/web)** | N8N webhook URL (env); optional `AUDIT_LOG_PATH`, `FEEDBACK_LOG_PATH` (file system) | Chat API proxies to N8N; audit/feedback JSONL when enabled. No direct DB. |
| **N8N workflow** | PostgreSQL (sessions, turns, personality_state, policy_chunks, etc.); LLM provider (env); optional RAG/verifier services | Orchestration, detector, generator, RAG retrieval, verifier, DB reads/writes. |
| **PostgreSQL** | Receives connections from N8N (and any future gateway/backend). | Single source of truth for sessions, turns, embeddings, policy corpus, metrics. |
| **Future gateway** | Next.js or N8N (routing); auth provider; rate-limit store. | Session lifecycle, authN/authZ, correlation IDs, routing (Spec §15.1.A). |

For production: restrict DB credentials to the minimal set of roles (e.g. N8N role with read/write only to required tables); ensure env vars for N8N webhook and LLM keys are not exposed to the frontend.

## Privacy and logging

- **Redaction and pseudonymization:** No raw user message content in audit or feedback logs; only pseudonymous identifiers (`session_id`, `request_id`). Use `redactForLog()` for any future free-text logging. See [PRIVACY-AND-REDACTION.md](PRIVACY-AND-REDACTION.md).
- **Retention and deletion:** Define retention and deletion policies for audit logs, feedback logs, and DB data in line with Swiss FADP and your governance. See [DATA-EXPORT-AND-DELETION.md](DATA-EXPORT-AND-DELETION.md) for recommended retention defaults and deletion order.
- **Personality profiling:** Explicit user consent is required before enabling personality profiling features.
- **Data export/delete:** Implement export and delete controls for profile-related and session data to support user requests (e.g. right to erasure). See [DATA-EXPORT-AND-DELETION.md](DATA-EXPORT-AND-DELETION.md) for API/script contracts, retention table, and consent.

## References

- Spec §17.4 (Security and Privacy Standards)
- [PRIVACY-AND-REDACTION.md](PRIVACY-AND-REDACTION.md) – Logging policy and redaction helper
- [SECRETS-AND-CREDENTIALS.md](SECRETS-AND-CREDENTIALS.md) – Credential storage
