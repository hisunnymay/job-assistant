# AI Job Fit Assistant  
# Project Alignment Document

## Document Information

| Field | Description |
|---|---|
| Project Name | AI Job Fit Assistant |
| Document Type | Project Alignment Document |
| Version | v0.2 |
| Status | Draft |
| Purpose | Record agreed product direction, documentation strategy, and key decisions before implementation |
| Owner | Mei Chang |

---

# 1. Project Overview

## 1.1 Product Vision

AI Job Fit Assistant is an AI-assisted job matching tool that helps recruiters quickly understand the relationship between job requirements and candidate experience.

The product aims to reduce the information gap between recruiters and candidates by transforming unstructured job descriptions and candidate information into structured requirement-evidence mappings.

---

## 1.2 Initial Validation Scenario

The initial validation scenario is:

> A candidate uses the product to improve the efficiency of recruitment communication.

The MVP focuses on a fixed candidate profile:

> Mei Chang

The product is initially designed to support Mei Chang’s job search process while maintaining a product direction that can potentially expand to broader recruitment scenarios.

---

# 2. Product Positioning

## 2.1 Core Positioning

The product is:

> An AI-assisted job matching tool.

The product is NOT:

- An AI capability showcase website;
- A resume generator;
- A recruitment decision system;
- A replacement for recruiters.

---

## 2.2 Core Value Proposition

The product helps recruiters answer:

> “How does this candidate’s experience match the requirements of this role?”

by providing:

- Structured job requirement analysis;
- Candidate evidence mapping;
- Missing information identification.

---

# 3. Product Principles

## 3.1 Evidence First

The product should prioritize evidence-based analysis.

The system should not make unsupported claims.

Example:

Incorrect:

> Candidate has RAG production experience.

Correct:

> No evidence of RAG production experience was found in the available candidate information.

---

## 3.2 Assist Decision Making, Not Replace Decision Making

The product supports recruiters by organizing and presenting information.

It should not make final hiring decisions.

Incorrect:

> This candidate is suitable for this position.

Correct:

> The candidate has evidence matching the following job requirements.

---

## 3.3 Transparency Over False Precision

The product should avoid meaningless AI-generated scores.

Instead of:

> Overall match score: 82%

Prefer:

- Strong match;
- Partial match;
- No evidence found.

The reasoning behind the result should be visible.

---

# 4. MVP Scope

## 4.1 MVP Goal

Build a usable demo within one week.

The MVP validates:

1. Whether recruiters are willing to use an AI-assisted matching tool;
2. Whether the tool can help recruiters understand candidate fit;
3. Whether the tool can improve recruitment communication conversion.

---

## 4.2 MVP Core User Flow

```text
Recruiter receives candidate information

↓

Visits AI Job Fit Assistant

↓

Inputs Job Description

↓

AI analyzes requirements

↓

AI maps requirements to candidate evidence

↓

Recruiter reviews matching report

↓

Recruiter decides whether to contact candidate
```

---

## 4.3 MVP Features

### Included

| Feature | Priority |
|---|---|
| Job Description Input | P0 |
| Job Requirement Analysis | P0 |
| Hard / Soft Requirement Classification | P0 |
| Candidate Knowledge Base | P0 |
| Requirement-Evidence Matching | P0 |
| Unknown Information Detection | P0 |
| Resume Preview | P0 |
| Contact CTA | P0 |
| Basic User Behavior Tracking | P0 |

---

## 4.4 MVP Excluded Features

The following features are intentionally excluded:

- Multi-candidate comparison;
- HR uploading other candidates’ resumes;
- Open-ended chatbot;
- Automated recruitment decision;
- Full recruitment SaaS workflow;
- Complete multilingual support;
- Complex user permission system.

---

# 5. Future Roadmap Direction

## Phase 1: Conversion Optimization

Potential features:

- Matching visualization;
- Requirement coverage charts;
- Limited follow-up assistant;
- Missing information collection;
- HR feedback loop.

---

