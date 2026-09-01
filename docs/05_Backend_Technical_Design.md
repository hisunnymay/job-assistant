# Backend Technical Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant Backend Technical Design |
| Document Type | Backend Technical Design |
| Version | v1.3 |
| Status | Finalized |
| Owner | Mei Chang |
| Last Updated | 2026-09-01 |
| Related Documents | Project Alignment Document, Product Requirement Document, Lightweight AI Design Decision, AI System Design, Frontend Technical Design |


## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v1.3 | 2026-09-01 | Changed the dashboard's `resumePreviews` and `contactCtaClicks` values to distinct non-test session counts while preserving the existing aggregate response shape and conversion cohort calculation. | Prevent repeated actions within one browser-tab session from inflating candidate-exploration and contact-intent metrics. |
| v1.2 | 2026-09-01 | Added server-owned Tracking Session test classification, retroactive whole-session metric exclusion, an idempotent test-mode designation endpoint, and an aggregate dashboard endpoint with shared inclusive date filtering. | Implement PRD v0.9 while preserving privacy-safe event payloads, layered ownership, existing AI behavior, and the prohibition on event-level analytics exposure. |
| v1.1 | 2026-08-28 | Designated the approved Hong Kong host and `sunnydemo.me` as the current recruiter-production environment; made production UI/API access public without Basic Auth; accepted bounded public-exposure risk while retaining HTTPS, immutable images, Ark spend controls, privacy-safe diagnostics, backup/restore, and local protected-demo validation. | Align the authoritative deployment boundary with the user's approved production decision and public recruiter access without treating provider-side spend limits as general API abuse protection. |
| v1.0 | 2026-08-28 | Finalized the local development/test, optional Hong Kong staging, and preferred mainland Beijing production boundaries; added the provider/domain/ICP pre-purchase gate, immutable digest-based release path, production-fix prohibition, and live validation requirements; aligned the stale database-decision text with the already implemented PostgreSQL architecture. | Make the MVP deployment path actionable without prematurely purchasing infrastructure, weakening release controls, treating production as a development environment, or leaving contradictory deployment dependencies. |
| v0.9 | 2026-08-27 | Defined separate second-attempt request behavior for invalid structured results and transient provider failures, safe Markdown rendering, a bounded gateway timeout, and a privacy-safe Mini validation record. | Improve strict-output recovery and end-to-end request safety without changing the public API, retry ceiling, persistence ownership, or default model. |
| v0.8 | 2026-08-27 | Replaced request-time PDF input with the user-verified fixed résumé Markdown as AI context while retaining the paired PDF for recruiter preview/download. | The fixed-candidate MVP can avoid repeated document parsing and use a simpler, more reliable text-only provider path without changing public APIs or adding upload scope. |
| v0.7 | 2026-08-27 | Corrected the real-AI transport to Ark's Responses API with inline Base64 PDF input, strict Responses structured output, and thinking disabled. | Provider clarification established the documented PDF endpoint while preserving the approved AI Service, persistence, and public API boundaries. |
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
- Classifying tracking sessions and returning privacy-safe aggregate dashboard metrics;
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

### Tracking Session

Purpose:

Represent the pseudonymous browser-tab session used for aggregate metric deduplication and server-owned test-mode classification. It is not a user account and must not be used to infer a person.

Suggested information:

- `sessionId`: primary key, client-generated random string up to 64 characters;
- `isTest`: server-owned boolean, default `false`;
- `createdAt`: server timestamp;
- `testModeActivatedAt`: nullable server timestamp.

Relationship:

```text
Tracking Session

1

↓

N

User Behavior Events
```

Once `isTest` becomes `true`, it is not reverted. Exiting test mode creates a new non-test `sessionId`; this prevents one tracking session from mixing excluded test activity with later production activity. The entity contains no login identifier, IP address, user-agent string, or user-entered content.

---



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
- `sessionId`: indexed relationship to Tracking Session;
- `occurredAt`: client interaction timestamp with timezone;
- `receivedAt`: indexed server persistence timestamp with timezone;
- `requestFingerprint`: internal SHA-256 digest of the canonical accepted event metadata;
- `conversationId`: nullable indexed foreign key to Conversation with `ON DELETE SET NULL`.

`sessionId` is a random pseudonymous visit identifier and is not a user account or Conversation identifier. Event ingestion creates the corresponding Tracking Session when it does not yet exist and must never reset an existing test session to non-test. `conversationId` is nullable because page visits and job-description submissions can occur before a Conversation exists.

