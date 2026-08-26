# Goal 3 — Follow-up Workflow and Persisted Conversation Context

## Version Log

- **v1.1 — 2026-08-26:** Recorded the context-resolution and retry-idempotency fixes prompted by Bugbot review, along with their regression coverage and revalidation.
- **v1.0 — 2026-08-26:** Recorded the completed Goal 3 implementation, validation, specification-conformance review, actual implementation time, and remaining intentional boundaries.

## Completed Scope

- Implemented the exact `POST /api/conversations/{conversationId}/messages` contract with `question` input and only `messageId` plus text/Markdown `content` output.
- Added a follow-up Controller, Service, provider-neutral AI context type, and repository operations while preserving Controller → Service → AI Service / Repository ownership.
- Kept the deterministic Mock AI Service behind the replaceable AI boundary and passed it the same static résumé PDF path plus the full ordered persisted history.
- Added deterministic answers for grounded candidate evidence, unavailable information, and prohibited or unrelated requests without adding a real provider, résumé extraction, scoring, or hiring decisions.
- Persisted each recruiter `follow_up_question` and assistant `follow_up_answer` atomically under the existing Conversation. Unknown conversations store nothing; AI, persistence, and unexpected failures roll back the entire new exchange.
- Enabled the existing bottom composer only after a completed matching analysis, trimmed and validated 1–1,000 character questions consistently, and added independent pending, failure, retry, and concurrent-submission state.
- Appended recruiter questions, processing state, and backend Markdown answers in the existing scrollable timeline. A failed question stays visible and retries without a duplicate user message.
- Preserved all current-session follow-up messages across Home, Job Matching, Resume Preview, and Contact Candidate navigation. Matching-report résumé/contact/feedback actions remain attached only to the matching report.

## Material Files

- Backend: `app/ai/follow_up.py`, `app/ai/mock.py`, `app/controllers/follow_up.py`, `app/services/follow_up.py`, repository/router/error-handler updates, and Goal 3 API/service tests.
- Frontend: `services/followUpClient.ts`, `types/followUp.ts`, conversation message types/labels, `App.tsx` follow-up state and rendering, responsive styles, API client tests, and workspace interaction tests.
- Planning: Goal 3 readiness and completion updates in `planning/PLAN.md`.

## Actual Implementation Time

- Approximately 21 minutes, measured by the Codex Goal timer through readiness documentation, implementation, automated validation, live API/persistence/failure/browser checks, conformance review, and documentation closeout.

## Validation

- `cd backend && uv run pytest` — passed, 34 tests against isolated PostgreSQL schemas.
- `cd backend && uv run mypy app` — passed; the broader `app tests` check passed across 40 source files.
- `cd backend && uv run ruff check .` — passed.
- `cd frontend && npm run test` — passed, 6 test files and 27 tests.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; Vite transformed 184 modules and produced the production bundle.
- Live API smoke testing created one matching analysis followed by two questions in the same conversation. Both follow-up responses returned HTTP 200 with exactly `messageId` and `content`.
- Direct PostgreSQL inspection confirmed six ordered rows under one conversation: `job_description`, `matching_analysis`, `follow_up_question`, `follow_up_answer`, `follow_up_question`, and `follow_up_answer`, with the expected roles and content boundaries.
- A live failure/recovery check stopped the backend for a follow-up request. The UI retained one failed question with an inline retry, PostgreSQL remained at four messages, and retry after restart produced one answer and exactly six messages without duplication.
- At 1280 × 720, the Conversation View height matched the viewport, the composer remained visible with an 18 px bottom gap, and the 588 px message viewport scrolled independently over 1,529 px of content without horizontal overflow.
- At 390 × 844, the compact navigation and 370 px composer remained visible, the 639 px message viewport scrolled independently over 2,526 px of content, and the inline failure card plus retry control stayed fully within the viewport with zero horizontal overflow.
- Browser checks completed three follow-up turns, including grounded, unavailable-information, and out-of-scope responses, and preserved all three questions and answers across résumé, contact, Home, and conversation navigation.
- Browser console inspection found no warnings or errors; only Vite connection messages and the React development information message were present.
- The two temporary smoke-test conversations were deleted after validation.
- A contextual-follow-up regression test confirms that “那这些呢？” inherits the nearest prior supported follow-up topic instead of being rejected as unrelated.
- A response-loss retry regression test confirms that an identical immediate retry returns the existing message ID and content, invokes the Mock only once, and leaves exactly one persisted question/answer pair.

## Specification-Conformance Review

- **Product scope:** Conforms to PRD F001, F005, and S002. Follow-ups remain candidate/matching-specific, unknown information is explicit, unsupported judgments are redirected, and recruiter/assistant messages persist under the evaluation conversation.
- **AI capability:** Conforms to Lightweight AI Design Decision Sections 1.2–1.4 and 2.1–2.2. The Mock receives the job description, matching report, prior turns, current question, and static résumé resource through a provider-neutral boundary; output remains text/Markdown.
- **Frontend behavior:** Conforms to Frontend Technical Design Sections 2.1–2.3, 3.3, 3.5, 4.2–4.3, 4.6–4.7, and 5.1–5.3. The anchored composer, scrollable shared timeline, independent follow-up state, retry path, navigation preservation, and presentation-only ownership are retained.
- **Backend architecture and contract:** Conforms to Backend Technical Design Conversation entities and Sections 3.2, 4.1–4.2, 5, and 6.1–6.3. The exact API fields are stable, the Service prepares ordered context and owns the transaction, repositories hide persistence, and the AI Service does not access storage.
- **Failure semantics:** Invalid input, unknown conversation, AI failure, persistence failure, and unexpected failure use safe errors. Tests and live recovery evidence confirm no partial or duplicate follow-up exchange is stored.
- **Scope boundaries:** No real provider or SDK, prompt/provider payload persistence, résumé extraction or text mirror, streaming, history-retrieval API, refresh restoration, tracking, candidate management, scoring, ranking, or hiring decision was added.
- **Result:** No unresolved material mismatch was found against the Goal 3 authoritative references.

## Problems Fixed and Remaining Known Issues

- Resolved the Bugbot finding where the Mock accepted full history but classified only the latest text; explicit referential wording now resolves against prior persisted follow-up questions.
- Resolved the Bugbot finding where an ambiguous client retry could duplicate a committed exchange; the Service locks the conversation and replays the latest completed answer for an identical immediate retry while retaining the exact `{ "question": ... }` API request.
- Replaced the Goal 4 disabled composer placeholder with the complete persisted workflow while preserving the approved workspace and supporting actions.
- Kept matching-analysis failure/retry state separate from follow-up failure/retry state so one path cannot erase or replace the other.
- Prevented concurrent submissions and duplicate optimistic questions during retry.
- Corrected the live validation environment by restarting a stale pre-Goal-3 backend before the final smoke tests.
- Conversation restoration after page refresh, real AI integration, product tracking, and richer AI evaluation remain intentionally deferred to later Goals.
