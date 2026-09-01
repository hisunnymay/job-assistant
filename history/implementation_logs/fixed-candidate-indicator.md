# Fixed Candidate Indicator

## Completed

- Added a persistent workspace indicator showing `当前候选人` and `梅唱`, aligned to the navigation's icon and text columns with a dedicated candidate-profile icon and an unframed information icon beside the candidate name.
- Added a keyboard-accessible information disclosure explaining that a later version will support résumé upload and candidate changes; it closes on a second click, outside pointer action, or `Escape`.
- Kept résumé upload and candidate switching outside the MVP; no inactive or misleading upload control was added.
- Updated Frontend Technical Design to v1.3 and added component and compact-browser coverage.

## Validation

- `npm test -- --run src/App.test.tsx` — 27 tests passed.
- `npm test -- --run src/components/CandidateContext.test.tsx` — 2 tests passed.
- `npm test` — 67 tests passed across 12 files.
- `npm run type-check` — passed.
- `npm run lint` — passed.
- `npm run build` — passed; Vite built 191 modules.
- `npm run test:e2e -- compact.spec.ts` — 1 compact Chromium test passed.
- `npm run test:e2e` — all 8 desktop and compact Chromium tests passed with `AI_PROVIDER=mock`.
- `git diff --check` — passed.

## Conformance

- The change makes the PRD's fixed-candidate limitation persistent across workspace views.
- The indicator and information disclosure introduce no candidate switching, résumé upload, API, persistence, or AI behavior.

## Problems Fixed

- Removed the `固定简历` badge after it compressed the candidate label, moved the unframed information icon beside `梅唱`, aligned the candidate content with the menu grid, and positioned the disclosure to the right on desktop while retaining a below-card compact fallback.

## Known Issues

- None identified during implementation.
