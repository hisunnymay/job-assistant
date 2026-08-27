# Goal 7A — Example Report, Truthful Waiting State, and Mini Validation

## Status

Complete. Offline implementation, full regression validation, Bugbot review, the authorized Mini baseline, and a user-requested supplemental JD check are closed. The result does not change the configured default model or local `.env`.

## Completed Offline Scope

- Added a human-checked static Markdown example report for the fixed candidate and existing example JD. It uses the formal `ConversationMessage` Markdown renderer, is visibly labelled, and supports résumé/contact navigation without analysis, follow-up, feedback, Conversation, or `matching_report_generated` side effects.
- Added a shared accessible loading status for matching and follow-up with the `30–60` second expectation, actual elapsed seconds, post-60-second guidance, no percentage, and timer cleanup/reset across request completion, failure, retry remount, navigation, and unmount.
- Kept the strict schemas, cross-field invariants, source-reference whitelist, public APIs, and two-attempt ceiling unchanged. Attempt two adds one generic safe correction only after invalid structured output; transient retries reuse the exact original request.
- Added privacy-safe retry-reason metadata and a gated Mini live result writer. The repository result excludes résumé, JD, question, prompt, provider payload/raw response, and generated Markdown; a temporary user-facing Markdown file exists only for manual grounding review and must be removed afterward.
- Kept the configured Pro default and ignored `.env` unchanged. The Mini model is used only through an explicit process environment override after approval.
- Escaped all provider-controlled strings before inserting them into renderer-owned Markdown, changed Ark/Mock failure text to provider-neutral wording, aligned the prepared Nginx gateway to the bounded two-attempt backend duration, and corrected the linked Ark research record to the verified-Markdown runtime path.

## Validation

- Backend: `142 passed, 1 skipped` with the opt-in live test skipped; full mypy and Ruff passed across app and tests.
- Frontend: `49 passed`; type-check, ESLint, and Vite production build passed.
- E2E: `6 passed` across desktop and compact Chromium, including provider-free example entry, no generated-report event before formal submission, truthful pending elapsed seconds, recovery, and compact no-overflow checks.
- Focused retry tests prove invalid/missing structured output adds the safe correction, transient retries are request-identical, follow-up uses the same correction branch, permanent failures do not retry, and exhaustion never exceeds two provider calls.
- Focused renderer and gateway tests prove provider Markdown control characters cannot create external images/headings and the default demo gateway does not terminate the approved bounded workflow at 60 seconds.
- `git diff --check` passed.

## Bugbot Review

- P1 provider-controlled Markdown injection: fixed with deterministic escaping and regression coverage.
- P1 60-second Nginx timeout versus two 180-second provider attempts: fixed with finite 400-second upstream timeouts and a configuration regression test; Goal 9 still owns release-environment revalidation.
- P2 provider-specific “Mock AI” error wording: fixed with provider-neutral copy.
- P2 stale Ark research record: updated to distinguish historical PDF evidence from the current verified-Markdown path.

## Mini Validation

- Model: `doubao-seed-2-0-mini-260428`.
- Standard run: one matching analysis and one follow-up through the same public APIs and strict production path used for Pro; both passed on attempt one, using 2 of the 4 authorized calls with no structured retry.
- Standard metrics: 100% first-attempt success, 11.26 seconds end to end (11.07 seconds inside the two AI workflows), valid schemas and legal source references. This is 23.02 seconds, or approximately 67%, faster than the 34.28-second Pro baseline.
- Manual grounding and behavior review: passed for the standard run. No invented candidate evidence, candidate score, hiring recommendation, future-performance claim, or source-heading violation was found.
- Privacy: `history/evaluation_runs/goal-07a-mini.json` contains metrics and review decisions only; it contains no résumé, JD, question, prompt, provider payload/raw response, or generated Markdown. The temporary review file was deleted after inspection.
- Supplemental user-provided retail merchandise/inventory JD: one matching call passed strict validation on attempt one in 11.00 seconds end to end, correctly identified the absence of merchandise/inventory tenure and SPU/SKU or inventory-system evidence, but overstated evidence strength for cross-department communication and inferred strong autonomous-learning/AI-interest traits from project experience. Its JD, output, temporary test, and temporary metrics were deleted after review.
- Decision: Mini is technically compatible and materially faster in this small sample, but the supplemental check shows that evidence-strength calibration still needs Goal 8 evaluation and prompt tuning. Do not switch the default model or `.env` without a separate user decision.

## Conformance and Remaining Issues

- Conformance review passed: fixed PDF remains preview/download only; verified Markdown remains the sole runtime candidate context; public APIs, persistence ownership, strict schemas/invariants/source whitelist, and the two-attempt ceiling remain unchanged; there is no streaming, upload, third call, frontend inference, or raw provider persistence.
- No approved deviation remains. Goal 8 should explicitly test subjective-trait inference and evidence-status calibration before any model-default decision.
- No commit, push, merge, or pull request was created.