`requestFingerprint` is derived only from `eventId`, `eventName`, `sessionId`, `occurredAt`, and the original optional `conversationId`. It is not supplied by the frontend and contains no raw interaction content. User Behavior Event must not contain job descriptions, resume content, follow-up questions, feedback comments, contact data, prompts, provider payloads, IP addresses, user-agent strings, or other user-entered content. The implementation approach, idempotency rule, and retention period are defined in Section 7.5.


## 3.2 Data Storage Strategy



### Persistence Decision

MVP persistent data:
- Conversation;
- Conversation Message;
- Feedback;
- Tracking Session;
- User Behavior Event.

### Candidate Resume Resource

The predefined candidate résumé is maintained as one approved static resource pair rather than persistent business data:

- `mei_chang_resume.pdf` is the recruiter preview/download artifact;
- The user-verified `mei_chang_resume.md` is the AI runtime context.

The AI Service verifies the approved Markdown filename and SHA-256 before sending its UTF-8 text to the selected provider. The PDF and Markdown must not be edited independently; replacing either artifact requires renewed verification and digest updates.

Request-time PDF extraction or preprocessing, résumé upload/management, and independently editable candidate data remain outside the MVP.

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



### Designate Test Mode

```text
Frontend submits current sessionId after the approved hidden gesture

↓

Controller validates the request

↓

Tracking Service creates or loads the Tracking Session and sets isTest = true

↓

Repository commits the designation

↓

Backend acknowledges active test classification
```

The operation is idempotent and one-way for a given `sessionId`. It changes analytics classification only and does not alter Conversation, Feedback, AI Service, provider selection, or recruiter-facing business behavior.

---



### Retrieve Data Dashboard

```text
Frontend requests all retained data or one inclusive date range

↓

Controller validates that both dates are present or both are omitted

↓

Analytics Service converts inclusive Asia/Shanghai dates to one half-open timestamp interval

↓

Repository aggregates non-test User Behavior Events only

↓

Service returns one privacy-safe aggregate response
```

Supporting metrics count accepted events. Contact Conversion Rate deduplicates qualifying events by `sessionId`; it does not count people and does not use raw event counts as its numerator or denominator.

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
| POST /api/tracking-sessions/test-mode             | Designate a tracking session as test mode |
| GET /api/dashboard                                | Return aggregate dashboard metrics |


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



### Test-mode Session Designation

Request:

```json
{
  "sessionId": "session_001"
}
```

Response:

```json
{
  "success": true,
  "sessionId": "session_001",
  "testMode": true
}
```

`sessionId` must be a non-empty string of at most 64 characters. The endpoint creates the Tracking Session when necessary or idempotently preserves its existing `isTest = true` state, then returns `200 OK` only after the designation is committed. It never changes a test session back to non-test. Invalid payloads return `400 Bad Request`; persistence failure returns the existing safe server-error envelope.

The designation applies to every User Behavior Event with that `sessionId`, including an event persisted before designation or delivered from the browser queue afterward. The endpoint does not change AI execution or business-data persistence. It is a hidden testing convenience, not authentication; the current public production boundary does not add user accounts or permissions for this endpoint.

---



### Data Dashboard Aggregate

Request:

```http
GET /api/dashboard
GET /api/dashboard?startDate=2026-08-01&endDate=2026-09-01
```

`startDate` and `endDate` are optional as a pair and use `YYYY-MM-DD`. Omitting both requests all events currently retained under Section 7.5. Supplying one without the other, using an invalid date, or using a start date later than the end date returns `400 Bad Request`.

For a custom range, both calendar dates are inclusive in `Asia/Shanghai` (`UTC+8`). The backend converts them to a half-open timestamp interval from the start date at `00:00:00` inclusive to the day after the end date at `00:00:00` exclusive and filters by `occurredAt`.

Response:

```json
{
  "reportingPeriod": {
    "mode": "custom",
    "startDate": "2026-08-01",
    "endDate": "2026-09-01",
    "timezone": "Asia/Shanghai"
  },
  "updatedAt": "2026-09-01T02:00:00.000Z",
  "contactConversion": {
    "rate": 0.423,
    "numerator": 128,
    "denominator": 303
  },
  "eventTotals": {
    "pageVisits": 12845,
    "jobDescriptionSubmissions": 1203,
    "matchingReportsGenerated": 303,
    "resumePreviews": 1874,
    "contactCtaClicks": 128,
    "feedbackSubmissions": 56
  }
}
```

