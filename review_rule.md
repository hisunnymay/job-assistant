## Proposed review rules

### 1. Necessity test

Keep an instruction only if it meets at least one condition:

- Applies across multiple implementation goals.
- Prevents a likely, costly project-specific mistake.
- Defines decision ownership or a source-of-truth boundary.
- Establishes a required verification, reporting, or approval process.

Remove or relocate content that:

- Repeats detailed technical documents without adding an operational rule.
- Describes one implementation goal.
- Covers hypothetical future requirements.
- Can be discovered directly from the repository.
- Duplicates general Codex safety or coding rules.



### 2. Document responsibilities

Use these boundaries:

- `AGENTS.md`: Persistent project rules, architectural boundaries, prohibited changes, and approval requirements.
- `planning/PLAN.md`: Ordered goals, implementation tasks, completion criteria, validation commands, dependencies, and status.
- `docs/`: Product behavior, AI design, frontend/backend architecture, and agreed contracts.
- Implementation logs: What was changed, tested, fixed, deferred, or intentionally deviated from the plan.

`AGENTS.md` should not duplicate detailed API definitions, implementation steps, goal status, or validation commands that belong in the other documents.

### 3. Logging review

I will evaluate adding one concise rule to `AGENTS.md` requiring implementation records, while storing the actual records somewhere else—likely `history/implementation_logs/`.

Each completed goal’s record should contain only:

- Goal completed.
- Important files or behavior changed.
- Validation performed and results.
- Problems discovered and fixed.
- Approved deviations from specifications.
- Remaining known issues.

It should not contain internal reasoning, every command executed, or a full conversation transcript.

### 4. Project-specific prohibitions

I will check whether `AGENTS.md` clearly prevents violations such as:

- Adding multiple candidates, candidate upload, comparison, ranking, or an overall match score.
- Extracting the static résumé PDF in the backend during the MVP.
- Placing AI reasoning in the frontend or controller layer.
- Exposing or persisting raw prompts, provider payloads, secrets, or internal errors.
- Bypassing the agreed backend layers or AI Service boundary.
- Introducing microservices or speculative infrastructure.
- Changing product behavior, AI boundaries, or API contracts without approval and document updates.

General rules already enforced by Codex will not be repeated.

### 5. PLAN.md overlap check

Anything that answers these questions should normally move to `PLAN.md`:

- What will be implemented next?
- In what order?
- What exact files or components are involved?
- How will completion be measured?
- Which validation commands must pass?
- What is currently blocked or unfinished?

`AGENTS.md` may require Codex to follow `PLAN.md`, but should not contain the plan itself.

### 6. Source-of-truth check

The review will verify that:

- Each document owns a clearly defined type of decision.
- `AGENTS.md` does not silently override finalized specifications.
- Conflicts are resolved through the owning document.
- Document changes require your explicit approval.
- Every approved document change updates its Version Log.



### 7. Missing-information research

I will compare the file against current official Codex guidance and check specifically for:

- Instruction scope and placement.
- Conciseness and duplication.
- Code-review expectations.
- Validation and completion reporting.
- Documentation synchronization.
- Whether any rules belong in nested frontend/backend instructions later instead of the root file.



### 8. Review output

After you confirm these rules, I will provide:

1. What should remain.
2. What should be shortened.
3. What should move to `PLAN.md`, technical documents, or implementation logs.
4. What should be removed.
5. What project-specific rules are missing.
6. A proposed concise `AGENTS.md` structure.

