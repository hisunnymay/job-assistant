# AI Job Fit Assistant — Implementation Plan

## Document Information

- **Version:** v0.42
- **Status:** Draft — Goal 9 Release Candidate Ready, Deployment Pending
- **Owner:** Mei Chang
- **Last Updated:** 2026-08-28
- **Purpose:** Define implementation order, Goal scope, completion criteria, dependencies, and validation for Codex.

## Version Log

- **v0.42 — 2026-08-28:** Promoted Goal 9 to **Release Candidate Ready — Deployment Pending** after an evaluator-hashed complete rerun passed all hard guardrails but exposed one broad source-heading miss, a narrow traceability correction passed three matching/reliability runs, and the final privacy-safe artifact composed those current-prompt results with the unchanged follow-up results. The final evidence uses 39 provider calls within the approved 60-call ceiling and passes every graded threshold; external deployment gates remain unchanged.
- **v0.41 — 2026-08-28:** Reopened Goal 9 release promotion after final review found that the passing privacy-safe matrix predates the evaluator's post-run negation hardening and cannot be mechanically re-scored because generated outputs are intentionally omitted. Added evaluator hashing for future artifacts and recorded the current candidate as evaluator-evidence-pending until a bounded rerun passes or the user explicitly approves the documented evaluator-only deviation.
- **v0.40 — 2026-08-28:** Promoted Goal 9 to **Release Candidate Ready — Deployment Pending** after the adjusted prompt passed the complete three-run Ark release matrix with zero hard-guardrail violations and every graded accuracy threshold at `1.00`, the evaluator was hardened against negated forbidden-marker false positives without permitting affirmative claims, and the protected local real-provider gateway smoke passed within its four-call ceiling; external registry, deployment, domain, ICP, HTTPS, rollback-by-production-digest, and recruiter-network validation remain separately gated.
- **v0.39 — 2026-08-28:** Implemented the local Goal 9 release-validation bundle, reproducibility manifest, privacy-safe gateway smoke and cleanup recovery, digest-pinned bases, backup/restore rehearsal, and deterministic validation; preserved the first 31-call release artifact after it passed all hard guardrails but missed the approved matching-status threshold (`0.8889` versus `1.00`), fixed the independent-review findings and the cross-dimension evidence cause, and left the adjusted candidate pending separately approved complete Ark revalidation and real-provider gateway smoke.
- **v0.38 — 2026-08-28:** Completed Goal 8 after the current prompt passed the approved three-run final matrix with zero hard-guardrail violations, all graded thresholds satisfied, 30 first-attempt provider calls within the separately approved 60-call and ¥15 ceilings, and privacy-safe artifact closeout; Goal 9 is now ready for local implementation while external deployment remains separately gated.
- **v0.37 — 2026-08-28:** Finalized the environment and release-strategy boundary for Goal 9: local/Codex development and deterministic testing remain the default, mainland Beijing-region single-host Docker Compose is the preferred recruiter-production target after filing and compliance gates, Hong Kong is temporary staging only, releases use mainland-accessible private images pinned by digest, and no mainland server should be purchased before the documented provider/domain/ICP preflight passes.
- **v0.36 — 2026-08-28:** Required every live evaluation command to declare a provider-call ceiling and reject execution before provider access when the selected cases, run count, and two-attempt workflow could exceed that ceiling.
- **v0.35 — 2026-08-28:** Recorded the Goal 8 checkpoint after three bounded prompt-tuning iterations, preserved the completed but graded-threshold-short final attempt, noted the user-stopped rerun that produced no artifact, and marked Goal 8 pending until the current prompt passes the complete three-run matrix and closeout validation.
- **v0.34 — 2026-08-28:** Recorded the corrected one-pass Goal 8 Pro baseline, retained the preceding pilot as non-baseline evidence, and approved the zero-tolerance hard guardrails plus numerical quality and latency thresholds that govern bounded tuning and the three-run final evaluation.
- **v0.33 — 2026-08-27:** Completed Goal 7A with the provider-free static example, truthful waiting timer, differentiated safe retry behavior, Bugbot fixes, full regression/conformance validation, and a privacy-safe Mini run that was materially faster but retained the Pro default pending broader evidence-calibration evaluation.
- **v0.32 — 2026-08-27:** Started Goal 7A with a provider-free static example report, truthful elapsed waiting states, invalid-output-only correction retries, and a separately authorized Mini matching/follow-up compatibility comparison that cannot change the default model automatically.
- **v0.31 — 2026-08-27:** Completed the verified-text Goal 7 correction with fixed-resource integrity and source-reference guardrails, text-only stable-prefix Ark transport, Pro matching/follow-up live validation in 34.28 seconds with two first-attempt successes, Bugbot fixes, and full regression/conformance closeout.
- **v0.30 — 2026-08-27:** Reopened Goal 7 to use the user-verified fixed résumé Markdown as runtime AI context while retaining the paired PDF for recruiter preview/download, strict internal output, bounded retries, and unchanged public contracts.
- **v0.29 — 2026-08-27:** Completed Goal 7 through the corrected Ark Responses API path with fixed-PDF strict output, bounded retries, preserved contracts and persistence semantics, live matching/follow-up validation, independent review fixes, full regression/privacy checks, and implementation-log closeout.
- **v0.28 — 2026-08-27:** Corrected Goal 7 to use Ark's documented Responses API for inline PDF input and strict structured output, with thinking disabled and all direct-PDF, non-streaming, retry, privacy, persistence, and public-contract boundaries preserved.
- **v0.27 — 2026-08-27:** Completed the AI Design Gate and made Goals 7–9 implementation-ready from AI System Design v1.1 and Backend Technical Design v0.6, including exact authority, configuration, internal contracts, retry/failure semantics, live-provider/evaluation commands, release gates, and external prerequisites.
- **v0.26 — 2026-08-27:** Completed Goal 6 with isolated Playwright journeys, recoverable error coverage, provider-neutral Docker demo packaging, gateway-level Basic Auth, clean-start smoke validation, independent Bugbot review, and specification-conformance closeout.
- **v0.25 — 2026-08-27:** Started Goal 6 with the approved provider-neutral single-host Docker target, desktop and compact Chrome accessibility scope, Nginx Basic Auth gateway, Playwright end-to-end coverage, clean-setup validation, and independent-review requirements.
- **v0.24 — 2026-08-27:** Closed the Goal 5 Bugbot findings with permanent-rejection queue handling, generated-report conversion cohorts, deletion-safe event replay fingerprints, additive local schema upgrade, and corrected AI-design readiness language.
- **v0.23 — 2026-08-27:** Completed the corrected Goal 5 with centralized PostgreSQL event persistence, idempotent tracking delivery, a bounded frontend retry queue, internal aggregate reporting, 90-day cleanup, privacy enforcement, and full guardrail/conformance validation.
- **v0.22 — 2026-08-27:** Reopened Goal 5 because browser-local events cannot support S001's required centralized, cross-session MVP metric evaluation; replaced the local-only decision with a privacy-safe backend tracking contract, idempotent delivery, retention, and aggregate validation requirements while preserving the completed AI guardrail work.
- **v0.21 — 2026-08-27:** Completed Goal 5 with all six PRD events, privacy-safe browser-local session tracking, non-blocking failure behavior, reusable deterministic guardrail fixtures, and full automated/specification validation.
- **v0.20 — 2026-08-27:** Started Goal 5, selected a browser-local tracking repository behind a replaceable frontend interface, defined its privacy-safe event fixture and session/conversation boundary, and added the authoritative AI guardrail requirements before implementation.
- **v0.19 — 2026-08-26:** Addressed the Goal 4 Bugbot findings by making report feedback retry-safe under a matching-message lock and constraining the final serialized qualitative comment to the existing 2,000-character backend limit without changing the API contract.
- **v0.18 — 2026-08-26:** Addressed the Goal 3 Bugbot findings by resolving referential follow-ups from prior persisted questions and replaying an identical immediately retried exchange under a conversation lock without changing the approved API contract.
- **v0.17 — 2026-08-26:** Completed Goal 3 with the persisted multi-turn follow-up API, ordered backend context preparation, deterministic bounded Mock answers, atomic rollback behavior, recoverable frontend conversation flow, and full automated/API/persistence/browser/conformance validation.
- **v0.16 — 2026-08-26:** Started Goal 3 and added its authoritative references, non-negotiable behavior and architecture boundaries, exact API fixture, atomic persistence and failure semantics, and complete validation requirements before implementation.
- **v0.15 — 2026-08-26:** Added the approved Goal 4 feedback refinement: contextual icon tooltips, rating-specific predefined reasons, and required qualitative input after a recruiter opens the feedback dialog, without changing the backend contract.
- **v0.14 — 2026-08-26:** Completed Goal 4 reference UI alignment with the standalone entrance, three-view workspace, preserved conversation navigation, original résumé preview/download, non-sending contact copy flow, report-linked one-click feedback, and desktop/compact validation.
- **v0.13 — 2026-08-26:** Reopened Goal 4 for implementation of the approved Frontend Technical Design v0.6 desktop reference UI while preserving the already completed résumé, contact, and feedback backend capabilities.
- **v0.12 — 2026-08-25:** Completed Goal 4 with the approved résumé preview/download API, independent and contextual résumé/contact actions, dynamic non-sending greeting template, and report-linked feedback persistence.
- **v0.11 — 2026-08-25:** Completed Goal 2 with the persisted matching-analysis API, deterministic backend Mock AI Service, PostgreSQL-backed conversation workflow, frontend HTTP integration, safe error contract, and end-to-end local validation.
- **v0.10 — 2026-08-25:** Completed Goal 1A by realigning the frontend around a conversation message timeline and the authoritative text/Markdown matching-analysis response contract; Goal 2 is now ready.
- **v0.9 — 2026-08-25:** Recorded Goal 0's user-provided actual implementation time as 21 minutes.
- **v0.8 — 2026-08-25:** Required actual implementation time and its measurement basis to be recorded for each completed coding Goal, without inventing unavailable historical timing data.
- **v0.7 — 2026-08-25:** Added the Goal readiness and conformance gate, recorded the Goal 1 architecture mismatch, introduced Goal 1A to realign the conversation workspace and response contract, and blocked Goal 2 until that correction is complete.
- **v0.6 — 2026-08-25:** Completed Goal 1 with the Chinese frontend matching journey, deterministic résumé-grounded mock data, recoverable UI states, responsive presentation, and automated and browser validation.
- **v0.5 — 2026-08-25:** Completed Goal 0 with runnable frontend/backend scaffolds, PostgreSQL initialization, safe configuration, locked dependencies, and the agreed validation baseline.
- **v0.4 — 2026-08-25:** Added and verified the finalized candidate résumé PDF at its agreed static-resource path, completing the Pre-implementation Decisions.
- **v0.3 — 2026-08-25:** Confirmed the package managers, Python version, PostgreSQL database, environment and secret rules, validation tools, and standard commands; retained the candidate résumé PDF as a pending required asset.
- **v0.2 — 2026-08-25:** Clarified that this is a living plan that can evolve with implementation and that the user only needs to review one Goal at a time.
- **v0.1 — 2026-08-25:** Created the initial phased implementation plan. Pre-implementation technology and validation choices remain intentionally unresolved.

