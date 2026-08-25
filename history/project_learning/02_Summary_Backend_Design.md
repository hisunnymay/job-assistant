# Backend Design Retrospective: Process Review and Learning Summary

## 1. Purpose of This Review

### 1.1 Goal

This review summarizes the backend design process for AI Job Fit Assistant.

The purpose is to capture:

- How the backend architecture was simplified for the MVP;
- How responsibilities between backend, frontend, and AI were separated;
- Which backend design principles can be reused in future projects.

The final Backend Technical Design defines:

- Backend architecture;
- Core data entities;
- Business processing flows;
- API contracts;
- AI integration boundaries;
- Intentionally unresolved implementation decisions.

---

# 2. Starting Point: Backend Design Approach

## 2.1 Initial Challenge

The main challenge was deciding how much backend architecture should be designed before implementation.

A traditional backend design could quickly expand into:

```text
Database schema
↓
Repository structure
↓
Service structure
↓
API implementation
↓
Infrastructure decisions
```

However, this MVP has a one-week implementation scope.

Therefore, defining too many implementation details too early would create unnecessary complexity.

## 2.2 Final Understanding

The backend design should focus on:

```text
Business Capability
↓
Responsibility Boundary
↓
Data Relationship
↓
Processing Flow
↓
API Contract
```

while leaving implementation choices flexible when they do not affect product behavior.

### Learning 1: Backend Design Should Define System Boundaries Before Implementation Details

A backend technical design should make important system decisions clear without trying to design every class, database table, or infrastructure component.

---

# 3. Major Design Decision 1: Keep the Architecture Simple for MVP

## 3.1 Initial Concern

Backend systems can introduce many architectural options:

- Microservices;
- Event-driven architecture;
- Multiple repositories;
- Complex infrastructure;
- Distributed services.

These approaches may be useful at larger scale, but they do not help validate the current MVP.

## 3.2 Final Decision

The backend uses:

```text
Modular Monolith
+
Layered Architecture
```

with clear responsibilities across:

```text
API Access Protection
↓
Controller
↓
Service
├── AI Service
└── Repository
```

The architecture is designed to remain simple while keeping responsibilities separated. 

### Learning 2: Architecture Complexity Should Match the Product Stage

For an MVP, architecture should optimize for:

- Development speed;
- Clarity;
- Ease of modification;

rather than future scale that has not yet been validated.

---

# 4. Major Design Decision 2: Separate Backend Workflow from AI Capability

## 4.1 Problem Identified

AI products create an additional responsibility boundary.

The backend needs AI capabilities, but it should not own:

- Prompt design;
- AI reasoning;
- Matching logic itself.

At the same time, AI services should not directly control backend persistence or conversation state.

## 4.2 Final Decision

The responsibility boundary became:

```text
Service Layer
↓
Prepare required context
↓
AI Service
↓
External AI Provider
```

The backend owns:

- Business workflow;
- Conversation context;
- Persistence;
- API behavior.

The AI layer owns the generation capability required to produce matching analysis and follow-up answers. 

The AI Service also hides provider-specific details so that changing AI providers does not require major changes to backend business logic. 

### Learning 3: Treat AI as a Replaceable Capability, Not the Backend Architecture

Backend workflow should depend on an AI capability interface rather than a specific provider.

This keeps:

```text
Business Logic
≠
AI Provider Implementation
```

---

# 5. Major Design Decision 3: Model Business Concepts Before Database Tables

## 5.1 Initial Concern

It is easy to start backend design by immediately defining database tables.

However, the important question is first:

> What information does the backend actually need to manage?

## 5.2 Final Decision

The backend first defines core concepts such as:

- Candidate Resume;
- Conversation;
- Conversation Message;
- Feedback;
- User Behavior Event.

Conversation and messages maintain the evaluation context required for matching analysis and follow-up questions. 

The predefined Candidate Resume is treated separately as a static PDF resource rather than persistent business data. 

### Learning 4: Define Data From Business Meaning Before Storage Technology

A better sequence is:

```text
Business Concept
↓
Relationship
↓
Persistence Requirement
↓
Database Implementation
```

rather than designing database tables first.

---

# 6. Major Design Decision 4: Explicitly Preserve Implementation Flexibility

Some decisions affect architecture and should be defined early.

Others can safely remain open until implementation.

The backend therefore explicitly records unresolved decisions such as:

- Deployment strategy;
- API access protection mechanism;
- Database technology;
- AI provider/framework;
- Tracking implementation;
- AI retry strategy. 

### Learning 5: An Unresolved Decision Is Better Than an Accidental Assumption

Technical design does not need to answer every implementation question.

When a decision can safely wait, it should be marked as unresolved rather than silently invented during documentation.

---

# 7. Final Learning Summary

## Principle 1

**Keep backend architecture proportional to the MVP.**

Do not introduce complexity before the product requires it.

## Principle 2

**Separate business workflow, data access, and AI capability.**

Clear responsibility boundaries make implementation easier to change.

## Principle 3

**Model business concepts before database structures.**

Start from what the system needs to represent, not from tables.

## Principle 4

**Treat AI providers as replaceable implementation details.**

Backend business logic should not depend directly on a specific AI provider.

## Principle 5

**Resolve important behavior, but preserve implementation flexibility.**

A good technical design gives developers enough direction to avoid misunderstanding without removing room for implementation decisions.
