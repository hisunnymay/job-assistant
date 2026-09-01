# Goal 10 — Aggregate Data Dashboard and Test-session Exclusion

## Completed Scope

- Added the `TrackingSession` entity, additive backfill/foreign-key migration, one-way test designation, ingestion-time session creation, and retention behavior that preserves test-session classification for queued late delivery.
- Added the public aggregate-only dashboard API with all-retained and inclusive `Asia/Shanghai` date modes, six total-event metrics, distinct-session contact conversion, atomic single-query snapshots, nullable no-data fields, and safe errors.
- Added the fourth persistent dashboard view, date filtering and recovery states, accessible responsive metric cards, three-click acknowledgement-gated test-mode entry, tab-scoped visible state, and explicit exit to a new normal session.
- Preserved existing tracking event payloads and fingerprints, Conversation/Feedback behavior, AI Service boundaries, fixed résumé resources, and recruiter workflow contracts.

## Validation

- Backend: `188 passed, 1 skipped`; MyPy passed for 70 source files; Ruff passed.
- Frontend: 10 Vitest files and 64 tests passed; TypeScript, ESLint, and production build passed (190 modules).
- Playwright: 8 desktop/compact Mock journeys passed, including retroactive and queued-event exclusion, date filtering, conversation restoration, error recovery, and compact accessibility.
- Migration coverage verified backfill of distinct existing session IDs while preserving event identity, fingerprint, Conversation association, and accepted row counts.
- Manual browser checks covered acknowledged test label, refresh/navigation persistence, explicit exit, dashboard navigation and states, conversation restoration, desktop composition, compact overflow, accessible names/status, and console cleanliness.
- `git diff --check` and final changed-file review passed. No paid provider call, external deployment, production migration, push, merge, or commit occurred.

## Independent Review and Fixes

The read-only security review found two medium and one low issue. All were fixed and regression-tested: dashboard values now share one SQL statement snapshot, retained test-session tombstones prevent late events from re-entering metrics, and unsupported minimum/maximum date boundaries return the safe 400 contract. Focused verification passed 23 tests, and the reviewer reported no remaining high-severity or unresolved security, privacy, or data-integrity finding.

## Specification Conformance

- PRD v0.9 F008/S001: the dashboard reports only approved aggregate metrics; supporting cards are event totals, conversion uses distinct sessions, dates are inclusive in Asia/Shanghai, and whole designated sessions are excluded before and after activation.
- Frontend Technical Design v1.1: the dashboard is the fourth mutually exclusive workspace view without clearing the conversation; loading, no-data, invalid, retry, reset, persistent test label, explicit exit, keyboard, screen-reader, desktop, and compact requirements are covered.
- Backend Technical Design v1.2: classification and aggregation remain backend-owned behind Controller → Service → Repository boundaries; public fixtures and safe errors are preserved; migration is additive and privacy-safe.
- Goal 10 prohibitions: no trend comparison, chart, drill-down, export, real-time refresh, authentication/fingerprinting, AI behavior change, raw identifiers, event rows, user content, candidate content, or person identity were added.

## Remaining Limitations and Operational Boundaries

- The hidden three-click gesture is intentionally not authentication; the aggregate dashboard remains public when separately deployed.
- The 90-day cleanup remains an operator-run maintenance command. Non-test empty sessions may be removed, while test-session classification tombstones are retained for correctness.
- Production migration and deployment require separate approval and have not been performed; the current production application is unchanged.
- Vitest emits the existing Node `--localstorage-file` warning, but all tests pass.