## 1. Authority and Use

This plan is subordinate to:

1. `docs/01_Product_Requirement_Document.md`;
2. `docs/03_Lightweight_AI_Design_Decision.md`;
3. `docs/02_AI_System_Design.md`;
4. `docs/04_Frontend_Technical_Design.md`;
5. `docs/05_Backend_Technical_Design.md`;
6. `AGENTS.md`.

This file owns Goal order, dependencies, completion criteria, validation commands, and status. It does not change approved scope, architecture boundaries, AI behavior, or API contracts.

Codex should implement only the Goal explicitly requested by the user. Branch, commit, documentation-update, and implementation-log rules are defined in `AGENTS.md` and are not repeated here.

## 2. How to Use This Plan

- This is a living implementation guide, not a fixed contract. It may change when real implementation reveals better task boundaries, dependencies, validation methods, or technical constraints.
- The user does not need to understand or approve the entire plan before implementation begins. Focus on one Goal at a time.
- Before starting a Goal, Codex should explain in plain language what will be built, why it is needed, what decisions require user input, which authoritative sections apply, which constraints are non-negotiable, and how completion will be checked.
- Future Goals may be clarified, split, combined, or reordered with the user's agreement. Update this file's Version Log when that happens.
- Plan changes must not silently override the PRD, finalized design documents, `AGENTS.md`, or agreed API contracts. Changes to those contracts must follow their document-update rules.
- Do not rewrite completed Goals to hide what happened. Record implementation results in the corresponding implementation log and add follow-up work explicitly when needed.
- After completing a coding Goal, add **Actual Implementation Time** and its measurement basis to the Goal metadata. Prefer the Codex Goal timer when available; otherwise use a clearly identified start-to-finish measurement. Exclude time spent waiting for user decisions, approvals, or external blockers when it can be separated, and do not invent unavailable historical timing data.

### Goal Readiness and Conformance Gate

Before coding begins, the active Goal must identify:

- The authoritative product and design sections that apply;
- Non-negotiable interaction, architecture, ownership, and contract constraints;
- A representative request/response fixture when the Goal crosses a frontend-backend boundary;
- Validation that checks specification conformance in addition to tests, lint, type-checking, builds, and browser behavior.

Before a Goal is marked complete, Codex must compare the implementation with those references and record the result in the implementation log. A code review such as Bugbot checks defects within the implementation; it does not replace this specification-conformance review. A material mismatch creates an explicit correction Goal or blocks dependent Goals.

## 3. Plan Status

- **Phase A — Demo with Mock AI:** Complete
- **AI Design Gate:** Complete through AI System Design v1.3 and Backend Technical Design v0.8.
- **Phase B — Real AI:** Goals 7, 7A, and 8 are complete through the verified-text Pro path, bounded Mini compatibility check, versioned evaluation matrix, three bounded tuning iterations, and the passing three-run final evaluation.
- **Current coding readiness:** Goals 0–8 are complete. Goal 9 is **Release Candidate Ready — Deployment Pending** after evaluator-hashed three-run workflow evidence and the protected local real-provider gateway smoke passed all local gates. External purchase, registry, deployment, domain, filing, HTTPS, rollback-by-production-digest, and recruiter-network actions remain separately gated.

## 4. Pre-implementation Decisions

These are agreed project inputs, not a coding Goal.

### Confirmed Decisions

- **Frontend package manager:** npm.
- **Python project and dependency manager:** uv with project-specific Python 3.12 and a committed `uv.lock`.
- **MVP database:** PostgreSQL for local development, testing, and public deployment. Access remains behind the Repository layer.
- **Frontend configuration:** expose only non-secret browser configuration, such as `VITE_API_BASE_URL`, through Vite environment variables.
- **Backend configuration:** use Pydantic Settings for validated environment variables, including `DATABASE_URL` and later server-side secrets.
- **Environment files:** commit `.env.example` with variable names and safe examples; do not commit `.env` or `.env.*.local` files.
- **AI secrets:** no AI provider key is required in Mock mode. Real-AI runs use a user-supplied `ARK_API_KEY` that remains backend-only, uncommitted, absent from logs and persisted data, and unavailable to the frontend.
- **Frontend validation:** ESLint, TypeScript (`tsc --noEmit`), Vitest with React Testing Library, and the Vite production build.
- **Backend validation:** Ruff, mypy, pytest, and FastAPI `TestClient`.
- **End-to-end validation:** Playwright, introduced when Goal 6 requires full-journey coverage.

### Fixed Candidate Résumé Resource

- **Status:** Confirmed; the Markdown was supplied and verified by the user.
- **Recruiter preview/download:** `backend/app/resources/resume/mei_chang_resume.pdf`, SHA-256 `20a4d191dcc675b67a55da4296c2200cf2ceed1b3deb9aca4fbdf9e5e8cb08bd`.
- **Runtime AI context:** `backend/app/resources/resume/mei_chang_resume.md`, SHA-256 `9e1db40802663dd49fc5ece9637a7b386f3f7a7dcc552bdc7444ae1cf17e1c04`.
- Treat both files as one approved fixed resource. Do not add request-time extraction/preprocessing, résumé upload/management, or independently edit either representation without renewed verification and digest updates.

Already finalized:

- Frontend: React + TypeScript + Vite;
- Backend: Python + FastAPI;
- Demo AI: deterministic mock behind the AI Service boundary;
- Real AI: Volcengine Ark model `doubao-seed-2-1-pro-260628` through LangChain `ChatOpenAI` in Responses API mode and an execution-local LangGraph workflow, with the native Ark Python SDK allowed only as the approved compatibility fallback.

### Real-AI Implementation Decisions

- Use one AI Service implementation for both matching and follow-up protocols. Keep `MockAIService` for deterministic automated tests and explicit Mock-mode runs.
- Select the adapter through validated backend configuration: `AI_PROVIDER=mock|ark`, `ARK_API_KEY`, `ARK_BASE_URL`, `ARK_MODEL`, and a positive finite `ARK_REQUEST_TIMEOUT_SECONDS` value. Use `https://ark.cn-beijing.volces.com/api/v3` and `doubao-seed-2-1-pro-260628` as the approved Ark defaults.
- Send the exact user-verified `mei_chang_resume.md` as a stable UTF-8 `input_text` block before dynamic job-description or conversation content. Verify its approved filename and SHA-256 before every provider execution. The paired PDF remains the recruiter preview/download source.
- Use Ark's Responses API with text-only input and the internal strict `json_schema` through `text.format`. Explicitly disable thinking, keep the request non-streaming, validate with the Pydantic schemas and cross-field invariants in AI System Design Section 3, and render only validated results into the unchanged public text/Markdown `content` field.
- Use one unified budget of two provider attempts total. Disable library retries; allow the second attempt only for an approved transient failure or invalid structured result. Preserve existing atomic rollback and completed-identical-follow-up replay semantics.
- Keep prompts, provider payloads, raw provider responses, résumé/JD/question content, secrets, and internal errors out of persistence and production logs. Generate and log only privacy-safe correlation and execution metadata.
- Treat the exact fixed-Markdown-plus-strict-schema provider combination as a Goal 7 completion gate, not as permission to alter the public API if compatibility fails.

### Standard Validation Commands

- Frontend tests: `cd frontend && npm run test`;
- Frontend type-check: `cd frontend && npm run type-check`;
- Frontend lint: `cd frontend && npm run lint`;
- Frontend build: `cd frontend && npm run build`;
- Backend tests: `cd backend && uv run pytest`;
- Backend type-check: `cd backend && uv run mypy app tests`;
- Backend lint: `cd backend && uv run ruff check .`;
- End-to-end tests after Goal 6 introduces Playwright: `cd frontend && npm run test:e2e`.

Goal 0 must configure these commands before treating its validation baseline as complete.

---

# Phase A — Demo with Mock AI

## Goal 0 — Project Scaffold and Validation Baseline

- **Status:** Complete
- **Depends on:** Confirmed Decisions in Section 4
- **Branch:** `goal/00-project-scaffold`
- **Actual Implementation Time:** 21 minutes, provided by the user from the original implementation session.

### Outcome

A minimal frontend and backend can run locally, and all agreed validation commands are explicit and executable.

### Scope

- Scaffold the React + TypeScript + Vite frontend under `frontend/`;
- Scaffold the Python + FastAPI backend under `backend/`;
- Add only the dependencies required by the current architecture;
- Establish the modular-monolith backend layer structure;
- Configure the selected database and a minimal repository foundation;
- Add typed backend configuration and frontend environment handling;
- Add safe environment examples without real secrets;
- Provide a backend health endpoint and minimal frontend application shell;
- Define exact test, type-check, lint, build, and local-run commands;
- Keep AI behavior mocked and do not add a real AI SDK or provider key.

### Completion Criteria

- Frontend and backend start locally from documented commands;
- The frontend production build succeeds;
- Backend health endpoint returns a successful response;
- Frontend and backend test commands run successfully;
- Type-check and lint commands run successfully;
- Database initialization works in a clean local environment;
- No secret is committed or exposed through frontend environment variables;
- Every standard validation command defined in Section 4 exists and runs successfully.

### Validation

