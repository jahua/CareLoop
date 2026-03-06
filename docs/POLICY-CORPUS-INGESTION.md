# Policy Corpus Ingestion

**Phase:** **Phase 2** (RAG and Policy Navigation). Corpus setup and ingestion are part of Phase 2 “Corpus and governance” and “Domain packs” (ROADMAP §5.2, §5.3).

---

## When to ingest

- **Initial load:** When the database has no (or too few) rows in `policy_chunks`, policy retrieval in the workflow will return no evidence. Ingest seed data so the Policy Navigation pillar can return cited answers.
- **DB init:** `infra/database/init.sql` creates `policy_chunks` and inserts 3 IV (Invalidenversicherung) seed chunks **only on first database creation** (when the Postgres data volume is empty). If you use an existing volume or a DB that was created before this script existed, the table may be empty.

---

## How to ingest (get policy chunks into the DB)

### Option 1: Run the seed script (recommended)

With the DB running (e.g. `docker compose up -d db` or your Postgres):

```bash
cd CareLoop
export DATABASE_URL="postgresql://careloop:YOUR_PASSWORD@localhost:5432/careloop"
npm run seed:policy
```

Default if `DATABASE_URL` is unset: `postgresql://careloop:changeme@localhost:5432/careloop`.

This creates `policy_chunks` (if missing), adds the full-text index, and inserts/updates the 3 IV seed chunks.

### Option 2: Run init SQL on an existing DB

If you prefer to run the SQL yourself:

```bash
psql "$DATABASE_URL" -f infra/database/init.sql
```

Note: `init.sql` also creates other tables (e.g. `chat_sessions`, `conversation_turns`). If those already exist, the script is idempotent (CREATE IF NOT EXISTS, ON CONFLICT DO NOTHING). Running it again is safe; it will add the policy seed rows if missing.

### Option 3: Fresh DB (Docker)

To get a clean DB that runs `init.sql` automatically:

```bash
cd CareLoop
docker compose -f infra/docker/docker-compose.yml down -v   # remove volumes
docker compose --env-file .env -f infra/docker/docker-compose.yml up -d db
```

Then start N8N and web as needed. The first `up` with a new volume runs `01-init.sql` and seeds the 3 policy chunks.

---

## What gets ingested

- **Current seed:** 3 chunks for IV (Invalidenversicherung): eligibility basics, registration process, Zurich supplementary benefits. Same content as in `init.sql` and `scripts/setup-rag-db.js`.
- **Adding more:** To add more policy or education content:
  - **From open resources (scrape/copy → chunks):** Put documents in a JSON file and run the chunk script. See **[Scraping and chunking open resources](SCRAPING-AND-CHUNKING-OPEN-RESOURCES.md)** and `npm run chunk:policy`.
  - **Manual seed:** Extend `scripts/setup-rag-db.js` or add INSERTs and run `npm run seed:policy` or SQL.
- Phase 3 P2-9 (background jobs) will later add corpus freshness and re-embedding; initial ingestion remains a Phase 2–style corpus setup.

---

## Education data

There is no separate education corpus or table yet. The Practical Education pillar uses regulation and generation only. If you add an education knowledge base later, ingestion would follow the same pattern (e.g. a table + seed script or ETL in the same phase as “corpus and governance”).
