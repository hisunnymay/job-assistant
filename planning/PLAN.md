# AI Job Fit Assistant — Implementation Plan

## Document Information

- **Version:** v0.2
- **Status:** Draft — Pending Pre-implementation Decisions
- **Owner:** Mei Chang
- **Last Updated:** 2026-08-25
- **Purpose:** Define implementation order, Goal scope, completion criteria, dependencies, and validation for Codex.

## Version Log

- **v0.2 — 2026-08-25:** Clarified that this is a living plan that can evolve with implementation and that the user only needs to review one Goal at a time.
- **v0.1 — 2026-08-25:** Created the initial phased implementation plan. Pre-implementation technology and validation choices remain intentionally unresolved.

## 1. Authority and Use

This plan is subordinate to:

1. `docs/01_Product_Requirement_Document.md`;
2. `docs/03_Lightweight_AI_Design_Decision.md`;
3. `docs/04_Frontend_Technical_Design.md`;
4. `docs/05_Backend_Technical_Design.md`;
5. `AGENTS.md`.

This file owns Goal order, dependencies, completion criteria, validation commands, and status. It does not change approved scope, architecture boundaries, AI behavior, or API contracts.

Codex should implement only the Goal explicitly requested by the user. Branch, commit, documentation-update, and implementation-log rules are defined in `AGENTS.md` and are not repeated here.

## 2. How to Use This Plan

- This is a living implementation guide, not a fixed contract. It may change when real implementation reveals better task boundaries, dependencies, validation methods, or technical constraints.
- The user does not need to understand or approve the entire plan before implementation begins. Focus on one Goal at a time.
- Before starting a Goal, Codex should explain in plain language what will be built, why it is needed, what decisions require user input, and how completion will be checked.
- Future Goals may be clarified, split, combined, or reordered with the user's agreement. Update this file's Version Log when that happens.
- Plan changes must not silently override the PRD, finalized design documents, `AGENTS.md`, or agreed API contracts. Changes to those contracts must follow their document-update rules.
- Do not rewrite completed Goals to hide what happened. Record implementation results in the corresponding implementation log and add follow-up work explicitly when needed.

## 3. Plan Status

- **Phase A — Demo with Mock AI:** Planned
- **AI Design Gate:** Not ready; `docs/02_AI_System_Design.md` has not been created or finalized.
- **Phase B — Real AI:** Deferred until the AI Design Gate is complete.
- **Current coding readiness:** Not ready; the Pre-implementation Decisions below remain open.

## 4. Pre-implementation Decisions — Pending

These are decisions, not a coding Goal. Resolve them through discussion before starting Goal 0.

- Frontend package manager;
- Python project and dependency manager;
- MVP database technology;
- Frontend and backend environment-variable conventions;
- Frontend test, type-check, and lint tools;
- Backend test, type-check, and lint tools;
- End-to-end test tool;
- Candidate résumé PDF filename and repository location.

Already finalized:

- Frontend: React + TypeScript + Vite;
- Backend: Python + FastAPI;
- Demo AI: deterministic mock behind the AI Service boundary;
- Real AI provider/framework: deliberately deferred until the AI System Design is approved.

### Validation Placeholders

Until the decisions above are resolved, this plan uses:

- `<FE_PM>` — selected frontend package manager command;
- `<PY_RUN>` — selected Python environment runner;
- `<FE_TEST>` — frontend test command;
- `<FE_TYPECHECK>` — frontend type-check command;
- `<FE_LINT>` — frontend lint command;
- `<BE_TEST>` — backend test command;
- `<BE_TYPECHECK>` — backend type-check command;
- `<BE_LINT>` — backend lint command;
- `<E2E_TEST>` — end-to-end test command.

After the decisions are resolved, update this plan to replace the placeholders with exact runnable commands before Goal 0 implementation begins.

---

# Phase A — Demo with Mock AI

## Goal 0 — Project Scaffold and Validation Baseline