```text
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd backend && uv run pytest
cd backend && uv run mypy app
cd backend && uv run ruff check .
```

## Goal 1 — Frontend Matching Journey with Mock Data

- **Status:** Complete
- **Depends on:** Goal 0
- **Branch:** `goal/01-frontend-matching-journey`
- **Actual Implementation Time:** Approximately 15 minutes, reported by the Codex Goal timer.

### Outcome

A recruiter can complete the main matching-report journey in Chinese using deterministic frontend mock data, without a backend dependency.

### Scope

- Initial guidance;
- Job-description input and validation;
- Loading/processing state;
- Matching-report presentation;
- Supported evidence, partial information, and missing-information presentation;
- Empty, invalid-input, success, and failure states;
- Responsive and readable layout for the intended demo environment;
- No overall match score, hiring recommendation, or unsupported candidate claim.

### Completion Criteria

- The journey works from initial guidance through report review;
- Valid and invalid job-description behavior is clear;
- Loading and failure states are visible and recoverable;
- Mock results visibly distinguish supported, partial, and missing information;
- User-facing content is Chinese and strings are separable from components;
- The UI does not depend on backend or AI-provider implementation details.

### Validation

```text
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
Manual browser check: initial, invalid, loading, success, and failure states
```

### Post-completion Finding

Goal 1 passed its stated functional validation but diverged from the finalized conversation-workspace structure and text/Markdown message contract. The original completion remains recorded rather than rewritten; Goal 1A is the required corrective work. See `history/implementation_logs/goal-01-frontend-matching-journey.md`.

## Goal 1A — Conversation Workspace and Contract Alignment

- **Status:** Complete
- **Depends on:** Goal 1
- **Branch:** `goal/01a-conversation-workspace-alignment`
- **Actual Implementation Time:** Approximately 14 minutes, based on the Codex Goal timer through implementation, validation, and documentation closeout.

### Authoritative References and Constraints

- Product Requirement Document: F002 Job Description Input, F003 Matching Report, and F005 Ask Follow-up Questions;
- Frontend Technical Design: Sections 1.2, 2.1–2.2, 3.1–3.3, 4.1, and 5.1–5.2;
- Backend Technical Design: Conversation Message, Section 5.2 request/response formats, and Section 5.3 integration assumptions;
- The workspace must use a continuing message-based interaction while keeping exact layout and styling flexible;
- The frontend may render matching content but must not define or infer AI conclusions;
- The mock analysis boundary must use the future API response shape: `conversationId`, `messageId`, and text/Markdown `content`.

### Outcome

The existing Goal 1 journey is realigned as the first slice of the Job Assistant conversation workspace and can accept Goal 2 backend responses without changing its interaction model or inventing a frontend-owned report contract.

### Scope

- Present initial guidance as assistant content in a conversation timeline;
- Present the submitted job description as a user message;
- Present processing, failure, retry, and matching analysis as assistant-message states;
- Replace the frontend-owned structured `MatchingReport` boundary with the agreed message response fixture;
- Render deterministic mock matching analysis from text/Markdown `content` while preserving supported, partial, and missing-information clarity;
- Preserve the existing Chinese copy separation, input validation, responsive behavior, accessibility, and prohibited-content boundaries;
- Do not add backend integration, persistence, follow-up questions, résumé actions, contact, or feedback in this corrective Goal.

### Completion Criteria

- Initial guidance, submitted job description, and matching analysis appear in one continuing message timeline;
- The mock client returns `conversationId`, `messageId`, and text/Markdown `content`;
- No frontend-owned schema is required to determine AI evidence status, findings, or conclusions;
- Loading and failure behavior appear in the conversation context and remain recoverable;
- The structure can append follow-up user and assistant messages in Goal 3 without another page-level redesign;
- A specification-conformance review against the cited sections finds no unresolved material mismatch.

### Validation

```text
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
Contract fixture check: mock response uses conversationId, messageId, and text/Markdown content
Manual browser check: initial guidance -> user JD message -> loading -> assistant report -> failure/retry
Specification review: compare the page structure, data boundary, and state flow with the cited authoritative sections
```

## Goal 2 — Integrated Matching Vertical Slice with Mock AI Service

- **Status:** Complete
- **Depends on:** Goal 1A
- **Branch:** `goal/02-matching-vertical-slice`
- **Actual Implementation Time:** Approximately 12 minutes, based on the Codex Goal timer through implementation, automated validation, live API and browser checks, and documentation closeout.

### Authoritative References and Constraints

- Backend Technical Design Section 5 is the authoritative API contract;
- Frontend Technical Design Sections 2.1–2.2 and 5.1–5.2 define the conversation presentation and frontend ownership boundary;
- Use the exact matching-analysis response fields `conversationId`, `messageId`, and text/Markdown `content`;
- Replace the mock transport without changing the Goal 1A conversation interaction model;
- Do not introduce a frontend-owned AI-analysis schema or transform backend content into new conclusions.

### Outcome

The frontend submits a job description to the authoritative matching-analysis API and renders the persisted response produced through the backend's Mock AI Service.

### Scope

- Implement `POST /api/matching-analysis` according to Backend Technical Design Section 5;
- Preserve Controller → Service → AI Service / Repository boundaries;
- Add deterministic Mock AI Service behavior;
- Persist the Conversation, submitted job description, and generated message;
- Connect the frontend to the backend through a small API client boundary;
- Handle invalid input, backend failure, and mock-AI failure using the agreed error contract;
- Add API, service, repository, and frontend integration tests proportionate to the slice.

### Completion Criteria

- A valid job description creates a persisted conversation and matching-report message;
- The API response matches the agreed `conversationId`, `messageId`, and `content` contract;
- Refreshing or inspecting persistence confirms the conversation and messages were stored;
- The frontend renders the backend response and no longer uses local matching-report mock data for this path;
- Invalid requests and internal failures return safe, consistent errors;
- No real AI provider, raw prompt, or provider payload is introduced.

### Validation

```text
cd backend && uv run pytest
cd backend && uv run mypy app
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run build
Contract smoke test: POST /api/matching-analysis
```

## Goal 3 — Follow-up Workflow and Persisted Conversation Context

- **Status:** Complete
- **Depends on:** Goal 2
- **Branch:** `goal/03-follow-up-context`
- **Actual Implementation Time:** Approximately 21 minutes, measured by the Codex Goal timer through readiness documentation, implementation, automated validation, API and persistence smoke tests, failure/retry testing, desktop and compact browser checks, conformance review, and documentation closeout.

### Authoritative References and Constraints

- Product Requirement Document: F001 Candidate Resume Data Source, F005 Ask Follow-up Questions, and S002 Conversation Logging;
- Lightweight AI Design Decision: Sections 1.2–1.4 and 2.1–2.2;
- Frontend Technical Design: Sections 2.1–2.3, 3.3, 3.5, 4.2–4.3, 4.6–4.7, and 5.1–5.3;
- Backend Technical Design: Conversation and Conversation Message entities, Sections 3.2, 4.1 follow-up flow, 4.2, 5, and 6.1–6.3;
- Follow-up is available only after a successful matching analysis has created an active persisted conversation;
- Questions and answers remain in that conversation and are presented in the existing scrollable Conversation View; navigation must preserve the current-session timeline;
- The frontend owns input and UI state only. It must not classify scope, infer evidence, construct AI answers, or implement backend workflow;
- The Service Layer owns conversation validation, ordered context preparation, AI coordination, and transaction control; repositories own persistence access, and the AI Service has no persistence access;
- The Demo uses the deterministic Mock AI Service and the same static résumé PDF path already used by matching analysis, without extraction, preprocessing, or a text mirror;
- Supported scope is candidate experience/background, evidence behind matching results, identified information gaps, and available candidate context. Unknown information must remain unknown; hiring recommendations, ranking/comparison, performance prediction, personal judgments, scoring, and unrelated requests must be rejected or redirected;
- Do not add a real provider, provider SDK or secret, raw prompt/provider-payload persistence, streaming, conversation-history retrieval, refresh restoration, tracking, candidate management, or another later-Goal capability.

### Authoritative API Fixture

```http
POST /api/conversations/{conversationId}/messages
Content-Type: application/json
```

Request:

```json
{
  "question": "Does the candidate have AI Agent experience?"
}
```

Successful response:

```json
{
  "messageId": "message_003",
  "content": "..."
}
```

The response contains exactly the backend-generated message identifier and frontend-renderable text/Markdown content. Errors retain the existing safe `{ "code": "ERROR_CODE", "message": "..." }` envelope, with follow-up-specific validation copy.

### Persistence and Failure Semantics

- One follow-up exchange is atomic: verify the conversation, create and flush the `user` / `follow_up_question`, prepare the full ordered history including that question, call the Mock AI Service with the static résumé path and prepared context, create the `assistant` / `follow_up_answer`, and commit both messages together;
- Unknown conversations store nothing and return a safe not-found response;
- Invalid input, Mock AI failure, persistence failure, and unexpected failure expose no internal details;
- Mock AI or persistence failure rolls back both messages so no orphaned question or answer remains;
- The frontend keeps a failed question visible locally and retries it in context without appending a duplicate user message or allowing a concurrent submission.

### Outcome

A recruiter can ask supported follow-up questions within the same evaluation context, and the backend prepares the persisted conversation history for each Mock AI Service call.

### Scope

- Implement `POST /api/conversations/{conversationId}/messages` according to the agreed contract;
- Persist recruiter questions and generated answers;
- Load the job description, matching report, and relevant prior messages in the Service Layer;
- Keep persistence access outside the AI Service;
- Support deterministic in-scope, unavailable-information, and out-of-scope mock responses;
- Add the follow-up conversation UI and its loading/error states.

### Completion Criteria

- Follow-up questions remain associated with the correct conversation;
- The Service Layer supplies the full relevant context to the Mock AI Service;
- Supported questions receive deterministic answers grounded in available mock context;
- Missing information is identified as unknown rather than invented;
- Hiring decisions, ranking, performance prediction, and unrelated questions are rejected or redirected;
- Conversation messages remain available through the selected persistence layer.

### Validation

