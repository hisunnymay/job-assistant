# Backend Technical Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant Backend Technical Design |
| Document Type | Backend Technical Design |
| Version | v0.2 |
| Status | Finalized |
| Owner | Mei Chang |
| Last Updated | 2026-08-25 |
| Related Documents | Project Alignment Document, Product Requirement Document, Lightweight AI Design Decision, Frontend Technical Design |


## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v0.2 | 2026-08-25 | Finalized the backend design and selected Python with FastAPI. | Establish the backend implementation baseline before planning. |


# 1. Backend Design Goal

## 1.1 Backend Responsibility

The backend is responsible for providing the core business capabilities required by the AI Job Fit Assistant.

The backend is responsible for:

- Handling API requests from frontend;
- Managing business workflow;
- Preparing required context for AI processing;
- Integrating with AI services;
- Persisting required business data;
- Providing stable APIs for frontend consumption.

The backend is not responsible for:

- User interface rendering;
- Frontend interaction logic;
- AI prompt design details;
- AI reasoning logic itself.

---



## 1.2 Design Principles

### Design for MVP Validation

The backend should prioritize validating the core user journey within the one-week MVP scope.

Avoid unnecessary complexity such as:

- Microservices;
- Distributed architecture;
- Event-driven systems;
- Advanced infrastructure.

The system should remain simple and easy to modify.

### Keep Responsibilities Separated

Backend responsibilities should remain clearly separated between:

- API handling;
- Business workflow;
- Data access;
- AI integration.

For example, the Controller Layer should not contain business logic, directly access the database, or directly call AI providers.

### Define Business Entities Before Database Structures

The design should first define meaningful business entities and their relationships.

Database tables and storage implementation should follow those requirements rather than drive the design.

### Separate AI Capability from Backend Workflow

The backend should orchestrate AI capabilities without implementing AI reasoning itself.

Business workflow should remain independent from the specific AI provider so that the AI integration can be replaced without major changes to the backend or frontend.


# 2. Backend Architecture Overview



## 2.1 Architecture Approach

The backend technology stack is:

- Python;
- FastAPI.

The MVP architecture uses:

```text
Modular Monolith

+

Layered Architecture
```

Reason:

- The product scope is limited;
- Multiple independent services are unnecessary;
- A modular monolith provides enough separation while keeping development simple.

High-level structure:

```text
Backend Application

├── API Access Protection Layer
│
├── Controller Layer
│
├── Service Layer
│
├── AI Service
│
└── Repository Layer
```

---



## 2.2 System Components

| Layer                 | Responsibility             |
| --------------------- | -------------------------- |
| API Access Protection | Protect API access         |
| Controller            | Handle HTTP communication  |
| Service               | Execute business workflows |
| AI Service            | Provide AI capability      |
| Repository            | Manage data persistence    |

### API Access Protection Layer

Purpose:

Provide lightweight protection for backend APIs.

Responsibilities:

- Validate API access;
- Prevent unauthorized direct API usage.

Not responsible for:

- User accounts;
- User authentication;
- Permission management.

Implementation details are deferred.

---



### Controller Layer

Purpose:

Handle communication between frontend and backend.

Responsibilities:

- Receive HTTP requests;
- Validate basic request format;
- Call Service Layer;
- Return API responses.

Controller Layer should not:

- Contain business logic;
- Directly access database;
- Directly call AI providers.

---



### Service Layer

Purpose:

Coordinate backend business workflows.

Responsibilities:

- Execute business processes;
- Coordinate AI Service;
- Coordinate Repository Layer;
- Manage workflow execution.

---



### AI Service

Purpose:

Provide AI capabilities through an abstraction layer.

Responsibilities:

- Prepare AI requests;
- Call external AI providers;
- Handle AI responses;
- Hide AI implementation details.

The backend should not tightly couple business logic to a specific AI provider.

---



### Repository Layer

Purpose:

Provide data access abstraction.

Responsibilities:

- Store business data;
- Retrieve business data;
- Hide database implementation details.

For MVP:

A single Repository Layer is sufficient.

The Repository Layer may manage different data types through different operations.

Separate repositories for each entity are not required at this stage.

---


## 2.3 High-level Data Flow

The architecture dependency is:

```text
Frontend

↓

API Access Protection Layer

↓

Controller Layer

↓

Service Layer

        |
        |
        ├──────────────┐
        ↓              ↓

   AI Service     Repository Layer

        ↓              ↓

 External AI       Database
 Provider
```

This represents dependency direction, not execution order.

The actual execution flow depends on specific business scenarios.

# 3. Backend Data Model



## 3.1 Core Data Entities

The backend design defines business entities based on MVP requirements.

The goal is to identify meaningful business concepts rather than directly designing database tables.

---



### Candidate Resume

The Candidate Resume is the predefined resume of the fixed MVP candidate.

It is used for:

- AI candidate-job analysis;
- Recruiter preview and download.

Candidate management is not required for the MVP.

---



### Conversation

Purpose:

Maintain the persistent context for recruiter evaluation sessions.

Conversation is a persistent entity because:

