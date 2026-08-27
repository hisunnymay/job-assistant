# Backend Technical Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant Backend Technical Design |
| Document Type | Backend Technical Design |
| Version | v0.6 |
| Status | Finalized |
| Owner | Mei Chang |
| Last Updated | 2026-08-27 |
| Related Documents | Project Alignment Document, Product Requirement Document, Lightweight AI Design Decision, AI System Design, Frontend Technical Design |


## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v0.6 | 2026-08-27 | Aligned the AI Service with AI System Design v1.1: selected Ark/LangChain/LangGraph integration, direct-PDF internal structured output, semantic validation, and a unified two-attempt retry budget; repaired the error-envelope Markdown fence. | Make the real-AI backend decisions authoritative and keep the document renderable while preserving persistence ownership and Section 5 API contracts. |
| v0.5 | 2026-08-27 | Selected a provider-neutral single-host Docker demo target with Nginx Basic Auth protecting the deployed UI and APIs. | Prepare a reproducible demo without adding user accounts, changing application API contracts, or deploying before approval. |
| v0.4 | 2026-08-27 | Added an internal request fingerprint for deletion-safe idempotent replay and restricted conversion to the generated-report session cohort. | Preserve the event contract after `ON DELETE SET NULL` and prevent contact-only sessions from inflating the MVP conversion metric. |
| v0.3 | 2026-08-27 | Selected a custom centralized tracking API and persistent User Behavior Event model, including privacy, idempotency, and retention rules. | Make S001 data queryable across sessions for MVP success metric evaluation. |
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
- Validate provider responses against the approved internal schemas and invariants;
- Render validated internal results into the existing text/Markdown message contract;
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

Purpose:

Persist the privacy-safe interaction events required for aggregate MVP usage and conversion evaluation.

The supported event names are:

- Page visits;
- Job description submission;
- Matching report generation;
- Resume preview click;
- Contact CTA click;
- Feedback submission.

Suggested information:

- `eventId`: primary key, client-generated string up to 64 characters;
- `eventName`: allowlisted event-name string;
- `sessionId`: indexed pseudonymous string up to 64 characters;
- `occurredAt`: client interaction timestamp with timezone;
- `receivedAt`: indexed server persistence timestamp with timezone;
- `requestFingerprint`: internal SHA-256 digest of the canonical accepted event metadata;
- `conversationId`: nullable indexed foreign key to Conversation with `ON DELETE SET NULL`.

`sessionId` is a random pseudonymous visit identifier and is not a user account or Conversation identifier. `conversationId` is nullable because page visits and job-description submissions can occur before a Conversation exists.

`requestFingerprint` is derived only from `eventId`, `eventName`, `sessionId`, `occurredAt`, and the original optional `conversationId`. It is not supplied by the frontend and contains no raw interaction content. User Behavior Event must not contain job descriptions, resume content, follow-up questions, feedback comments, contact data, prompts, provider payloads, IP addresses, user-agent strings, or other user-entered content. The implementation approach, idempotency rule, and retention period are defined in Section 7.5.


## 3.2 Data Storage Strategy



### Persistence Decision

MVP persistent data:
- Conversation;
- Conversation Message;
- Feedback;
- User Behavior Event.

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
```

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
| POST /api/tracking-events                         | Persist a user behavior event |


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

### User Behavior Event Submission

Request:

```json
{
  "eventId": "event_001",
  "eventName": "matching_report_generated",
  "sessionId": "session_001",
  "occurredAt": "2026-08-27T00:00:00.000Z",
  "conversationId": "conversation_001"
}
```

`eventName` must be one of:

- `page_visit`;
- `job_description_submitted`;
- `matching_report_generated`;
- `resume_previewed`;
- `contact_cta_clicked`;
- `feedback_submitted`.

`conversationId` is optional and should be omitted until the relevant Conversation exists. `eventId`, `sessionId`, and `conversationId`, when present, must be non-empty strings of at most 64 characters. `occurredAt` must be a valid RFC 3339 timestamp.

Response:

```json
{
  "success": true
}
```

The endpoint returns `200 OK` only after the event is persisted or an identical event with the same `eventId` already exists. Replaying an identical event is idempotent and must not create another row. Reusing an `eventId` with different event data returns `409 Conflict`. Invalid payloads return `400 Bad Request`; an unknown supplied `conversationId` returns `404 Not Found`.

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
| User Behavior Event    | Frontend detects, Backend validates and stores |
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

The AI Service performs provider-response parsing, strict internal-schema validation, cross-field invariant validation, and Markdown rendering before returning AI-generated content to the Service Layer. The internal schemas are defined by AI System Design v1.1 and do not change the Section 5 public response contracts.

### Successful Response

```text
AI Provider returns response

