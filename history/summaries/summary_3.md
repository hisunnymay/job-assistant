# 4. Major Turning Point 2: From System Workflow to User Journey

## 4.1 Initial Approach

In the early PRD drafts, we described the MVP workflow using the steps required for the Agent to generate the final output.

The workflow looked like:

```text
Job Description Input

↓

Job Requirement Analysis

↓

Candidate Information Matching

↓

Evidence-based Matching Report

↓

Further Communication
```

This was a reasonable description from a system perspective because these are indeed the logical steps required to produce the matching result.

The Project Alignment Document also described similar internal processing steps:

```text
AI analyzes requirements

↓

AI maps requirements to candidate evidence

↓

Recruiter reviews matching report
```

---



# 4.2 Problem Identified

The problem was not that the workflow was incorrect.

The problem was:

> The same workflow was trying to represent two different things.

It mixed:

## User Journey

The question:

> What does the recruiter do?

Example:

```text
Recruiter enters JD

↓

Reviews report

↓

Decides whether to contact candidate
```

---



## AI Workflow

The question:

> How does the Agent generate the report?

Example:

```text
JD

↓

Requirement Extraction

↓

Requirement Classification

↓

Evidence Matching

↓

Gap Detection

↓

Report Generation
```

---

The confusion happened because AI products naturally expose internal reasoning as part of their value proposition.

For traditional software:

```text
User clicks button

↓

System processes data

↓

User receives result
```

The separation is obvious.

For AI products:

```text
User enters request

↓

Agent reasons

↓

Agent generates answer
```

The reasoning process itself can look like a product feature.

---



# 4.3 Turning Point

The key question became:

> "Would the recruiter actually perform this step?"

For each step:

## Job Requirement Analysis

Would recruiter do this?

No.

The recruiter provides the JD.

The Agent analyzes it.

---



## Hard / Soft Requirement Classification

Would recruiter do this?

No.

It is an internal interpretation capability.

---



## Requirement-Evidence Matching

Would recruiter do this?

No.

It is the core intelligence behind the report.

---



## Unknown Information Detection

Would recruiter do this?

No.

It is another internal analysis capability.

---



## Matching Report

Would recruiter interact with this?

Yes.

This is the actual product output.

---

This distinction allowed us to move:

From:

```text
Feature = every capability needed to generate result
```

To:

```text
Feature = user-visible capability that helps validate product value
```

---



# 4.4 Final Decision

The final PRD structure separated:

## User-facing Product Flow

```text
Job Description Input

↓

Matching Report

↓

Ask Follow-up Questions (Optional)

↓

Contact Candidate
```

---



## AI Internal Capability Flow

```text
Job Requirement Analysis

↓

Hard / Soft Requirement Classification

↓

Requirement-Evidence Matching

↓

Unknown Information Detection

↓

Matching Report Generation
```

---

This also affected the Feature List.

The initial feature list contained:

- Job Requirement Analysis;
- Hard / Soft Requirement Classification;
- Requirement-Evidence Matching;
- Unknown Information Detection;
- Matching Report.

The later understanding was:

The first four are not independent user features.

They are the internal capabilities required by the Matching Report.

The final PRD therefore positions Matching Report as the core user-facing capability.

---



# 4.5 Why This Change Was Important

This decision improved several later documents.

## For PRD

The product requirement remains focused:

> What value does the recruiter receive?

---



## For AI System Design

The Agent design becomes clearer:

> What capabilities are needed to generate that value?

---



## For Frontend Design

The interface becomes clearer:

The frontend does not need pages for:

- Requirement Analysis;
- Evidence Matching;
- Unknown Detection.

It needs:

- Input;
- Report display;
- Follow-up interaction;
- Contact action.

---



# 4.6 Could This Have Been Avoided Earlier?

Partially yes.

This iteration could have been reduced by introducing a simple classification step before creating the Feature List.

For every candidate feature, ask:

## Question 1

Does the user directly interact with it?

If yes:

→ Product Feature

---



## Question 2

Does it describe how AI/system reaches the result?

If yes:

→ Technical Capability

---

Example:


| Item                  | Classification    |
| --------------------- | ----------------- |
| Job Description Input | Product Feature   |
| Matching Report       | Product Feature   |
| Resume Preview        | Product Feature   |
| Requirement Analysis  | AI Capability     |
| Evidence Matching     | AI Capability     |
| Prompt Strategy       | AI Implementation |


---



# Learning 3: In AI Products, Separate "Reasoning Process" from "User Value"

A common mistake in AI product documentation is:

> Treating the model's internal process as product functionality.

A better approach:

Start from:

```text
User Problem

↓

Desired User Outcome

↓

User-facing Capability

↓

Required AI Capability
```

not:

```text
AI Capability

↓

Expose Everything as Features
```

---



# Reflection

This was probably the most important structural improvement in the PRD process.

The final PRD became much cleaner because it stopped explaining:

> "How the AI works"

and focused on:

> "What the recruiter can accomplish with the AI."

This boundary will also be useful when creating the next documents:

- AI System Design explains the reasoning process;
- Frontend Design explains interaction;
- Backend Design explains data/system support.

---

