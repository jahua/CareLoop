# N8N workflows

## Phase 0 skeleton

Import `big5loop-phase0-skeleton.json` in N8N (http://localhost:5678):

1. Workflow → Import from File → select `big5loop-phase0-skeleton.json`
2. Activate the workflow.
3. POST to `http://localhost:5678/webhook/big5loop-turn` with body:
   ```json
   {
     "session_id": "<uuid>",
     "turn_index": 1,
     "message": "Hello",
     "context": { "language": "en", "canton": "ZH" }
   }
   ```
4. Response matches §6.4 (Final Response Output) with stub content.

To persist turns: add PostgreSQL credentials in N8N and connect the optional Insert Session / Insert Turn nodes (see workflow comments).

---

## Phase 1 MVP (Detection → EMA → Mode → Build Response → Respond)

Import `big5loop-phase1-mvp.json`:

1. Import and activate the workflow.
2. **Run Next.js on the host** so the EMA step can call `http://host.docker.internal:3000/api/personality/ema`.  
   From Big5Loop root: `npm run dev --workspace=web` (or `cd apps/web && npm run dev`).
3. If N8N runs on the same host (not in Docker), change the EMA Code node URL to `http://localhost:3000/api/personality/ema`.
4. Response includes `personality_state` (OCEAN + stable + ema_applied) and `coaching_mode` (e.g. `emotional_support`).
5. Frontend shows OCEAN and mode when the response contains them.

---

## Imported from `pmt/MVP/workflows/N8N/phase1-2-postgres.json`

Import `big5loop-phase1-2-postgres-mvp.json`:

1. Workflow -> Import from File -> select `big5loop-phase1-2-postgres-mvp.json`
2. Activate the workflow.
3. This is adapted from the MVP file you pointed to: `pmt/MVP/workflows/N8N/phase1-2-postgres.json`.
4. Webhook path is normalized to `big5loop-turn` for Big5Loop frontend compatibility.
5. Configure PostgreSQL credential in N8N as **Big5Loop PostgreSQL** before enabling DB writes.
6. Set NVIDIA runtime env in `Big5Loop/.env`: `NVIDIA_API_URL`, `NVIDIA_API_KEY`, `NVIDIA_MODEL`.
7. This workflow already includes hybrid memory nodes:
   - `Build Memory Query Vector` → `Hybrid Memory Retrieve (pgvector)` → `Attach Hybrid Memory Context`
   - `Build Memory Write Payload` → `Hybrid Memory Write (pgvector)`


---

## Gemma 3 + Hybrid External Memory

Recommended production direction for this repo:

1. Keep `big5loop-phase1-2-postgres-mvp.json` as core runtime workflow.
2. Serve Gemma 3 (`google/gemma-3-12b-it`) via OpenAI-compatible API (vLLM/TGI).
3. Keep PostgreSQL for audit + EMA state; add pgvector retrieval for long-term memory recall.

---

## Phase 5 — PANDORA evaluation (v4)

Import `big5loop-pandora-eval-v4.json`:

1. **Workflow → Import from File** → select `big5loop-pandora-eval-v4.json`.
2. **Activate** the workflow (toggle) **and** under n8n **2.x** run **Publish** so the webhook is registered (`Draft` alone can yield HTTP 404 on `/webhook/...`). From Docker:  
   `docker exec docker-n8n-1 n8n publish:workflow --id=<workflow-uuid>` then `docker restart docker-n8n-1`.
3. Ensure only **one** workflow uses path `big5loop-pandora-eval-v4` (duplicate imports can bind the webhook to an old copy). The `Respond to Webhook` node must keep that **exact name** when `Webhook` uses *Respond using Respond to Webhook*.
4. POST to `http://localhost:5678/webhook/big5loop-pandora-eval-v4` (same body shape as parallel v3; optional `ground_truth_ocean` and `pandora_sample_id` for benchmark runs).

This export is derived from `big5loop-phase1-2-parallel-v3.json` with a dedicated webhook path and `pandora_evaluation: true` in ingest. See **`evaluation_data/PHASE5-SPECIFICATION.md`** (naming, testing, versioning), `evaluation_data/PHASE5-PANDORA.md`, and `ROADMAP.md` §8.

---

## Phase 5 — PANDORA evaluation v4 **(five detector nodes)** — canonical for `/api/chat`

Use this workflow when the Next.js app should run the **5 parallel NVIDIA trait detectors** (O, C, E, A, N fan out after `Stamp parallel detection start`, then `Merge parallel trait branches` → `Assemble OCEAN (parallel)`). Detection timing reports `five_parallel_nvidia_calls`.

| | |
|---|---|
| **N8N name** | Big5Loop Phase 5 PANDORA Evaluation v4 (5 detector nodes) |
| **Workflow id** | `940251a5-dd5b-4f5f-b024-513023536523` |
| **Export file** | `big5loop-pandora-eval-v4-five-detectors.json` |
| **Webhook path (POST)** | `big5loop-pandora-eval-v4-five` |
| **App env** | `N8N_DEFAULT_WORKFLOW_PATH=big5loop-pandora-eval-v4-five` (set in Docker Compose and `.env.example`) |

1. Import `big5loop-pandora-eval-v4-five-detectors.json`, **Activate**, **Publish** (n8n 2.x).
2. Ensure no other active workflow registers the same path + method.
3. Re-import updates the same workflow when the JSON `id` matches the UUID above (`scripts/build_pandora_eval_v4_five_detectors.py` keeps it stable).
