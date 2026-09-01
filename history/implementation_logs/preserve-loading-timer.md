# Preserve In-Flight Loading Time Across Navigation

## Completed Fix

- Moved matching and follow-up request start timestamps to the conversation-owning `App` state.
- Changed `LoadingStatus` to derive elapsed time from the request timestamp, so remounting the visible status does not reset the clock.
- Kept the display interval scoped to the mounted loading component; navigating away still removes the hidden interval.
- Updated Frontend Technical Design v1.5 and replaced the previous reset expectation with component, application, and browser regression coverage.

## Validation

- `cd frontend && npm run test` — 68 tests passed.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed after replacing a synchronous effect update with render-time elapsed derivation.
- `cd frontend && npm run build` — passed.
- `cd frontend && npm run test:e2e -- e2e/errors.spec.ts` — 4 Mock-only desktop Chromium tests passed, including sidebar navigation during an active matching request.
- `git diff --check` — passed.

## Conformance

- Matches Frontend Technical Design Section 4.2: the same in-flight request retains truthful wall-clock elapsed time across workspace navigation, while success, failure, and retry boundaries retain separate lifecycles.
- Preserves the approved synchronous request-response UI, accessibility roles, frontend/backend contracts, persistence ownership, and AI Service boundary.
- No provider calls, deployment changes, API changes, or known deviations remain.
