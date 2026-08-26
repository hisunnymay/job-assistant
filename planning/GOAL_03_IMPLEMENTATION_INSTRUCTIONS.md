# Goal 3 Implementation Handoff — Follow-up Workflow and Persisted Context

## Purpose

Use this file when Goal 4 has been completed and the user explicitly asks Codex to implement Goal 3.

This is a task-specific handoff, not a replacement for `AGENTS.md`, `planning/PLAN.md`, or the finalized documents under `docs/`. Read the current versions of all applicable files before coding. If this handoff conflicts with a newer authoritative document, follow the authoritative document and stop for user direction when the difference would change product behavior, architecture, persistence meaning, or an API contract.

## Required Reading Order

Before taking implementation action, read:

1. `AGENTS.md`;
2. `planning/PLAN.md`, especially the Goal Readiness and Conformance Gate and Goal 3;
3. This handoff;
4. `docs/01_Product_Requirement_Document.md`, especially F005 Ask Follow-up Questions and S002 Conversation Logging;
5. `docs/03_Lightweight_AI_Design_Decision.md`, especially Sections 1.2–1.4 and 2.1–2.2;
6. `docs/04_Frontend_Technical_Design.md`, especially Sections 2.1–2.3, 3.3, 3.5, 4.6–4.7, and 5.1–5.3;
7. `docs/05_Backend_Technical_Design.md`, especially the Conversation and Conversation Message entities, the follow-up processing flow, Section 4.2, Section 5, and Sections 6.2–6.3;
8. The current Goal 2 and Goal 4 implementation logs and the current code, rather than assuming the repository still matches the snapshot that existed when this handoff was written.

## Git and Entry Gate

Do not begin Goal 3 coding until all of the following are true:

- Goal 4 work has been reviewed and safely recorded in Git;
- The working tree is clean except for changes the user explicitly wants included in Goal 3;
- The Goal 3 base contains the completed Goal 4 conversation workspace and disabled bottom composer;
- Codex is on a short-lived branch named `goal/03-follow-up-context`;
- No unrelated or user-owned changes will be mixed into the Goal 3 branch.

The preferred sequence is:

1. Obtain explicit authorization for the Goal 4 local commit;
2. Obtain separate explicit authorization before merging Goal 4 into `main`;
3. Create `goal/03-follow-up-context` from the updated `main`;
4. Implement only Goal 3.

Do not stash, discard, commit, merge, push, or open a pull request merely to make the tree convenient. Follow the authorization rules in `AGENTS.md`. If Goal 4 is still uncommitted or absent from the intended base, report that state and stop before coding.

## Goal 3 Readiness Update

Before coding, update the Goal 3 section of `planning/PLAN.md` so it satisfies the plan's own readiness gate. Add:

- The authoritative references listed above;
- The non-negotiable behavior and architecture constraints in this handoff;
- The representative request and response fixture below;
- Explicit failure and persistence expectations;
- The complete automated, smoke, browser, and specification-conformance validation listed below.

Update the Plan Version Log without rewriting the history of completed Goals. `PLAN.md` is subordinate to the finalized design documents. Do not edit a finalized document under `docs/` or `AGENTS.md` without first identifying the affected document and obtaining the user's explicit approval.

## Authoritative API Fixture

Implement the existing Backend Technical Design Section 5 contract exactly:

```http
POST /api/conversations/{conversationId}/messages
Content-Type: application/json
```

Request:

```json
{
  "question": "Does the candidate have AI Agent experience?"
}
```

Successful response:

```json
{
  "messageId": "message_003",
  "content": "..."
}
```

`content` remains backend-provided text/Markdown. Do not add `conversationId`, evidence categories, scores, recommendations, provider fields, or a new structured AI-output schema to this response unless the authoritative contract is explicitly updated and approved.

Use the existing safe error envelope:

```json
{
  "code": "ERROR_CODE",
  "message": "User-friendly error message"
}
```

At minimum, cover invalid input, an unknown conversation, Mock AI failure, persistence failure, and unexpected failure. Suggested implementation-level codes are `INVALID_REQUEST`, `CONVERSATION_NOT_FOUND`, `AI_SERVICE_UNAVAILABLE`, and `PERSISTENCE_ERROR`, provided no newer authoritative contract defines different codes. Follow-up validation errors must refer to the follow-up question, not to the job description or feedback.

