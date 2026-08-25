# Goal 1 — Frontend Matching Journey with Mock Data

## Version Log

- **v1.3 — 2026-08-25:** Recorded that Goal 1A resolved the conversation-workspace and response-contract mismatch before Goal 2 began.
- **v1.2 — 2026-08-25:** Added prevention measures and clarified which controls belong in `AGENTS.md`, `PLAN.md`, and the finalized frontend design.
- **v1.1 — 2026-08-25:** Added the post-implementation architecture review after identifying that the frontend journey and mock response model do not follow the finalized conversation-workspace design.
- **v1.0 — 2026-08-25:** Recorded the initial Goal 1 implementation and validation results.

## Completed Scope

- Built the complete Chinese recruiter journey from initial guidance and job-description entry through loading, failure recovery, and matching-report review.
- Added deterministic frontend mock analysis behind an injectable client boundary, with evidence grounded in the fixed candidate résumé.
- Presented supported, partial, and missing-information states without a match score, hiring recommendation, or unsupported candidate claims.
- Added responsive desktop and mobile layouts, accessible labels and live regions, focus states, and reduced-motion behavior.
- Kept all user-facing copy in the Chinese content module and introduced no backend or real AI-provider dependency.

## Validation

- `cd frontend && npm run test` — passed, 2 test files and 6 tests.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed.
- Manual browser validation passed for initial, empty-input, short-input, loading, success, failure, retry, and reset behavior.
- Desktop and 390 px mobile layouts had no horizontal overflow; browser console checks found no warnings or errors.

## Problems Fixed and Known Issues

- Added explicit React Testing Library cleanup after the first expanded test run revealed DOM state leaking between tests.
- The mock report is intentionally static and does not analyze arbitrary job-description content. Goal 2 will replace this path with the backend Mock AI Service while preserving the frontend client boundary.
- A post-implementation review identified a major architecture mismatch between the implemented dashboard-style journey and the finalized conversation-workspace design. This must be resolved before building Goal 2 or Goal 3 on top of the current frontend foundation.

## Post-implementation Review — Architecture Misalignment

### What Is Misaligned

The finalized Frontend Technical Design defines the product as a Job Assistant Workspace centered on a Conversation Area. Initial guidance, the submitted job description, matching analysis, and later follow-up questions and answers should appear as messages in one continuing interaction.

Goal 1 instead implemented a two-column dashboard:

- A persistent job-description form appears on the left;
- The right panel replaces its content between empty, loading, failure, and report states;
- The submitted job description is stored inside a collapsible report detail rather than presented as a user message;
- The matching result is presented as a standalone report rather than an assistant message in a conversation timeline.

The implementation therefore completes the narrow input-to-report flow, but it does not establish the assistant-like interaction foundation required by the finalized frontend design.

The mock client also returns a frontend-defined structured `MatchingReport` containing requirements, evidence states, findings, and information gaps. This conflicts with the finalized frontend and backend assumptions that matching analysis is returned as `content` in text/Markdown and rendered by the frontend. It also makes the frontend responsible for a report structure that belongs to the AI/backend response.

### Why This Happened

1. **The Goal 1 checklist was treated as the primary design brief.** The implementation focused on the Goal's explicit states—initial, input validation, loading, success, failure, and evidence categories—without tracing those states back to the authoritative Conversation Area structure.
2. **“Matching journey” was interpreted as a standalone dashboard flow.** The implementation optimized the first visible demo for form-and-report readability instead of treating Goal 1 as the first slice of a persistent conversation experience.
3. **The mock was designed around the desired visual cards instead of the agreed integration contract.** A structured frontend report model made the Goal 1 UI convenient to build, but it diverged from the authoritative `conversationId`, `messageId`, and text/Markdown `content` response that Goal 2 must integrate.
4. **Validation checked behavior, not design traceability.** Tests and manual browser checks verified state transitions, responsive layout, accessibility, errors, and prohibited content. They did not include an explicit check that the page structure and data model matched the finalized frontend and backend designs.
5. **The code review evaluated implementation defects within the chosen design.** Because the tests passed and the implementation behaved consistently, Bugbot found no code bug. The problem is a requirements and architecture mismatch, which was outside that narrow review signal.

### Impact

- Goal 2 cannot replace the frontend mock with the authoritative backend response without either adapting the backend response into the frontend-owned report schema or changing the current rendering model.
- Goal 3 follow-up questions cannot be added naturally because the current UI has no conversation-message model or persistent message timeline.
- Continuing with the current foundation would increase rework and risk moving business or AI-output interpretation into the frontend.
- Passing tests and a visually functional page should not be treated as evidence that Goal 1 conforms to the finalized product design.

### Required Correction Direction

Before Goal 2 begins, the frontend foundation should be realigned around a conversation workspace and message timeline. The Goal 1 mock boundary should model the agreed backend-facing message response rather than a frontend-owned matching-report schema. Exact layout and styling remain flexible, but the interaction structure and ownership boundaries are not optional.

### Resolution Status

Resolved by Goal 1A on 2026-08-25. The frontend now presents initial guidance, the submitted job description, processing and failure states, and matching analysis in one message timeline. The mock client uses the authoritative `conversationId`, `messageId`, and text/Markdown `content` response shape, and the frontend-owned structured matching-report schema has been removed. Goal 2 may proceed on this corrected foundation.

### Prevention for Future Goals

The problem was not primarily caused by missing UI detail in the Frontend Technical Design. That document already defines the conversation workspace, message-based interaction, frontend responsibility boundary, and text/Markdown response assumption. Adding detailed layouts or component specifications would reduce implementation flexibility without addressing the real failure: the implementation did not trace the Goal back to its authoritative requirements.

Prevention should be divided across the project documents as follows:

1. **`AGENTS.md` — add one concise project-wide traceability rule.** Before implementing a Goal, Codex should identify the authoritative document sections and list the non-negotiable product, architecture, and contract constraints that apply. Before declaring the Goal complete, Codex should check the implementation against that list. If `PLAN.md` omits or appears to conflict with an authoritative constraint, the finalized document remains authoritative and Codex should stop for clarification rather than choosing an interpretation silently.
2. **`PLAN.md` — make constraints and validation Goal-specific.** Each coding Goal should include a short “Authoritative references and constraints” subsection. Goal completion criteria should validate not only visible states and command results, but also the required interaction model, ownership boundaries, and API shape. For a frontend-backend slice, use a representative contract fixture early so the frontend mock has the same shape as the future backend response.
3. **Frontend Technical Design — keep it mostly unchanged.** Exact layout and component details remain intentionally flexible. If extra clarity is desired, add only a short statement that the Conversation Area and message-based interaction are required product structures, while their visual layout is flexible. A larger rewrite is unnecessary.
4. **Review workflow — separate code review from specification review.** Automated tests and Bugbot can confirm that the chosen implementation behaves consistently, but they cannot prove that the chosen design matches the product documents. Every meaningful Goal should therefore have a specification-conformance review that compares the implementation with its cited authoritative sections before commit or merge.

For this project, the most effective correction is a small `AGENTS.md` rule plus stronger Goal-level references and completion checks in `PLAN.md`. The finalized frontend design already contains enough information and should not become a detailed implementation specification.
