# Dashboard Session Deduplication

## Completed

- Changed résumé-preview and Contact CTA dashboard values from accepted-event totals to distinct non-test session counts within the selected reporting period.
- Prevented already-active Résumé Preview and Contact Candidate navigation items from emitting repeat tracking events.
- Updated the dashboard labels and descriptions so the two session-based metrics are distinguishable from the four event-total metrics.
- Updated the PRD and frontend/backend technical design version logs and metric contracts.

## Validation

- Focused backend dashboard tests: 12 passed.
- Backend Ruff and mypy: passed.
- Full backend test suite: 188 passed and 1 skipped; one unrelated pre-existing release-manifest test failed because the locked runtime résumé hash does not match the current approved Markdown resource.
- Frontend tests: 67 passed.
- Frontend type-check, lint, and production build: passed; 191 modules transformed.
- Mock-provider browser tests: all 8 desktop and compact journeys passed, including repeat active-navigation and copy-action tracking assertions.

## Conformance

- Preserved the existing dashboard response shape, tracking payload contract, event ingestion, test-session exclusion, date filtering, and distinct-session conversion calculation.
- Copy actions remain untracked and do not affect the Contact CTA session metric.

## Known Issues

- The existing Contact Conversion Rate query requires generated-report and Contact CTA events in the same session and reporting period, but it does not currently enforce that the Contact CTA timestamp is later than the generated-report timestamp. The product definition and event boundary should be resolved before changing this separately governed metric.
