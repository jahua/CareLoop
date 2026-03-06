# Routing, Intent, and Mode Design

Canonical reference for **where** each routing decision lives in the CareLoop stack and **why**. Aligned with Technical Specification §8.4.F (Router Decision Policy), §15.1.A (Gateway), §15.1.B (Dual Router).

---

## 1. Decision layers (clean separation)

```
Frontend (user preference)
    ↓  routing_hints: { model_tier, workflow? }
Gateway (infra + routing policy)
    → auth, rate limit
    → model_tier default / validation → context.model_tier
    → workflow selection (simple vs full) from model_tier or routing_hints.workflow
    ↓  { session_id, message, context.model_tier, workflow? }
Chat API (proxy / fallback)
    → picks N8N webhook path from workflow
    → fallback coaching_mode (only when workflow does not return one)
    ↓  full body forwarded to N8N
N8N Workflow (content + intent — authoritative)
    → ingest → load state → detect → EMA
    → intent router (coaching_mode) from message + context + personality
    → pillar-specific branch (RAG for policy, coaching for emotional/education)
    → generate → verify → respond
```

### Which layer owns which decision

| Decision | Owner | Rationale |
|----------|-------|-----------|
| **Intent / pillar mode** (`coaching_mode`) | N8N workflow | Depends on message content, session history, personality state, and EMA — all available inside the workflow after step 5 (§8.4.G). |
| **Model tier** (`light`/`medium`/`heavy`) | Gateway | Cost/infra decision based on user preference; the workflow may escalate (e.g. force `heavy` for ambiguous policy) but the gateway sets the default. |
| **Workflow selection** (`simple` vs `full`) | Gateway | Deployment/routing decision; derived from `model_tier` or explicit `routing_hints.workflow`. |
| **User preference** (Simple/Standard/Detailed) | Frontend | UI sends `routing_hints`; does **not** set `coaching_mode` or `workflow` directly. |
| **Fallback coaching_mode** | Chat API | Only when the N8N response has no `coaching_mode`; keyword-based heuristic as a safety net. |

---

## 2. Intent router (N8N workflow — authoritative)

### Current implementation

The "Enhanced Regulation" node in the workflow now applies a normalized keyword scorer with decision-table style routing:

- Normalized `policy`/`education`/`emotional` scores (`0..1`) plus raw scores.
- Threshold routing aligned with Spec §8.4.F (`0.55` and mixed `0.45` policy+emotional).
- Tie-break rules:
  - Policy + education tie with legal/benefit cues → `policy_navigation`
  - Emotional + education tie with explicit next-step wording → `practical_education`
  - Three-way low-confidence tie → `emotional_support` + clarification
- Emits routing metadata: `mode_scores`, `mode_scores_raw`, `mode_confidence`, `mode_routing_reason`, `needs_clarifying_question`, `clarifying_question`.

### Target (Spec §8.4.F)

The Spec defines a decision table with score thresholds:

| Condition | Selected mode | Notes |
|-----------|---------------|-------|
| policy score ≥ 0.55 | `policy_navigation` | Force citation-required path |
| education score ≥ 0.55 and policy < 0.55 | `practical_education` | Structured coaching output |
| emotional score ≥ 0.55 and policy < 0.55 | `emotional_support` | No policy assertions without retrieval |
| policy ≥ 0.45 and emotional ≥ 0.45 | `mixed` | Two-segment response |
| all scores < 0.55 | `emotional_support` | + ask one clarifying question |

Tie-break rules:
- Policy + education tie → `policy_navigation` if legal/benefit keywords present.
- Emotional + education tie → `practical_education` if user asks for explicit next steps.
- All three tie at low confidence → `emotional_support` + clarification.

### Improvement path

1. **Short-term (done):** Normalize keyword scores to 0–1 range and apply threshold/tie-break routing with low-confidence clarification metadata in the workflow Regulation node.
2. **Medium-term:** Add an LLM-based intent classification prompt (short, before generation) for higher accuracy; use keyword score as fallback.
3. **Long-term:** Use intent confidence to drive tier escalation (low intent confidence on policy → force `heavy`).

---

## 3. Model-tier router (Gateway — default; workflow — escalate)

See [MODEL-TIER-ROUTER-DESIGN.md](MODEL-TIER-ROUTER-DESIGN.md) for full tier definitions.

**Flow:**

1. **Gateway** reads `routing_hints.model_tier` (from frontend), validates (`light`/`medium`/`heavy`), defaults to `medium`. Sets `context.model_tier`.
2. **Workflow** receives `context.model_tier`. For now, logs it. Later, can:
   - Adjust `max_tokens`, temperature, or number of retrieval chunks.
   - Escalate: if intent is `policy_navigation` or `mixed` and tier was `light`, escalate to `medium` (safety rule).
3. **Safety invariant:** Tier never skips retrieval or verification for policy-relevant turns (Spec §15.1.B).

**Router precedence (Spec §15.1.B):**
1. Intent router selects pillar mode.
2. Model-tier router selects compute tier for the selected mode.
3. Safety policies can escalate tier but cannot skip mandatory grounding/verification.

---

## 4. Workflow selection (Gateway)

| Condition | Webhook | Workflow file |
|-----------|---------|---------------|
| `routing_hints.workflow === "simple"` or `model_tier === "light"` | `careloop-turn-simple` | `careloop-turn-simple.json` |
| Otherwise | `careloop-turn` | `careloop-phase1-2-postgres-mvp.json` |

Gateway sets `workflow: "simple"` on the body forwarded to `/api/chat`; the chat API picks the webhook path accordingly.

See [TWO-WORKFLOWS-AND-MODE-SWITCH.md](TWO-WORKFLOWS-AND-MODE-SWITCH.md) for import instructions and frontend usage.

---

## 5. API fallback coaching_mode

`apps/web/src/app/api/chat/route.ts` has `inferCoachingMode()` — a keyword scorer that mirrors the workflow's logic. This is a **pure fallback**: it only applies when the N8N response does not include a `coaching_mode` (e.g. when the workflow is the simple stub or the pipeline fails).

**Do not** treat this as the primary intent router. The workflow is authoritative.

---

## 6. What the frontend should (not) do

- **Should:** Show mode preference buttons (Simple / Standard / Detailed) and send `routing_hints: { model_tier, workflow? }`.
- **Should not:** Set `coaching_mode` — it doesn't have session context, personality state, or EMA history.
- **Should not:** Hardcode `workflow` when going through the gateway — the gateway derives it from `model_tier`.
- **Should:** Display `coaching_mode` from the response (returned by the workflow).

---

## References

- **Spec:** §8.4.F (Router Decision Policy), §8.4.G (N8N Branch Mapping), §15.1.A (Gateway), §15.1.B (Dual Router)
- **Model-tier:** [MODEL-TIER-ROUTER-DESIGN.md](MODEL-TIER-ROUTER-DESIGN.md)
- **Workflows:** [TWO-WORKFLOWS-AND-MODE-SWITCH.md](TWO-WORKFLOWS-AND-MODE-SWITCH.md)
- **Gateway:** [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md)