`reportingPeriod.mode` is `all_retained` when both query parameters are omitted; in that mode `startDate` and `endDate` are `null` and the frontend labels the period as all available data within the 90-day retention boundary. `updatedAt` is the latest `receivedAt` among included non-test events and is `null` when the result contains no events.

`contactConversion.rate` is a decimal ratio between `0` and `1`, calculated from distinct `sessionId` values according to PRD Section 2.2. It is `null` when `denominator` is zero. Within `eventTotals`, `pageVisits`, `jobDescriptionSubmissions`, `matchingReportsGenerated`, and `feedbackSubmissions` count accepted events; `resumePreviews` and `contactCtaClicks` count distinct `sessionId` values. Every field uses the same reporting period and excludes Tracking Sessions where `isTest = true`.

The endpoint returns aggregate values only. It must not return event records, `sessionId` values, Conversation identifiers, timestamps for individual interactions, user-entered content, or candidate content.

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
| Tracking Session       | Frontend creates identifier, Backend owns test classification |
| User Behavior Event    | Frontend detects, Backend validates and stores |
| Dashboard Aggregate    | Backend calculates, Frontend filters and renders |
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

The AI Service performs provider-response parsing, strict internal-schema validation, cross-field invariant validation, and Markdown rendering before returning AI-generated content to the Service Layer. The internal schemas are defined by AI System Design v1.3 and do not change the Section 5 public response contracts.

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

If the first AI response is missing, unusable, or violates the approved schema or invariants, the AI Service applies the Section 7.6 invalid-output retry behavior. After the retry budget is exhausted:

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

For the default 180-second provider-attempt timeout and two-attempt application ceiling, the prepared Nginx demo gateway uses a finite 400-second upstream read/send timeout. This prevents the gateway from returning a 60-second timeout while the bounded backend workflow is still active. Goal 9 must revalidate this value if the provider timeout or release gateway changes.

Decision:

Use the same provider-neutral single-host Docker Compose bundle across production-shaped environments. The bundle contains PostgreSQL, the FastAPI backend, the built React frontend, and an Nginx gateway. The gateway exposes one browser origin, serves the frontend, and proxies backend routes internally.

Environment boundaries:

- **Development and deterministic testing:** Run Docker Compose locally on the developer Mac. Codex implements bug fixes and feature iterations locally and runs normal automated tests with Mock AI and no provider network dependency. Ark live tests remain explicit, bounded, separately approved, and opt-in.
- **Recruiter production:** Use the user-approved single Hong Kong host at `https://sunnydemo.me`. It runs the same immutable-image, single-host Compose topology as the release candidate and is the only active production environment for the current MVP.
- **Future mainland environment:** A mainland China deployment is deferred and is not required for the current production designation. If later requested, it requires a new provider/domain/ICP, cost, network-access, data-migration, and cutover decision; Hong Kong and mainland must not become unplanned dual-active production systems.

Build and release:

- Build immutable production-platform images locally or in CI. Prefer CI for reproducibility; local Buildx is an acceptable MVP fallback only when the target CPU architecture is explicit and a clean build is verified;
- Distribute application images through an approved registry or a bounded local-to-host image transfer for the single-host MVP, and pin every deployed Compose service to an immutable registry digest or verified local content ID;
- Record the deployed and immediately preceding digests so application rollback is exact;
- Do not clone from GitHub, depend on Docker Hub for application images, or build source on the production server;
- Do not edit source or running containers in production. For production defects, inspect privacy-safe diagnostics, reproduce and fix locally, run the required validation, publish a new immutable image, and redeploy by digest.

Hong Kong production gate:

- The user approved the Hong Kong provider/region, existing server, `sunnydemo.me`, HTTPS certificate issuance, public recruiter access, Ark activation, and deployment action for this release;
- Keep the Ark key and database secret outside Git and images, and keep certificate and database backup ownership explicit;
- Record the server commitment/free-trial end date and certificate expiry/renewal path so continued availability does not depend on an unnoticed external expiration;
- Any new infrastructure purchase, domain transfer, future mainland filing, provider migration, or material recurring cost remains a separate approval.

Production validation before recruiter release:

- Verify HTTP-to-HTTPS redirection, certificate validity, HSTS, and intentional public access to the UI and API routes without Basic Auth;
- Complete production-shaped matching and follow-up calls through Ark without exposing submitted or generated content in diagnostics;
- Verify PostgreSQL persistence, backup and restore, atomic failure behavior, and completed-identical-follow-up replay;
- Verify the finite backend/gateway timeout and safe retry-exhaustion behavior;
- Record active immutable image content IDs and, after the next release creates a preceding version, verify rollback before restoring the release images;
- Test accessibility and the complete recruiter journey from representative intended recruiter networks.