- **Status:** Not started
- **Depends on:** Pre-implementation Decisions
- **Branch:** `goal/00-project-scaffold`

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
- Every validation placeholder in this file is replaced with an exact command.

### Validation

```text
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_LINT>
cd frontend && <FE_PM> run build
cd backend && <BE_TEST>
cd backend && <BE_TYPECHECK>
cd backend && <BE_LINT>
```

## Goal 1 — Frontend Matching Journey with Mock Data

- **Status:** Not started
- **Depends on:** Goal 0
- **Branch:** `goal/01-frontend-matching-journey`

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
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_LINT>
cd frontend && <FE_PM> run build
Manual browser check: initial, invalid, loading, success, and failure states
```

## Goal 2 — Integrated Matching Vertical Slice with Mock AI Service

- **Status:** Not started
- **Depends on:** Goal 1
- **Branch:** `goal/02-matching-vertical-slice`

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
cd backend && <BE_TEST>
cd backend && <BE_TYPECHECK>
cd backend && <BE_LINT>
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_PM> run build
Contract smoke test: POST /api/matching-analysis
```

## Goal 3 — Follow-up Workflow and Persisted Conversation Context

- **Status:** Not started
- **Depends on:** Goal 2
- **Branch:** `goal/03-follow-up-context`

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
cd backend && <BE_TEST>
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_PM> run build
Conversation smoke test: matching analysis followed by multiple questions
```

## Goal 4 — Résumé, Contact, and Feedback Actions

- **Status:** Not started
- **Depends on:** Goal 2
- **Branch:** `goal/04-supporting-actions`

### Outcome

Recruiters can review/download the fixed résumé, access the candidate contact action, and submit feedback associated with a matching report.

### Scope

- Add the approved static candidate résumé PDF;
- Implement `GET /api/resume` returning `application/pdf`;
- Provide résumé preview and download from navigation and the report context;
- Use the same PDF resource intended for later AI context;
- Do not add backend PDF extraction, preprocessing, upload, or candidate management;
- Add the static contact CTA and recruiter-name greeting template;
- Do not automatically send a message;
- Implement `POST /api/feedback` and persist feedback against its conversation/message;
- Add clear success and error feedback in the UI.

### Completion Criteria

- The approved PDF can be previewed and downloaded;
- Preview/download uses the same unmodified static PDF resource;
- Contact information and greeting behavior are correct and do not send externally;
- Valid feedback is persisted against the correct report context;
- Invalid feedback returns the agreed safe error format;
- Independent navigation to résumé and contact actions works.

### Validation

```text
cd backend && <BE_TEST>
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_PM> run build
File smoke test: GET /api/resume returns the expected PDF
Feedback smoke test: POST /api/feedback persists the expected record
Manual browser check: preview, download, contact, and feedback
```

## Goal 5 — Product Tracking and Deterministic AI Guardrails

- **Status:** Not started
- **Depends on:** Goals 3 and 4
- **Branch:** `goal/05-tracking-and-guardrails`

### Entry Decision

Choose the MVP tracking implementation before coding this Goal. If the choice adds or changes a backend API, request approval and update Backend Technical Design Section 5 and corresponding frontend assumptions before implementation.

### Outcome

The Demo records the required product events and has repeatable checks for the AI behavior boundaries that can be tested without a real provider.

### Scope

- Track page visit, job-description submission, résumé preview, contact CTA, and feedback submission;
- Keep tracking session identity separate from Conversation identity;
- Associate events with the relevant session and conversation when available;
- Avoid sensitive content in event payloads;
- Add deterministic fixtures/checks for supported evidence, partial information, missing information, out-of-scope questions, and unsupported scoring;
- Prepare reusable behavior cases for later real-AI evals without integrating an eval platform or real model.

### Completion Criteria

- Every PRD-required event is emitted once at the correct interaction point;
- Events contain enough context for MVP usage analysis without storing raw prompts or résumé content;
- Tracking failures do not break the recruiter journey;
- Guardrail tests reject invented evidence, hiring recommendations, ranking, prediction, and overall scoring;
- The behavior cases can be reused after real AI integration.

### Validation

```text
cd backend && <BE_TEST>
cd frontend && <FE_TEST>
Run tracking integration checks for every required event
Run deterministic AI-boundary fixture suite
```

## Goal 6 — Demo Validation, Review, and Readiness

- **Status:** Not started
- **Depends on:** Goals 0–5
- **Branch:** `goal/06-demo-readiness`

### Entry Decisions

- Confirm the Demo hosting target and accessibility needs;
- Confirm the required API access-protection mechanism;
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
cd frontend && <FE_TEST>
cd frontend && <FE_TYPECHECK>
cd frontend && <FE_LINT>
cd frontend && <FE_PM> run build
cd backend && <BE_TEST>
cd backend && <BE_TYPECHECK>
cd backend && <BE_LINT>
<E2E_TEST>
Independent read-only code review
Clean-environment setup and smoke test
```

