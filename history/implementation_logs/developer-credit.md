# Developer Credit

## Completed

- Added the subtle credit `产品设计与开发：梅唱` to the entrance page and the bottom of the workspace sidebar.
- Kept the workspace credit visually separate from `当前候选人：梅唱` so developer and candidate roles remain distinguishable.
- Added responsive placement beneath the navigation on narrower workspace layouts.
- Added component and browser coverage for the credit.

## Validation

- `npm test` — 67 tests passed across 12 files.
- `npm run type-check` — passed.
- `npm run lint` — passed.
- `npm run build` — passed; Vite built 191 modules.
- `npm run test:e2e` — all 8 desktop and compact Chromium tests passed with `AI_PROVIDER=mock`.
- `git diff --check` — passed.

## Conformance

- The change is presentation-only and introduces no workflow, API, persistence, analytics, or AI behavior.

## Known Issues

- None identified during implementation.
