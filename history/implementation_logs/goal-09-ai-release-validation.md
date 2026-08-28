# Goal 9 — AI-enabled Release Validation

## Status

Release Candidate Ready — Deployment Pending. Local implementation, deterministic validation, clean locked image builds, protected Mock and real-provider gateway validation, persistence/privacy inspection, backup/restore rehearsal, evaluator-hashed Ark validation, and independent-review fixes are complete. External deployment and recruiter-production validation remain separately gated.

## Implemented Scope

- Added a versioned release manifest that freezes the Ark client path, model, finite two-attempt timeout budget, exact runtime résumé, backend/frontend lockfile hashes, base-image digests, prompt/schema hashes, prerequisite Goal 8 evidence, and the current Goal 9 evaluation state.
- Isolated the demo Compose project, made application/database images overrideable for digest-based deployment, pinned all local build/runtime base images by multi-platform digest, and kept Ark configuration backend-only.
- Removed runtime dependency synchronization from the backend production entrypoint so the image executes only its locked non-development virtual environment.
- Aligned Nginx's finite 400-second send/read timeout with two 180-second provider attempts plus a 40-second gateway margin.
- Added a separate privacy-safe gateway smoke covering unauthenticated `401` enforcement, authenticated UI/health, exact résumé PDF digest, safe invalid request, matching, follow-up, completed-identical-follow-up replay, tracking and conversation persistence, all-service log privacy, database privacy, and cleanup.
- Added unique smoke-run markers and backend quiescing on failure so a committed workflow can be recovered and removed even when the response contains no usable Conversation identifier or the client connection fails while a mutation may still be active.
- Added a database privacy audit that checks persisted messages and feedback for effective Ark secrets, internal prompts, and raw structured-provider markers without printing content.
- Hardened Basic Auth generation with a restrictive creation umask, validated usernames, SHA-512 crypt, stdin-only password delivery to OpenSSL, and removal of the inherited password before child processes are launched.
- Documented local build/start/smoke/teardown, immutable production image use, backup/restore rehearsal, digest rollback, and the external deployment/ICP/HTTPS/accessibility approval boundary.

## Evaluation Record

- The first Goal 9 three-run matrix is stored at `history/evaluation_runs/goal-09-release.json` and consumed 31 Ark provider calls within the approved 60-call and ¥15 expected-cost ceilings.
- Every hard guardrail passed. Importance and follow-up-answerability accuracy were `1.00`; evidence-anchor correctness was `0.9667`; explanation usefulness was `3.57 / 4`; valid-first-attempt rate was `0.9667`; retry recovery was `1.00`; mean latency was `6,293.8 ms`; and P95 latency was `10,931 ms`.
- Matching-status accuracy was `0.8889`, below the approved `1.00` threshold. In one of three runs, cost/efficiency evidence was reused to label an independent revenue-growth field `partial` instead of `missing`.
- The failed artifact remains privacy-safe and preserved with its original prompt hash. It is marked superseded in `deploy/release-candidate.json` and is not used as evidence for the adjusted candidate.
- A narrow matching-prompt correction requires qualitative evidence to belong to the same business-result dimension and prohibits reusing one independent result field's evidence for another.
- The corrected complete three-run matrix is stored at `history/evaluation_runs/goal-09-release-final.json` with SHA-256 `3ce318b4eb154218279b9ba3f9a4ee2ba04b63df90ce2af14139d715d755581e`. It consumed 30 calls within the approved 60-call ceiling, passed every hard guardrail, and scored `1.00` for matching status, importance, follow-up answerability, and evidence-anchor correctness; usefulness was `3.4 / 4`, first-attempt validity was `1.00`, mean latency was `5,893.13 ms`, and P95 latency was `11,166 ms`.
- An initial final artifact correctly answered the page-number challenge but the literal forbidden-marker detector matched the forbidden phrase inside an explicit refusal. The artifact remained privacy-safe and was not promoted. A denial-aware evaluator was introduced and the complete matrix then reran successfully. Final review subsequently narrowed that evaluator further so fields are independent and one denial can govern only one marker occurrence; because the passing artifact predates this final hardening and omits generated text by design, it is not promoted without a rerun or explicitly approved deviation.
- After the matrix passed, the separately approved protected local Ark gateway smoke completed matching and follow-up within the four-call ceiling and passed Basic Auth, exact résumé, public-contract, identical replay, persistence, all-service log privacy, database privacy, and cleanup checks.
- The approved final-evaluator rerun is stored at `history/evaluation_runs/goal-09-release-hardened-final.json`. It used 30 calls and passed every hard guardrail plus matching-status, importance, and follow-up-answerability thresholds; one response used the broad `工作经历` heading rather than specific project headings, leaving evidence-anchor correctness at `0.9667`.
- A narrow matching-prompt correction now requires the most specific visible source heading and splits cross-heading evidence. The three-run matching/reliability revalidation at `history/evaluation_runs/goal-09-release-matching-final.json` used 9 calls and passed all matching, importance, evidence-anchor, hard-guardrail, and reliability checks.
- `history/evaluation_runs/goal-09-release-composite-final.json` (SHA-256 `4f3c11acdec4c7996eb68cb61a21bed73b586ccd6679339069ca7268568403b4`) combines current-prompt matching/reliability runs with unchanged-prompt follow-up runs. The manifest pins both source artifacts and records 39 total approved provider calls. The complete 45-case-run artifact passes all hard guardrails; matching status, importance, follow-up answerability, and evidence anchors are each `1.00`; usefulness is `3.4 / 4`; first-attempt validity is `1.00`; mean latency is `6,290.3 ms`; and P95 is `13,330 ms`.

