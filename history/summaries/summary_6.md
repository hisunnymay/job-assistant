# 7. Major Turning Point 5: Feature Boundary Refinement — Candidate Profile Data Source vs Resume Preview

## 7.1 Initial Approach

During the feature definition stage, we encountered an overlap:

- Candidate Profile Data Source;
- Resume Preview.

At first glance, both seemed to represent:

> Candidate information.

This created uncertainty:

- Are they the same feature?
- Should one be removed?
- Is resume access just another form of candidate data access?

This is a common ambiguity in AI products because the same information can exist in multiple layers.

---

# 7.2 Problem Identified

The key mistake was treating:

> "Information about the candidate"

as one single product concept.

However, candidate information has different roles.

The important distinction became:

## Who uses the information and for what purpose?

---



## Candidate Profile Data Source

Purpose:

> Provide information for AI analysis.

Relationship:

```text id="r7u5qf"
Candidate Information

↓

AI Processing

↓

Matching Report

↓

Follow-up Answers
```

The recruiter does not directly operate on this data source.

It is a system capability.

---



## Resume Preview

Purpose:

> Allow recruiters to access the original candidate information.

Relationship:

```text id="1r5c7y"
Resume

↓

Recruiter View / Download
```

This is a user-facing capability.

---



# 7.3 Turning Point

The key question became:

> Is this information used by the AI, or viewed by the user?

This created the final separation:


| Capability                    | Role                       |
| ----------------------------- | -------------------------- |
| Candidate Profile Data Source | AI input/context           |
| Resume Preview                | Recruiter-facing reference |


---



# 7.4 Final Decision



## F001 Candidate Profile Data Source

Position:

> A product/system capability that provides candidate information context required for AI-powered candidate-job fit analysis.

It may include:

- Resume content;
- Project experience;
- Other related candidate information.

Its purpose is:

- Generate Matching Report;
- Answer Follow-up Questions.

---



## F004 Resume Preview

Position:

> A recruiter-facing feature that provides direct access to the original resume.

It supports:

- Reviewing background details;
- Verifying AI analysis;
- Downloading the resume when needed.

---

The relationship became:

```text id="r1x9p3"
              Candidate Profile Data Source
                         |
                         |
              AI Candidate-Job Analysis
                         |
                         ↓
                  Matching Report
                         |
              --------------------
              |                  |
              ↓                  ↓

      Follow-up Questions    Resume Preview
                             
                         Recruiter Reference
```

---



# 7.5 Why This Change Was Important

This clarification solved several future problems.

## Frontend Design

Without this distinction, developers might ask:

> Where is the Candidate Profile page?

But the answer is:

There is no dedicated F001 page.

F001 is not a UI feature.

---



## Backend Design

Backend can now distinguish:

### Internal data:

```text id="n4c6v5"
Candidate Profile Data
```

from:

### User-accessible resource:

```text id="s9dz8g"
Resume File / Resume View
```

---



## AI Design

AI System Design can define:

- How candidate information is structured;
- How evidence is retrieved;
- How context is provided.

---



# 7.6 Could This Have Been Avoided Earlier?

Yes.

This issue came from a common AI product documentation problem:

> We started from data objects instead of user capabilities.

A better approach would be to classify every item before putting it into Feature List:

---



## Classification Framework

For every item:

### Question 1:

Does the user directly interact with it?

If yes:

→ User Feature

Example:

- Resume Preview;
- Contact CTA;
- Feedback.

---



### Question 2:

Does the system need it to generate outputs?

If yes:

→ System Capability

Example:

- Candidate Profile Data Source;
- Knowledge Base;
- Retrieval Context.

---



### Question 3:

Does it describe how AI reasons?

If yes:

→ AI Capability

Example:

- Requirement Classification;
- Evidence Matching.

---



# Learning 6: In AI Products, Separate Data Source, User Interface, and Intelligence Layer

A useful three-layer model:

```text id="v3yq8s"
Layer 1: User Experience

What can users see and do?

Examples:
- Report
- Resume
- Contact


Layer 2: Product Data

What information does the product manage?

Examples:
- Candidate profile
- JD
- Conversation history


Layer 3: Intelligence

How does AI process information?

Examples:
- Extraction
- Matching
- Reasoning
```

Many AI product requirements become confusing because these three layers are mixed together.

---



# Reflection

This was a smaller iteration compared with user definition or MVP scope, but it was important because it exposed a recurring challenge in AI product design:

Traditional software often separates:

- Data model;
- UI;
- Business logic.

AI products add another layer:

- Intelligence behavior.

The PRD becomes much clearer when these layers are explicitly separated.

---