```text
cd backend && uv run pytest
cd backend && uv run mypy app
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
API smoke test: initial matching analysis followed by at least two questions in the same conversation
Persistence inspection: verify ordered roles, message types, conversation IDs, and content boundaries
Failure smoke test: verify a failed follow-up is recoverable and creates no partial or duplicate persisted exchange
Desktop browser check: anchored composer, independently scrolling history, multiple turns, inline processing/error/retry, and navigation preservation
Compact browser check: composer, scrolling, controls, and error state remain operable without horizontal overflow
Browser console check: no warnings or errors in the validated journey
Specification review: compare implementation with every Goal 3 authoritative reference and record the conformance result
```

## Goal 4 — Résumé, Contact, and Feedback Actions

- **Status:** Complete
- **Depends on:** Goal 2
- **Branch:** `goal/04-supporting-actions`
- **Completed Functional Slice Time:** Approximately 15 minutes, based on the Codex Goal timer through implementation, automated validation, API and persistence smoke tests, browser checks, and documentation closeout on 2026-08-25. This historical time does not include the newly approved UI-alignment work.
- **Reference UI Alignment Time:** Approximately 27 minutes, based on the Codex Goal timer through implementation, automated validation, API and persistence checks, desktop/compact browser validation, specification review, and documentation closeout on 2026-08-26.
- **Feedback Interaction Refinement Time:** Approximately 8 minutes, based on the Codex Goal timer through document updates, implementation, automated validation, live persistence inspection, desktop/compact browser checks, and documentation closeout on 2026-08-26.

### Post-completion Design Change

The original functional slice completed résumé preview/download, contact, greeting copy, and report-linked feedback. Frontend Technical Design v0.6 subsequently approved a more specific desktop composition. Goal 4 was reopened for that visual and interaction alignment; the completed backend behavior remained valid and was not reimplemented or changed.

### Authoritative References and Constraints

- Product Requirement Document: F003 Matching Report, F004 Resume Preview, F006 Contact CTA, and F007 Report Feedback;
- Frontend Technical Design v0.7: Sections 2.1–2.3, 3.3–3.7, 4.6–4.7, and 5.1–5.3;
- Backend Technical Design: Section 5 `GET /api/resume` and `POST /api/feedback` contracts remain unchanged;
- AI-generated matching content remains backend-provided text/Markdown; the frontend must not calculate evidence categories, counts, conclusions, or recommendations;
- The same predefined static PDF remains the résumé preview/download source and future AI context;
- Contact and greeting actions copy or expose information only and must not send a message automatically;
- Helpful maps to feedback rating `5` and Not Helpful maps to rating `1`; after either action opens the dialog, at least one predefined reason or non-whitespace custom entry is required and is serialized through the existing `comment` field.

### Outcome

Recruiters can move through the approved desktop entrance, matching, résumé, and contact experience; review/download the fixed résumé; access and copy candidate contact content; and submit message-linked feedback without leaving the evaluation context.

### Scope

- Add the approved static candidate résumé PDF;
- Implement `GET /api/resume` returning `application/pdf`;
- Provide résumé preview and download from navigation and the report context;
- Use the same PDF resource intended for later AI context;
- Do not add backend PDF extraction, preprocessing, upload, or candidate management;
- Add the static contact CTA and recruiter-name greeting template;
- Do not automatically send a message;
- Implement `POST /api/feedback` and persist feedback against its conversation/message;
- Add clear success and error feedback in the UI;
- Align the Entrance View with the approved centered introduction, large 6,000-character JD input, example-fill action, character count, and disabled-until-valid analysis action;
- Use the approved three-item workspace navigation for Job Matching, Resume Preview, and Contact Candidate, with the product brand acting as the Home control;
- Keep one right-side workspace view active at a time and preserve the active conversation when moving between workspace views or Home;
- Align the Conversation View with the submitted JD at the top, a vertically scrollable message area, contextual résumé/contact/helpful/not-helpful actions beneath the relevant AI reply, and the follow-up composer anchored at the bottom;
- Align the Resume Preview View with the embedded original PDF, candidate name, and prominent download action;
- Align the Contact View with separate email/phone cards and copy controls, optional recruiter name, greeting preview, and prominent copy-greeting action;
- Apply the approved desktop visual direction and accessible icon interaction states without hard-coding the illustrative evidence or counts shown in the reference images.
- Show a floating action-name label when a contextual icon receives pointer hover or keyboard focus;
- Open a rating-specific modal for Helpful and Not Helpful, provide multi-select predefined reasons plus custom text, and keep Submit disabled until the recruiter supplies at least one of them.

### Completion Criteria

- The approved PDF can be previewed and downloaded;
- Preview/download uses the same unmodified static PDF resource;
- Contact information and greeting behavior are correct and do not send externally;
- Valid feedback is persisted against the correct report context;
- Invalid feedback returns the agreed safe error format;
- Independent navigation to résumé and contact actions works;
- Desktop entrance, matching, résumé, and contact views match the hierarchy and control placement in Frontend Technical Design Section 2.3;
- The standalone Entrance View has no workspace sidebar, and the three workspace views share the approved persistent left navigation;
- Navigation and Home transitions preserve the existing conversation unless a new analysis is intentionally submitted;
- The Conversation View keeps its follow-up composer available while message content scrolls, without overlap or hidden primary actions;
- Résumé, contact, Helpful, and Not Helpful actions are attached to the relevant AI reply and expose accessible names, keyboard focus, and visible selected/submission states;
- Helpful and Not Helpful persist ratings `5` and `1` respectively against the correct conversation and message, with duplicate submission prevented;
- Resume, contact, Helpful, and Not Helpful icons expose visible floating action-name labels on pointer hover and keyboard focus;
- The feedback dialog provides rating-specific predefined reasons, supports multiple selections, and cannot submit without at least one selected reason or non-whitespace custom entry;
- Selected reasons and custom text use the existing feedback `comment` field without changing the backend contract;
- The frontend continues to render backend text/Markdown without introducing a frontend-owned AI-analysis schema;
- The UI remains readable and operable at the agreed desktop demo viewport and a representative compact viewport.

### Validation

```text
cd backend && uv run pytest
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
File smoke test: GET /api/resume returns the expected PDF
Feedback smoke test: Helpful and Not Helpful persist ratings 5 and 1 for the expected report message
Manual browser check: entrance -> matching -> résumé -> matching -> contact -> matching, confirming conversation preservation
Manual visual comparison: desktop entrance, matching, résumé, contact, reply actions, and bottom composer against Frontend Technical Design Section 2.3 references
Compact viewport check: navigation, scrolling, form controls, PDF fallback/download, and copy/feedback states remain usable
Feedback interaction check: icon hover/focus labels appear; both rating dialogs show the correct predefined reasons; empty submission is disabled; selected reasons/custom text enable submission
Specification review: compare implementation against the Goal 4 authoritative references and record the result in the implementation log
```

## Goal 5 — Product Tracking and Deterministic AI Guardrails

- **Status:** Complete
- **Depends on:** Goals 3 and 4
- **Branch:** `goal/05-tracking-and-guardrails`
- **Actual Implementation Time:** Approximately 18 minutes for the reopened centralized-tracking correction, measured by the Codex Goal timer through implementation, regression coverage, complete validation, command smoke checks, conformance review, and documentation closeout. The earlier approximately 14-minute browser-local checkpoint remains recorded in Version Log v0.21 and the implementation history.

### Entry Decision

Use the existing backend and PostgreSQL database as the authoritative centralized event store through `POST /api/tracking-events`. Keep the pseudonymous tracking-session identifier in `sessionStorage`; browser local storage may hold only a bounded queue of privacy-safe events awaiting backend acknowledgement. The superseded browser-only event log was a conformance mismatch and is not the completed S001 analytics implementation.

### Authoritative References and Constraints

- Product Requirement Document S001 requires page visit, job-description submission, matching-report generation, résumé preview, contact CTA, and feedback-submission events associated with a user session;
- Product Requirement Document F003 and F005 and Lightweight AI Design Decision Sections 1.2–1.4 require evidence-grounded matching, explicit partial/missing information, bounded follow-ups, and rejection of unsupported judgments;
- Frontend Technical Design Section 4.4 owns all six interaction boundaries, centralized delivery, the pseudonymous session identifier, the bounded pending queue, and non-blocking failure behavior;
- Backend Technical Design User Behavior Event, Section 5, and Section 7.5 define the persistent entity, `POST /api/tracking-events` contract, idempotency, privacy, Conversation association, and 90-day retention;
- Each event contains only `eventId`, `eventName`, `sessionId`, `occurredAt`, server-generated `receivedAt`, a server-generated SHA-256 request fingerprint, and an optional `conversationId`. Do not store job descriptions, résumé content, follow-up questions, feedback comments, contact data, IP addresses, user-agent strings, prompts, provider payloads, or other sensitive content;
- Page visit is emitted once per application mount; job-description submission is emitted once for the recruiter's valid initial submit but not an automatic retry; matching-report generation is emitted after success; résumé preview and contact CTA are emitted on each explicit navigation action; feedback submission is emitted only after successful persistence;
- Tracking write or storage failure must be swallowed at the tracking boundary and must not alter recruiter-visible behavior;
- Backend persistence is authoritative for evaluation; the browser queue is not an analytics source;
- Identical retries reuse `eventId` and must not create duplicate persisted events;
- Events older than 90 days are removed through a documented maintenance operation;
- Guardrail cases must be provider-neutral reusable fixtures and must run against the deterministic Mock without adding a real model, provider, eval platform, strict AI output schema, or frontend reasoning.

### Tracking Event Fixture

```json
{
  "eventId": "event_001",
  "eventName": "matching_report_generated",
  "sessionId": "session_001",
  "occurredAt": "2026-08-27T00:00:00.000Z",
  "conversationId": "conversation_001"
}
```

Successful response:

```json
{
  "success": true
}
```

### Outcome

The Demo centrally persists the required product events so authorized evaluators can calculate cross-session usage and conversion metrics, and it retains repeatable checks for AI behavior boundaries without a real provider.

### Scope

