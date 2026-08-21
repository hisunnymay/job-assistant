# AI Job Fit Assistant  
# Project Alignment Document

## Document Information

| Field | Description |
|---|---|
| Project Name | AI Job Fit Assistant |
| Document Type | Project Alignment Document |
| Version | v0.3 |
| Status | Draft |
| Purpose | Record agreed product direction, documentation strategy, and project-level decisions before implementation |
| Owner | Mei Chang |
| Last Updated | 2026-08-20 |

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

The initial product scenario is Mei Chang’s job search process.

However, the product positioning should remain general enough to support broader recruitment scenarios in the future.

---

# 2. Product Positioning

## 2.1 Core Positioning

The product is:

> An AI-assisted job matching tool.

The product is not:

- An AI capability showcase website;
- A resume generator;
- A recruitment decision system;
- A replacement for recruiters.

---

## 2.2 Core Value Proposition

The product helps recruiters understand:

> “How does this candidate’s experience match the requirements of this role?”

by providing:

- Structured job requirement analysis;
- Candidate evidence mapping;
- Missing information identification.

---

# 3. Product Principles

## 3.1 Evidence First

The product should prioritize evidence-based analysis.

The system should avoid unsupported conclusions.

Example:

Incorrect:

> Candidate has RAG production experience.

Correct:

> No evidence of RAG production experience was found in the available candidate information.

---

## 3.2 Assist Decision Making, Not Replace Decision Making

The product supports recruiters by organizing information.

It should not make final hiring decisions.

---

## 3.3 Transparency Over False Precision

The product should avoid unsupported numerical scoring.

Instead of:

> Overall match score: 82%

Prefer:

- Strong match;
- Partial match;
- No evidence found.

The reasoning behind the result should be understandable.

---

# 4. MVP Scope

## 4.1 MVP Goal

Build a usable demo within one week.

The MVP validates:

1. Whether recruiters are willing to use an AI-assisted matching tool;
2. Whether the tool helps recruiters understand candidate fit;
3. Whether the tool improves recruitment communication conversion.

---

## 4.2 MVP Core User Flow

```text
Recruiter receives candidate information

↓

Visits AI Job Fit Assistant

↓

Inputs Job Description

↓

AI generates Matching Report

↓

Recruiter reviews Matching Report

↓

Recruiter decides whether to contact candidate
```

---

## 4.3 MVP Features

| Feature | Priority |
|---|---|
| Candidate Profile Data Source | P0 |
| Job Description Input | P0 |
| Matching Report | P0 |
| Resume Preview | P0 |
| Ask Follow-up Questions | P1 |
| Contact CTA | P0 |
| Basic User Behavior Tracking | P0 |
| Report Feedback | P1 |

---
## 4.4 Core Matching Capabilities
| Capability | Description |
|---|---|
| Requirement Analysis | Analyze and structure key requirements from the provided job description |
| Hard / Soft Requirement Classification | Classify requirements based on their importance and evaluation criteria |
| Requirement-Evidence Matching | Map job requirements to relevant candidate evidence |
| Unknown Information Detection | Identify requirements where sufficient candidate evidence is unavailable |

## 4.5 MVP Excluded Features

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

The project maintains four separate documents:

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
| Product Requirement Document | Define product requirements, user problems, scope, features, and roadmap |
| AI System Design | Define AI capabilities, Agent workflow, knowledge strategy, and AI-related requirements |
| Frontend Technical Design | Define frontend implementation based on product requirements |
| Backend Technical Design | Define backend implementation based on product requirements and AI system requirements |

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

However, product design should remain compatible with future localization.

Requirements:

- Avoid hard-coded UI text;
- Keep language configuration separable;
- Avoid architecture decisions that block future localization.

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
|v0.2|2026-08-20|Updated documentation structure|Separate product and technical documents|
|v0.3|2026-08-20|Updated document dependency model and roadmap ordering|Improve documentation consistency|

---
Sure. Please replace Section 8 with the following version:

---

# 8. Document Dependency

The relationship between documents:

```text
                    Product Requirement Document
                               |
        ------------------------------------------------
        |                      |                       |
        ↓                      ↓                       ↓

 AI System Design      Frontend Technical Design   Backend Technical Design


        AI System Design
                |
                ↓

       Backend Technical Design


 Frontend Technical Design  ↔  Backend Technical Design
                |
                ↓

            API Contract
```

## Dependency Explanation

- **Product Requirement Document → AI System Design**
  
  PRD defines required product capabilities and user-facing behaviors.  
  AI System Design defines how AI-related capabilities are designed and implemented.

- **Product Requirement Document → Frontend Technical Design**
  
  PRD defines user flows, interface requirements, and product interactions.  
  Frontend Technical Design defines how these requirements are implemented on the frontend.

- **Product Requirement Document → Backend Technical Design**
  
  PRD defines functional requirements and business logic.  
  Backend Technical Design defines the backend services and infrastructure required to support these requirements.

- **AI System Design → Backend Technical Design**
  
  AI System Design provides AI-specific implementation requirements, such as AI workflows, model integration, and AI-related processing logic. Backend Technical Design needs to support these capabilities.

- **Frontend Technical Design ↔ Backend Technical Design**
  
  Frontend and backend communicate through API contracts.

  The API Contract defines:
  - Request formats;
  - Response formats;
  - Data structures;
  - Error handling rules;
  - Communication interfaces between frontend and backend.

---

## Documentation Principle

- PRD is the source of truth for product requirements.
- Technical documents define implementation details based on PRD requirements.
- Technical documents should not redefine product requirements without updating PRD.
- Changes affecting interfaces between frontend and backend should update the API Contract accordingly.


# 9. Current Product Decisions

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

AI-related capability analysis is one application scenario.

---

## Decision 3

MVP focuses on structured matching analysis instead of conversational AI.

Reason:

The initial validation flow is:

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