↓

AI Service validates structured result

↓

AI Service renders text/Markdown

↓

Service Layer stores AI Response as Conversation Message

↓

Return response to frontend
```

Validation should confirm that:

- A response was successfully returned;
- The response is not empty;
- The response matches the approved strict internal schema;
- The matching or follow-up cross-field invariants hold;
- The validated result can be rendered into frontend-renderable text/Markdown.

Runtime validation checks structure and deterministic internal consistency. It does not prove that model evidence is factually grounded or that a conclusion is high quality; those properties are measured by the approved AI evaluation set before release.

### Invalid AI Response

If the AI response is missing, unusable, or violates the approved schema or invariants, the AI Service applies the Section 7.6 retry decision. After the retry budget is exhausted:

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

If the external AI provider fails or times out, the AI Service applies the Section 7.6 retry decision. After a non-retryable failure or retry exhaustion:

- Do not store an AI response message;
- Log the failure for debugging;
- Return a user-friendly error to the frontend.

The Service Layer preserves the existing atomic transaction semantics while the AI Service performs its bounded attempts. A failed matching execution commits neither its new Conversation nor its messages. A failed follow-up commits neither its new question nor answer. Provider retry behavior must not bypass the existing completed-identical-follow-up replay rule or create duplicate messages.

### Storage

For the MVP:

- Store only the user-facing AI response as a Conversation Message;
- Do not store raw AI provider responses;
- Do not store provider-specific request or response payloads.

# 7. Deployment and Implementation Decisions

The following decisions are either finalized for the MVP or explicitly deferred to deployment. Each subsection states its current decision.

## 7.1 Deployment Strategy

Decision:

Prepare a provider-neutral single-host Docker Compose deployment bundle for the Demo phase. The bundle contains PostgreSQL, the FastAPI backend, the built React frontend, and an Nginx gateway. It is preparation only and must not be deployed without explicit approval.

The gateway exposes one browser origin, serves the frontend, and proxies backend routes internally. HTTPS termination and the actual hosting provider remain deployment-time choices because the intended recruiters' network accessibility, domain, and hosting account are not yet confirmed.

Considerations:

- Target users are primarily located in China, so frontend and backend accessibility should be considered;
- AI provider network accessibility may affect deployment choices;
- Development and testing environments should remain accessible for local/Codex-assisted development;
- Development and production databases may use different environments.

---

## 7.2 API Access Protection

Decision:

Use Nginx HTTP Basic Auth at the single public gateway for the deployed Demo. The gateway protects both the frontend and backend routes before requests reach the application. Credentials are supplied through an uncommitted password file and must not be stored in the repository.

Local development remains unprotected. This protection does not add user accounts, application authentication, permission management, browser-visible API keys, or changes to the Section 5 API contracts.

This mechanism is appropriate only for the bounded recruiter Demo. A broader production release would require a separate security decision.

---

## 7.3 Database Technology

Decision:

Deferred until implementation.

The MVP requires persistence for:

- Conversation;
- Conversation Message;
- Feedback;
- User Behavior Event.

The database should prioritize simple setup, development speed, and compatibility with the selected deployment environment.

---

## 7.4 AI Provider / Framework

Decision:

Use Volcengine Ark with model `doubao-seed-2-1-pro-260628` behind the existing AI Service boundary. The primary integration uses LangChain `ChatOpenAI` with Ark's OpenAI-compatible base URL. LangGraph owns temporary per-execution generation, validation, retry, and Markdown-rendering orchestration; it does not own or checkpoint persistent conversation state.

The AI Service supplies the exact predefined PDF through Base64 `file_data`, requests the strict internal Pydantic-backed schema defined in AI System Design v1.1, validates the result and its cross-field invariants, and renders text/Markdown for the unchanged Section 5 APIs. Backend PDF extraction, a résumé text mirror, RAG, and a frontend-visible structured-report contract remain outside the MVP.

Goal 7 must first exercise the fixed repository PDF and production-shaped matching and follow-up schemas through the primary `ChatOpenAI` path. If an Ark-specific PDF or strict-schema capability is not represented correctly, the Volcengine Ark Python SDK may be used inside the same AI Service and LangGraph boundary. If neither path supports the approved combination, stop for a design decision rather than changing the public API or adding extraction.

Provider configuration is validated by backend settings. The Ark API key remains a backend-only secret; base URL, model ID, and finite request timeout remain backend configuration. No real secret is committed, logged, persisted, or returned to the frontend.

Changing the provider must remain isolated to the AI Service and must not require changes to business workflows, persistence ownership, or frontend APIs.

---

## 7.5 User Behavior Tracking Implementation

Decision:

Use the custom `POST /api/tracking-events` endpoint and persist User Behavior Events in the existing MVP database. Centrally persisted events are the authoritative analytics source; browser storage is limited to a temporary delivery queue.

Tracking session and Conversation are separate concepts:

- Tracking session identifies a user's product visit and may exist before a Conversation is created;
- Conversation identifies a specific candidate-job evaluation context.

The Controller validates the HTTP payload and delegates to a tracking Service. The Service enforces the event allowlist, optional Conversation association, idempotency, and retention rules, then persists through the Repository Layer. Controllers must not access the database directly.

The backend stores only `eventId`, `eventName`, `sessionId`, `occurredAt`, server-generated `receivedAt`, the server-generated `requestFingerprint`, and optional `conversationId`. The fingerprint is a SHA-256 digest of the canonical accepted event metadata and preserves the original request identity if `conversationId` is later cleared. The backend must not log request bodies or persist raw interaction content, IP addresses, user-agent strings, secrets, prompts, or provider payloads as tracking data. Access to event-level data is limited to authorized MVP evaluators; product reporting should use aggregate counts and rates.

Events are retained for 90 days from `receivedAt`, covering the MVP evaluation period. Events older than 90 days must be removed by a documented maintenance operation; the MVP does not require a distributed scheduler or separate analytics service. Deleting a Conversation must not delete its historical metric event; the nullable foreign key is set to null.

The backend uses `eventId` as the unique idempotency key and compares retries against the immutable `requestFingerprint`. Identical retries return success without creating duplicates, including after Conversation deletion sets the relational `conversationId` to null. Tracking failures are returned through the tracking endpoint but must remain isolated from the recruiter-facing workflow by the frontend tracking boundary.

The MVP does not expose event-level tracking data or a recruiter-facing analytics API. Instead, it provides a documented internal aggregate report operation for authorized evaluators. For a requested evaluation period, the report returns total and distinct-session counts for each approved event name and calculates Contact Conversion Rate as:

```text
Distinct sessionId values with both contact_cta_clicked and matching_report_generated

/

Distinct sessionId values with matching_report_generated
```

The report must handle a zero denominator without returning an invalid numeric value. Event-level export and a visual Dashboard remain outside MVP scope.


## 7.6 AI Retry Strategy
Decision:

Use one unified budget of at most two provider attempts per matching-analysis or follow-up execution: one initial attempt and at most one retry.

The single retry may be used for:

- A transient connection or timeout failure;
- Provider rate limiting or temporary service unavailability;
- A response that fails the approved schema or cross-field invariant validation.

Do not retry authentication/authorization failure, invalid request, unsupported-model/capability error, safety refusal, or another permanent provider error. Disable library-level automatic retries so client behavior cannot multiply the workflow budget. Every attempt uses a finite backend-configured timeout, and Goal 7 must validate that timeout with the fixed PDF and gateway configuration.

After a non-retryable failure or retry exhaustion, the AI Service returns the existing safe AI-processing failure to the Service Layer. It must not persist an assistant message, expose raw provider details, or add background queues, evaluator loops, distributed retry infrastructure, or a new API contract.
