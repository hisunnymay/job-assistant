# Dashboard Default Range

## Completed change

- Updated PRD v0.10 and Frontend Technical Design v1.2 to define the initial inclusive dashboard range as 2026-09-01 through the current `Asia/Shanghai` calendar date.
- Removed the “产品使用概览” kicker and its unused styling.
- Prefilled both date controls and automatically requested the approved initial range while preserving Reset as the all-retained-data path.
- Updated component and Playwright coverage for the default values, automatic request, removed copy, invalid-range preservation, Reset behavior, conversation preservation, test-session exclusion, and compact layout.

## Validation

- `cd frontend && npm test` — 11 files and 65 tests passed.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; 190 modules transformed.
- `cd frontend && npm run test:e2e` — 8 desktop/compact Chromium journeys passed with Mock AI and the isolated test database.
- `git diff --check` — passed.

## Problems and conformance

- Corrected the retry-range state type so Reset can continue issuing the approved date-less all-retained request.
- Cleared one stale E2E Uvicorn process on port 8010 before the successful browser run; the live backend on port 8000 was not changed.
- Conformance passed: the backend API contract, inclusive `Asia/Shanghai` semantics, shared reporting period, aggregate-only rendering, test-session exclusion, conversation preservation, and Reset-to-all-retained behavior remain unchanged.
- No provider calls, deployment, commit, push, or production changes were made. The completed Goal 10 section in `planning/PLAN.md` still records its original all-retained initial default as historical completion criteria; current PRD v0.10 and Frontend Technical Design v1.2 supersede that earlier behavior.
