# CareLoop Frontend Improvements TODO

**Version:** 1.0  
**Last Updated:** 2026-03-06  
**References:** `pmt/MVP/frontend`, `pmt/MVP/nextchat-personality-enhanced`, [ROADMAP.md](../ROADMAP.md), [Technical-Specification-RAG-Policy-Navigation.md](../Technical-Specification-RAG-Policy-Navigation.md) §15.2

This document lists frontend improvements for **display**, **KPI/metrics**, **logs**, **user history**, and **visual design**, aligned with the roadmap (Phase 3 observability, Phase 4 pilot) and patterns from the MVP/NextChat-enhanced frontends.

---

## 1. Frontend display

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 1.1 | **Chat UI upgrade** | High | Replace inline styles with a design system (Tailwind or tokens). Adopt layout/patterns from `pmt/MVP/frontend` (EnhancedChatInterface, message bubbles, typing indicator) or NextChat-enhanced. |
| 1.2 | **Message list UX** | High | Done: auto-scroll to bottom on new messages/loading; timestamps and "Answered in X.Xs" (frontend-measured latency); turn_index/request_id in meta. |
| 1.3 | **Personality state panel** | High | Add OCEAN visualization (bars/charts) and “Stable / Learning” badge like `PersonalityDashboard.tsx` and `EnhancedPersonalityDashboard` in pmt/MVP/frontend. |
| 1.4 | **Coaching mode display** | Medium | Done: SessionBar shows coaching mode badge when present. |
| 1.5 | **Citations display** | Medium | When response includes policy citations, render them as expandable refs or footnotes (Spec §6.3, §8). |
| 1.6 | **Error and degraded states** | High | Use structured error envelope (Phase 3); show user-friendly message + optional “Retry” and avoid raw stack traces. |
| 1.7 | **System health banner** | Medium | Show API/N8N/DB status when degraded (pattern from pmt/MVP/frontend header system health). |

---

## 2. KPI and metrics (frontend-facing)

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 2.1 | **Session KPI strip** | High | Done: SessionBar shows message count, coaching mode, personality stable/learning, session ID. |
| 2.2 | **Per-turn metrics (optional)** | Medium | If backend returns `stage_timings` or `turn_latency_ms`, show per-message: e.g. “Answered in 2.3s” or stage breakdown (detection, retrieval, generation, verification). See `performance-metrics.ts` and SLO-AND-MONITORING.md. |
| 2.3 | **Feedback summary** | Low | After thumbs up/down, optionally show “Thanks for feedback” and aggregate (e.g. “3 helpful” this session) if backend exposes it. |
| 2.4 | **OCEAN confidence** | Medium | Done: PersonalityPanel shows confidence % per trait when personality_state.confidence_scores is returned. |

---

## 3. Logs and observability (UI for operators/debug)

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 3.1 | **Request/session correlation** | Medium | Show `request_id` and `session_id` in UI (e.g. footer or “Copy session ID” for support). Already in audit; expose in UI. |
| 3.2 | **Dev/debug panel (optional)** | Low | Optional collapsible panel: last request_id, last turn_index, correlation ID for pasting into log search. Only in dev or behind feature flag. |
| 3.3 | **Gateway shadow indicator** | Low | When using gateway and shadow logging, optional badge “Gateway (shadow)” so testers know traffic is logged. |

---

## 4. User history

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 4.1 | **Restore session on load** | High | ✅ Done: when `?session_id=<uuid>` is in URL, app uses that session and calls GET /api/data/export to restore messages + personality. See `apps/web/src/app/page.tsx` and `lib/api.ts` `fetchSessionHistory`. |
| 4.2 | **Session list (optional)** | Medium | List recent sessions (e.g. from localStorage or from backend if endpoint exists) and “Continue session” to load a session. |
| 4.3 | **Export/delete from UI** | Medium | ✅ Done: DataActions component with “Export my data” (downloads JSON) and “Delete my data” (confirm + POST /api/data/delete, then new session). See `components/DataActions.tsx`. |

---

## 5. Visual design and UX

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 5.1 | **Design system** | High | Done: CSS variables (colors, spacing, typography) in globals.css; reused across components. |
| 5.2 | **Responsive layout** | High | ✅ Done: two-column grid on desktop (chat \| personality + data actions sidebar); single column on mobile. See `globals.css` `.careloop-main` and `@media (min-width: 768px)`. |
| 5.3 | **Accessibility (WCAG 2.1 AA)** | High | Thumbs and main actions have aria-label; HealthBanner has role=alert and aria-live. |
| 5.4 | **Loading and empty states** | Medium | Skeleton or spinner for “Thinking…”; empty state copy for “No messages yet” and “No history” (friendly, actionable). |
| 5.5 | **Chat mode selector** | Medium | Done: Simple / Standard / Detailed as styled tabs in SessionBar area. |
| 5.6 | **Animations** | Low | Subtle transitions (e.g. Framer Motion) for message append and panel switch; avoid motion for users who prefer reduced motion. |

---

## 6. Structure and code (apps/web)

| # | Task | Priority | Notes / Reference |
|---|-----|----------|-------------------|
| 6.1 | **Component split** | High | ✅ Done: ChatMessage, ChatInput, ErrorBanner, PersonalityPanel, SessionBar, DataActions, HealthBanner; page.tsx composes them. |
| 6.2 | **State management** | Medium | In-page useState for session, messages, personality, etc.; can move to Zustand later if needed. |
| 6.3 | **API client** | Medium | ✅ Done: `lib/api.ts` for fetchSessionHistory, exportSessionData, deleteSessionData; health checked in page. |

---

## 7. References

- **ROADMAP:** Phase 3 (§6 Observability), Phase 4 (§7 Pilot, §7.2 Accessibility).
- **Spec:** §15.2 (Frontend stack), §17.6 (Operational standards), §6 (Contracts for response/citations).
- **MVP frontend:** `pmt/MVP/frontend` — ChatInterface, EnhancedChatInterface, PersonalityDashboard, MultiAgentDashboard, usePersonalityStore.
- **NextChat-enhanced:** `pmt/MVP/nextchat-personality-enhanced` — NextChat-style layout, personality dashboard, multi-agent dashboard, health check.
- **CareLoop APIs:** `/api/health`, `/api/chat`, `/api/gateway/chat`, `/api/feedback`, `/api/data/export`, `/api/data/delete`; audit and performance_metrics (backend).
- **Docs:** SLO-AND-MONITORING.md, DATA-EXPORT-AND-DELETION.md, OPERATIONS-RUNBOOK.md.

---

## Quick priority summary

- **High:** Chat UI upgrade, personality panel, error states, session KPI strip, restore session on load, design system, responsive layout, accessibility, component split.
- **Medium:** Coaching mode display, citations, system health banner, per-turn metrics, OCEAN confidence, correlation IDs in UI, session list, export/delete UI, loading/empty states, chat mode selector, state management, API client.
- **Low:** Feedback summary, dev/debug panel, gateway shadow indicator, animations.

Use this list to plan sprints or to pick items for the next frontend iteration alongside ROADMAP Phase 3/4.