---

# AI Design Gate

Phase B must not begin until all of the following are approved:

- `docs/02_AI_System_Design.md` is created and finalized;
- AI provider/framework and supported PDF-input approach are selected;
- Prompt/context strategy and supported-scope behavior are defined;
- AI response-validation and limited retry behavior are defined;
- Representative AI-evaluation cases and pass criteria are defined;
- Required provider secrets and deployment constraints are known.

If the chosen provider cannot use the static PDF through the AI Service boundary without backend extraction, stop and request a design decision instead of adding extraction silently.

# Phase B — Real AI

## Goal 7 — Real AI Provider Integration

- **Status:** Deferred
- **Depends on:** Goal 6 and AI Design Gate
- **Branch:** `goal/07-real-ai-integration`

### Outcome

The real AI adapter replaces the mock without changing frontend behavior, backend business workflows, persistence ownership, or agreed API contracts.

### Completion Criteria

- The provider is called only through the AI Service;
- The static PDF is supplied using the approved provider-supported approach;
- Matching and follow-up flows use the backend-prepared context;
- Secrets remain backend-only;
- Raw prompts and provider-specific payloads are not persisted or exposed;
- Provider failure and invalid output produce safe application errors;
- Existing deterministic tests still pass.

### Validation

Exact commands and provider smoke tests will be added after the AI System Design is approved.

## Goal 8 — AI Evaluation and Behavior Tuning

- **Status:** Deferred
- **Depends on:** Goal 7
- **Branch:** `goal/08-ai-evaluation`

### Outcome

Representative matching and follow-up cases measure whether the real AI remains grounded, handles unknowns correctly, respects supported scope, and avoids unsupported scoring or decisions.

### Completion Criteria

- The eval set contains representative job descriptions and follow-up questions;
- Evaluation criteria cover evidence grounding, partial/missing information, scope control, and prohibited conclusions;
- Baseline results are recorded before tuning;
- Approved pass criteria are met or remaining failures are explicitly accepted;
- Prompt or behavior changes do not alter public API contracts.

### Validation

Exact eval commands and pass thresholds will be added after the AI System Design is approved.

## Goal 9 — AI-enabled Release Validation

- **Status:** Deferred
- **Depends on:** Goal 8
- **Branch:** `goal/09-release-validation`

### Outcome

The AI-enabled MVP passes application validation, AI evals, independent review, and approved deployment checks.

### Completion Criteria

- Deterministic tests, end-to-end tests, and AI evals pass the approved thresholds;
- Real-provider error and timeout behavior is recoverable;
- Access protection and secret configuration are verified;
- Deployment accessibility is checked for the intended users;
- No unresolved high-severity review issue remains;
- Deployment occurs only after explicit user approval.

### Validation

Exact release and deployment checks will be added after the provider and hosting decisions are approved.

## Supporting References

These sources inform plan structure and implementation practice but do not override project documents:

- [OpenAI model guidance — validation and traceable implementation planning](https://developers.openai.com/api/docs/guides/latest-model)
- [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals)
- [Vite environment variables and modes](https://vite.dev/guide/env-and-mode)
- [FastAPI settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
