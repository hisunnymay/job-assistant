# AI Job Fit Assistant Implementation Strategy

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant Implementation Strategy |
| Document Type | Implementation Strategy |
| Version | v0.1 |
| Status | Approved |
| Owner | Mei Chang |
| Last Updated | 2026-08-25 |
| Related Documents | Product Requirement Document, Lightweight AI Design Decision, Frontend Technical Design, Backend Technical Design, AGENTS.md |

## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v0.1 | 2026-08-25 | Defined the Codex implementation workflow and compared autonomy options. | Prepare the MVP for coding with appropriate automation and review boundaries. |

## 1. Most Suitable Solution

Use a **single primary Codex agent with bounded Goal-mode phases, automatic validation, and selective reviewer subagents**.

Working method:

1. Give Codex one vertical slice at a time, with a clear outcome and stopping condition.
2. Let Codex implement the slice and run relevant unit tests, type checks, builds, and smoke tests.
3. Use a separate read-only reviewer or `/review` at meaningful checkpoints.
4. Use subagents only for bounded independent work such as code review, test-gap analysis, security review, or failure investigation—not simultaneous frontend/backend editing by default.
5. Add a small AI evaluation suite after the real AI path works, using PRD behaviors such as evidence grounding, unknown-information handling, controlled follow-up answers, and no overall match score.
6. Involve the user only when a product or contract decision is unresolved, an external/costly action needs approval, a finalized document may need updating, or visual/product judgment is required.

This is suitable because the project is a one-week, single-candidate MVP with a modular-monolith backend, explicit API contracts, and a limited end-to-end workflow. It benefits from autonomous execution and validation, but not from the coordination cost of a permanent multi-agent team.

This is **controlled, eval-driven iteration**, not self-evolution:

```text
Implement
-> Run deterministic tests
-> Run AI behavior evals when available
-> Review the diff
-> Fix verified problems
-> Stop when acceptance criteria pass
```

## 2. Comparison

### Solution A: Normal Single-agent Development

**Decision:** Not selected as the primary workflow.

**Pros:**

- Simplest and lowest coordination cost;
- Easy to understand and control;
- Suitable for small, short changes.

**Cons:**

- Requires more frequent user prompting;
- Long tasks may stop between phases;
- The implementing agent may also be the only reviewer.

**Why not choose it:** It would involve the user more often than necessary and provides weaker continuity and independent review for the complete MVP build.

### Solution B: Primary Agent + Goal Mode + Automatic Validation

**Decision:** Selected.

**Pros:**

- Can work independently through multiple implementation steps;
- Maintains one coherent view of frontend, backend, AI, and API contracts;
- Tests and stopping conditions reduce scope drift;
- Lower coordination cost than a permanent multi-agent team.

**Cons:**

- Requires clear goals and runnable validation commands;
- Still needs occasional human decisions;
- A poorly defined goal may produce unnecessary work.

**Why not choose it:** Not applicable—this is the selected solution. It should only be reconsidered if the project cannot define reliable completion criteria or if the user prefers manual approval after every change.

### Solution C: Multiple Agents from the Beginning

Example: separate frontend, backend, AI, and reviewer agents.

**Decision:** Not selected as the default.

**Pros:**

- Can reduce elapsed time for genuinely independent work;
- Useful for parallel research, testing, and review;
- Keeps noisy investigation outside the main implementation context.

**Cons:**

- Uses more tokens and adds coordination overhead;
- Parallel code edits can conflict;
- Frontend, backend, and AI share the same API and conversation model;
- Encourages premature separation for a modular-monolith MVP.

**Why not choose it:** The MVP is too small and tightly connected to benefit from permanent parallel implementation agents. Subagents are more valuable selectively for read-heavy reviews and investigation.

### Solution D: Automatic Loop, Scheduled Task, or Self-evolving System

**Decision:** Not selected during initial implementation.

**Pros:**

- Requires little ongoing user involvement;
- Useful for repeated maintenance or measurable optimization;
- Can perform many iterations when a reliable score exists.

**Cons:**

- Unsafe or ineffective without fixed success metrics and stopping conditions;
- May optimize the wrong behavior or expand scope;
- AI quality cannot be judged only by build and unit-test results;
- Scheduled tasks are designed mainly for recurring background work.

**Why not choose it:** The project does not yet have a stable implementation or eval baseline. An automatic improvement loop would have no trustworthy score to optimize and would add complexity before the MVP is validated.

## References

- [Long-running work and Goal mode](https://learn.chatgpt.com/docs/long-running-work)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Code review](https://learn.chatgpt.com/docs/code-review)
- [Iterate on difficult problems](https://learn.chatgpt.com/use-cases/iterate-on-difficult-problems)
- [Add evals to an AI application](https://learn.chatgpt.com/use-cases/ai-app-evals)
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations)
