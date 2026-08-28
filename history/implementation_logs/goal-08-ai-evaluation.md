# Goal 8 — AI Evaluation and Behavior Tuning

## Status

Complete. The typed evaluation infrastructure, corrected baseline, approved thresholds, three bounded prompt-tuning iterations, passing three-run final matrix, deterministic regression validation, independent review, and specification closeout are recorded. The current prompt passed every approved hard guardrail and graded release threshold.

## Implemented Scope

- Added the versioned `goal-08-real-ai-v2` matrix with 10 real-AI matching/follow-up cases and 5 network-free retry/reliability cases covering every required Goal 8 category.
- Added strict typed suite, case, human-review, run-result, privacy, and aggregate-metric models plus deterministic status, importance, answerability, evidence-anchor, schema/invariant, forbidden-behavior, retry, and latency evaluation.
- Added a gated interactive runner that uses the approved Pro model and AI Service path, supports focused case reruns, stores only privacy-safe IDs, hashes, metadata, metrics, rule results, and failure categories, and rejects noninteractive, non-Ark, or wrong-model execution.
- Added an offline artifact rescorer for deterministic evaluator corrections without additional provider calls.
- Exposed structured AI workflow results and privacy-safe execution metadata inside the AI Service while preserving the existing public text/Markdown return contracts and two-attempt ceiling.
- Tuned matching and follow-up prompts in three bounded iterations to handle contextual gap references, direct evidence selection, composite capability requirements, independent quantitative result fields, and qualitative-versus-quantitative partial evidence.
- Expanded mypy coverage to `evals` and added network-free evaluator/runner regression tests.
- Added a mandatory `--max-provider-calls` ceiling. The runner calculates the selected run's two-attempt worst case and rejects an undersized budget before any provider request.
- Updated `planning/PLAN.md` through v0.36 with the approved baseline, thresholds, tuning/final checkpoint, pending status, exact call accounting, remaining work, and budgeted validation commands.

## Evaluation Record

- `goal-08-baseline-pilot.json`: 11-call harness-development pilot; retained for history and excluded from the formal baseline.
- `goal-08-baseline.json`: corrected 11-call Pro baseline. Status `1.00`, importance `1.00`, answerability `0.8571`, evidence anchors `0.80`, usefulness `2.90 / 4`, first-attempt validity `0.90`, mean latency `9,204.2 ms`, and P95 `26,024 ms`. The contextual gap case exhausted both structured-output attempts, so hard guardrails did not pass.
- `goal-08-tuning-01.json`: 3-call focused run after contextual-gap and direct-evidence tuning. Every applicable hard guardrail and graded accuracy metric passed; usefulness was `3.33 / 4`.
- `goal-08-final-attempt-01.json`: first complete three-run attempt with 30 live executions and 30 provider calls. Every hard guardrail passed; answerability was `1.00`, evidence anchors `0.90`, usefulness `3.23 / 4`, first-attempt validity `1.00`, mean latency `6,708.1 ms`, and P95 `13,215 ms`. Matching status `0.6667` and importance `0.7778` missed the approved `1.00` thresholds because compound requirements were split or combined inconsistently.
- `goal-08-tuning-02.json`: 6-call focused three-run check. The composite capability case stabilized, but the independent quantitative fields still merged in two runs.
- `goal-08-tuning-03.json`: 3-call focused three-run check after the final allowed prompt iteration. Every hard guardrail passed; status, importance, evidence anchors, and first-attempt validity were `1.00`, with usefulness `4.00 / 4`.
- A post-tuning complete final rerun was stopped at the user's request after 3 provider calls. The runner writes only complete artifacts, so no `goal-08-final.json` was created.
- `goal-08-final.json`: passing three-run final matrix using the current prompt and schema hashes. All 30 live executions succeeded on their first provider attempt; every hard guardrail passed; status, importance, answerability, and evidence anchors were `1.00`; usefulness was `3.30 / 4`; mean latency was `7,048.9 ms`; and P95 latency was `12,904 ms`. Retry recovery is `N/A` because no live retry occurred.
- Stored artifacts substantiate 94 Goal 8 provider calls: 11 pilot, 11 corrected baseline, 3 tuning iteration 1, 30 first final attempt, 6 tuning iteration 2, 3 tuning iteration 3, and 30 passing-final calls. The user-stopped rerun recorded 3 additional calls but intentionally produced no artifact, bringing the operational history to 97 while leaving 94 independently reconstructable. Every group stayed within its explicitly approved call and expected-cost ceiling; the final run stayed within the approved 60-call and ¥15 ceilings. Actual provider billing was not queried.