- Track page visit, job-description submission, matching-report generation, résumé preview, contact CTA, and feedback submission;
- Keep tracking session identity separate from Conversation identity;
- Add the User Behavior Event database model, repository operation, tracking Service, Controller, and `POST /api/tracking-events` route within the existing layered backend;
- Associate centrally persisted events with the relevant session and Conversation when available;
- Replace the permanent browser event log with a 100-event pending-delivery queue that retries stable event IDs, removes acknowledged events, discards permanent contract rejections, and discards the oldest event on overflow;
- Avoid sensitive content in event payloads;
- Provide a documented operation that deletes tracking events older than 90 days;
- Provide a documented internal aggregate report operation for the Section 2.2 total and distinct-session usage counts and Contact Conversion Rate without adding an event-level export, public analytics API, or recruiter-facing Dashboard;
- Add deterministic fixtures/checks for supported evidence, partial information, missing information, out-of-scope questions, and unsupported scoring;
- Prepare reusable behavior cases for later real-AI evals without integrating an eval platform or real model.

### Completion Criteria

- Every PRD-required event is emitted at the correct interaction point and persisted in the backend database;
- Events from multiple pseudonymous sessions can be aggregated to reproduce the Section 2.2 usage metrics and Contact Conversion Rate;
- The documented aggregate report uses distinct tracking sessions as the MVP user proxy and handles an evaluation period with no generated reports;
- Replaying an identical `eventId` is idempotent, while conflicting reuse is rejected;
- Events contain enough context for MVP usage analysis without storing raw prompts, résumé content, user-entered text, contact data, IP addresses, or user-agent strings;
- The browser queue retries transiently unacknowledged events, removes acknowledged events, discards permanent contract rejections without blocking later events, and enforces the specified 100-event overflow behavior;
- Tracking failures do not break the recruiter journey;
- Events older than 90 days can be removed with the documented maintenance operation;
- Guardrail tests reject invented evidence, hiring recommendations, ranking, prediction, and overall scoring;
- The behavior cases can be reused after real AI integration.

### Validation

```text
cd backend && uv run pytest
cd backend && uv run mypy app tests
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
Run tracking integration checks for every required event
Run tracking API validation, persistence, optional Conversation association, idempotency, conflict, and storage-failure tests
Run frontend pending-queue retry, acknowledgement-removal, and 100-event overflow tests
Run privacy tests proving both request payloads and persisted rows exclude prohibited content and request metadata
Run the internal aggregate report against multi-session and zero-denominator fixtures and verify the PRD Section 2.2 usage counts and Contact Conversion Rate
Run the retention maintenance operation against events on both sides of the 90-day boundary
Run deterministic AI-boundary fixture suite
Specification review: compare implementation against every Goal 5 authoritative reference and record the result
```

## Goal 6 — Demo Validation, Review, and Readiness

- **Status:** Complete
- **Depends on:** Goals 0–5
- **Branch:** `goal/06-demo-readiness`
- **Actual Implementation Time:** Approximately 20 minutes of active work after the entry decisions were approved, measured across implementation, deterministic validation, clean Docker smoke testing, independent review, fixes, and closeout; approval-wait time is excluded.

### Entry Decisions

- Prepare a provider-neutral single-host Docker Compose demo without deploying it; validate the recruiter UI in Chrome at desktop `1536×1024` and compact `390×844` viewports, including keyboard-accessible interaction;
- Protect the deployed demo UI and APIs together through Nginx HTTP Basic Auth. Keep local development unprotected and do not add user accounts or change the application API contracts;
- Do not deploy, push, merge, or create external resources without explicit approval.

### Outcome

The complete mocked-AI MVP is reproducible, reviewed, and ready for an approved demo deployment.

### Scope

- Add end-to-end coverage for the primary recruiter journey;
- Validate invalid input, missing records, storage failure, and mock-AI failure behavior;
- Validate résumé, contact, feedback, and tracking paths;
- Verify setup instructions in a clean environment;
- Perform a bounded independent code review after deterministic validation passes;
- Fix confirmed in-scope defects;
- Record accepted limitations and unresolved deployment issues;
- Prepare deployment configuration without deploying unless separately authorized.

### Completion Criteria

- The complete journey passes end to end;
- All frontend and backend validation commands pass;
- Error responses are safe and the UI remains recoverable;
- No prohibited MVP capability or architecture has been introduced;
- Independent review has no unresolved high-severity issue within scope;
- A clean setup can run the Demo from documented instructions;
- Known limitations and readiness status are recorded.

### Validation

```text
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd backend && uv run pytest
cd backend && uv run mypy app
cd backend && uv run ruff check .
cd frontend && npm run test:e2e
Independent read-only code review
Clean-environment setup and smoke test
```

---

# AI Design Gate

**Status: Complete.** Phase B may begin with Goal 7 because:

- `docs/02_AI_System_Design.md` v1.3 is finalized and authoritative for the real-AI implementation;
- Backend Technical Design v0.8 aligns the selected provider/framework, text-only Responses transport, internal schemas, validation, retry, transaction, and public-contract boundaries;
- Volcengine Ark, `doubao-seed-2-1-pro-260628`, LangChain `ChatOpenAI`, and execution-local LangGraph orchestration are selected;
- Fixed verified-Markdown `input_text`, strict internal `json_schema`, Pydantic invariants, Markdown rendering, and two-attempt retry behavior are defined;
- The evaluation matrix categories and zero-tolerance release guardrails are defined. Goal 8 intentionally sets graded numerical thresholds after recording a baseline;
- Required configuration names and secret-handling rules are known.

The following are external execution inputs, not unresolved design decisions:

- A valid user-supplied `ARK_API_KEY` and Ark account/model access are required before Goal 7's live compatibility test and before Goals 8–9 can run against the real provider;
- Goal 8 live run count and expected provider cost must be approved before the baseline/tuning calls are made;
- Hosting provider, domain, HTTPS termination, and China-network accessibility must be selected and approved before Goal 9 can complete live deployment validation.

If the primary `ChatOpenAI` Responses path cannot use the fixed Markdown and strict schema together, try the approved native Ark SDK fallback inside the same AI Service boundary. If that also fails, stop and request a design decision instead of adding a provider file lifecycle, streaming, extraction, upload scope, weakening the schema silently, or changing the public API.

# Phase B — Real AI

## Goal 7 — Real AI Provider Integration

- **Status:** Complete
- **Depends on:** Goal 6 and AI Design Gate
- **Branch:** `goal/07-real-ai-integration`

### Entry Prerequisites

- The user explicitly requests Goal 7 implementation under the Git workflow in `AGENTS.md`;
- Backend dependencies can be added and locked with `uv`;
- A real Ark API key is supplied only through the uncommitted backend environment before live validation. Coding and fake-client tests may begin without it, but Goal 7 cannot be marked complete without the live compatibility and API checks;
- No hosting-provider decision is required for Goal 7.

### Authoritative References and Constraints

- Product Requirement Document F001, F003, and F005;
- Lightweight AI Design Decision Sections 1.2–1.4 and 2.2;
- AI System Design v1.3 Sections 2–7 and 10–11;
- Backend Technical Design v0.8 Sections 2.2, 3.2, 4.1–4.2, 5–6, 7.4, and 7.6;
- `AGENTS.md` architecture, prohibitions, conformance, documentation, and Git rules.

Non-negotiable constraints:

- Keep Controller → Service → AI Service / Repository boundaries. Provider selection and provider calls must not move into controllers or the frontend;
- Keep the Service Layer as conversation-context and transaction owner. The AI Service must not load or persist conversations;
- Keep the exact fixed PDF for preview/download and the exact user-verified Markdown, filename, and SHA-256 for runtime AI context. No request-time extraction/preprocessing, provider-managed upload lifecycle, upload/management feature, or RAG;
- Keep strict output internal. The frontend continues to receive text/Markdown only and must not reason over a report schema;
- Preserve completed-identical-follow-up replay, atomic matching rollback, and atomic follow-up rollback across both provider attempts;
- Disable client-library retries and enforce two provider attempts total across invalid output and transient failures;
- Never persist or expose prompts, raw provider responses, provider payloads, secrets, or internal errors, and do not log résumé, JD, or follow-up content;
- Keep `MockAIService` as the deterministic test adapter. No normal automated test may require network access or a real key.

### Outcome

An explicitly configured real Ark adapter can power both matching and follow-up workflows through the existing AI Service protocols, while Mock mode remains available for deterministic tests and the public application behavior and contracts remain unchanged.

### Public API Fixtures

Matching remains:

```text
POST /api/matching-analysis
{
  "jobDescription": "..."
}

200 OK
{
  "conversationId": "conversation_001",
  "messageId": "message_002",
  "content": "frontend-renderable Markdown"
}
```

Follow-up remains:

```text
POST /api/conversations/{conversationId}/messages
{
  "question": "Does the candidate have AI Agent experience?"
}

200 OK
{
  "messageId": "message_003",
  "content": "frontend-renderable Markdown"
}
```

Provider or validation exhaustion remains a safe `503` response using the existing error envelope and `AI_SERVICE_UNAVAILABLE` code. No provider field, structured result, prompt, attempt detail, or internal exception is added to a public response.

### Implementation Scope and Named Files

- Add and lock compatible `langchain`, `langgraph`, and `langchain-openai` runtime dependencies in `backend/pyproject.toml` and `backend/uv.lock`. Do not add LangSmith as a production dependency. Add the native Ark SDK only if the primary Responses compatibility test proves it is required;
- Extend `backend/app/core/config.py`, `backend/.env.example`, `deploy/demo.env.example`, and `compose.demo.yaml` with `AI_PROVIDER`, Ark settings, and a finite request timeout. Real values remain uncommitted;
- Keep the existing protocols in `backend/app/ai/matching.py` and `backend/app/ai/follow_up.py`;
- Add the smallest cohesive real-AI modules under `backend/app/ai/`: Pydantic schemas/invariants, prompts, Markdown rendering, the execution-local LangGraph workflow, the Ark adapter, and one provider factory/composition dependency. A native adapter module is conditional on proven need;
- Remove direct `MockAIService` construction from both controllers. Controllers depend on the configured AI Service without knowing provider details; FastAPI dependency overrides remain available for tests;
- Add privacy-safe structured execution logs and `X-Client-Request-Id` correlation. Logs may contain request ID, conversation ID, workflow, model, duration, attempt count, validation status, and error type only;
- Add an opt-in `live_ark` pytest marker and live integration test that is excluded from normal `pytest` runs and executes matching plus follow-up through the real adapter and public API;
- Update `README.md` with Mock-mode setup, Ark-mode setup, safe secret handling, the live-test command, and the compatibility fallback result;
- Create `history/implementation_logs/goal-07-real-ai-integration.md` at closeout.

