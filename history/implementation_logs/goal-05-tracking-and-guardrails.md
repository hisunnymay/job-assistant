# Goal 5 — Product Tracking and Deterministic AI Guardrails

## Version Log

- **v2.1 — 2026-08-27:** Recorded the Goal 5 Bugbot fixes for queue progress, conversion cohorts, deletion-safe replay, schema compatibility, and AI-design gate wording.
- **v2.0 — 2026-08-27:** Recorded the corrected centralized tracking implementation after S001 was clarified, including backend persistence, delivery retry, reporting, retention, validation, and conformance results.
- **v1.0 — 2026-08-27:** Recorded the superseded browser-local tracking implementation and deterministic AI guardrail fixtures.

## Completed Scope

- Added the privacy-safe `UserBehaviorEvent` database entity with stable event ID, allowlisted event name, pseudonymous tracking session, interaction and receipt timestamps, an immutable SHA-256 request fingerprint, and nullable Conversation association using `ON DELETE SET NULL`.
- Added `POST /api/tracking-events` through Controller, Service, and Repository layers. The workflow validates the Conversation association, rejects unexpected content fields, persists accepted events, replays identical event IDs idempotently, rejects conflicting reuse, and returns safe errors.
- Replaced the permanent browser event log with centralized delivery and a 100-event pending queue. The frontend retries transient failures on startup and later tracking actions, removes acknowledged events, discards permanent contract rejections, discards the oldest event on overflow, and keeps failures isolated from the recruiter journey.
- Preserved all six required interaction boundaries: `page_visit`, `job_description_submitted`, `matching_report_generated`, `resume_previewed`, `contact_cta_clicked`, and `feedback_submitted`.
- Added the internal `app.commands.tracking_report` command for total and distinct-session counts plus Contact Conversion Rate, including the zero-denominator case and generated-report cohort enforcement.
- Added the `app.commands.cleanup_tracking_events` maintenance command to delete events older than the 90-day retention boundary.
- Retained the versioned, provider-neutral guardrail fixtures and deterministic Mock adapter covering supported, partial, missing, invented, hiring-recommendation, ranking, prediction, and overall-scoring cases.

## Material Files

- Backend tracking: `backend/app/db/models.py`, `backend/app/controllers/tracking.py`, `backend/app/services/tracking.py`, `backend/app/repositories/tracking.py`, API registration/error handling, and tracking API/reporting tests.
- Internal operations: `backend/app/commands/tracking_report.py` and `backend/app/commands/cleanup_tracking_events.py`.
- Frontend tracking: `frontend/src/types/tracking.ts`, `frontend/src/services/trackingClient.ts`, its unit tests, and the six event boundaries in `frontend/src/App.tsx` and `frontend/src/App.test.tsx`.
- Guardrails: `backend/evals/goal_05_guardrail_cases.json` and `backend/tests/test_ai_guardrail_fixtures.py`.
- Usage documentation: `README.md` and `planning/PLAN.md`.

## Actual Implementation Time

- The reopened centralized-tracking correction took approximately 18 minutes, measured by the Codex Goal timer through implementation, regression coverage, complete validation, command smoke checks, conformance review, and documentation closeout.
- The superseded browser-local checkpoint took approximately 14 minutes and remains recorded for historical accuracy.

## Validation

- `cd backend && uv run pytest` — passed, 66 tests, including API validation, PostgreSQL persistence, deletion-safe idempotent replay, conflict handling, privacy rejection, Conversation deletion, cohort-safe aggregate metrics, zero denominator, 90-day retention, command output, and all deterministic guardrail fixtures.
- `cd backend && uv run mypy app tests` — passed across 49 source files.
- `cd backend && uv run ruff check .` — passed.
- `cd backend && uv run python -m app.commands.tracking_report --help` — passed.
- `cd backend && uv run python -m app.commands.cleanup_tracking_events --help` — passed.
- `cd frontend && npm run test` — passed, 7 test files and 46 tests, including permanent and transient delivery failure handling.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; Vite transformed 186 modules and produced the production bundle.
- `git diff --check` — passed.

## Specification-Conformance Review

- **PRD S001:** Conforms. All six events are centrally persisted and can be aggregated across pseudonymous sessions; Contact Conversion Rate counts only contact sessions inside the generated-report cohort.
- **Frontend Technical Design Section 4.4:** Conforms. The frontend owns interaction detection, transmits only the approved event schema, separates tracking session from Conversation, retries transient failures through the bounded queue, discards permanent contract rejections, and never blocks recruiter-visible behavior.
- **Backend Technical Design User Behavior Event, Section 5, and Section 7.5:** Conforms. The implementation uses the approved endpoint and layered workflow, privacy-safe persistence fields, optional Conversation relationship, fingerprint-backed event-ID idempotency after Conversation deletion, cohort-safe internal aggregate reporting, and 90-day cleanup operation.
- **AI behavior:** Conforms to PRD F003/F005 and Lightweight AI Design Decision Sections 1.2–1.4 through the provider-neutral deterministic fixtures and Mock adapter.
- **Architecture and scope:** No Dashboard, public analytics read API, event-level export, frontend AI reasoning, sensitive tracking content, real provider, eval platform, ranking, score, prediction, or hiring decision was added.
- **Result:** No unresolved material mismatch remains for Goal 5.

## Problems Fixed and Remaining Known Issues

- Corrected the browser-only design that could not support centralized, cross-session S001 evaluation.
- Fixed an empty-startup-flush race that could leave a same-tick event pending until another tracking action or reload.
- Fixed permanent `400`, `404`, and `409` tracking rejections blocking all later queued events.
- Fixed Contact Conversion Rate exceeding 100% when contact-only sessions were counted outside the generated-report cohort.
- Fixed identical event replay returning a conflict after Conversation deletion cleared the relational association; existing local rows are backfilled by the additive database initialization step.
- Corrected the draft AI System Design so it does not claim the real-AI implementation gate is approved or open.
- Tracking remains best-effort: events can be discarded after the pending queue exceeds 100 items during an extended outage, as specified by the frontend design.
- The frontend test runner still emits the environment-level `--localstorage-file` warning; the suite and all other validations pass.
- Real AI integration and provider-level evaluation remain gated by the unfinished AI System Design and are outside Goal 5.
