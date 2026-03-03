# Technical Specification
## Adaptive Personality-Aware Caregiver Assistant (v2.7.6)

## 1. Purpose and Scope

This specification defines the production-oriented technical design for a Swiss caregiver assistant with:
- personality-aware dialogue (OCEAN + EMA smoothing),
- Retrieval-Augmented Generation (RAG),
- policy navigation for Swiss caregiver support workflows.

This document is implementation-focused and aligned with the requirements in `pmt/Preliminary-Study-V2.7.6.md`.

## 2. System Goals

- Provide emotionally adaptive responses based on continuous OCEAN inference.
- Deliver grounded Swiss policy guidance with citations.
- Separate factual policy retrieval from personality-dependent presentation style.
- Ensure auditable, privacy-aware operation with reproducible logs and deterministic contracts.

## 3. High-Level Architecture

Core flow:
1. `User Input`
2. `Detection` (OCEAN + confidence)
3. `EMA State Update` (per trait)
4. `Regulation` (behavioral directives + mode)
5. `Generation`
6. `Verification`
7. `Persistence + Audit`
8. `Client Response`

Runtime components:
- `Frontend` (Next.js): chat UI, personality dashboard, policy response display.
- `Orchestrator` (N8N): workflow graph and service integration.
- `Policy/RAG services` (HTTP/Code nodes): retrieval, rerank, citation packaging.
- `Database` (PostgreSQL): sessions, turns, personality states, policy evidence, metrics.
- `Cache` (Redis, optional): session context and hot policy chunks.

## 4. Functional Requirements

### 4.1 Dialogue and Personality
- Infer O/C/E/A/N values continuously in range `[-1.0, +1.0]`.
- Infer per-trait confidence in `[0.0, 1.0]`.
- Apply EMA with default `alpha=0.3`.
- Block low-confidence updates with threshold `0.4`.
- Mark profile stable after sufficient consistent turns (target 6+ turns, variance threshold configurable).

### 4.2 RAG and Policy Navigation
- Detect policy-intent queries (benefits, eligibility, procedures, forms, canton-specific support).
- Retrieve top-k relevant policy chunks from trusted corpus.
- Return response with explicit citations and source metadata.
- Enforce no policy claim without source evidence.
- If retrieval fails, return safe fallback and ask clarifying question.

### 4.3 Personality-Styled Policy Delivery
- Policy facts are retrieval-grounded and invariant.
- Presentation style is adapted:
  - High C: structured checklist and ordered steps.
  - Low C: concise summary with optional details.
  - High N: reassuring framing and emotional containment.
  - High O: include alternatives and optional paths.
  - High A: collaborative phrasing.

## 5. Non-Functional Requirements

- Availability target: degrade gracefully if upstream modules fail.
- Contract validity: JSON response schema compliance >= 99.5%.
- Latency targets (p95):
  - General dialogue: <= 6s
  - Policy mode with retrieval: <= 9s
- Security:
  - Secrets only in env vars.
  - Pseudonymized IDs in logs.
  - No raw sensitive personal content in analytics exports.

## 6. Data Contracts

### 6.1 Inbound Request

```json
{
  "session_id": "uuid",
  "turn_index": 1,
  "message": "user text",
  "context": {
    "language": "en",
    "canton": "ZH"
  }
}
```

### 6.2 Detection Output

```json
{
  "ocean": {"O": 0.12, "C": 0.34, "E": -0.05, "A": 0.41, "N": 0.57},
  "confidence": {"O": 0.80, "C": 0.74, "E": 0.62, "A": 0.85, "N": 0.88},
  "reasoning": "short summary"
}
```

### 6.3 RAG Retrieval Output

```json
{
  "mode": "policy_navigation",
  "query_rewrite": "canonical retrieval query",
  "top_k": 3,
  "evidence": [
    {
      "source_id": "iv_guideline_2025_01",
      "title": "IV eligibility criteria",
      "url": "https://...",
      "chunk_id": "iv_13",
      "excerpt": "..."
    }
  ]
}
```

### 6.4 Final Response Output

```json
{
  "session_id": "uuid",
  "message": {
    "role": "assistant",
    "content": "final response",
    "timestamp": "ISO-8601"
  },
  "personality_state": {
    "ocean": {"O": 0.12, "C": 0.34, "E": -0.05, "A": 0.41, "N": 0.57},
    "confidence": {"O": 0.80, "C": 0.74, "E": 0.62, "A": 0.85, "N": 0.88},
    "stable": true,
    "ema_applied": true
  },
  "policy_navigation": {
    "active": true,
    "citations": [
      {
        "source_id": "iv_guideline_2025_01",
        "title": "IV eligibility criteria",
        "url": "https://..."
      }
    ]
  },
  "pipeline_status": {
    "detector": "ok",
    "regulator": "ok",
    "generator": "ok",
    "verifier": "ok",
    "retrieval": "ok"
  }
}
```

## 7. RAG Design

