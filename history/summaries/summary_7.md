# 8. Process Retrospective: What Could Have Been Improved in the PRD Creation Process

This section steps back from individual product decisions and reviews the **method we used to create the PRD**.

The goal is not to say "we should have avoided discussion". The discussions were valuable because they uncovered real product ambiguity.

The goal is:

> How can we reach the same quality faster in future projects?

---

# 8.1 What Worked Well

## 1. We challenged assumptions instead of only editing documents

A strong part of the process was that we did not immediately optimize wording.

For example:

Instead of asking:

> "How should we describe Job Requirement Analysis?"

we asked:

> "Should Job Requirement Analysis even exist as a PRD feature?"

This changed the problem from:

```
Writing problem
```

to:

```
Product definition problem
```

This produced bigger improvements.

---

## 2. We repeatedly returned to the core product hypothesis

Many decisions were evaluated against:

> Can this MVP validate whether AI-assisted matching helps recruiters understand candidate fit and initiate communication?

This prevented feature expansion.

The final MVP remained focused on:

- Input Job Description;
- Generate Matching Report;
- Support recruiter understanding;
- Enable communication action.

This aligns with the original MVP goal:

> Build a usable demo within one week and validate whether recruiters are willing to use an AI-assisted matching tool, understand candidate fit, and improve communication conversion. 

---

## 3. We treated document boundaries as a product design problem

A common mistake is to treat documents as formatting.

In this process, the document structure itself became part of the product architecture:

```
PRD
 |
 ├── AI System Design
 ├── Frontend Technical Design
 └── Backend Technical Design
```

The final PRD explicitly defines these responsibilities:

- PRD: product requirements;
- AI System Design: AI capability design and Agent workflow;
- Frontend Technical Design: UI implementation;
- Backend Technical Design: system architecture and APIs.



This made later implementation planning easier.

---

# 8.2 What Caused Unnecessary Iterations

## Issue 1: Feature List Was Defined Too Early

This was probably the biggest efficiency issue.

The initial thinking was closer to:

```
Product idea

↓

Possible features

↓

Write PRD
```

However, for AI products, a better order is:

```
Product problem

↓

Validation hypothesis

↓

User behavior

↓

Required capabilities

↓

Features
```

Because AI products often have many impressive capabilities that are not necessarily MVP requirements.

---

## How to Improve

Before creating the Feature List, add a short "Capability Classification" step:

Example:

| Item | Category |
|-|-|
| Matching Report | User Feature |
| Resume Preview | User Feature |
| Contact CTA | User Feature |
| Requirement Analysis | AI Capability |
| Evidence Matching | AI Capability |
| Candidate Profile Data Source | System Capability |

This would have prevented several later discussions.

---

# 8.3 Issue 2: User Definition Started From Business Roles

Initial thinking:

```
Recruitment process participants

↓

Product users
```

Better approach:

```
People interacting with the product

↓

Product users
```

The distinction:

| Role | Should appear in User Definition? |
|-|-|
| Recruiter using assistant | Yes |
| Candidate whose information is analyzed | No |
| Hiring Manager not using MVP | No |

---

## How to Improve

Before writing User Definition:

Create a simple table:

| Person | Uses Product? | Provides Data? | Receives Value? |
|-|-|-|-|
| Recruiter | Yes | Yes | Yes |
| Candidate | No | Yes | Indirect |
| Hiring Manager | No | No | Indirect |

Only the first category enters User Journey.

---

# 8.4 Issue 3: PRD and AI Design Boundary Should Be Defined Earlier

The biggest AI-product-specific challenge was:

> Internal reasoning looks like a product feature.

For example:

```
Requirement Analysis

Requirement Classification

Evidence Matching

Unknown Detection
```

These are valuable capabilities.

But they answer:

> How does AI work?

not:

> What does the user do?

---

## How to Improve

Before writing PRD:

Create a two-column list:

## Product Requirements

- User actions;
- User-visible outputs;
- User decisions.

## AI Requirements

- Reasoning process;
- Prompt strategy;
- Retrieval;
- Evaluation.

Then write separate documents.

---

# 8.5 Improved Future PRD Creation Process

Based on this project, I would recommend the following process.

---

# Phase 1: Product Foundation

## Output:

Project Alignment Document

Define:

- Product vision;
- Problem;
- User;
- MVP goal;
- Non-goals.

Questions:

1. Who uses the product?
2. What problem are we validating?
3. What does success look like?

---

# Phase 2: Validation Design

Before features:

Define:

```
Hypothesis

↓

Observable behavior

↓

Metric

↓

Interpretation
```

Example:

```
AI analysis improves understanding

↓

Recruiter reviews report

↓

Report usage + feedback

↓

Evaluate usefulness
```

---

# Phase 3: Capability Mapping

Separate:

```
User Features

System Capabilities

AI Capabilities
```

Only user-facing capabilities enter PRD Feature List.

---

# Phase 4: User Journey

Create:

```
User Goal

↓

User Action

↓

Product Response
```

Avoid including:

- AI workflow;
- Backend process.

---

# Phase 5: Functional Requirements

For each feature:

Define:

1. Purpose;
2. User story;
3. Functional requirements;
4. Acceptance criteria.

---

# Phase 6: Technical Design Documents

Generate:

## AI System Design

Answers:

> How does AI generate the result?

## Frontend Design

Answers:

> How does the user interact?

## Backend Design

Answers:

> How does the system support it?

---

# 9. Final Learning Summary

After this PRD creation process, the most important principles are:

## Principle 1

**Start from validation, not features.**

Bad:

```
What can AI do?
```

Better:

```
What behavior do we need to validate?
```

---

## Principle 2

**Separate user value from system intelligence.**

Bad:

```
AI capability = feature
```

Better:

```
User outcome
    ↓
Product feature
    ↓
AI capability
```

---

## Principle 3

**Define users by interaction, not business relationship.**

Bad:

```
Everyone involved in the process
```

Better:

```
Everyone who performs actions in the product
```

---

## Principle 4

**Keep MVP focused on learning speed.**

The goal of an MVP is not:

> Show everything the technology can do.

The goal is:

> Learn whether the core assumption is true.

---

## Overall Retrospective Conclusion

The PRD creation process took longer than expected (around two days), but most additional iterations were not wasted editing work. They uncovered deeper product decisions:

- What the product actually is;
- Who the user actually is;
- What the MVP is actually validating;
- What belongs in PRD versus technical documents.

The biggest improvement for future projects would not be "write faster".

It would be:

> Spend more time on product boundaries before writing detailed sections.

Doing that earlier would likely reduce rewriting while preserving the same depth of thinking.