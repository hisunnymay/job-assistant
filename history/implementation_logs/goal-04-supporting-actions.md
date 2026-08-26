# Goal 4 — Résumé, Contact, and Feedback Actions

## Version Log

- **v1.5 — 2026-08-26:** Recorded the approved required-feedback interaction, predefined reason options, contextual icon tooltips, document updates, and validation.
- **v1.4 — 2026-08-26:** Recorded the requested conversation-density, sidebar-width, feedback-dialog, and icon refinements with automated and browser validation.
- **v1.3 — 2026-08-26:** Recorded completion of the approved reference UI alignment, final validation, and specification-conformance review.
- **v1.2 — 2026-08-25:** Recorded the approved workspace redesign: entrance page, mutually exclusive right-side views, navigation-driven replacement, conversation preservation, and updated validation.
- **v1.1 — 2026-08-25:** Recorded the approved post-completion layout refinement: desktop left navigation, bottom-anchored JD composer, responsive mobile navigation, and validation results.
- **v1.0 — 2026-08-25:** Recorded the completed Goal 4 functional implementation, validation, specification-conformance review, and actual implementation time.

## Completed Scope

- Kept the existing `GET /api/resume` and `POST /api/feedback` contracts and the same approved static résumé PDF used by the AI Service boundary.
- Implemented the approved standalone Entrance View with no workspace navigation, a centered product introduction, 6,000-character JD input, example-fill action, character count, and disabled-until-valid analysis action.
- Implemented the three-view workspace with persistent desktop navigation for Job Matching, Resume Preview, and Contact Candidate; the product brand acts as Home.
- Preserved the active conversation while moving among workspace views or Home, with only one right-side workspace view visible at a time.
- Rendered the submitted JD and backend-provided Markdown report in a scrollable Conversation View. The frontend adds presentation and actions but does not calculate AI conclusions, evidence categories, or counts.
- Attached résumé, contact, Helpful, and Not Helpful actions to the report. Helpful persists rating `5`; Not Helpful persists rating `1`; once either feedback dialog opens, a predefined reason or written detail is required, and duplicate submission is prevented.
- Presented the original résumé in an embedded PDF viewer with a prominent download action.
- Presented résumé-backed email and phone in separate copyable cards, plus an optional recruiter name, Chinese greeting preview, and copy action. No message is sent automatically.
- Added accessible icon names, focus/selected/submission states, compact-layout behavior, and a visually anchored disabled follow-up composer. The actual follow-up workflow remains owned by Goal 3.

## Actual Implementation Time

- Approximately 15 minutes for the original functional slice on 2026-08-25.
- Approximately 4 additional minutes for the initial navigation/composer refinement and approximately 12 additional minutes for the earlier workspace redesign on 2026-08-25.
- Approximately 27 additional minutes for the approved reference UI alignment, automated validation, API and persistence checks, desktop/compact browser validation, specification review, and documentation closeout on 2026-08-26, measured by the Codex Goal timer.
- Approximately 6 additional minutes for the requested conversation-density, sidebar-width, feedback-dialog, and icon refinements with automated and browser validation on 2026-08-26, measured by the Codex Goal timer.
- Approximately 8 additional minutes for Frontend Technical Design v0.7 and PLAN v0.15 updates, contextual icon tooltips, required feedback contribution, predefined reasons, automated validation, live persistence inspection, and desktop/compact browser checks on 2026-08-26, measured by the Codex Goal timer.

## Validation

- `cd backend && uv run pytest` — passed, 15 tests against isolated PostgreSQL schemas, including explicit persistence coverage for ratings `1` and `5`.
- `cd backend && uv run mypy app` — passed for 28 source files.
- `cd backend && uv run ruff check .` — passed.
- `cd frontend && npm test -- --run` — passed, 5 test files and 19 tests.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed; Vite transformed 183 modules and produced the production bundle.
- `GET /api/resume` returned HTTP 200, `application/pdf`, inline disposition, 326,049 bytes, and SHA-256 `20a4d191dcc675b67a55da4296c2200cf2ceed1b3deb9aca4fbdf9e5e8cb08bd`.
- `GET /api/resume?download=true` returned attachment disposition and the same SHA-256.
- A live Helpful action persisted rating `5` against the expected conversation and matching-analysis message; isolated API tests verify persistence for ratings `1` and `5`, while frontend tests verify the Helpful/Not Helpful mappings and duplicate lock.
- At 1536 × 1024, browser checks passed for the standalone entrance, valid/invalid JD action state, workspace navigation, scrollable report, bottom composer placement, original PDF preview/download, dynamic greeting/copy actions, one-click feedback state, Home return, and conversation preservation.
- At 390 × 844, browser checks confirmed zero horizontal overflow, accessible compact navigation, visible bottom composer, usable contact cards, and visible résumé preview/download controls.
- Browser console checks found no warnings or errors in the validated journey.