- Matching Analysis and follow-up interactions belong to the same evaluation context;
- Follow-up answers depend on previous conversation history;
- AI requires conversation history to generate context-aware responses;
- Feedback may need to reference specific AI responses.

Relationship:

```text
Conversation

1

↓

N

Conversation Messages
```
Suggested information:

- conversationId
- created time

---



### Conversation Message

Purpose:

Represent individual user inputs and AI outputs within a conversation.

Example:

```text
Conversation

├── User Message
│   └── Job Description
│
├── AI Message
│   └── Matching Analysis
│
├── User Message
│   └── Follow-up Question
│
└── AI Message
    └── Follow-up Answer
```

Suggested information:

```text
Conversation Message

- messageId
- conversationId
- role
    - user
    - assistant
- messageType
    - job_description
    - matching_analysis
    - follow_up_question
    - follow_up_answer
- content
- created time
```

---


### Feedback

Purpose:

Collect user feedback after reviewing AI output.

Feedback should be associated with:

- Conversation Message

Relationship:

```text
Conversation Message

↓

Feedback
```

Suggested information:
- feedbackId
- conversationId
- messageId
- rating
- comment
- created time

### User Behavior Event

The product requires tracking:

- Page visits;
- Job description submission;
- Matching report generation;
- Resume preview click;
- Contact CTA click;
- Feedback submission.

The implementation approach is defined in Section 7.5.


## 3.2 Data Storage Strategy



### Persistence Decision

MVP persistent data:
- Conversation;
- Conversation Message;
- Feedback.

### Candidate Resume Resource

The predefined candidate resume is maintained as a static PDF resource rather than persistent business data.

For the MVP, the same resume file is used for:

- Recruiter preview and download;
- AI processing as candidate context.

The AI Service is responsible for providing the resume to the selected AI provider in a supported format.

Backend-side resume text extraction or preprocessing is not required for the MVP.

### Repository Strategy

For MVP:

Use a lightweight Repository Layer.

Responsibilities:

- Hide database implementation details;
- Provide data access methods;
- Separate business logic from storage.

The MVP does not require:

- Multiple repository classes;
- Multiple databases;
- Complex data access architecture.

# 4. Backend Processing Flow


## 4.1 Business Logic Flow



### Generate Matching Analysis

User flow:

```text
Recruiter submits Job Description

↓

Create Conversation

↓

Store Job Description as User Message

↓

Generate Matching Analysis

↓

Store AI Response Message

↓

Return result
```

---



### Answer Follow-up Questions

User flow:

```text
Recruiter submits follow-up question

↓

Store User Question Message

↓

Load Conversation Context

↓

Generate AI Answer

↓

Store AI Answer Message

↓

Return answer
```

---



### Submit Feedback

User flow:

```text
Recruiter submits feedback

↓

Identify target Conversation Message

↓

Store feedback

↓

Return submission result
```

---



### Resume Preview

User flow:

```text
Recruiter clicks View Resume

↓

Frontend requests resume

↓

Backend provides resume file

↓

Frontend displays PDF preview/download
```

---



## 4.2 Error Handling

The backend should provide meaningful errors while hiding internal implementation details.

### Error Response Format

API errors should use a consistent frontend-facing format:

```json
{
  "code": "ERROR_CODE",
  "message": "User-friendly error message"
}
Frontend may map error `code` values to localized user-facing messages; backend `message` should not be the sole source for UI localization.

Potential error categories:

### Invalid Request

Examples:

- Missing Job Description;
- Invalid feedback format.

Response:

```text
400 Bad Request
```

---



### AI Service Failure

Examples:

- AI provider unavailable;
- AI generation failure.

Response:

```text
500 Internal Server Error

or

Service unavailable response
```

---



### Data Storage Failure

Examples:

- Failed to store conversation messages;
- Failed to store feedback.

The backend should:

- Log internal details;
- Return user-friendly error messages.

---

### Invalid API Access

If API access validation fails:

- Reject the request before business processing;
- Return an access error without exposing internal details.




# 5. Backend Interface Design



## 5.1 API Overview

The MVP exposes the following APIs.


| API                                               | Purpose                    |
| ------------------------------------------------- | -------------------------- |
| POST /api/matching-analysis                       | Generate matching analysis |
| POST /api/conversations/{conversationId}/messages | Answer follow-up questions |
| GET /api/resume                                   | Provide resume file        |
| POST /api/feedback                                | Submit feedback            |


---



## 5.2 Request / Response Format



### Generate Matching Analysis

Request:

```json
{
  "jobDescription": "..."
}
```

Response:

```json
{
  "conversationId": "conversation_001",
  "messageId": "message_002",
  "content": "..."
}
```

---



### Follow-up Question

Request:

```json
{
  "question": "Does the candidate have AI Agent experience?"
}
```

Response:

```json
{
  "messageId": "message_003",
  "content": "..."
}
```

---



### Resume Preview

Request:

```http
GET /api/resume
```

Response:

```text
application/pdf
```

---



### Feedback Submission

Request:

```json
{
  "conversationId": "conversation_001",
  "messageId": "message_004",
  "rating": 5,
  "comment": "..."
}
```

Response:

```json
{
  "success": true
}
```

---



## 5.3 Integration Considerations



### Frontend-Backend Responsibility Boundary

Frontend:

- User interaction;
- Input collection;
- UI state management;
- Rendering backend responses.

Backend:

- Business workflow;
- AI processing;
- Data persistence;
- File access control.

---



### Data Ownership


| Data                   | Owner                                |
| ---------------------- | ------------------------------------ |
| Job Description Input  | Frontend collects, Backend processes |
| AI Generated Messages  | Backend generates and stores         |
| Resume File            | Backend provides                     |
| Feedback               | Frontend collects, Backend stores    |
| Contact Me Information | Frontend static content              |


---



### Integration Assumptions

- Frontend should not depend on AI implementation details.
- Backend APIs should expose business capabilities rather than database structures.
- AI provider changes should not require frontend changes.
- API contracts should remain stable during implementation iterations.
- For the MVP, AI-generated `content` is returned as text/Markdown that can be rendered directly by the frontend.

# 6. AI Integration Design
## 6.1 AI Request Flow

For the MVP, AI requests are initiated by the Service Layer and sent through the AI Service abstraction.

```
Service Layer

