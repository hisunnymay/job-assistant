# Frontend Design Retrospective: Process Review and Learning Summary

## Outline

- [1. Purpose of This Review](#1-purpose-of-this-review)
  - [1.1 Goal](#11-goal)
- [2. Starting Point: Frontend Design Approach](#2-starting-point-frontend-design-approach)
  - [2.1 Initial Challenge](#21-initial-challenge)
  - [2.2 Final Understanding](#22-final-understanding)
  - [Learning 1: Frontend Technical Design Should Define User Interaction, Not Implementation Details](#learning-1-frontend-technical-design-should-define-user-interaction-not-implementation-details)
- [3. Major Design Decision 1: From UI Components to User Experience](#3-major-design-decision-1-from-ui-components-to-user-experience)
  - [3.1 Initial Thinking](#31-initial-thinking)
  - [3.2 Problem Identified](#32-problem-identified)
  - [3.3 Final Decision](#33-final-decision)
  - [Learning 2: Design From User Goals Before UI Structure](#learning-2-design-from-user-goals-before-ui-structure)
- [4. Major Design Decision 2: Separating Frontend Responsibility from Backend Capability](#4-major-design-decision-2-separating-frontend-responsibility-from-backend-capability)
  - [4.1 Problem Identified](#41-problem-identified)
  - [4.2 Final Decision](#42-final-decision)
  - [Learning 3: Frontend Should Render and Enable Interaction, Not Own Business Logic](#learning-3-frontend-should-render-and-enable-interaction-not-own-business-logic)
- [5. Major Design Decision 3: Avoiding Over-Specification for Vibe Coding](#5-major-design-decision-3-avoiding-over-specification-for-vibe-coding)
  - [5.1 Initial Concern](#51-initial-concern)
  - [5.2 Final Decision](#52-final-decision)
  - [Learning 4: Technical Design Should Guide Implementation Without Restricting Exploration](#learning-4-technical-design-should-guide-implementation-without-restricting-exploration)
- [6. Final Learning Summary](#6-final-learning-summary)
  - [Principle 1](#principle-1)
  - [Principle 2](#principle-2)
  - [Principle 3](#principle-3)



# 1. Purpose of This Review



## 1.1 Goal

This review summarizes the frontend design process for AI Job Fit Assistant.

The purpose is not only to document the final frontend design, but also to capture:

- Why certain frontend boundaries were chosen;
- Which decisions improved implementation clarity;
- Which design approaches should be reused in future projects.

The final Frontend Technical Design became the source of truth for:

- Frontend user interaction;
- Page structure;
- Information requirements;
- Frontend-backend responsibility boundaries.

It intentionally does not define:

- AI reasoning logic;
- Backend implementation;
- Detailed UI implementation choices.

---



# 2. Starting Point: Frontend Design Approach



## 2.1 Initial Challenge

When designing the frontend, the natural approach was to think from implementation:

```text
Page

↓

Components

↓

State

↓

API Integration
```

This is common in traditional software development.

However, for this MVP, the development approach is different:

- The frontend will be built through vibe coding;
- UI implementation may evolve during development;
- Better UI solutions may emerge during implementation.

Therefore, a highly detailed UI specification could become a constraint.

---



## 2.2 Final Understanding

The frontend technical design should focus on:

```text
User Goal

↓

User Interaction

↓

Required Information

↓

Frontend Responsibility
```

Instead of:

```text
Specific Component Implementation

↓

Specific UI Layout

↓

Specific Code Structure
```

The purpose of the document is to align the implementation direction while keeping flexibility.

---



## Learning 1: Frontend Technical Design Should Define User Interaction, Not Implementation Details

A frontend design document should answer:

- What can users do?
- What information should users see?
- What interactions should be supported?

It should avoid defining:

- Exact component hierarchy;
- UI libraries;
- Styling implementation;
- State management approach.

This is especially important when using an iterative development approach.

---



# 3. Major Design Decision 1: From UI Components to User Experience



## 3.1 Initial Thinking

The initial approach focused on frontend elements:

```text
Input Area

Report Area

Resume Area

Contact Area
```

This described visible UI parts but did not fully explain how users move through the product.

---



## 3.2 Problem Identified

The product is not a collection of independent pages.

The recruiter experience is a continuous workflow:

```text
Enter Job Description

↓

Review Matching Analysis

↓

Ask Follow-up Questions

↓

View Resume

↓

Contact Candidate
```

Therefore, designing only from UI sections could lose the overall user journey.

---



## 3.3 Final Decision

The frontend structure became:

```text
Job Assistant Workspace

├── Conversation Area
│
├── Contextual Action Area
│
└── Navigation
```

The design focuses on supporting the recruiter workflow inside one workspace.

The main principle:

> Organize the frontend around user tasks, not isolated screens.

---



## Learning 2: Design From User Goals Before UI Structure

A better frontend design sequence is:

```text
User Goal

↓

User Journey

↓

Interaction Area

↓

Implementation
```

rather than:

```text
Possible UI Components

↓

Try to create user flow
```

This reduces unnecessary pages and keeps the experience coherent.

---



# 4. Major Design Decision 2: Separating Frontend Responsibility from Backend Capability



## 4.1 Problem Identified

AI products create a common boundary challenge.

Some information is generated by AI, but the frontend displays it.

For example:

```text
Matching Analysis
```

could be misunderstood as a frontend feature.

However:

- AI decides the content;
- Backend provides the output;
- Frontend presents the result.

---



## 4.2 Final Decision

The responsibility boundary became:

```text
Frontend

- User interaction;
- Information presentation;
- UI state management.


Backend / AI System

- Business logic;
- AI processing;
- Data generation.
```

Examples:

Resume Preview:

```text
Frontend:
Display and provide access.

Backend:
Provide resume information/resource.
```

Matching Analysis:

```text
Frontend:
Render AI output.

AI System:
Generate analysis.
```

---



## Learning 3: Frontend Should Render and Enable Interaction, Not Own Business Logic

For AI products, avoid putting AI responsibility into frontend design.

A useful boundary:

```text
User sees → Frontend

System decides → Backend / AI System

System stores → Backend
```

This keeps documents independent and easier to maintain.

---



# 5. Major Design Decision 3: Avoiding Over-Specification for Vibe Coding



## 5.1 Initial Concern

Traditional technical documents often describe:

- Exact components;
- Detailed UI behavior;
- Implementation patterns.

However, for this MVP:

- Development speed matters;
- UI may improve during implementation;
- The developer and product designer iterate together.

Too much detail may reduce flexibility.

---



## 5.2 Final Decision

The frontend document defines:

- Workspace structure;
- User interactions;
- Required information;
- Integration assumptions.

It intentionally leaves open:

- Component library;
- Visual style;
- Detailed layout;
- Implementation approach.

---



## Learning 4: Technical Design Should Guide Implementation Without Restricting Exploration

A good technical design document should provide alignment, not replace implementation decisions.

The right level of detail is:

```text
Clear enough to avoid misunderstanding

+

Flexible enough to allow improvement
```

---



# 6. Final Learning Summary



## Principle 1

**Frontend design should start from user interaction, not implementation structure.**

A frontend exists to support user goals.

---



## Principle 2

**Keep frontend responsibility separate from AI and backend responsibility.**

Frontend should present information and enable interaction, while backend and AI systems handle processing.

---



## Principle 3

**For iterative development, technical documents should guide rather than constrain.**

Especially in MVP development, the best design is not the most detailed design.

It is the design that creates enough alignment while preserving room for improvement.