The first production release has no preceding application image to exercise as a rollback target. Its verified active content IDs and database backup establish the rollback baseline for the next release; this limitation must remain visible in the implementation record.

---

## 7.2 API Access Protection

Decision:

Expose the current recruiter-production UI and Section 5 API routes publicly through the single Nginx HTTPS gateway without Basic Auth or application user accounts. This is an explicit, user-approved access decision for the current MVP.

The repository's protected local demo harness may continue to use Basic Auth for deterministic gateway regression, but the Hong Kong production overlay removes both the Nginx authentication directives and password-file mount. This does not add application authentication, permission management, browser-visible API keys, or changes to the Section 5 API contracts.

Ark-side quotas or rate limits can bound model spend, but they do not prevent repeated public API requests, database growth, or non-AI traffic. The user accepted that current exposure risk and plans to configure Ark constraints. Application/gateway abuse controls, monitoring, and host hardening remain follow-up production work if the audience broadens or traffic warrants them.

---

## 7.3 Database Technology

Decision:

Use PostgreSQL for local development, deterministic testing, and recruiter production. Database access remains behind the Repository Layer. Each environment uses an isolated database; production data must not be copied into local development as a debugging shortcut.

For the single-host MVP, PostgreSQL runs as part of the Docker Compose bundle with a persistent volume. Before recruiter release, document and verify backup, restore, migration, and rollback procedures. A managed database, replica, or multi-host failover topology remains outside the MVP unless a later reliability requirement justifies a separate design decision.

The MVP requires persistence for:

- Conversation;
- Conversation Message;
- Feedback;
- User Behavior Event.

The database should prioritize simple setup, development speed, and compatibility with the selected deployment environment.

---

## 7.4 AI Provider / Framework

Decision:

Use Volcengine Ark with model `doubao-seed-2-1-pro-260628` behind the existing AI Service boundary. The primary integration uses LangChain `ChatOpenAI` with Ark's OpenAI-compatible base URL and `use_responses_api = true`. LangGraph owns temporary per-execution generation, validation, retry, and Markdown-rendering orchestration; it does not own or checkpoint persistent conversation state.

The AI Service verifies and supplies the exact user-approved `mei_chang_resume.md` as a stable UTF-8 `input_text` block before dynamic job-description or conversation content. It requests the strict internal Pydantic-backed schema defined in AI System Design v1.3 through `text.format`, explicitly disables thinking, validates the result and its cross-field invariants, and renders text/Markdown for the unchanged Section 5 APIs. The paired PDF remains the recruiter preview/download artifact. Provider-managed file upload, streaming, request-time PDF extraction or preprocessing, RAG, and a frontend-visible structured-report contract remain outside the MVP.

Goal 7 must exercise the fixed repository Markdown and production-shaped matching and follow-up schemas through the primary `ChatOpenAI` Responses path. If an Ark-specific Responses capability is not represented correctly, the Volcengine Ark Python SDK may be used inside the same AI Service and LangGraph boundary. If neither path supports the approved combination, stop for a design decision rather than changing the public API, adding a provider file lifecycle, streaming, extraction, or upload scope.

Provider configuration is validated by backend settings. The Ark API key remains a backend-only secret; base URL, model ID, and finite request timeout remain backend configuration. No real secret is committed, logged, persisted, or returned to the frontend.

Changing the provider must remain isolated to the AI Service and must not require changes to business workflows, persistence ownership, or frontend APIs.

---

## 7.5 User Behavior Tracking Implementation

Decision:

Use Tracking Session and User Behavior Event records in the existing PostgreSQL database. `POST /api/tracking-events` remains the event-ingestion boundary, `POST /api/tracking-sessions/test-mode` owns one-way test classification, and `GET /api/dashboard` returns the approved aggregate view. Centrally persisted state is authoritative; browser storage remains limited to pseudonymous current-session state and the bounded temporary event-delivery queue.

Tracking session and Conversation are separate concepts:

- Tracking session identifies a user's product visit and may exist before a Conversation is created;
- Conversation identifies a specific candidate-job evaluation context.

`sessionId` deduplicates one browser-tab tracking session, not one person. The tracking Service creates a Tracking Session on first event ingestion when it does not exist. Test-mode designation sets the session's server-owned `isTest` flag to `true` and never reverts it; the frontend exits test mode by creating a new random non-test `sessionId`.

