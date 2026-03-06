# Gateway Shadow Mode (P2)

Design for the CareLoop gateway in **shadow mode** and the path to canary/GA. Aligned with Technical Specification §15.1.A, §15.1.G.

---

## 1. Gateway role (Spec §15.1.A)

The gateway centralizes:

- **Session lifecycle** and **request correlation IDs** (`request_id`, `session_id`)
- **AuthN/authZ** and **rate limits** (when enabled)
- **Model-tier selection** and **workflow routing** (`light`→simple, `medium`/`heavy`→full pipeline)
- **Retry/backoff** and **timeout budgets**
- **Tool invocation policy** (allowed actions by mode)

> **Note:** The gateway owns **model tier** and **workflow selection**. It does **not** own **intent / pillar mode** (`coaching_mode`) — that is determined by the N8N workflow based on message content and personality state. See [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) for the full separation.

---

## 2. Minimum request envelope

Incoming requests to the gateway use this shape:

```json
{
  "request_id": "uuid",
  "session_id": "uuid",
  "user_id": "pseudonymous-id",
  "message": "text",
  "context": { "canton": "ZH", "language": "en" },
  "routing_hints": { "force_policy_mode": false }
}
```

- **request_id:** Optional; gateway generates if missing.
- **session_id:** Required for turn continuity.
- **user_id:** Optional pseudonymous user ID (for future authZ/rate limits).
- **message:** User message text.
- **context:** Optional; `language`, `canton`, etc.
- **routing_hints:** Optional; `force_policy_mode`, `model_tier` (`light`|`medium`|`heavy`), `workflow` (`simple`). The gateway **derives** the backend request: sets `context.model_tier` from `routing_hints.model_tier` (default `medium`), and sets `workflow: "simple"` when `routing_hints.workflow === "simple"` or `model_tier === "light"`, so the chat API routes to the simple N8N webhook. **Handling modes in the gateway** keeps routing policy in one place and avoids clients sending inconsistent combinations.

The gateway forwards a **backend envelope** to `/api/chat`: `session_id`, `turn_index`, `message`, `context` (including `model_tier`), `request_id`, and optionally `workflow: "simple"`.

---

## 3. Shadow mode

- **Goal:** Run the gateway in **observe-only**: log request/response for validation, no traffic *required* to go through it.
- **Implementation:**
  - **Option A:** Frontend (or proxy) sends a **copy** of each request to the gateway; gateway logs envelope + response and returns 202. Main traffic still goes to `/api/chat`.
  - **Option B:** Frontend sends **all** traffic to the gateway; gateway logs envelope, then forwards to `/api/chat` (or in-process pipeline) and returns the pipeline response. This is “shadow” in the sense that gateway does not yet do auth/rate-limit/route; it only logs and forwards.

Current stub implements **Option B**: `POST /api/gateway/chat` accepts the gateway envelope, optionally logs it when `GATEWAY_SHADOW_LOG` is set, then forwards to the same pipeline as `/api/chat` and returns its response.

**Optional auth:** When `GATEWAY_API_KEY` is set in the environment, the gateway requires `x-api-key` or `Authorization: Bearer <key>` on each request; otherwise it returns 401. When not set, no auth is required (suitable for shadow/canary behind a trusted proxy).

**Optional rate limit:** When `GATEWAY_RATE_LIMIT_PER_MINUTE` is set and > 0, the gateway allows at most that many requests per minute per key. Key = `user_id` from the envelope if present, else client IP (from `x-forwarded-for` or `x-real-ip`). Over-limit requests receive 429 with `Retry-After: 60` and a JSON body. Successful responses include `X-RateLimit-Remaining` when the limit is enabled. Limiter is in-memory (single-instance); for multi-instance use a shared store (e.g. Redis) later.

---

## 4. Rollout (Spec §15.1.G)

1. **Shadow:** Gateway deployed; request/response (or envelope) logged; traffic can go through gateway (Option B) or only a copy (Option A).
2. **Canary:** Route a small fraction of traffic (e.g. 10%) through the gateway; compare error rate and latency to baseline.
3. **GA:** Full traffic through gateway; auth/rate-limit and model-tier routing enabled as needed.

**Success gate for full rollout:**

- No critical hallucination increase.
- Stable or improved policy benchmark scores.
- Same or better user-rated quality; optionally reduced average inference cost.

---

## 5. Next steps (after shadow)

- **Auth:** Require valid token or API key for `/api/gateway/chat` when enabled.
- **Rate limits:** Per `user_id` or IP; return 429 when exceeded.
- **Model-tier router:** Use `routing_hints` and intent to select `light` | `medium` | `heavy`; pass tier to pipeline (e.g. N8N) for model/param choice.
- **Dual router:** Intent router (pillar mode) + model-tier router (Spec §15.1.B).

---

## 6. Canary checklist (before routing traffic through gateway)

- [ ] Shadow log (`GATEWAY_SHADOW_LOG`) reviewed; envelope and response shape correct.
- [ ] Baseline metrics captured (error rate, p95 latency) for traffic to `/api/chat` without gateway.
- [ ] Route a small share of traffic (e.g. 10%) to `/api/gateway/chat`; compare error rate and latency to baseline.
- [ ] No increase in 5xx or error-envelope rate; latency within SLO (e.g. turn p95 ≤ 2s at API).
- [ ] Policy benchmark and citation coverage unchanged (or improved).
- [ ] Then increase gateway share (e.g. 50%, then 100%) and repeat checks; document success gate per §4.

### Optional automation: gateway canary gate script

Capture baseline first (without gateway path):

- Run `npm run job:gateway-baseline-capture`.
- Record `baseline_env.BASELINE_P95_MS` and `baseline_env.BASELINE_5XX_RATE` from output JSON.

Use `npm run job:gateway-canary-check` to evaluate the checklist with measurable gates from `GATEWAY_SHADOW_LOG`:

- Parses gateway request/response events and checks:
  - sample volume (`MIN_REQUESTS`)
  - envelope validity
  - 5xx rate vs baseline (`BASELINE_5XX_RATE`, `MAX_5XX_ABS_INCREASE`)
  - p95 latency vs baseline (`BASELINE_P95_MS`, `MAX_P95_INCREASE_MS`)
  - 429 rate threshold (`MAX_429_RATE`)
  - error-envelope rate threshold (`MAX_ERROR_ENVELOPE_RATE`)
- Optional policy citation-coverage guard when baseline/canary audit logs are provided:
  - `BASELINE_AUDIT_LOG_PATH`, `CANARY_AUDIT_LOG_PATH`, `MAX_POLICY_CITATION_DROP`
- Exits `0` on pass, `1` on fail (CI/cron friendly).

---

## 7. References

- Spec §15.1.A (Gateway control plane), §15.1.G (Rollout plan)
- [PHASE3-TODO.md](PHASE3-TODO.md) P2-6, P2-7
- [OPERATIONS-RUNBOOK.md](OPERATIONS-RUNBOOK.md) §7