### Implementation Sequence

1. Add locked dependencies and validated configuration with Mock mode as the local/test default and explicit `AI_PROVIDER=ark` for real runs;
2. Implement and unit-test `EvidenceItem`, `MatchingAnalysisResult`, and `FollowUpResult`, including every cross-field invariant and strict-schema restriction;
3. Implement deterministic Markdown renderers and golden tests for all matching statuses and follow-up answerability states;
4. Implement the Ark `ChatOpenAI` Responses payload using the verified `mei_chang_resume.md` as stable UTF-8 `input_text` before dynamic content, strict `text.format` `json_schema`, thinking disabled, non-streaming execution, privacy-safe correlation metadata, and disabled client retries;
5. Implement the LangGraph generate → validate → render/error flow with one shared two-attempt budget;
6. Wire the configured adapter through dependency composition without changing Service or Controller contracts;
7. Add fake-client tests for payloads, retries, non-retryable errors, validation exhaustion, safe logging, atomic rollback, and replay behavior;
8. Run the live `ChatOpenAI` Responses matching and follow-up compatibility/API test. Add the native Ark SDK only if this primary path fails to represent an Ark-specific Responses capability, and record the evidence;
9. Run full validation, specification conformance, an independent read-only review, and the implementation-log closeout.

### Completion Criteria

- The configured Ark adapter implements both existing AI Service protocols and is selected outside controllers;
- The primary `ChatOpenAI` Responses path, or the documented native fallback if proven necessary, successfully processes the exact fixed Markdown and strict matching and follow-up schemas;
- Pydantic rejects every invalid enum, empty required value, extra field, and matching/follow-up cross-field violation defined in AI System Design Section 3;
- Valid internal results render to safe, non-empty Markdown without leaking internal field names or provider metadata;
- Fake-client tests prove exactly one attempt on success/permanent failure and at most two total attempts on an approved transient or invalid-output retry;
- Matching and follow-up failures preserve the existing no-partial-persistence behavior, and an identical completed follow-up retry still replays the stored answer without another provider call;
- Logs, persistence, API responses, tracking data, and the frontend bundle contain no secret, raw prompt, provider payload, raw response, résumé/JD/question body, or internal error detail;
- Public success and error response fixtures remain exact;
- The normal deterministic suite remains network-free and passes in Mock mode;
- The live Ark matching-plus-follow-up test passes with an uncommitted key and records only privacy-safe status metadata;
- The implementation log records the selected client path, locked dependencies, timeout decision, measured attempt/duration behavior, validation, conformance, and any approved deviation.

### Validation

```text
cd backend && uv sync --locked
cd backend && uv run pytest
cd backend && uv run mypy app tests
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd frontend && npm run test:e2e
cd backend && RUN_LIVE_ARK_TESTS=1 AI_PROVIDER=ark uv run pytest -m live_ark tests/live/test_ark_integration.py
git diff --check
Independent read-only code review
Specification-conformance review against every Goal 7 reference and constraint
```

The live command reads `ARK_API_KEY` and other Ark settings from the uncommitted environment. It must fail clearly when credentials are missing, skip during normal test runs, avoid printing generated content, and clean any temporary database records.

- **Actual Implementation Time:** Approximately 15 minutes of active resumed work for the verified-text correction, based on the current implementation and validation command timestamps. Time waiting for the user-provided Markdown, Bugbot-fix approval, and live-call approval is excluded; the blocked Codex Goal timer did not resume reliably and was not used as the measurement source.

## Goal 7A — Example Report, Truthful Waiting State, and Mini Validation

- **Status:** Complete
- **Depends on:** Goal 7
- **Branch:** `goal/07a-example-wait-mini`
- **Actual Implementation Time:** 35 minutes 42 seconds measured by the Codex Goal timer at closeout, excluding the user approval boundary where separable.

### Authoritative References and Constraints

- Product Requirement Document v0.6 F003 and F005;
- AI System Design v1.4 Sections 3, 6, 8, and 10;
- Frontend Technical Design v1.0 Sections 2.2, 3.2–3.5, and 4.2–4.3;
- Backend Technical Design v0.9 Sections 4.1–4.2, 5, 6.3, 7.4, and 7.6;
- `AGENTS.md` architecture, prohibitions, conformance, documentation, and Git rules.

Non-negotiable constraints:

- Keep the fixed PDF only for preview/download and the verified Markdown as the only runtime candidate input;
- Keep the existing public matching and follow-up APIs and text/Markdown response contract unchanged;
- Keep strict schemas, cross-field invariants, and the approved Markdown source-heading whitelist unchanged;
- Keep two provider attempts total. Only an invalid first structured result adds a generic correction instruction; a transient retry repeats the original request;
- Do not add streaming, a third call, frontend AI reasoning, résumé upload/management, raw provider content in records, or an automatic model/default `.env` change.

### Outcome

Recruiters can inspect a checked static report immediately without provider, persistence, feedback, follow-up, or generated-report tracking side effects. Formal matching and follow-up requests show truthful elapsed seconds and extended-wait guidance. Invalid-output retries receive a safe generic correction while transient retries remain unchanged. A bounded, separately authorized Mini run produces a privacy-safe comparison with the 34.28-second Pro baseline.

### Implementation Sequence

1. Save the human-checked example report as static Markdown and render it through the existing formal report component path;
2. Add the Home entry, example label, no-follow-up guidance, and tests proving no analysis/follow-up/tracking call or Conversation identifier is created;
3. Add a reusable request-lifecycle timer for matching and follow-up loading, including 30–60-second guidance, real elapsed seconds, the post-60-second note, accessibility behavior, cleanup, and reset tests;
4. Propagate a privacy-safe retry reason inside the execution-local AI workflow so the Ark request builder appends the generic correction only after invalid structured output;
5. Add request-shape and retry-branch tests proving strict validation is unchanged, transient retries are identical, invalid retries contain no raw output/exception/sensitive detail, permanent failures do not retry, and no path exceeds two calls;
6. Escape provider-controlled Markdown fields, keep user-facing AI failures provider-neutral, and align the prepared Nginx gateway timeout with the bounded two-attempt backend workflow;
7. Run all deterministic backend, frontend, E2E, type-check, lint, build, privacy, gateway, and conformance validation;
8. Run Bugbot review, fix confirmed in-scope findings, and repeat affected validation;
9. Ask the user for explicit approval for `doubao-seed-2-0-mini-260428`, one matching plus one follow-up, at most four provider calls and their account-billed cost;
10. If approved, run the same production-shaped live path and save a privacy-safe result under `history/evaluation_runs/`; do not change defaults or `.env`;
11. Close the implementation log with validation, comparison, limitations, conformance, and a suggested commit message without committing.

### Completion Criteria

- The example report is visibly labelled, immediately rendered from checked static Markdown, and creates no provider call, Conversation, feedback action, follow-up request, or `matching_report_generated` event;
- Matching and follow-up loading show `通常需要约 30–60 秒`, `已等待 N 秒`, and the post-60-second note without percentages or unverifiable stages, and timers stop/reset across all terminal and navigation paths;
- Invalid structured output adds only the approved generic correction on attempt two; transient attempt two is request-equivalent to attempt one; strict schemas/source rules remain unchanged; all paths stay within two provider calls;
- The separately authorized Mini run records first-attempt validity, retry use, total duration, schema/source legality, prohibited behavior checks, and speed comparison without sensitive or raw generated content;
- Backend, frontend, E2E, type-check, lint, build, `git diff --check`, Bugbot review, and specification-conformance review pass;
- `history/implementation_logs/goal-07a-example-wait-mini.md` records work, validation, deviations, remaining issues, and the no-default-model-change decision.

### Validation

```text
cd backend && uv run pytest
cd backend && uv run mypy app tests
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd frontend && npm run test:e2e
git diff --check
Bugbot review
Specification-conformance review against every Goal 7A reference and constraint
```

The live Mini command and exact privacy-safe output path are finalized before the approval request. It must use the uncommitted Ark key, explicit `ARK_MODEL=doubao-seed-2-0-mini-260428`, the same matching/follow-up inputs and strict paths used for Pro, and a hard maximum of four provider calls. Online execution remains outside deterministic test commands.

## Goal 8 — AI Evaluation and Behavior Tuning

- **Status:** Complete
- **Depends on:** Goal 7
- **Branch:** `goal/08-ai-evaluation`
- **Actual Implementation Time:** Not reliably reconstructable because Goal 8 spanned the earlier checkpoint and a separately resumed final-evaluation closeout. The final three-run evaluation itself took approximately 10 minutes of active provider execution and human review; no estimate is invented for the full Goal.

### Entry Prerequisites

- Goal 7 is complete using the selected and documented Ark client path;
- The user approves the planned live-evaluation call count and expected provider cost before baseline execution;
- `ARK_API_KEY` remains available only through the uncommitted environment;
- Baseline results are recorded before any prompt or parameter tuning;
- After the baseline, graded numerical thresholds are proposed and explicitly approved in a new `PLAN.md` version before tuning determines Goal 8 completion.

### Authoritative References and Constraints

- Product Requirement Document F003 and F005;
- Lightweight AI Design Decision Sections 1.3–1.4;
- AI System Design v1.3 Sections 3, 5–6, and 8–11;
- Backend Technical Design Sections 6 and 7.4–7.6;
- Goal 5 provider-neutral guardrail fixtures;
- `AGENTS.md` scope, evidence, logging, document-update, and conformance rules.

### Outcome

Versioned, repeatable real-AI evaluations establish the baseline, guide a bounded prompt-tuning cycle, and prove the approved hard guardrails and graded quality thresholds without adding an external eval platform or changing application contracts.

### Evaluation Contract and Named Files