The Controller validates each HTTP payload and delegates to the tracking or analytics Service. The tracking Service enforces the event allowlist, optional Conversation association, idempotency, session creation, and one-way test classification. The analytics Service validates the reporting period and coordinates aggregate repository queries. Controllers must not access the database or calculate metrics directly.

The backend stores only the approved Tracking Session metadata plus `eventId`, `eventName`, `sessionId`, `occurredAt`, server-generated `receivedAt`, server-generated `requestFingerprint`, and optional `conversationId`. The fingerprint remains a SHA-256 digest of the canonical accepted event metadata and preserves original request identity if `conversationId` is later cleared. Test classification is not part of the event payload or fingerprint. The backend must not log request bodies or persist raw interaction content, IP addresses, user-agent strings, secrets, prompts, or provider payloads as tracking data.

Events are retained for 90 days from `receivedAt`, covering the MVP evaluation period. Events older than 90 days must be removed by a documented maintenance operation; the MVP does not require a distributed scheduler or separate analytics service. Deleting a Conversation must not delete its historical metric event; the nullable foreign key is set to null.

Tracking Sessions with no remaining events and no activity inside the retention period may be removed by the same maintenance operation. A schema migration must backfill one non-test Tracking Session for every distinct existing event `sessionId` before enforcing the relationship. Existing event identity, request fingerprints, and Conversation deletion behavior remain unchanged.

The backend uses `eventId` as the unique idempotency key and compares retries against the immutable `requestFingerprint`. Identical retries return success without creating duplicates, including after Conversation deletion sets the relational `conversationId` to null. Tracking failures are returned through the tracking endpoint but must remain isolated from the recruiter-facing workflow by the frontend tracking boundary.

Test-mode designation is idempotent. It applies retroactively and prospectively through the Tracking Session relationship: every event with the designated `sessionId` is excluded even if it was accepted before designation or arrives later from the browser queue. A designation failure must not be acknowledged as active. The hidden gesture and endpoint are testing conveniences, not authentication; they do not grant access or change AI, Conversation, Feedback, or provider behavior.

The dashboard endpoint replaces the former internal-only aggregate report as the visual aggregate reporting boundary. It returns total event counts for all six approved event names and calculates Contact Conversion Rate as:

```text
Distinct sessionId values with both contact_cta_clicked and matching_report_generated

/

Distinct sessionId values with matching_report_generated
```

Both sides use non-test sessions whose qualifying events occur inside the same requested reporting period. Supporting totals count accepted events, while the conversion numerator and denominator count distinct `sessionId` values. The dashboard must not infer or label these sessions as people.

With no date parameters, aggregation includes all events currently retained. With `startDate` and `endDate`, both dates are required, inclusive, interpreted in `Asia/Shanghai`, converted to a half-open UTC timestamp interval, and applied to `occurredAt`. Every returned metric uses the same interval. A zero denominator returns `rate = null`; it never returns NaN, infinity, or another invalid numeric value.

The current production app and APIs are public under the approved v1.1 deployment boundary, so the dashboard aggregate is publicly reachable when linked from navigation. It returns aggregate values only and introduces no event-level export, user account, person identity, raw tracking access, or broader recruitment-management capability.


## 7.6 AI Retry Strategy
Decision:

Use one unified budget of at most two provider attempts per matching-analysis or follow-up execution: one initial attempt and at most one retry.

The single retry may be used for:

- A transient connection or timeout failure;
- Provider rate limiting or temporary service unavailability;
- A response that fails the approved schema or cross-field invariant validation.

The AI Service distinguishes the second request by the first failure category:

- After invalid structured output, rebuild the original request with one short, generic correction instruction requiring a complete result that follows the already supplied strict schema and field rules;
- After a transient provider failure, resend the original request unchanged and do not add the correction instruction.

The correction instruction must not contain or quote the raw response, validation exception, field-level diagnostics, secret, prompt, résumé, job description, or follow-up text beyond what is already present in the original request. The strict schema, Pydantic invariants, approved Markdown source-heading whitelist, request correlation ID, and two-attempt ceiling remain unchanged.

Do not retry authentication/authorization failure, invalid request, unsupported-model/capability error, safety refusal, or another permanent provider error. Disable library-level automatic retries so client behavior cannot multiply the workflow budget. Every attempt uses a finite backend-configured timeout, and Goal 7 must validate that timeout with the fixed Markdown context and gateway configuration.

After a non-retryable failure or retry exhaustion, the AI Service returns the existing safe AI-processing failure to the Service Layer. It must not persist an assistant message, expose raw provider details, or add background queues, evaluator loops, distributed retry infrastructure, or a new API contract.