### v1.4 UI Refinement Validation

- Reduced the desktop sidebar from the earlier 240–316 px range to a responsive 190–220 px range; browser measurement at the validated desktop viewport reported 190 px.
- Reduced report text to 13.44 px with a 21.77 px computed line height and reduced the submitted JD text to 14.08 px, while retaining readable heading hierarchy.
- Removed the visible `补充说明` disclosure. Helpful and Not Helpful now open rating-specific modal prompts with an optional textarea, Cancel, and Submit actions before sending feedback.
- Replaced the earlier custom thumb drawings with simpler consistent outline icons; both retain accessible names and selected states.
- Automated frontend tests, type-checking, lint, and production build passed. Browser checks confirmed both popup variants, cancellation, zero console warnings/errors, and a 350 px-wide modal with zero horizontal overflow at 390 × 844.

### v1.5 Feedback Interaction Validation

- Updated Frontend Technical Design to v0.7 and PLAN to v0.15 before implementation. The PRD's voluntary initiation rule and the backend `POST /api/feedback` contract remain unchanged.
- Added floating action-name labels for résumé, contact, Helpful, and Not Helpful icons. Browser hover inspection confirmed the correct visible label for all four actions.
- Added four predefined positive reasons and four predefined negative reasons with multi-select states. The modal also accepts custom text.
- Kept Submit disabled until at least one predefined reason is selected or non-whitespace custom text is entered. Automated tests cover empty-state locking, option selection, combined serialization, both rating mappings, duplicate prevention, and recoverable submission errors.
- `npm test -- --run`, `npm run type-check`, `npm run lint`, and `npm run build` passed; 5 test files and 20 tests passed, and Vite transformed 183 modules.
- A live Helpful submission persisted rating `5` with `选择项：证据清晰可核验；信息缺口标注清楚` and `补充：结构清楚，便于核验。` in the existing comment field.
- Desktop browser checks confirmed tooltip visibility and both rating-specific option sets. At 390 × 844, the required-feedback modal measured 350 × 490.25 px with zero horizontal overflow. No browser console warnings or errors were observed.

## Specification-Conformance Review

- **Product behavior:** Conforms to PRD F003, F004, F006, and F007. The UI presents the backend report, exposes the approved PDF, provides copy-only contact initiation, and stores optional report-linked feedback.
- **AI boundary:** Conforms to Lightweight AI Design Decision Sections 1.2–1.4 and 2.1. Matching content remains backend-provided text/Markdown; the frontend does not invent or derive candidate evidence.
- **Frontend composition:** Conforms to Frontend Technical Design v0.7 Sections 2.1–2.3, 3.3–3.7, 4.6–4.7, and 5.1–5.3. The entrance is standalone, the three workspace views are mutually exclusive, the active conversation is preserved, contextual icons expose action labels, and report feedback requires a reason or written detail after initiation.
- **Backend contracts and layers:** Conforms to Backend Technical Design Section 5 and the controller/service/repository boundaries. The résumé and feedback request/response contracts were not changed.
- **Scope boundaries:** No résumé upload/extraction, candidate management, automatic messaging, frontend AI reasoning, real AI provider, tracking implementation, or follow-up workflow was added.
- **Result:** No unresolved material mismatch was found against the authoritative Goal 4 references.

## Problems Fixed and Remaining Known Issues

- Corrected the earlier long-page composition to the approved standalone entrance and one-active-view workspace without changing the completed backend capabilities.
- Prevented compact layouts from pushing the bottom composer outside the viewport and added explicit accessible names when visible navigation labels collapse.
- Kept qualitative feedback available through a compact modal opened by either thumb action, without changing the existing rating/comment API contract.
- Required a meaningful contribution after the modal opens and serialized selected reasons plus custom text through the existing comment field; feedback initiation itself remains voluntary.
- Preserved feedback submission state across workspace navigation so a recruiter cannot accidentally submit a duplicate for the same report in the current session.
- Follow-up questions remain intentionally deferred to Goal 3; the current disabled composer establishes placement only.
- Product behavior tracking remains intentionally deferred to Goal 5.