### 7.1 Corpus and Source Governance
- Source classes:
  - federal policy pages,
  - cantonal authority pages,
  - approved guidance documents.
- Each source record stores: `source_id`, `title`, `jurisdiction`, `publish_date`, `url`, `version_hash`.
- Chunking strategy:
  - semantic chunking with overlap (200-400 tokens per chunk, 15-20% overlap),
  - preserve section headers for legal/procedural context.

### 7.2 Retrieval Pipeline
1. Intent classifier (`policy_navigation` vs `general_support`).
2. Query normalization and expansion.
3. Hybrid retrieval:
   - vector similarity,
   - lexical keyword fallback for legal phrases.
4. Optional rerank by:
   - jurisdiction match (federal/canton),
   - recency,
   - source authority score.
5. Evidence packaging with citation metadata.

### 7.3 Grounding Rules
- Every policy claim in output must map to at least one evidence chunk.
- If evidence confidence below threshold:
  - do not assert eligibility as fact,
  - provide conditional guidance and official contact direction.
- Hard fail conditions:
  - fabricated references,
  - missing citation for policy claims.

## 8. Policy Navigation Specification

### 8.1 Supported Domain Packs (Phase Scope)
- Domain pack A: `IV / Invalidenversicherung`
- Domain pack B: `Hilflosenentschaedigung`

Each pack includes:
- FAQ benchmark set (20-30 Q/A),
- eligibility logic notes,
- required documents checklist,
- process steps,
- office/contact routing hints.

### 8.2 Navigation Modes
- `Explain`: summarize entitlement concept.
- `Eligibility`: evaluate likely fit with disclaimers.
- `Procedure`: provide step-by-step submission path.
- `Document Prep`: list required evidence and forms.
- `Escalation`: direct to official channels for edge cases.

### 8.3 Personality-Aware Rendering Layer
- Apply style transform after facts are fixed.
- Input: `{facts, citations, ocean, confidence}`
- Output: user-facing response with adapted tone/structure.
- Prohibited: modifying policy facts due to personality style.

## 9. Database Schema (Minimum)

- `chat_sessions(session_id, created_at, status, locale, canton)`
- `conversation_turns(session_id, turn_index, user_msg, assistant_msg, mode, latency_ms, created_at)`
- `personality_states(session_id, turn_index, ocean_json, confidence_json, stable, ema_alpha, created_at)`
- `policy_evidence(session_id, turn_index, source_id, chunk_id, title, url, excerpt_hash)`
- `performance_metrics(session_id, turn_index, stage, status, duration_ms, error_code, created_at)`

Indexes:
- `conversation_turns(session_id, turn_index)`
- `personality_states(session_id, turn_index)`
- `policy_evidence(source_id, chunk_id)`

## 10. Workflow Nodes (N8N Logical)

1. Webhook Trigger
2. Input Normalize
3. Load Previous Personality State
4. Detection Call
5. EMA Update
6. Coaching Mode + Policy Intent Classification
7. RAG Retrieval (if policy intent)
8. Regulation
9. Generation
10. Verification (grounding + format)
11. Save Turn + State + Evidence
12. Return Response

## 11. Observability and Audit

- JSONL per turn with:
  - input hash,
  - detected traits/confidence,
  - retrieval ids,
  - citation list,
  - verifier decision,
  - final status.
- Correlation IDs across frontend, orchestrator, and DB writes.
- Redaction rules for personal names and contact details before long-term storage.

## 12. Failure Handling

- Detector failure: keep prior stable traits and move to neutral style.
- RAG failure: provide non-policy emotional support, request clarification, set `retrieval=degraded`.
- Verifier failure: safe fallback response with minimal claims.
- Upstream timeout: return controlled fallback JSON, never plain text error.

## 13. Testing Strategy

- Unit:
  - EMA update logic,
  - confidence gating,
  - style renderer invariance on factual claims.
- Integration:
  - full detect->RAG->generate->verify pipeline.
- Evaluation:
  - benchmark policy Q/A packs,
  - citation coverage checks,
  - hallucination audit.
- Regression:
  - golden conversations for high-N, high-C, mixed profiles.

## 14. Acceptance Criteria

- OCEAN contract valid for >= 99.5% turns.
- Policy responses contain citations for 100% policy claims.
- No critical hallucination in audit set.
- RAG domain packs answer benchmark Q/A with target correctness threshold defined by evaluator protocol.
- Frontend shows non-empty OCEAN feedback whenever detection path is active (native or recovery detector path).

## 15. Implementation Notes

- Keep provider abstraction for model endpoints (`NVIDIA`, `OpenAI-compatible`).
- Expose feature flags:
  - `ENABLE_RAG_POLICY_NAV`,
  - `ENABLE_PERSONALITY_STYLING`,
  - `ENABLE_RECOVERY_DETECTOR`.
- Version policy packs separately from workflow code.

## 16. Deliverables in This Spec Package

- This document (`Technical-Specification-RAG-Policy-Navigation.md`)
- New directory location:
  - `pmt/technical-specification-v2.7.6/`