## Non-negotiable Product Behavior

- Follow-up questions are allowed only after a matching analysis has created an active conversation;
- Questions and answers remain associated with that same persisted conversation;
- Supported scope is limited to candidate experience and background, evidence behind matching results, identified information gaps, and additional context present in the available candidate information;
- Unavailable information must be identified as unknown rather than invented;
- Hiring recommendations, candidate ranking or comparison, future-performance prediction, personal judgments, overall scoring, and unrelated questions must be rejected or redirected;
- The frontend presents user input and backend output but does not decide whether a question is supported;
- The backend Service Layer owns the workflow and prepares the full relevant conversation context;
- The AI Service must not access persistence;
- The Demo continues to use a deterministic Mock AI Service behind the AI boundary;
- Do not add a real AI provider, SDK, provider secret, raw prompt persistence, raw provider-response persistence, résumé extraction, a résumé text mirror, candidate management, open-ended chat, streaming, tracking, or any later-Goal capability;
- Continue using the same predefined static résumé PDF through the AI Service boundary.

## Recommended Persistence Semantics

Treat one follow-up exchange as one atomic transaction:

1. Verify that the conversation exists;
2. Create and flush the recruiter `follow_up_question` message;
3. Load or prepare the full ordered history, including the current question;
4. Call the Mock AI Service with the static résumé path and prepared history;
5. Create the assistant `follow_up_answer` message;
6. Commit both messages together.

If Mock AI generation or persistence fails, roll back both new messages. The frontend should keep the failed question visible locally and offer an in-context retry without appending a duplicate user message. This avoids orphaned persisted questions and duplicate records on retry.

If a newer authoritative document defines different failure persistence semantics, stop and ask the user to resolve the conflict before implementation.

## Backend Implementation Direction

Keep the established boundary:

```text
API Access Protection -> Controller -> Service -> AI Service / Repository
```

Implement the smallest vertical slice that conforms to it:

- Add a follow-up controller for HTTP parsing, dependency injection, response serialization, and safe error mapping;
- Add a follow-up Service that owns conversation validation, transaction control, context preparation, AI coordination, and result construction;
- Extend the repository with only the operations Goal 3 needs, such as retrieving a conversation and retrieving its messages in deterministic chronological order;
- Pass a small provider-neutral context value to the AI Service rather than passing repository or SQLAlchemy objects across the AI boundary;
- Extend or complement the existing AI Service protocol with a follow-up operation that receives the static résumé path and prepared ordered conversation context;
- Extend the deterministic Mock AI Service with at least three explicit behaviors: supported question, unavailable information, and out-of-scope request;
- Persist recruiter questions with role `user` and message type `follow_up_question`;
- Persist generated answers with role `assistant` and message type `follow_up_answer`;
- Reuse the existing ID style and safe exception translation;
- Register the new router without changing existing matching, résumé, or feedback contracts.

The Mock implementation may use deterministic fixtures and simple routing, but every candidate claim must already be supported by the available fixed-candidate context. It must not imply that the Mock parsed the PDF, and it must not invent evidence merely to answer a supported-topic question.

## Frontend Implementation Direction

Preserve the Goal 4 workspace, navigation, message scrolling, contextual report actions, résumé/contact views, feedback behavior, and conversation preservation.

Do not reuse the initial matching-analysis loading/error/retry state for follow-ups. Add independent follow-up state, including:

- Current question input;
- Submission eligibility;
- Pending state;
- Failed-question state and an in-context retry path;
- Follow-up-specific localized error content.

Implement the interaction as follows:

1. Enable the existing bottom composer only when a valid `conversationId` and completed matching analysis are available;
2. Trim and validate the question consistently across frontend and backend;
3. Append the recruiter question to the existing message history;
4. Show processing status in that same history while leaving the original matching report intact;
5. Send the question through a small follow-up API client using the active `conversationId`;
6. Append the returned assistant answer as text/Markdown;
7. On failure, show a follow-up-specific inline error and allow retry without duplicating the displayed or persisted question;
8. Disable concurrent submissions so message order remains deterministic;
9. Preserve all follow-up messages when navigating among Home, Job Matching, Resume Preview, and Contact Candidate in the current frontend session.