↓

Prepare required AI context

↓

AI Service

↓

External AI Provider

↓

AI Service receives response

↓

Return result to Service Layer
```

## 6.2 AI Context Management

The backend owns conversation context and is responsible for preparing the information required for each AI request.

The AI Service should not load or persist conversation data directly.

### Matching Analysis Context

Required context:

```text
Candidate Resume

+

Job Description
```

The Service Layer retrieves the predefined candidate resume and the submitted Job Description, then passes them to the AI Service.

### Follow-up Question Context

Required context:

```text
Candidate Resume

+

Full Conversation History
```

The Service Layer retrieves the persisted conversation and prepares the relevant conversation history before calling the AI Service.

Conversation history may include:

```text
Job Description

↓

Matching Analysis

↓

Previous Follow-up Questions

↓

Previous Follow-up Answers
```

## 6.3 AI Response Handling

The AI Service performs basic validation before returning AI-generated content to the Service Layer.

### Successful Response

```text
AI Provider returns response

↓

AI Service performs basic validation

↓

Service Layer stores AI Response as Conversation Message

↓

Return response to frontend
```

Basic validation should confirm that:

- A response was successfully returned;
- The response is not empty;
- The response is in a frontend-renderable format.

The backend does not evaluate whether the AI conclusion itself is correct or high quality.

### Invalid AI Response

If the AI response is missing or unusable:

```text
Invalid AI Response

↓

Record diagnostic information in application logs

↓

Do not store it as a Conversation Message

↓

Return AI processing error
```

Diagnostic logs should contain enough information to investigate the failure without unnecessarily storing complete raw AI requests or responses.

### AI Provider Failure

If the external AI provider fails or times out:

- Do not store an AI response message;
- Log the failure for debugging;
- Return a user-friendly error to the frontend.

### Storage

For the MVP:

- Store only the user-facing AI response as a Conversation Message;
- Do not store raw AI provider responses;
- Do not store provider-specific request or response payloads.

# 7. Unresolved Decisions

The following implementation decisions are intentionally deferred until development or deployment.

## 7.1 Deployment Strategy

Decision:

Deferred until implementation.

Considerations:

- Target users are primarily located in China, so frontend and backend accessibility should be considered;
- AI provider network accessibility may affect deployment choices;
- Development and testing environments should remain accessible for local/Codex-assisted development;
- Development and production databases may use different environments.

---

## 7.2 API Access Protection

Decision:

API access protection is required, but the exact mechanism is deferred.

Possible approaches include:

- Lightweight API key;
- Short-lived access token;
- Gateway or hosting-level protection.

The final approach depends on the frontend/backend deployment architecture and required security level.

---

## 7.3 Database Technology

Decision:

Deferred until implementation.

The MVP requires persistence for:

- Conversation;
- Conversation Message;
- Feedback.

The database should prioritize simple setup, development speed, and compatibility with the selected deployment environment.

---

## 7.4 AI Provider / Framework

Decision:

Deferred until implementation.

The backend AI Service abstraction should allow the MVP to use different implementations, such as:

- OpenAI API;
- Dify workflow;
- Other compatible AI providers.

Changing the AI provider should not require major changes to backend business logic or frontend APIs.

---

## 7.5 User Behavior Tracking Implementation

Decision:

Deferred until implementation.

The product requires tracking key user behaviors, but the implementation approach has not been selected.

Possible approaches include:

- Custom backend tracking API;
- Third-party analytics platform.

The final approach should prioritize MVP implementation speed and sufficient data for product evaluation. Tracking data should support association with the corresponding user session.

Tracking session and Conversation are separate concepts:

- Tracking session identifies a user's product visit and may exist before a Conversation is created;
- Conversation identifies a specific candidate-job evaluation context.

The exact tracking session implementation depends on the selected tracking approach.


## 7.6 AI Retry Strategy
Decision:

Deferred until implementation.

The MVP may either:

- Return an error immediately when an AI request fails; or
- Perform a limited automatic retry for transient provider failures.

The implementation should avoid complex retry infrastructure.