## Validation

- Goal 8 evaluator/runner regression after the final roll-up fix: `8 passed`.
- Full backend after the final roll-up fix: `150 passed, 1 skipped`; the opt-in live test remained skipped.
- Mypy: no issues across `app`, `evals`, and `tests` (`67` source files).
- Ruff: all checks passed.
- Frontend Vitest: `8` files and `49` tests passed.
- Frontend TypeScript, ESLint, and Vite production build passed (`188` modules transformed).
- Playwright: `6 passed` across desktop and compact Chromium with `AI_PROVIDER=mock`.
- `git diff --check` passed.
- Normal automated validation remained Mock-based and network-free; no Ark call was made by the final regression or Bugbot-fix validation.
- Approved live final matrix: 30 first-attempt provider calls, zero hard-guardrail violations, and every approved graded threshold passed. The stored artifact contains no résumé, JD, question, prompt, generated response, provider payload/raw response, secret, or internal-error content.

## Independent Review

- Bugbot reported one P1 finding: the paid live runner reported call usage only after completion and did not enforce the approved ceiling.
- Fixed by requiring an explicit provider-call budget, calculating the selected cases' two-attempt worst case, rejecting insufficient budgets before provider access, updating all documented commands, and adding a regression assertion that rejection produces zero provider requests.
- Final closeout review found one P2 roll-up defect: a deterministic forbidden-claim marker was recorded in a case's failure categories but did not force the artifact-level hard-guardrail flag to fail. The aggregate now treats that marker as a hard failure, with regression coverage proving a human-safe review cannot mask it. The passing final artifact contains no forbidden-claim marker, so it was revalidated offline without another provider call.
- No post-budget-fix Bugbot rerun was requested. Focused and full deterministic validation passed after the budget fix, and the final closeout reviewer verified the artifact metrics, hashes, privacy fields, case/run counts, and public-contract boundaries before reporting and closing the roll-up defect.
- The follow-up read-only review confirmed both the roll-up defect and provider-call auditability wording were resolved, `git diff --check` passed, and no material finding remained. Goal 8 therefore required no additional provider call for final sign-off.

## Conformance and Closeout

- The implemented checkpoint conforms to the approved scope and architecture: the fixed verified Markdown remains the only runtime candidate context; the PDF remains preview/download only; AI handling remains behind the AI Service; public APIs, persistence ownership, frontend behavior, strict internal schemas/invariants, source-heading validation, and the two-attempt ceiling remain unchanged.
- Evaluation artifacts contain no résumé, JD, question, prompt, generated response, provider payload/raw response, secret, or internal error content. No upload, request-time extraction, RAG, streaming, new provider, scoring, ranking, hiring decision, or frontend AI reasoning was introduced.
- At Goal 8 closeout, the passing final matrix matched the then-current matching, follow-up, correction-prompt, and internal-schema hashes. No model, parameter, provider, public API, persistence, frontend, or architecture change was introduced before that closeout.
- Goal 8 is complete with no accepted graded shortfall and no remaining material conformance mismatch. Deployment sequencing and external purchase/deployment approvals remain owned by Goal 9.
- Goal 9 later exposed one stochastic cross-dimension evidence error in its separate release matrix and applied a narrow matching-prompt correction. The passing Goal 8 artifact remains valid historical prerequisite evidence for its recorded prompt hash, but it no longer matches the adjusted Goal 9 prompt and is not used as current-candidate release evidence; the separate corrected Goal 9 matrix subsequently passed.

## Actual Implementation Time

The full Goal 8 time is not reliably reconstructable because implementation, bounded tuning, the user-stopped rerun, and final closeout occurred across separate sessions. The passing final matrix took approximately 10 minutes of active provider execution and human review; no full-Goal estimate is invented.