## Validation Completed

- Locked backend install plus final full Mock regression: `166 passed, 1 skipped`; the opt-in live test remained skipped.
- Mypy: no issues across `app`, `evals`, and `tests` (`72` source files).
- Ruff: all checks passed.
- Frontend Vitest: `8` files and `49` tests passed; TypeScript, ESLint, and Vite production build passed (`188` modules transformed).
- Playwright: `6 passed` across desktop and compact Chromium with Mock AI and an isolated PostgreSQL container.
- Digest-pinned clean Docker build passed for backend and gateway; the production backend image contains no pytest, mypy, or Ruff executable and no Ark runtime setting is baked into either application image.
- Compose configuration validation passed with isolated network/volume names and backend-only Ark settings.
- The corrected Mock gateway smoke passed every access, public-contract, persistence, replay, privacy, and cleanup check through Nginx Basic Auth using the generated SHA-512 credential file.
- PostgreSQL custom-format backup/restore rehearsal succeeded into a separate empty database and restored all four public tables; the rehearsal database and exact temporary backup were removed afterward.
- `git diff --check` passed.
- Corrected complete Ark release matrix: passed all release thresholds and zero-tolerance hard guardrails with 30 provider calls.
- Protected local real-Ark gateway smoke: passed every check; the isolated containers, network, credential file, and disposable database volume were removed afterward.

## Independent Review

- The first review correctly blocked release-ready status because the first Goal 9 artifact missed the approved matching-status threshold and the initial manifest did not enforce that gate.
- The release manifest and regression tests now preserve the failed result truthfully and prevent it from being presented as current-candidate validation.
- Review also found Basic Auth command-line exposure/private-creation risk, incomplete cleanup recovery before parsing a Conversation identifier, and incomplete log/effective-secret coverage. All three were fixed with network-free regression coverage and a passing post-fix Mock Compose smoke.
- Follow-up read-only review confirmed the three security findings are resolved, the prompt hardening is narrow, and the manifest truthfully marks the old artifact as superseded with the adjusted candidate pending revalidation. Its only remaining documentation finding—the stale PLAN header version—was corrected.
- Final release review found that one denial cue could extend across a later same-field affirmative marker and that the Goal 8 log still described Goal 9 revalidation as pending. The detector now evaluates fields independently and permits one denial to suppress only the single forbidden-marker occurrence it directly governs; regressions prove later affirmative claims still fail with both explicit and unlisted connectors. The historical status wording is corrected, and focused tests, mypy, Ruff, and the final full Mock regression passed after the fixes.
- Final follow-up review found no remaining release-gating issue. It independently verified the workflow-scoped composition, 45 unique case-runs, source and final hashes, evaluator/schema/prompt compatibility, 39-call accounting, recomputed thresholds, privacy declarations, and release-ready-versus-deployment-pending wording.

## Conformance and Remaining Work

- Public APIs, frontend behavior, persistence ownership, verified Markdown/PDF roles, strict internal schemas/invariants, two-attempt provider ceiling, non-streaming behavior, and the AI Service boundary remain unchanged.
- No upload, request-time extraction, candidate comparison, ranking, score, hiring decision, prediction, frontend AI reasoning, provider payload persistence, production edit, external deployment, server purchase, image publication, push, merge, or pull request was added or performed.
- Goal 9 satisfies the local release-candidate criteria and is recorded as **Release Candidate Ready — Deployment Pending**, not recruiter-production complete. The final artifact and both source artifacts are privacy-safe and evaluator-hashed; the workflow-scoped composition is limited to the matching prompt that changed, while the follow-up prompt/schema/evaluator hashes are identical across sources.
- Mainland provider/domain/ICP eligibility, registry creation, server purchase, image publication, HTTPS, rollback by preceding production digest, and representative recruiter-network accessibility remain deployment-pending and require separate approvals.

## Actual Implementation Time

The work spans multiple interrupted turns, interactive human grading, review/fix cycles, and external approval waits, so a reliable full active-time total is not reconstructed. No estimate is invented.
