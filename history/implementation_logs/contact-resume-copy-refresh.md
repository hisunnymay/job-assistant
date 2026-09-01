# Contact, Résumé, and Loading-copy Refresh

## Completed Changes

- Replaced the fixed recruiter preview/download PDF with the user-supplied two-page résumé and updated the verified PDF digest.
- Versioned the embedded résumé URL and disabled API caching so browser PDF viewers cannot reuse the previous fixed PDF after a replacement.
- Synchronized the runtime résumé Markdown contact line to `电话 / 微信号：18810675122` and `hisunnymay@gmail.com`, then updated its verified digest.
- Updated the recruiter contact view to use the Gmail address and the `电话 / 微信号` label.
- Removed the greeting-preview signature line entirely; the optional recruiter name is now used only in the opening sentence.
- Removed the `通常需要约 30–60 秒` copy from follow-up waiting only; initial report generation continues to show it.
- Compacted dashboard spacing, date controls, conversion summary, six metric cards, and metadata so the full dashboard fits without vertical scrolling at the tested compact viewport while retaining every metric definition.

## Validation and Boundaries

- The supplied PDF was inspected as data only: two A4 pages, unencrypted, no form, no JavaScript, and no detected rendering defect after replacement.
- The served and repository PDF bytes both matched SHA-256 `03f5c8b961b6d13647cf365be3d36d84aecf714ecd0a0910c2c46fbc361768d1`; extracted first-page text contained `hisunnymay@gmail.com`, and API tests covered the versioned preview URL plus no-store response headers.
- Backend application regression excluding the intentionally stale production-manifest gate passed with `175 passed, 1 skipped`; MyPy and Ruff passed.
- Frontend regression passed with 11 Vitest files and 65 tests, TypeScript, ESLint, and a 190-module production build; all 8 desktop/compact Mock Playwright journeys passed, including a compact no-scroll dashboard assertion.
- Manual browser validation at approximately `334 × 804` verified that the dashboard panel height stayed within its available viewport (`660px` within `697px`) and that entering a recruiter name produced no signature line.
- The complete backend suite reported `187 passed, 1 skipped, 1 expected release-gate failure` because the deployed manifest intentionally remains pinned to the previous résumé Markdown digest.
- `deploy/release-candidate.json` remains pinned to the currently deployed production resource. The new local résumé has not been deployed or provider-revalidated; those remain separately approved release actions.