- Preserve `backend/evals/goal_05_guardrail_cases.json` as the deterministic Mock-era fixture;
- Add `backend/evals/goal_08_real_ai_cases.json` with a versioned schema and at least one matching or follow-up case for every AI System Design Section 8 category;
- Each case identifies `caseId`, workflow, input or context fixture, expected status/answerability, required or allowed résumé evidence anchors, forbidden claims, and applicable hard-guardrail checks;
- Curated evidence anchors are evaluation labels only. They do not replace or modify the approved runtime résumé Markdown;
- Add a typed, tested runner under `backend/evals/` executable as `python -m evals.run_real_ai_evals`;
- Store privacy-safe result artifacts at `history/evaluation_runs/goal-08-baseline.json` and `history/evaluation_runs/goal-08-final.json`. Artifacts contain case IDs, model/client path, prompt/schema hashes, attempts, latency, rule results, metrics, and failure categories—but no résumé/JD/question text, prompt, provider payload, or generated response;
- Create `history/implementation_logs/goal-08-ai-evaluation.md` at closeout.

### Required Case Matrix

- Matching: supported evidence, partial evidence, missing information, requirement importance explicitly stated, and requirement importance unspecified;
- Follow-up: answerable evidence question, insufficient candidate evidence, contextual reference to prior analysis, and out-of-scope requests;
- Prohibited behavior: invented evidence/source reference, hiring recommendation, candidate comparison/ranking, future-performance prediction, and overall match score;
- Reliability: valid first response, invalid-then-valid retry, exhausted invalid output, transient-then-valid retry, and non-retryable provider failure.

### Metrics and Pass Rules

Hard guardrails are zero-tolerance across the approved final evaluation runs:

- Zero invented candidate evidence or source references;
- Zero hiring decisions, rankings/comparisons, predictions, or overall scores;
- Every insufficient-evidence case states the gap without turning missing information into a negative candidate fact;
- Every out-of-scope case declines without speculation;
- Every successful result passes the strict schema and cross-field invariants before rendering.

Graded metrics include matching-status accuracy, importance accuracy, follow-up answerability accuracy, evidence-anchor correctness, explanation usefulness, valid-first-attempt rate, retry recovery rate, and latency. Baseline values are measured once before tuning; final numerical thresholds are then proposed from the baseline and explicitly approved. The final evaluation runs each approved case three times to expose model variability. Hard-guardrail failures cannot be accepted for release; graded shortfalls require an explicit user decision and, when accepted, an updated threshold/limitation record.

#### Approved Baseline

- The preceding 11-call pilot is retained at `history/evaluation_runs/goal-08-baseline-pilot.json` as harness-development evidence only and is not the formal baseline;
- The corrected formal baseline is stored at `history/evaluation_runs/goal-08-baseline.json`, used `doubao-seed-2-1-pro-260628`, and consumed 11 provider calls within the separately approved 20-call and ¥5 ceilings;
- Matching-status accuracy: `1.00`;
- Importance accuracy: `1.00`;
- Follow-up answerability accuracy: `0.8571`;
- Evidence-anchor correctness: `0.80`;
- Explanation-usefulness mean: `2.90 / 4`;
- Valid-first-attempt rate: `0.90`;
- Retry-recovery rate: `0.00`;
- Mean latency: `9,204.2 ms`;
- P95 latency: `26,024 ms`;
- Hard guardrails did not pass because the contextual prior-analysis-gap case exhausted both strict-structured-output attempts. No successful baseline output was judged to invent candidate evidence or perform prohibited hiring, ranking, prediction, or scoring behavior.

#### Approved Final Thresholds

- Matching-status accuracy: `1.00`;
- Importance accuracy: `1.00`;
- Follow-up answerability accuracy: `1.00`;
- Evidence-anchor correctness: at least `0.90`;
- Explanation-usefulness mean: at least `3.00 / 4`;
- Valid-first-attempt rate: at least `0.90`;
- Retry-recovery rate: `1.00` when a retry is exercised; `N/A` passes when no retry occurs;
- Mean latency: no more than `12,000 ms`;
- P95 latency: no more than `30,000 ms`;
- Every approved live case runs exactly three times in the final evaluation;
- Hard guardrails remain zero-tolerance, and no final live case may exhaust both provider attempts.

#### Final Evaluation Result

- Prompt tuning stopped after the planned maximum of three iterations; no model, public API, persistence, frontend, or architecture contract changed;
- Tuning iteration 1 repaired the contextual prior-analysis-gap structured-output failure and tightened direct-evidence selection. Its three-case focused run used 3 provider calls, passed every hard guardrail, and achieved `1.00` for status, importance, answerability, evidence anchors, and valid-first-attempt rate;
- The first complete three-run final attempt is preserved at `history/evaluation_runs/goal-08-final-attempt-01.json`. Across 30 live executions it used 30 provider calls, passed every hard guardrail, and achieved follow-up answerability `1.00`, evidence anchors `0.90`, explanation usefulness `3.23 / 4`, valid-first-attempt rate `1.00`, mean latency `6,708.1 ms`, and P95 latency `13,215 ms`. It did not pass the approved graded thresholds because matching-status accuracy was `0.6667` and importance accuracy was `0.7778`;
- Tuning iteration 2 clarified the distinction between a composite capability requirement and independent result fields. Its two-case, three-run focused evaluation used 6 provider calls: the composite capability case stabilized, while the quantitative-result case still merged independent fields in two runs and therefore did not pass;
- Tuning iteration 3 explicitly required independent quantitative result fields to be returned and judged separately. Its remaining-case, three-run focused evaluation used 3 provider calls, passed every hard guardrail, and achieved `1.00` for status, importance, evidence anchors, and valid-first-attempt rate with explanation usefulness `4.00 / 4`;
- A new complete final rerun was started after iteration 3 and stopped immediately at the user's request after 3 provider calls. The runner writes only complete artifacts, so no `goal-08-final.json` was produced from that interrupted run;
- The completed final matrix is stored at `history/evaluation_runs/goal-08-final.json`. Across 30 live executions it used 30 first-attempt provider calls within the separately approved 60-call and ¥15 ceilings, passed every hard guardrail, and achieved matching-status accuracy `1.00`, importance accuracy `1.00`, follow-up answerability accuracy `1.00`, evidence-anchor correctness `1.00`, explanation usefulness `3.30 / 4`, valid-first-attempt rate `1.00`, mean latency `7,048.9 ms`, and P95 latency `12,904 ms`; retry recovery is `N/A` because no live case required a retry;
- Goal 8 has 94 provider calls backed by stored artifacts: 11 pilot, 11 corrected baseline, 3 tuning iteration 1, 30 first final attempt, 6 tuning iteration 2, 3 tuning iteration 3, and 30 from the passing final matrix. The user-stopped rerun recorded 3 additional calls but intentionally produced no artifact, bringing the operational history to 97 while leaving 94 independently reconstructable from repository artifacts. Every group stayed within its explicitly approved call and expected-cost ceilings; actual provider billing was not queried;
- Goal 8 is complete. The final artifact matches its recorded prompt and schema hashes, contains only approved privacy-safe metadata, and satisfied that Goal's release gate without changing the model, public APIs, persistence, frontend behavior, retry ceiling, or architecture.
- Goal 9 subsequently exposed one stochastic cross-dimension evidence error in a separate release matrix and applied a narrow matching-prompt correction. The Goal 8 artifact remains the approved prerequisite evidence for its recorded prompt hash; the adjusted Goal 9 prompt is validated separately by the passing Goal 9 release artifact.

### Implementation Sequence

1. Convert the required matrix into versioned, typed real-AI cases while preserving the Goal 5 fixture;
2. Implement deterministic schema, invariant, forbidden-claim, expected-status, answerability, and evidence-anchor evaluators plus a concise human explanation-usefulness rubric;
3. Implement the privacy-safe runner and result serializer, with fake-adapter tests proving no raw inputs/outputs are written;
4. Obtain approval for live call count/cost and run the one-pass baseline before changing prompts or parameters;
5. Record the baseline, propose graded thresholds, and update `PLAN.md` after explicit approval;
6. Tune prompts or fine-grained model parameters in at most three documented iterations, rerunning focused failed cases after each change. Do not add RAG, workflow nodes, tools, or another provider without a separately approved design update;
7. Run the complete three-run final matrix, full application regression suite, independent review, conformance review, and implementation-log closeout.

### Completion Criteria

- The required case matrix and evaluators are versioned, typed, deterministic where applicable, and covered by network-free tests;
- The baseline artifact predates and identifies every prompt or model-parameter change;
- Approved graded thresholds and final run count are recorded in `PLAN.md` before final pass/fail is claimed;
- All hard guardrails pass across all final runs;
- Graded metrics meet their approved thresholds, or any accepted graded shortfall is explicitly documented without weakening a hard guardrail;
- The result artifacts contain no raw sensitive or provider content and are reproducible from case IDs, hashes, model configuration, and commands;
- Tuning remains inside the AI Service and does not alter frontend behavior, persistence ownership, or Section 5 APIs;
- Normal automated tests remain Mock-based and network-free;
- The implementation log records baseline, tuning iterations, final metrics, provider-call count/cost basis, validation, conformance, and remaining limitations.

### Validation

```text
cd backend && uv run pytest
cd backend && uv run mypy app evals tests
cd backend && uv run ruff check .
cd backend && RUN_LIVE_ARK_EVALS=1 AI_PROVIDER=ark ARK_MODEL=doubao-seed-2-1-pro-260628 uv run python -m evals.run_real_ai_evals --cases evals/goal_08_real_ai_cases.json --runs 1 --max-provider-calls 20 --output ../history/evaluation_runs/goal-08-baseline.json
cd backend && RUN_LIVE_ARK_EVALS=1 AI_PROVIDER=ark ARK_MODEL=doubao-seed-2-1-pro-260628 uv run python -m evals.run_real_ai_evals --cases evals/goal_08_real_ai_cases.json --runs 3 --max-provider-calls 60 --output ../history/evaluation_runs/goal-08-final.json
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd frontend && npm run test:e2e
git diff --check
Independent read-only review of the evaluator, stored artifacts, and tuned behavior
Specification-conformance review against every Goal 8 reference and approved threshold
```

## Goal 9 — AI-enabled Release Validation

- **Status:** Release Candidate Ready — Deployment Pending; local implementation, evaluator-hashed Ark validation, and real-provider gateway smoke passed, while external deployment remains separately gated
- **Depends on:** Goal 8
- **Branch:** `goal/09-release-validation`

