# AI Job Fit Assistant — Codex Implementation Guide

## Project Goal

Build a usable, Chinese-language MVP that helps a recruiter evaluate how the fixed candidate, Mei Chang, matches a supplied job description. The product should turn the job description and candidate resume into evidence-based matching analysis, expose missing information clearly, and help the recruiter decide whether to contact the candidate.

This is a one-week validation demo. Optimize for a complete, understandable core journey—not production-scale infrastructure.

## Source of Truth

Use each finalized document only for the decisions it owns:

1. **Product Requirement Document (PRD)** — source of truth for product requirements, MVP behavior, priorities, and acceptance criteria.
2. **Lightweight AI Design Decision** — AI inputs, outputs, supported capabilities, and limitations.
3. **Frontend Technical Design** — recruiter experience, UI behavior, frontend state, and presentation responsibilities.
4. **Backend Technical Design** — backend architecture, persistence, workflows, AI integration, and unresolved backend decisions. Section 5 is the MVP API contract.

Do not let this file silently override those documents. If documents appear to conflict, follow the document that owns the decision and resolve the inconsistency before changing product behavior or an agreed interface.

## MVP Scope

Implement the end-to-end recruiter flow:

- Show initial guidance and accept a job description.
- Generate and display a Matching Report. `Matching Analysis` is the AI-generated content; `Matching Report` is its recruiter-facing presentation.
- Analyze job requirements, distinguish hard/soft requirements where appropriate, map requirements to resume evidence, and identify unknown or unsupported information.
- Allow follow-up questions within the current evaluation conversation.
- Preview and, where supported, download the candidate's original resume PDF.
- Provide candidate contact entry points using frontend-owned static content. Recruiter name is optional if collected for contact initiation.
- Collect report/response feedback.
- Track page visits, job-description submission, matching-report generation, resume-preview clicks, contact-CTA clicks, and feedback submission.
- Use synchronous request/response behavior for MVP; show clear loading and error states.

The website UI is Chinese. Keep user-facing strings separable from components so later localization remains possible; a full i18n system is not required.

## Non-goals

Do not add:

- Multiple candidates or candidate comparison;
- Recruiter resume upload or candidate management;
- Resume generation or editing;
- Open-ended chat unrelated to the current evaluation;
- Candidate ranking, an overall AI match score, hiring decisions, or performance prediction;
- User accounts, a complex permission system, or a full recruitment SaaS workflow;
- Microservices, event-driven infrastructure, multiple databases, or speculative scale work;
- Streaming AI output or strict structured AI output unless later agreed.



## Architecture and Responsibility Boundaries

Use a **modular monolith with layered architecture**:

```text
API Access Protection -> Controller -> Service -> AI Service / Repository
```

- **Frontend:** collect input; manage UI/loading/error state; render text/Markdown AI content without changing its conclusions; provide static initial guidance and contact content; display the PDF; emit tracking events. It must not implement AI reasoning or backend workflows.
- **Controller:** handle HTTP, basic request validation, service calls, and responses. It must not contain business logic, access persistence directly, or call an AI provider directly.
- **Service:** own business workflows and conversation context; coordinate the AI Service and Repository.
- **AI Service:** hide provider-specific file/request/response handling; call the selected provider and perform basic response validation. It must not load or persist conversations itself.
- **Repository:** hide storage details for conversations, messages, and feedback. One lightweight repository layer is sufficient.
- **AI capability/provider:** analyze requirements, match evidence, identify information gaps, generate analysis, and answer supported follow-ups. It must not invent evidence, make hiring decisions, rank candidates, or return false precision.

The backend validates that an AI response exists and is renderable; it does not judge whether the AI conclusion is substantively correct.

## Resume Handling

The Candidate Resume is one predefined **static PDF resource**, not persistent business data.

- Use the same PDF for recruiter preview/download and as candidate context for AI processing.
- The Service supplies the resume resource; the AI Service packages or uploads it in the format supported by the selected provider.
- Do **not** build backend PDF text extraction, preprocessing, or a required text/Markdown mirror for MVP.
- Do **not** add resume upload merely to anticipate a future version.



## Backend and API Expectations

Keep the agreed business-capability APIs stable:

```text
POST /api/matching-analysis
  { jobDescription }
  -> { conversationId, messageId, content }

POST /api/conversations/{conversationId}/messages
  { question }
  -> { messageId, content }

GET /api/resume
  -> application/pdf

POST /api/feedback
  { conversationId, messageId, rating, comment }
  -> { success }
```

- Return AI `content` as frontend-renderable text/Markdown.
- Use a consistent error body: `{ code, message }`. Do not expose internal errors or provider payloads. The frontend may map `code` to localized UI copy rather than relying only on `message`.
- Apply lightweight API access protection before business processing; this is backend API protection, not user authentication.
- Persist `Conversation`, `Conversation Message`, and `Feedback`. Messages must distinguish `job_description`, `matching_analysis`, `follow_up_question`, and `follow_up_answer`.
- Matching generation uses `Candidate Resume + Job Description`.
- Follow-up generation uses `Candidate Resume + Full Conversation History`.
- Store user-facing AI responses as conversation messages. Do not store raw prompts, raw provider responses, or provider-specific payloads. Log only enough diagnostic information to investigate failures safely.
- Do not store missing/unusable AI output as a conversation message.
- A tracking session identifies a product visit and may exist before a Conversation; do not treat `conversationId` as the universal analytics session identifier.



## Implementation Principles

- Choose the simplest implementation that completes and demonstrates the MVP flow.
- Preserve clear module/layer boundaries, but avoid boilerplate abstractions with no current use.
- Model business concepts before database tables; keep schemas minimal.
- Expose business capabilities, not database structures, through APIs.
- Keep the AI provider replaceable behind the AI Service boundary.
- Prefer small, testable vertical slices and verify the end-to-end journey as implementation progresses.
- Do not design for hypothetical future requirements.



## Intentionally Unresolved Decisions

Codex may choose these pragmatically during implementation, using the simplest option compatible with the contracts above:

- Frontend framework, component library, detailed layout, state management, and PDF preview method;
- Deployment and hosting approach;
- API access-protection mechanism;
- Database technology and exact table/repository structure;
- AI provider, framework, SDK, and provider-specific PDF handoff;
- Custom versus third-party behavior tracking and tracking-session mechanism;
- No retry versus one limited retry for transient AI failures.

Do not introduce complex retry infrastructure, distributed systems, or new product behavior while resolving these choices. Record material choices in the relevant technical document.

## Keep Documentation in Sync

If implementation appears to require a change to product behavior, AI capability boundaries, data ownership, persistence meaning, or an API request/response/error contract:

1. **Ask the user explicitly whether the corresponding project document should be updated. Do not update it without confirmation.**
2. After approval, update the document that owns the changed decision.
3. Add or update the **Version Log** in every changed document, recording the version, date, change, and reason.

For an approved frontend-backend contract change, update Backend Technical Design Section 5 and the corresponding frontend integration assumptions together.
