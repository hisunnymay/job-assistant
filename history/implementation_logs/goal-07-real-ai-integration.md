# Goal 7 — Real AI Provider Integration

## Version Log

- **v1.2 — 2026-08-27:** Closed the verified-text correction after Pro matching/follow-up live validation, final regression/privacy checks, Bugbot fixes, and conformance review.
- **v1.1 — 2026-08-27:** Reopened the record for the approved user-verified Markdown runtime correction, integrity/reference guardrails, current offline validation, and final Bugbot findings; Pro live validation remains pending its separate cost approval.
- **v1.0 — 2026-08-27:** Recorded the completed Ark Responses API integration, provider-path correction, live compatibility evidence, Bugbot fixes, validation, and conformance result.

## Completed Scope

- Added validated Mock/Ark provider selection while keeping Mock mode as the local and normal-test default.
- Added the real `ArkAIService` behind both existing matching and follow-up AI Service protocols without changing Controller, Service, Repository, persistence, or public API contracts.
- Added strict Pydantic matching/follow-up schemas and cross-field invariants, deterministic Chinese Markdown rendering, privacy-safe prompts, and an execution-local LangGraph generate → validate → render/error workflow.
- Enforced one shared budget of two provider attempts, disabled client-library retries, classified transient and permanent provider failures, and made Responses safety refusals non-retryable.
- Retained the exact fixed PDF for recruiter preview/download and moved the user-supplied, user-verified Markdown unchanged to `backend/app/resources/resume/mei_chang_resume.md` for runtime AI context.
- Verify the fixed Markdown filename and SHA-256 before every provider execution, and reject a modified or renamed resource before any provider call.
- Send the verified UTF-8 résumé text before dynamic JD or conversation content through LangChain `ChatOpenAI(use_responses_api=True)`; all provider input is `input_text`, strict structured output remains in `text.format`, thinking is disabled, and execution remains non-streaming.
- Restrict `sourceReference` to the exact visible section, company, project, and education headings in the approved Markdown. Fabricated PDF page locators and non-existent headings fail structured validation and consume only the existing bounded retry budget.
- Added `X-Client-Request-Id` correlation and privacy-safe execution metadata without logging or persisting input, prompt, payload, raw response, secret, or internal exception details.
- Preserved atomic matching/follow-up rollback and completed-identical-follow-up replay through the real adapter.
- Added the opt-in real-provider public-API test and kept all ordinary tests deterministic and network-free.
- Updated `AGENTS.md` v0.6, AI System Design v1.3, Backend Technical Design v0.8, PLAN v0.30, configuration examples, Docker demo environment, README, and a sanitized provider research record.

## Material Files

- AI implementation: `backend/app/ai/ark.py`, `dependencies.py`, `prompts.py`, `rendering.py`, `schemas.py`, and `workflow.py`.
- Fixed candidate resources: `backend/app/resources/resume/mei_chang_resume.pdf`, `mei_chang_resume.md`, and `backend/app/resources/candidate_resume.py`.
- Composition/configuration: both AI controllers, `backend/app/core/config.py`, backend/deployment environment examples, and `compose.demo.yaml`.
- Tests: `backend/tests/test_ai_schemas.py`, `test_ai_rendering.py`, `test_ark_ai_service.py`, `test_ark_api_integration.py`, configuration/API regression tests, and `backend/tests/live/test_ark_integration.py`.
- Dependencies: `backend/pyproject.toml` and `backend/uv.lock`.
- Documentation: `README.md`, `docs/02_AI_System_Design.md`, `docs/05_Backend_Technical_Design.md`, `planning/PLAN.md`, and `history/provider_research/ark-responses-api.md`.

## Provider Path and Timeout Evidence

- Selected client path: LangChain `ChatOpenAI` 1.6 through Ark's OpenAI-compatible Responses API; no native Ark SDK dependency was required.
- Locked direct dependencies: `langchain` 1.3.17, `langchain-openai` 1.6.0, and `langgraph` 1.2.11. LangSmith was not added as a direct production dependency.
- Client retries are disabled with `max_retries=0`; LangGraph permits at most two total provider attempts for approved transient or invalid-output conditions.
- The configured timeout remains finite at 180 seconds per provider attempt.
- Diagnostic Chat Completions calls with default thinking exhausted two 60-second and then two 180-second attempts for the production-shaped matching request. Isolated capability probes succeeded, which led to provider clarification that documented PDF input belongs on the Responses API.
- A temporary Chat Completions call with thinking disabled completed, but it was not accepted as completion evidence because that endpoint was not the documented PDF path.
- The earlier non-streaming Responses API live test completed matching plus follow-up through the unchanged public APIs in approximately 75 seconds total with the fixed PDF and production-shaped strict schemas. This is retained as historical transport evidence, not completion evidence for the corrected Markdown runtime path.
- The corrected non-streaming Pro-model live test completed matching plus follow-up through the unchanged public APIs in 34.28 seconds (35.91 seconds command wall time) with the fixed Markdown and production-shaped strict schemas. Both workflows succeeded on their first provider attempt: 2 actual provider calls out of the approved maximum of 4.
- Compared with the earlier approximately 75-second fixed-PDF matching-plus-follow-up run, the corrected text path was approximately 54% faster in this local test. This is one paired workflow observation, not a statistically stable latency benchmark.

## Validation

