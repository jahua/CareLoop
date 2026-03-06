# Background Jobs and Corpus Hygiene (P2-9)

Design for scheduled and on-demand jobs: corpus freshness, citation validity, and retrieval quality regression. Aligned with Technical Specification §15.1.E.

---

## 1. Job types

| Job | Purpose | Suggested schedule | Output / telemetry |
|-----|---------|--------------------|--------------------|
| **Corpus freshness** | Check policy_chunks count, DB connectivity; optionally alert if empty or stale. | Daily (cron) or on-demand | job_id, job_type, status, duration_ms, chunk_count, min_created_at |
| **Source recrawl / re-embedding** | Trigger ingestion pipeline for updated sources; re-embed and upsert into policy_chunks. | Weekly or after source config change | job_id, job_type, status, duration_ms, sources_processed, chunks_upserted |
| **Stale citation detector** | Check citation URLs or version hashes; flag broken or outdated links. | Weekly or on-demand | job_id, job_type, status, duration_ms, checked_count, stale_count |
| **Retrieval quality regression** | Run benchmark questions against retrieval (and optionally full pipeline); compare recall/precision or citation coverage. | On release candidate or weekly | job_id, job_type, status, duration_ms, pass_count, fail_count, details |

**Safety:** Jobs must not mutate production data without explicit confirmation or dry-run mode where applicable (e.g. re-embedding should support preview).

---

## 2. Telemetry (Spec §15.1.E)

Emit structured job telemetry so that runs are observable. Spec mentions `performance_metrics` with `stage=background_job`; that table is tied to `session_id`/`turn_index`, so for jobs use either:

- **Option A – File (current):** Append one JSONL line per run to a log file (e.g. `BACKGROUND_JOB_LOG_PATH`). Each line: `job_id`, `job_type`, `stage: "background_job"`, `status`, `duration_ms`, `error_code?`, `details?`, `created_at`.
- **Option B – Dedicated table (future):** Add `background_job_runs (id, job_type, stage, status, duration_ms, error_code, details JSONB, created_at)` and write there for querying and alerting.

Same shape can be used for both; scripts should accept an env var for log path and, when available, DB write.

---

## 3. Corpus freshness check (first job)

- **Input:** `DATABASE_URL` (or `AUDIT_DATABASE_URL`).
- **Logic:** Connect to DB; `SELECT COUNT(*) FROM policy_chunks`; optionally `SELECT MIN(created_at) FROM policy_chunks`. If connection fails or count is 0 (and a non-empty corpus is expected), set `status: "fail"` and `error_code` accordingly.
- **Output:** One telemetry record (file and/or DB). Optional: exit code 1 on failure for cron alerting.
- **Script:** `scripts/corpus-freshness-check.js` (or under `scripts/jobs/`). Run with `node scripts/corpus-freshness-check.js`; schedule via cron or CI.

---

## 4. Retrieval regression suite

- **Input:** A set of benchmark questions (and expected source/chunk IDs or expected behaviour). See [PILLAR-TEST-MATRIX-EXECUTION.md](PILLAR-TEST-MATRIX-EXECUTION.md) for policy test cases; retrieval-only subset can run without full generation.
- **Logic:** For each question, call retrieval (or full pipeline); assert that expected chunks appear in top-k or that citation coverage meets threshold. Aggregate pass/fail.
- **Output:** Telemetry record with pass_count, fail_count, and optional details (e.g. which cases failed). Block or alert on regression when run in CI.
- **Smoke script:** `scripts/retrieval-regression-smoke.js` runs a single policy question via `POST /api/chat`; `npm run job:retrieval-smoke`.
- **Multi-case runner:** `scripts/retrieval-regression-runner.js` runs multiple cases from a JSON file (or built-in defaults). Usage: `node scripts/retrieval-regression-runner.js [path-to-cases.json]`. Cases format: `[ { case_id, message, context?, require_policy_mode?, expected_coaching_mode?, min_citations? } ]`. This allows explicit policy-intent assertions (for example, require `coaching_mode=policy_navigation`) to catch unintended fallback to emotional mode. Example file: `scripts/fixtures/retrieval-cases.json`. Emits one JSONL line (job_type `retrieval_regression`, pass_count, fail_count, failures). `npm run job:retrieval-regression` (default cases) or `npm run job:retrieval-regression -- scripts/fixtures/retrieval-cases.json`.