## Phase 2: Product Transparency and Iteration Showcase

Goal:

Demonstrate continuous AI product development.

Potential features:

- Product evolution history;
- Roadmap display;
- Product design documentation.

---

## Phase 3: General Recruitment Assistant

Potential features:

1. Resume Upload;
2. Multi-candidate Analysis;
3. Candidate Comparison;
4. Interview Assistance.

---

# 6. Documentation Strategy

## 6.1 Documentation Set

The project maintains four separate documents.

```text
AI Job Fit Assistant Documentation

├── Product Requirement Document
├── AI System Design
├── Frontend Technical Design
└── Backend Technical Design
```

---

## 6.2 Document Responsibility

| Document | Responsibility |
|---|---|
| Product Requirement Document | Define product requirements, user problems, scope, features, roadmap |
| AI System Design | Define AI capabilities, Agent workflow, prompts, knowledge strategy |
| Frontend Technical Design | Define frontend implementation |
| Backend Technical Design | Define backend implementation |

---

## 6.3 Documentation Language Strategy

All documentation uses English as the source of truth.

| Document | Language |
|---|---|
| PRD | English |
| AI System Design | English |
| Frontend Technical Design | English |
| Backend Technical Design | English |
| Website UI | Chinese for MVP |

---

## 6.4 Localization Strategy

MVP does not implement full multilingual support.

However, the product design should remain compatible with future localization.

Requirements:

- Avoid hard-coded UI text;
- Keep language configuration separable;
- Avoid architecture decisions that block future multilingual support.

---

# 7. Documentation Structure Strategy

Each document should be:

- Long-term maintainable;
- Easy to review;
- Suitable for AI-assisted development;
- Independent but connected.

Each document should include:

## Document Information

Including:

- Version;
- Status;
- Owner;
- Related documents.

---

## Version Log

Purpose:

Record:

- What changed;
- Why it changed.

Example:

|Version|Date|Changes|Reason|
|-|-|-|-|
|v0.1|2026-08-20|Initial document created|Define project direction|

---

# 8. Document Dependency

The relationship between documents:

```text
                 Product Requirement Document
                              |
        ------------------------------------------------
        |                      |                       |
        ↓                      ↓                       ↓

 AI System Design   Frontend Technical Design   Backend Technical Design
                             
```

Additional dependency:

```text
AI System Design

        ↓

Backend Technical Design
```

PRD is the source of truth for product requirements.

Technical documents define implementation details based on PRD requirements.

Changes to product requirements should be reflected in related technical documents.

---

# 9. Current Key Decisions

## Decision 1

The product positioning is not limited to AI Product Manager recruitment.

Reason:

The fundamental problem is the difficulty of mapping candidate capabilities to job requirements.

AI PM recruitment is only the initial validation scenario.

---

## Decision 2

AI capability is not the core product value.

Reason:

The product solves a broader recruitment information matching problem.

AI-related capability analysis is only one application scenario.

---

## Decision 3

MVP focuses on structured matching analysis instead of conversational AI.

Reason:

The core validation goal is:

```text
JD Input

↓

Matching Report

↓

Contact Conversion
```

---

## Decision 4

MVP does not provide a single overall matching score.

Reason:

A single AI-generated score lacks transparency and may reduce user trust.

---

## Decision 5

English is used as documentation source language.

Reason:

- Better alignment with technical ecosystem;
- Easier AI-assisted development;
- Consistent terminology.

---

# 10. Next Steps

The project will proceed in the following order:

1. Finalize PRD;
2. Review and freeze PRD;
3. Create AI System Design;
4. Create Frontend Technical Design;
5. Create Backend Technical Design;
6. Start MVP implementation.

---

One small note: I kept **“Current Key Decisions”** instead of removing all decision-related content. This is slightly different from the removed “Decision Log”.

Reason:
- A maintained Decision Log is a process overhead;
- A short list of current product principles/decisions is useful context for future documents.

If later this section grows too much, we can remove it or merge it into Version Log.