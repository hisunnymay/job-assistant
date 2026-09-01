# Feedback Reason for Long Report Generation

## Completed change

- Added “报告生成时间较长” as a predefined Not Helpful reason in the existing rating-specific feedback dialog.
- Added component coverage confirming that the new option is rendered for rating 1.

## Validation and conformance

- `cd frontend && npm test -- --run src/App.test.tsx` — 27 focused App tests passed.
- `cd frontend && npm test` — 11 files and 65 tests passed.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; 190 modules transformed.
- `git diff --check` — passed.
- The change remains frontend-only and uses the existing feedback serialization and API contract.
- No product capability, persistence behavior, tracking payload, provider behavior, or finalized document changed.
