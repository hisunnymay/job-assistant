# PRD Creation Retrospective: Process Review and Learning Summary

## 1. Purpose of This Review

### 1.1 Goal

This review aims to understand how the AI Job Fit Assistant PRD evolved from an initial product idea into a structured product requirement document, and extract reusable principles for future product design work.

The focus is not only the final PRD quality, but also:

- How decisions were made;
- Why certain directions changed;
- Which iterations were necessary;
- Which iterations could have been avoided with a better process.

The final PRD became the source of truth for:

- Product scope;
- User scenarios;
- Functional requirements;

while explicitly separating responsibilities from:

- AI System Design;
- Frontend Technical Design;
- Backend Technical Design.

---



# 2. Starting Point: Initial Product Definition



## 2.1 Original Starting Point

At the beginning, the product idea was already relatively clear:

> Build an AI-assisted job matching tool that helps recruiters understand how a candidate's experience matches a job requirement.

The original product concept focused on:

- Parsing Job Description;
- Understanding candidate experience;
- Matching requirements with evidence;
- Helping recruiters decide whether to continue communication.

This core idea remained stable throughout the PRD process.

The final PRD still describes the product as:

> "an AI-assisted job matching tool that helps recruiters quickly understand the relationship between job requirements and candidate experience." 

The biggest changes were not about **what the product is**, but about:

- How to define its boundaries;
- How to represent users;
- How to separate product requirements from implementation details.

---



# 2.2 Initial Challenges

The first version of thinking had several natural ambiguities caused by the nature of AI products.

Unlike traditional software, an AI product often has three different layers:

```
User Value Layer

        ↓

Product Feature Layer

        ↓

AI Capability Layer
```

At the beginning, these layers were not fully separated.

For example:

```
Job Requirement Analysis

Hard / Soft Requirement Classification

Requirement-Evidence Matching

Unknown Information Detection

Matching Report
```

were initially treated similarly.

However, later we recognized:

- The first four are **internal AI capabilities**;
- Matching Report is the **user-facing product output**.

This eventually led to the document boundary:

- PRD defines user-facing requirements;
- AI System Design defines Agent workflow and AI capability implementation.

This boundary is now explicitly reflected in the PRD:

> AI System Design defines AI capability design, Agent workflow, knowledge strategy, and AI-related implementation requirements. 

---



# 2.3 Initial Assumption vs Final Understanding



## Initial Assumption

The product could be described by listing all capabilities involved in generating the result.

Example:

```
Input JD

↓

Analyze Requirements

↓

Classify Requirements

↓

Match Evidence

↓

Detect Missing Information

↓

Generate Report
```

This is a natural engineering-oriented view.

---



## Final Understanding

A PRD should describe:

> What value the user receives.

Not:

> Every internal step required to create that value.

Therefore:

PRD:

```
Job Description Input

↓

Matching Report

↓

Communication Decision
```

AI Design:

```
Requirement Analysis

↓

Classification

↓

Evidence Matching

↓

Unknown Detection

↓

Report Generation
```

---



# Learning 1: Define Document Boundaries Before Writing Detailed Features

The biggest efficiency improvement for future PRDs would be:

Before writing the feature list, first answer:

## Question:

"Is this document describing:

A. User value?

B. Product behavior?

C. System implementation?"

A simple classification table could prevent many iterations:


| Item                        | Belongs to      |
| --------------------------- | --------------- |
| User sees matching report   | PRD             |
| User clicks contact CTA     | PRD             |
| Agent extracts requirements | AI Design       |
| Prompt strategy             | AI Design       |
| Database storage            | Backend Design  |
| Component layout            | Frontend Design |


---