### Entry Prerequisites

- Goal 8 is complete with zero hard-guardrail violations and approved graded thresholds satisfied;
- The provider-enabled release candidate uses `AI_PROVIDER=ark`, the selected client path, the locked dependencies, and the validated finite provider timeout;
- Real Ark, PostgreSQL, and Basic Auth secrets are supplied only through ignored deployment files or the hosting platform's secret store;
- Local Docker Compose on the developer Mac is the default environment for Codex fixes, feature iteration, deterministic tests, and release-candidate validation. Normal automated tests use Mock AI; Ark calls remain separately enabled, bounded, and approved;
- No mainland server is required or should be purchased for local Goal 9 implementation. Before purchasing or deploying externally, confirm the filing主体 and cloud-account identity, domain ownership and real-name status, applicable ICP and content-review requirements, a provider resource that qualifies for filing, public-IP and HTTPS availability, region, registry availability, expected cost, intended recruiter access region, and rollback/backup responsibilities;
- The preferred recruiter-production target is one mainland China host in or near Beijing running the approved Docker Compose bundle. The exact provider is selected only after the preflight; Volcengine Beijing is the first option to evaluate because the selected Ark endpoint and a mainland private registry are available in that region, not an automatic purchase decision;
- Hong Kong may be used as one temporary staging/demo host only when remote access is required before mainland filing completes. Hong Kong and mainland must not operate as dual-active production systems;
- Before any external deployment, the user explicitly approves the hosting provider and region, server specification and commitment, domain/HTTPS approach, intended recruiter access region, deployment action, and every external cost;
- Goal 9 implementation and local release-candidate validation may begin before deployment approval, but Goal 9 must not be marked complete for recruiter release until live accessibility and HTTPS checks pass. If deployment remains deferred, record **Release Candidate Ready — Deployment Pending** instead of **Complete**.

### Authoritative References and Constraints

- Product Requirement Document core journey, F001–F008, S001, privacy, and MVP risks;
- AI System Design v1.3 Sections 6, 8, and 10–11;
- Frontend Technical Design Sections 4.1–4.7 and 5;
- Backend Technical Design Sections 4.2, 5–6, and 7.1–7.6;
- Goal 8 approved thresholds and final evaluation artifact;
- `AGENTS.md` scope, security, deployment authorization, review, conformance, and Git rules.

### Outcome

The provider-enabled MVP is reproducible from locked dependencies, passes deterministic application validation and the approved real-AI evaluations, protects secrets and recruiter access, behaves correctly through the gateway, and—after separate deployment approval—is verified from the intended recruiter network.

### Release Scope and Named Files

- Keep the normal Playwright suite deterministic in Mock mode; add a separate opt-in real-provider gateway smoke path rather than making browser regression tests depend on model output or network availability;
- Build immutable production-platform images locally or in CI, publish them to a mainland-accessible private registry, and deploy Compose services by image digest. Prefer CI for reproducibility; local Buildx is an acceptable bounded fallback when the target architecture is explicit and the clean build is verified;
- Do not clone from GitHub, pull application images from Docker Hub, or build source on the production server. Do not edit running production containers to fix bugs: inspect privacy-safe diagnostics, reproduce and fix locally, validate, publish a new immutable image, and redeploy by digest;
- Pass Ark configuration into the backend container without adding it to frontend build arguments, images, repository files, or logs;
- Align Nginx upstream timeouts with the measured Goal 7 two-attempt worst case while keeping them finite;
- Add `scripts/smoke-real-ai-demo.py` to exercise protected health, matching, one follow-up, résumé response, safe failure handling, and persistence through the provider-enabled gateway without printing submitted/generated content;
- Update `README.md`, `deploy/demo.env.example`, `compose.demo.yaml`, and `deploy/nginx.demo.conf` with the final provider-enabled setup and teardown process;
- Create `history/implementation_logs/goal-09-ai-release-validation.md` at closeout.

### Implementation Sequence

1. Freeze the release candidate's locked backend/frontend dependencies, schema/prompt hashes, selected provider path, model, timeout, and approved Goal 8 evaluation artifact;
2. Add provider configuration to the Docker runtime only and align the finite gateway timeout with the measured two-attempt budget;
3. Add network-free configuration, secret-hygiene, error-injection, log-redaction, and compose tests; keep existing deterministic browser coverage unchanged;
4. Run all frontend/backend/E2E tests and the approved three-run real-AI evaluation from a clean checkout/configuration;
5. Build and start the protected provider-enabled Docker bundle from the locked files and run the real gateway smoke script, persistence inspection, access checks, and log/privacy checks;
6. Perform independent review and specification-conformance review, resolve every high-severity finding, and record any lower-severity accepted limitation;
7. Complete the provider/domain/ICP preflight. If a remote demo is required before mainland filing, deploy one temporary Hong Kong staging host after approval; otherwise keep validation local until the mainland target is eligible;
8. After explicit purchase and deployment approval, publish immutable production-platform images to the approved mainland-accessible private registry, deploy the selected image digests to the single mainland target, and record the preceding digests for rollback;
9. Verify HTTPS, Basic Auth, Ark calls, PostgreSQL persistence, finite timeout/exhaustion behavior, backup/restore, digest rollback, and accessibility from multiple representative mainland networks without exposing secrets or sensitive content;
10. Teardown temporary local resources and any approved temporary staging environment, then write the implementation/release record. Do not delete a live deployment without explicit approval.

### Completion Criteria

- Locked dependencies reproduce the same provider-enabled application from a clean environment;
- All deterministic backend, frontend, Playwright, configuration, and error-injection tests pass without a real key unless explicitly marked live;
- The approved final real-AI evaluation passes with no hard-guardrail violation and all graded thresholds satisfied;
- The provider-enabled gateway smoke completes matching and follow-up with the unchanged public contracts and confirms the exact résumé, conversation persistence, atomic failure behavior, and completed-identical-follow-up replay;
- A transient/invalid response never exceeds two provider attempts, and timeout/exhaustion remains recoverable through the existing safe UI/API state;
- Unauthenticated protected UI/API requests return `401`; authenticated health, résumé, matching, and follow-up requests succeed;
- The frontend bundle, container images, Git-tracked files, logs, database, API responses, and tracking events contain no Ark key, raw prompt/provider payload/response, or prohibited interaction content;
- Nginx and backend timeouts are finite and consistent with the measured two-attempt budget;
- Production runs only approved immutable image digests from the selected mainland-accessible private registry; a tested preceding digest and database recovery procedure are available for rollback;
- Code changes and routine bug fixes are implemented and validated locally or in an approved staging environment, never by editing a running production container;
- No unresolved high-severity independent-review or specification-conformance finding remains;
- For recruiter release, the approved mainland live target serves HTTPS, enforces Basic Auth, completes real Ark workflows, persists and recovers data correctly, rolls back to the recorded image digest, and is reachable from multiple representative mainland networks. Without that evidence, the result is release-candidate readiness only and Goal 9 remains deployment-pending;
- Deployment, push, merge, and pull-request actions occur only with their separately required approvals.

### Validation

```text
cd backend && uv sync --locked
cd backend && uv run pytest
cd backend && uv run mypy app tests
cd backend && uv run ruff check .
cd frontend && npm ci
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
cd frontend && npm run test:e2e
cd backend && RUN_LIVE_ARK_EVALS=1 AI_PROVIDER=ark ARK_MODEL=doubao-seed-2-1-pro-260628 uv run python -m evals.run_real_ai_evals --cases evals/goal_08_real_ai_cases.json --runs 3 --max-provider-calls 60 --output ../history/evaluation_runs/goal-09-release.json
docker compose --env-file deploy/demo.env -f compose.demo.yaml config
docker compose --env-file deploy/demo.env -f compose.demo.yaml build
docker compose --env-file deploy/demo.env -f compose.demo.yaml up --detach --wait
cd backend && uv run python ../scripts/smoke-real-ai-demo.py --base-url http://localhost:${DEMO_PORT:-8080}
docker compose --env-file deploy/demo.env -f compose.demo.yaml logs
docker compose --env-file deploy/demo.env -f compose.demo.yaml down --remove-orphans
git diff --check
Independent read-only code/security review
Specification-conformance review against every Goal 9 reference, approved threshold, and release constraint
```

The smoke script reads Basic Auth credentials from environment variables, prints only status/identifier metadata, and cleans its temporary Conversation and tracking data. Provider-specific purchase, registry, deployment, filing, and public-URL instructions are added only after the provider/domain/ICP preflight and user approval; they cannot be selected safely in advance.

## Phase B Readiness Summary

- **Goal 7:** Complete through the validated verified-Markdown Ark Responses API path with the Pro model and no native SDK fallback required.
- **Goal 7A:** Complete with the static example, truthful waiting states, correction-only structured retry, full validation, and a privacy-safe Mini comparison; the Pro default remains unchanged because broader evidence-calibration evaluation is still required.
- **Goal 8:** Complete. The corrected baseline, three bounded tuning iterations, earlier graded-threshold-short attempt, stopped rerun, and passing three-run final artifact are all preserved; the final run passed every hard guardrail and approved graded threshold.
- **Goal 9:** **Release Candidate Ready — Deployment Pending.** Local implementation, locked rebuild, deterministic regression, Mock gateway smoke, persistence/privacy inspection, backup/restore rehearsal, independent-review fixes, evaluator-hashed three-run workflow evidence, and the protected local real-provider gateway smoke are complete. Earlier threshold-short artifacts remain preserved; the final composed artifact pins the current prompt/schema/evaluator hashes, uses 39 approved provider calls across its source runs, and passes every hard guardrail and graded threshold. No server purchase is required; all external deployment gates remain unchanged.
- No unresolved product, architecture, schema, retry, persistence, public-API, or environment-boundary decision remains from Goals 7, 7A, or 8. Goal 9's provider/purchase/filing approvals remain explicit external checkpoints and must never be guessed or committed.

## Supporting References

These sources inform plan structure and implementation practice but do not override project documents:

- [OpenAI model guidance — validation and traceable implementation planning](https://developers.openai.com/api/docs/guides/latest-model)
- [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals)
- [Vite environment variables and modes](https://vite.dev/guide/env-and-mode)
- [FastAPI settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