- `cd backend && uv sync --locked` — passed; 71 packages resolved and 66 checked from the lockfile.
- `cd backend && uv run pytest` — passed after the Markdown correction; 138 tests passed and the opt-in live test skipped normally.
- `cd backend && AI_PROVIDER=ark uv run pytest -m 'not live_ark'` — passed after the final source-reference cases; all 138 ordinary tests passed with real-provider configuration present and no Ark network call.
- `cd backend && uv run mypy app tests` — passed across 60 source files.
- `cd backend && uv run ruff check .` — passed.
- `cd frontend && npm run test` — passed, 7 files and 46 tests.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; Vite transformed 186 modules and produced the production bundle.
- `cd frontend && npm run test:e2e` — passed, 5 Playwright tests across desktop and compact Chromium projects. The first corrected run exposed that Playwright inherited the developer `.env` Ark mode; `AI_PROVIDER=mock` is now explicit in the isolated test server and the rerun passed 5/5.
- Corrected Markdown integrity tests verify the approved PDF/Markdown filenames and SHA-256 values, UTF-8 readability, exact visible-heading reference allowlist, rejection of modified/renamed Markdown before provider access, and stable-before-dynamic text-only transport.
- `cd backend && RUN_LIVE_ARK_TESTS=1 AI_PROVIDER=ark ARK_MODEL=doubao-seed-2-1-pro-260628 uv run pytest -m live_ark tests/live/test_ark_integration.py` — passed; matching and follow-up each returned HTTP 200 on the first attempt, 2 provider calls total, 34.28 seconds pytest duration, and no generated content printed.
- Exact PDF and Markdown SHA-256 verification, ignored `.env` verification, source-reference drift checks, privacy-safe live output, and `git diff --check` — passed. The real key was found in the ignored backend `.env`, exact-value scanning found zero copies elsewhere in deliverable files, the frontend bundle contained no Ark key/base-URL/model markers, and temporary PDF renders were removed.

## Independent Review

- Bugbot reported one P1 and two P2 findings in the initial Goal 7 implementation.
- Fixed the P1 test-isolation issue by overriding the shared provider dependency with `MockAIService` for every ordinary client test, even when `AI_PROVIDER=ark` is present.
- Fixed the first P2 strict-schema issue by rejecting snake_case aliases instead of allowing both field-name and camelCase input.
- Fixed the second P2 privacy issue by preventing live-test assertion introspection from exposing returned content in pytest failure output.
- The subsequent provider-path correction retained those fixes. Final protocol review additionally added Responses operation-URL rejection and non-retryable Responses refusal handling.
- The final verified-text Bugbot review found one P1: source references could still contain fabricated PDF locators. Fixed it by constraining the schema to the exact visible Markdown headings and adding drift and invalid-reference regression tests.
- The review also found this implementation record stale at P2; v1.1 corrects the runtime path, authority versions, validation status, and conformance claims.

## Specification-Conformance Review

- **Product scope:** Conforms to PRD F001, F003, and F005. The implementation analyzes only the fixed candidate, exposes evidence and information gaps, supports bounded follow-up, and adds no score, ranking, comparison, prediction, or hiring decision.
- **AI capability boundary:** Conforms to Lightweight AI Design Decision Sections 1.2–1.4 and 2.2 and AI System Design v1.3 Sections 2–7 and 10–11. Strict structured results remain internal and only validated Markdown reaches the public API.
- **Provider transport:** Offline implementation conforms to the approved v1.3 correction. The exact verified Markdown uses text-only Responses input before dynamic content; the paired PDF remains preview/download only. No Files API lifecycle, request-time extraction/preprocessing, upload feature, RAG, streaming, another model, or native fallback was added.
- **Architecture:** Conforms to Backend Technical Design v0.8. Controllers depend on shared provider composition, Services retain conversation/transaction ownership, the AI Service owns provider/schema/rendering behavior without persistence access, and repositories remain unchanged.
- **Reliability:** Conforms. Client retries are disabled, the application budget is bounded to two attempts, permanent failures and safety refusals stop after one attempt, invalid/transient cases may use one retry, rollback remains atomic, and identical completed follow-ups replay without a provider call.
- **Privacy and contracts:** Conforms. Secrets and raw AI content are absent from tracked files, logs, persistence, tracking, API errors, and the frontend bundle. Matching/follow-up success and safe `503` fixtures remain exact.
- **Validation:** Conforms. Normal tests remain Mock-based and network-free; the corrected fixed-Markdown matching-plus-follow-up gate passed with the Pro model and uncommitted key.
- **Result:** Goal 7 has no unresolved material specification mismatch.

## Problems Fixed and Remaining Known Issues

- Corrected the initial undocumented Chat Completions PDF path to the provider-documented Responses API after live timeout diagnostics and provider clarification.
- Fixed the migration-specific full-operation base-URL validation and Responses refusal classification.
- The finite 180-second provider timeout is validated for the current local Goal 7 environment; Goal 9 still owns alignment of deployment-gateway timeouts with the selected release environment.
- The fixed-Markdown Pro live compatibility test passed within the approved provider-call and cost authorization. Goal 8 still owns repeatable multi-case quality and latency evaluation.
- Ark provider availability, beta structured-output behavior, and account/model access remain external dependencies. Another environment should rerun the opt-in live compatibility test before release.
- The frontend test runner continues to emit the existing Node `--localstorage-file` warning; it does not fail or alter test results.

## Actual Implementation Time

Approximately 15 minutes of active resumed work for the verified-text correction, based on the current implementation and validation command timestamps. Time waiting for the user-provided Markdown, Bugbot-fix approval, and live-call approval is excluded; the blocked Codex Goal timer did not resume reliably and was not used as the measurement source.
