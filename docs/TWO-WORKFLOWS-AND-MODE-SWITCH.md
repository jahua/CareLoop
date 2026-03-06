# Two Workflows and Frontend Mode Switch

The frontend can switch between **Simple**, **Standard**, and **Detailed** chat modes. Simple mode uses a second, lightweight N8N workflow; Standard and Detailed use the full pipeline. **Prefer handling mode/workflow in the gateway** when traffic goes through `POST /api/gateway/chat`: the gateway sets `context.model_tier` and `workflow` from `routing_hints`, so routing policy lives in one place (see [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md)).

---

## 1. Frontend mode switch

- **Simple** → `context.model_tier: "light"`, `workflow: "simple"`. API calls webhook `careloop-turn-simple`. Use for quick replies without RAG or full detection.
- **Standard** → `context.model_tier: "medium"`, no `workflow`. API calls webhook `careloop-turn`. Full pipeline (detection, RAG, verification).
- **Detailed** → `context.model_tier: "heavy"`, no `workflow`. Same webhook `careloop-turn`; workflow can use `context.model_tier` for heavier reasoning/params later.

The UI shows three buttons (Simple | Standard | Detailed). The chosen mode is sent with every chat request.

---

## 2. Two N8N workflows

| Workflow file | Webhook path | Purpose |
|---------------|--------------|---------|
| `careloop-phase1-2-postgres-mvp.json` | `careloop-turn` | Full pipeline: ingest, detection, regulation, RAG, generation, verification, DB. |
| `careloop-turn-simple.json` | `careloop-turn-simple` | Quick mode: webhook → short reply → respond. No DB, no RAG, no detection. |

**Import in N8N:**

1. **Standard/Detailed:** Import and activate `workflows/n8n/careloop-phase1-2-postgres-mvp.json` (webhook path `careloop-turn`).
2. **Simple:** Import and activate `workflows/n8n/careloop-turn-simple.json` (webhook path `careloop-turn-simple`).

Both must be **active** if the user can switch to Simple in the UI. If the simple workflow is not imported or not active, choosing Simple returns 404 from N8N and the API returns an error.

---

## 3. API behaviour

- **Chat route** (`POST /api/chat`): Reads `body.workflow`. If `workflow === "simple"`, requests go to `${N8N_WEBHOOK_URL}/webhook/careloop-turn-simple`; otherwise to `/webhook/careloop-turn`. The body (including `context.model_tier`) is forwarded as-is.

---

## 4. Gateway-handled modes (recommended)

When the frontend calls **`POST /api/gateway/chat`** instead of `/api/chat`, send the envelope with **`routing_hints`**:

- `routing_hints.model_tier`: `"light"` | `"medium"` | `"heavy"` (optional; default `medium`).
- `routing_hints.workflow`: `"simple"` (optional). If omitted, the gateway sets `workflow: "simple"` when `model_tier === "light"`.

The gateway then builds the body for `/api/chat`: it sets `context.model_tier` and `workflow: "simple"` when appropriate, so the chat API routes to the correct N8N webhook. Benefits: single entry point, consistent mode→workflow mapping, and routing policy in one place (auth, rate limit, and mode routing in the gateway).

**Frontend:** Set `NEXT_PUBLIC_USE_GATEWAY=true` to send chat requests to `/api/gateway/chat` with `routing_hints`; the gateway will derive `workflow` and `context.model_tier` and forward to `/api/chat`. If unset, the frontend continues to call `/api/chat` directly with `workflow` and `context.model_tier` in the body.

---

---

## 5. Intent routing is not here

The frontend mode switch (Simple/Standard/Detailed) controls **model tier** and **workflow selection**. It does **not** control **intent** (`coaching_mode`). Intent (`emotional_support`, `practical_education`, `policy_navigation`, `mixed`) is determined inside the N8N workflow based on message content and personality state.

See [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) for the canonical routing separation.

---

## References

- **Routing design:** [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) (who owns what)
- **Model-tier design:** [MODEL-TIER-ROUTER-DESIGN.md](MODEL-TIER-ROUTER-DESIGN.md)
- **Gateway:** [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md)
- **Workflows:** `CareLoop/workflows/n8n/`
