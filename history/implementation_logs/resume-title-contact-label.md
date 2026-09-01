# Resume Title and Contact Navigation Label

## Completed

- Changed the approved PDF's internal Title metadata from `梅唱 - AI 产品经理简历 - 模块标题底色版` to `mei_chang_resume.pdf`; the served filename remains `mei_chang_resume.pdf`.
- Updated the approved PDF SHA-256 and frontend cache-busting version after the metadata-only binary change.
- Changed the workspace navigation label from `联系候选人` to the selected four-character label `联系方式`; contact-page content and behavior are unchanged.
- Removed the redundant `联系方式` section heading beneath the page title `联系梅唱`; the email and phone cards now follow the page title directly.

## Validation

- `pdfinfo backend/app/resources/resume/mei_chang_resume.pdf` — Title is exactly `mei_chang_resume.pdf`; the PDF remains two unencrypted A4 pages.
- Rendered both pages before and after the metadata update at 120 DPI; corresponding PNG SHA-256 values are identical, and both final pages passed visual inspection.
- Final PDF SHA-256 is `30ebd7e42087fe6975ef7d4e067d88f2ab7a075844e370ccbddf14257c80fe79`.
- Focused backend résumé and release-smoke tests — 8 passed with `AI_PROVIDER=mock`.
- Frontend tests — 67 passed across 12 files; type-check, lint, and production build passed with 191 modules.
- Full Mock Playwright suite — 8 passed after one unrelated test-mode click timeout passed on isolated retry and on the clean full rerun.
- `git diff --check` — passed.

## Conformance

- The PDF content, page count, visible rendering, candidate facts, API path, and served filename remain unchanged.
- The navigation change is presentation-only and does not alter contact workflows, analytics semantics, or API contracts.

## Known Issues

- The broader Goal 9 release-validation file retains one unrelated manifest mismatch: `deploy/release-candidate.json` expects runtime Markdown SHA-256 `9e1db4…`, while the current approved Markdown is `8bcb54…`. This task did not change the Markdown résumé or release manifest.
