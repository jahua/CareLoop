# N8N Workflow Error Envelope (Phase 3 P0-2)

When the CareLoop N8N workflow needs to return a **structured error** (e.g. detector failure, RAG failure, verifier failure) instead of a normal success response, it should return the following JSON so the Chat API can map it to an `ErrorResponseEnvelope` and return 503 with a consistent shape.

## Required response shape

Return this as the **webhook response** (HTTP 200 with body):

```json
{
  "success": false,
  "error": {
    "error_code": "detector_fallback",
    "message": "Personality detection failed; using neutral style.",
    "stage": "detection",
    "retryable": true
  },
  "request_id": "{{ pass-through from request }}",
  "session_id": "{{ pass-through from request }}",
  "fallback_content": "I'm here to help. How can I support you today?"
}
```

- **success**: must be `false`.
- **error.error_code**: one of the canonical codes (see below).
- **error.message**: short, user-safe description.
- **error.stage** (optional): `detection` | `retrieval` | `generation` | `verification` | `unknown`.
- **error.retryable** (optional): `true` if the client may retry.
- **request_id**, **session_id**: pass through from the incoming request for correlation.
- **fallback_content** (optional): safe text to show in the UI when in fallback mode.

## Canonical error codes

Use these in `error.error_code` so the API and frontend behave consistently:

| Code | Typical use |
|------|-------------|
| `detector_fallback` | Personality detection API failed; using heuristic/prior state. |
| `rag_fallback` | RAG retrieval failed or returned no evidence; clarification prompt. |
| `verifier_fallback` | Verifier rejected or could not validate; minimal safe response. |
| `timeout_fallback` | Upstream (e.g. LLM) timed out. |
| `ema_divergence` | EMA state diverged; reverted to last stable state. |
| `mixed_mode_overflow` | Token limit in mixed mode; compressed support segment. |
| `language_fallback` | Language detection failed; responding in best-effort language. |
| `validation_failed` | Input validation failed. |
| `internal_error` | Unclassified internal failure. |

Full list and schema: `packages/contracts` → `errors.ts` (`ERROR_CODES`, `StructuredErrorSchema`).

## How to add an error branch in N8N

1. In the workflow, add a path that runs when a node fails or when you detect a fallback condition (e.g. detector API error, empty RAG result you want to treat as error).
2. Add a **Code** node (or **Set** node) that builds the object above. Use `$json` from the previous node to get `request_id`, `session_id`, and any incoming fields.
3. Connect this node to the **Respond to Webhook** (or the node that sends the HTTP response) and return this object as the response body.
4. The Chat API (`/api/chat`) will see `success: false` and `error`, and will return HTTP 503 with the same envelope shape (and will not log raw stack traces to the client).

## Stage timings (optional, P1-10)

To feed **performance_metrics** for per-stage latency, include a **stage_timings** array in the **success** response (same payload as the normal reply). Each item: `{ stage: string, status: string, duration_ms?: number, error_code?: string }`. Example: `stage_timings: [ { stage: "retrieval", status: "ok", duration_ms: 420 }, { stage: "verification", status: "ok", duration_ms: 180 } ]`. The Chat API writes these to `performance_metrics(session_id, turn_index, stage, status, duration_ms, error_code)` when present (fire-and-forget). The turn must already exist (workflow persists it before responding). See `docs/SLO-AND-MONITORING.md`.

## Reference

- Technical Specification §12 (failure paths)
- `packages/contracts/src/errors.ts` – `ErrorResponseEnvelopeSchema`, `ERROR_CODES`
- `apps/web/src/app/api/chat/route.ts` – normalization of N8N 200 + error body; `writeStageTimingsToDb` when `stage_timings` present