Extend the frontend message types and accessible labels with `follow_up_question` and `follow_up_answer`. Keep résumé, contact, and report-feedback actions attached only where the current approved behavior requires them; do not silently extend feedback scope to follow-up answers.

Do not add a conversation-history retrieval API or refresh restoration unless an authoritative document is updated and the user approves the expanded scope. Goal 3 requires persisted backend context and current-session frontend continuity, not a new conversation-management product.

## Required Tests

### Backend

- Exact successful request/response contract;
- Invalid or empty question returns a safe follow-up-specific error;
- Unknown conversation returns a safe not-found error and stores nothing;
- One successful follow-up stores one question and one answer under the correct conversation;
- Multiple follow-ups preserve deterministic message order;
- A recording AI test proves that the Service supplies the static résumé path and the ordered context: job description, matching analysis, previous questions, previous answers, and current question;
- Supported, unavailable-information, and out-of-scope Mock cases return the intended bounded response;
- Mock AI failure exposes no internal detail and rolls back the new exchange;
- Persistence failure exposes no internal detail and rolls back the new exchange;
- Existing matching-analysis, résumé, and feedback tests continue to pass.

### Frontend

- Composer remains unavailable before a successful matching analysis and becomes available afterward;
- Empty or invalid questions cannot be submitted;
- A question is appended once, processing appears in context, and the answer is appended as Markdown;
- Follow-up failure uses follow-up-specific copy and does not replace or clear the matching report;
- Retry does not duplicate the user question;
- Concurrent submission is prevented;
- Multiple questions and answers stay in order;
- Home, résumé, contact, and Job Matching navigation preserves the active conversation and follow-up messages;
- The frontend does not classify scope, infer evidence, calculate counts, or generate a recommendation;
- Existing Goal 4 feedback, résumé, contact, accessibility, and responsive tests continue to pass.

## Required Validation

Run all of the following before declaring Goal 3 complete:

```text
cd backend && uv run pytest
cd backend && uv run mypy app
cd backend && uv run ruff check .
cd frontend && npm run test
cd frontend && npm run type-check
cd frontend && npm run lint
cd frontend && npm run build
```

Also perform and record:

- API smoke test: initial matching analysis followed by at least two questions in the same conversation;
- Persistence inspection: confirm the exact ordered roles, message types, conversation IDs, and content boundaries;
- Failure smoke test: confirm a failed follow-up is recoverable and does not create a partial or duplicate persisted exchange;
- Desktop browser check: composer anchoring, independently scrolling history, multiple turns, inline processing/error/retry, and navigation preservation;
- Representative compact-viewport check: composer, scrolling, controls, and error state remain operable without horizontal overflow;
- Browser console check;
- Specification-conformance review against every authoritative section identified in the Goal 3 readiness update.

Automated tests and a successful build do not replace the specification-conformance review.

## Completion and Records

Before reporting Goal 3 complete:

- Compare the implementation with the Goal 3 authoritative references and non-negotiable constraints;
- Create `history/implementation_logs/goal-03-follow-up-context.md` with completed behavior, material files, validation results, fixed problems, approved deviations, remaining issues, conformance result, and actual implementation time with its measurement basis;
- Update Goal 3 status, actual implementation time, Plan status, and Plan Version Log without rewriting prior Goal history;
- Mark Goal 5 ready only if both Goals 3 and 4 are complete and no unresolved conformance mismatch remains;
- Review the final diff and exclude unrelated or user-owned changes;
- Propose a concise Goal-level commit message;
- Create a local commit only with explicit user authorization;
- Never push, merge, or open a pull request without explicit user approval.

## Stop Conditions

Stop and ask the user before coding or continuing if:

- Goal 4 work is not safely recorded or the working tree cannot be cleaned without affecting user-owned changes;
- The current authoritative documents conflict about follow-up behavior, architecture, persistence, or the API contract;
- Implementation would require changing Backend Technical Design Section 5 or corresponding frontend assumptions;
- A candidate claim cannot be grounded in the available fixed-candidate context;
- The static PDF cannot be passed through the existing AI Service boundary without extraction or a new text mirror;
- Completing the work would require adding a prohibited or later-Goal capability.
