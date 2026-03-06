# Audit Log Persistence (Phase 3 P1-3)

Phase 3 audit emits one JSONL line per turn to a file when `AUDIT_LOG_PATH` is set (see `apps/web/src/lib/audit.ts`). When **compliance requires** storing audit records in the database, use the `audit_log` table.

## Schema

The table is created by `infra/database/init.sql`:

- **audit_log**: `id`, `request_id`, `session_id`, `turn_index`, `coaching_mode`, `pipeline_status` (JSONB), `personality` (JSONB), `retrieval_ids` (TEXT[]), `citation_count`, `verifier_status`, `input_hash`, `turn_latency_ms`, `created_at`.
- Indexes: `(session_id, turn_index)`, `request_id`, `created_at`.

The columns match the fields of `AuditTurnPayload` in `apps/web/src/lib/audit.ts` so the same payload can be written to DB.

## When to persist to DB

- **File-only (default):** Set `AUDIT_LOG_PATH`; no DB write. Sufficient for local/dev and many deployments.
- **DB persistence:** When your governance or Swiss FADP retention/audit requirements demand queryable audit records, implement a second write from the API (or a log shipper) into `audit_log`.

## Implementing DB persistence

1. Ensure the `audit_log` table exists (run `init.sql` or apply the same DDL).
2. In the app that builds the audit payload (currently the Next.js chat route), after calling `auditTurn(payload)` for the file, optionally insert into PostgreSQL using the same `AuditTurnPayload`:
   - Map `pipeline_status` object → `pipeline_status` JSONB.
   - Map `personality` object → `personality` JSONB.
   - Map `retrieval_ids` array → `retrieval_ids` TEXT[].
3. Use an env var (e.g. `AUDIT_DB_WRITE=true` or a dedicated `DATABASE_URL` for the web app) to gate the DB write so file-only remains the default.
4. Keep the write non-blocking (e.g. fire-and-forget or background job) so the response path is not delayed.

**Implemented (P1-3):** When `AUDIT_DB_WRITE=true` and `AUDIT_DATABASE_URL` (or `DATABASE_URL`) is set, the chat API calls `writeAuditToDb(payload)` after each successful turn. See `apps/web/src/lib/audit-db.ts`; the write is fire-and-forget (non-blocking). Ensure the `audit_log` table exists (run `infra/database/init.sql`).

## References

- `apps/web/src/lib/audit.ts` – `AuditTurnPayload`, `buildAuditPayload`, `auditTurn`
- `infra/database/init.sql` – `audit_log` table and indexes
- `docs/PRIVACY-AND-REDACTION.md` – no raw user content in audit
