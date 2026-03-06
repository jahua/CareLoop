# Model-Tier Router (P2-8)

Design for the **model-tier router**: select `light` | `medium` | `heavy` per turn for cost–quality tradeoff without skipping grounding/verification. Aligned with Technical Specification §15.1.B.

---

## 1. Tiers (Spec §15.1.B)

| Tier   | Use case | Typical behaviour |
|--------|----------|--------------------|
| **light**  | Short, non-policy turns; low reasoning depth (e.g. greetings, simple acknowledgements). | Minimal context; single-step generation; retrieval/verification can be skipped only when intent is clearly non-policy. |
| **medium** | Standard coaching + moderate policy complexity. | Normal retrieval and verification; standard context window and model params. |
| **heavy**   | Ambiguous eligibility, procedural edge-cases, verification retries, complex multi-step reasoning. | Longer context; optional retry/refinement; stricter verification. |

**Safety rule:** For any turn that may assert policy (eligibility, amounts, procedures), grounding and verification **must** run. The tier affects *how much* compute/context is used, not *whether* RAG/verification runs.

---

## 2. Selection inputs

Tier can be chosen from:

1. **Gateway envelope**  
   - `routing_hints.model_tier`: optional `"light"` | `"medium"` | `"heavy"` from client or upstream proxy. If present and valid, can be used as the tier (subject to safety override below).

2. **Intent / pillar**  
   - `emotional_support` only, short message → candidate `light`.  
   - `policy_navigation` or `mixed` → at least `medium`; if message suggests ambiguity or multi-step (e.g. “what if I also work part-time?”) → `heavy`.  
   - `practical_education` with “steps” or “plan” → `medium` or `heavy` depending on complexity.

3. **Heuristics (optional)**  
   - Message length, question marks, presence of policy keywords, previous turn errors (e.g. verifier_fallback) can nudge toward `medium` or `heavy`.

4. **Safety override**  
   - If the intent or content is policy-relevant, tier must not be `light` in a way that skips retrieval/verification. Prefer: policy-relevant ⇒ at least `medium`; ambiguous/edge-case ⇒ `heavy`.

---

## 3. Passing tier to the pipeline

- **Gateway → API:** Add optional `model_tier` to the backend envelope (e.g. in the body sent from gateway to `/api/chat`). Gateway computes tier from `routing_hints.model_tier` and/or intent (when intent is available at gateway) and sets `model_tier` on the forwarded payload.
- **API → N8N:** Include `model_tier` in the webhook payload (e.g. `context.model_tier` or top-level `model_tier`). N8N workflow branches on this to choose model params, max tokens, or retry behaviour; it must **not** branch in a way that skips retrieval or verification for policy-relevant turns.
- **Default:** If tier is missing or invalid, use `medium`.

---

## 4. Observability

- Emit the chosen tier in audit (e.g. `pipeline_status.model_tier` or `coaching_mode`-adjacent field) so that cost and behaviour can be analysed per tier.
- Optionally log tier in gateway shadow log when the gateway performs the selection.

---

## 5. Implementation order (suggested)

1. **Contract:** Add `model_tier?: "light" | "medium" | "heavy"` to gateway envelope and to the body passed to `/api/chat` and N8N.
2. **Gateway:** If `routing_hints.model_tier` is set and valid, pass it through; otherwise set default `medium`. Later: add intent-based or heuristic selection.
3. **N8N:** Consume `model_tier`; for now use it only for logging and optional param overrides (e.g. max_tokens). Ensure retrieval and verification still run for policy-relevant turns.
4. **Safety:** Document and enforce in workflow: policy_navigation and policy segment of mixed ⇒ never skip retrieval/verification regardless of tier.

---

---

## 5.1 Current implementation status

- Implemented in `workflows/n8n/careloop-phase1-2-postgres-mvp.json`:
  - Ingest validates `context.model_tier` and defaults to `medium`.
  - Regulation computes `model_tier_requested` and `model_tier_effective`.
  - Safety escalation is active: `light` is escalated to `medium` for `policy_navigation` and `mixed`.
  - Retrieval top-k is tier-aware via `retrieval_top_k` (`light=2`, `medium=3`, `heavy=5`).
  - Generation uses tier-aware parameters (`max_tokens`, `temperature`) and records them in `generator.generation_config`.
- Remaining:
  - Tune thresholds with benchmark/pilot cases.
  - Add stronger heavy-tier triggers for ambiguous procedural/policy edge cases.
  - Optionally emit tier in `pipeline_status` for direct dashboard aggregation.

---

## 6. Relationship to intent routing

Model tier is selected **after** intent (Spec §15.1.B). The intent router lives in the **N8N workflow** (authoritative), not in the gateway or API. The gateway provides a **default tier** from user preference; the workflow may **escalate** it (e.g. policy_navigation + `light` → escalate to `medium`).

See [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) for the full routing separation.

---

## References

- **Spec:** §15.1.B (model-tier router), §15.1 (OpenClaw-inspired)
- **Routing design:** [ROUTING-AND-INTENT-DESIGN.md](ROUTING-AND-INTENT-DESIGN.md) (decision layers, who owns what)
- **Gateway:** [GATEWAY-SHADOW-DESIGN.md](GATEWAY-SHADOW-DESIGN.md) (envelope, routing_hints)
- **TODO:** [PHASE3-TODO.md](PHASE3-TODO.md) P2-8
