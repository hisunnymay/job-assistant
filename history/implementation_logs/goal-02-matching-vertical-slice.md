# Goal 2 — Integrated Matching Vertical Slice with Mock AI Service

## Version Log

- **v1.1 — 2026-08-25:** Fixed the post-review invalid-request recovery path so recruiters can edit and resubmit a rejected job description instead of retrying an unchanged payload.
- **v1.0 — 2026-08-25:** Recorded the completed Goal 2 implementation, validation, specification-conformance review, and actual implementation time.

## Completed Scope

- Implemented `POST /api/matching-analysis` with the authoritative `jobDescription` request and `conversationId`, `messageId`, and text/Markdown `content` response.
- Added PostgreSQL Conversation and Conversation Message models plus a lightweight repository boundary.
- Added a transactional matching-analysis Service workflow that stores the submitted job description and generated analysis under one persisted conversation.
- Added a replaceable AI Service protocol and deterministic backend Mock AI Service without a real provider, SDK, prompt payload, or provider response.
- Passed the predefined `mei_chang_resume.pdf` path through the AI Service boundary and added no backend PDF extraction, preprocessing, or text mirror.
- Added safe, consistent invalid-request, Mock-AI failure, persistence failure, and unexpected-error responses.
- Added local CORS configuration for the frontend origin and replaced the production frontend Mock transport with a small HTTP API client.
- Preserved the Goal 1A conversation interaction model and kept frontend rendering limited to backend-provided Markdown content.

## Actual Implementation Time

- Approximately 12 minutes, based on the Codex Goal timer through implementation, automated validation, live API and browser checks, and documentation closeout.

## Validation

- `cd backend && uv run pytest` — passed, 8 tests against isolated schemas in the agreed PostgreSQL database.
- `cd backend && uv run mypy app` — passed; the broader `app tests` check also passed across 28 source files.
- `cd backend && uv run ruff check .` — passed.
- `cd frontend && npm run test` — passed, 4 test files and 13 tests, including invalid-request edit-and-resubmit recovery.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; Vite transformed 178 modules and produced the production bundle.
- A live `POST /api/matching-analysis` smoke test returned HTTP 200 with exactly `conversationId`, `messageId`, and `content`.
- Direct PostgreSQL inspection confirmed the conversation, user `job_description` message, and assistant `matching_analysis` message were persisted with matching identifiers and content.
- A real local browser check confirmed the frontend called the backend, rendered the returned Markdown report, received a backend-generated conversation ID, had no console warnings/errors, and had no horizontal overflow.
- A live regression check using 20 supplementary Unicode characters confirmed that a backend `INVALID_REQUEST` restores the exact submitted text in the editable composer, removes the ineffective retry action, and produces no browser warnings/errors.
- Invalid input returned HTTP 400 with the safe error contract; Mock-AI failure returned HTTP 503 and rolled back partial persistence; persistence failure returned HTTP 500 without exposing internal details.

## Specification-Conformance Review

- **API contract:** Conforms to Backend Technical Design Section 5.2. The request and response fields match exactly, and response content remains text/Markdown.
- **Layer ownership:** Conforms to the Controller → Service → AI Service / Repository boundary. Controllers handle HTTP, the Service owns the transaction and workflow, the AI Service has no persistence access, and repositories hide session operations.
- **Data model and flow:** Conforms to Backend Technical Design Sections 3 and 4. A valid request creates one Conversation and two ordered Conversation Messages for the JD and analysis.
- **Candidate résumé handling:** Conforms to Backend Technical Design Sections 3.2 and 6.2. The same static PDF resource is passed into the AI boundary without extraction or preprocessing.
- **Frontend integration:** Conforms to Frontend Technical Design Sections 2.1–2.2 and 5.1–5.2. The existing message timeline renders backend content and does not infer or restructure AI conclusions.
- **AI scope:** Conforms to the Lightweight AI Design Decision. Output remains deterministic Mock Markdown, identifies supported, partial, and missing evidence, and avoids scoring or hiring recommendations.
- **Result:** No unresolved material mismatch was found against the authoritative Goal 2 references.

## Problems Fixed and Known Issues

- Fixed a Bugbot finding where a backend `INVALID_REQUEST` response could leave the recruiter with only an ineffective retry action. The rejected JD is now restored in an editable composer, while retry remains available for recoverable service failures.
- Added CORS handling so the separately hosted local frontend can call the backend during development.
- Used isolated PostgreSQL schemas for persistence tests so validation does not substitute SQLite or alter developer data.
- Temporary smoke-test conversations were removed after persistence inspection.
- Follow-up questions, résumé delivery, contact, feedback, tracking, real AI integration, and API-access protection mechanism remain intentionally deferred to their planned Goals or design gate.