---

## 5. Stale citation detector

- **Input:** Chunks with URLs (e.g. from `policy_chunks.url` or metadata). Optional: version hash or last-checked timestamp per source.
- **Logic:** HEAD or GET requests to URLs (with rate limit and timeout); compare version hash if available. Record which links are broken or outdated.
- **Output:** Telemetry + report (e.g. list of stale/broken URLs). No automatic deletion; human or separate process decides re-crawl or removal.
- **Script:** `scripts/stale-citation-detector.js` → `npm run job:stale-citation`.
  - Reads distinct URLs from `policy_chunks`.
  - Probes each URL with timeout (`STALE_CITATION_TIMEOUT_MS`, default 5000ms), using HEAD and optional GET fallback.
  - Emits JSONL telemetry with `checked_count`, `stale_count`, `stale_ratio`, and `stale_samples`.
  - Exit 1 when stale ratio exceeds `STALE_CITATION_FAIL_THRESHOLD` (default 0.1) or URL set is empty.

---

## 6. Scheduling and execution

- **Cron:** Use system cron or a scheduler (e.g. GitHub Actions, Kubernetes CronJob) to run scripts. Example: `0 2 * * * cd /app && node scripts/corpus-freshness-check.js`.
- **Env:** Document required env (e.g. `DATABASE_URL`, `BACKGROUND_JOB_LOG_PATH`) in `.env.example` and runbook.
- **Queue (future):** For horizontal scaling, run workers that consume jobs from a queue; emit same telemetry per job. See Spec §15.1.E: "Use queue-backed workers for background tasks".

---

## 7. Implementation order (suggested)

1. **Telemetry shape:** Define and document the JSONL line shape (job_id, job_type, stage, status, duration_ms, error_code, details, created_at).
2. **Corpus freshness:** Implement `scripts/corpus-freshness-check.js`; write telemetry to file (and optionally to a new table later). Add `BACKGROUND_JOB_LOG_PATH` to `.env.example`. Add npm script `job:corpus-freshness`.
3. **Regression suite:** Add retrieval benchmark script or extend pillar test runner; emit same telemetry for "retrieval_regression" job type.
4. **Stale citation + re-embedding:** Stale citation detector script implemented (`job:stale-citation`). Re-embedding remains pending and should share the same telemetry pattern.

### 7.1 Source recrawl / re-embedding baseline

- **Script:** `scripts/source-recrawl-reembed.js` → `npm run job:source-recrawl`.
- **Input:**
  - Source registry: `SOURCE_CONFIG_PATH` (default `data/sources/cantonal/sources.config.json`)
  - Fetched documents: `SOURCE_DOCUMENTS_PATH` (default `data/documents/cantonal/documents.json`)
- **Logic:**
  - Compute content hash per source from fetched documents.
  - Compare against latest stored `metadata.content_hash` for each `source_id` in `policy_chunks`.
  - If changed, mark source for recrawl/re-embedding.
  - In apply mode (`SOURCE_RECRAWL_DRY_RUN=0`): replace existing chunks for changed source with re-chunked content and updated metadata hash.
- **Safety default:** dry-run is enabled by default (`SOURCE_RECRAWL_DRY_RUN=1`).
- **Telemetry:** `sources_checked`, `sources_changed`, `sources_unchanged`, `sources_missing_content`, `chunks_deleted`, `chunks_upserted`, `changed_sources`.

---

## References

- **Spec:** §15.1.E (Scheduler and Background Ops)
- **TODO:** [PHASE3-TODO.md](PHASE3-TODO.md) P2-9
- **Pillar matrix:** [PILLAR-TEST-MATRIX-EXECUTION.md](PILLAR-TEST-MATRIX-EXECUTION.md) (benchmark cases)
