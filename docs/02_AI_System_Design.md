# AI Job Fit Assistant AI System Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant AI System Design |
| Document Type | AI System Design |
| Version | v1.4 |
| Status | Final |
| Last Updated | 2026-08-27 |
| Related Documents | Product Requirement Document, Frontend Technical Design, Backend Technical Design, AI System Strategy Comparison, Implementation Plan |

## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v1.4 | 2026-08-27 | Distinguished invalid-structured-output correction retries from transient provider retries and defined the bounded Mini compatibility check. | Improve second-attempt recovery without weakening validation or leaking raw output, while measuring whether the lower-latency model is viable before any default-model decision. |
| v1.3 | 2026-08-27 | Replaced runtime direct-PDF input with the user-verified fixed résumé Markdown while retaining the paired PDF for recruiter preview/download, strict internal output, and unchanged public contracts. | For the fixed-candidate MVP, sending the verified text avoids repeated document parsing and creates a simpler latency and reliability path without adding runtime extraction or upload scope. |
| v1.2 | 2026-08-27 | Corrected the Ark document-input integration to use the Responses API with inline Base64 `input_file`, Responses structured output, and thinking disabled while preserving the direct-PDF and public-contract boundaries. | Provider clarification established that PDF document input is documented on Ark's Responses API rather than Chat Completions. |
| v1.1 | 2026-08-27 | Completed the internal output schemas and invariants, unified retry accounting, added workflow failure branches, required provider-compatibility validation, and clarified evaluation-gate sequencing. | Resolve implementation ambiguity without changing product scope, persistence ownership, or public API contracts. |
| v1.0 | 2026-08-27 | Finalized the initial real-AI architecture, provider, model, direct-PDF approach, structured output, validation, retry, and tracing decisions. | Open the real-AI planning stage after the Mock-AI demo. |

## 1. AI System Goal and Boundary

The AI system helps recruiters understand how a candidate's experience relates to a job description through traceable evidence.

The AI system should:

- Analyze job requirements;
- Find relevant candidate evidence;
- Classify each requirement as **Supported**, **Partial**, or **Missing**;
- Explain the evidence behind each conclusion;
- Answer candidate-related follow-up questions;
- Clearly indicate unavailable or unsupported information.

The AI system should not:

- Make hiring decisions;
- Rank candidates;
- Predict future performance;
- Invent candidate information;
- Produce an overall match score.

Responsibility boundary:

```text
Frontend
→ Collect input and display results

Backend
→ Manage workflow, conversation, persistence, and AI context

AI System
→ Perform candidate-job analysis and follow-up reasoning

LLM Provider
→ Perform model inference
```

## 2. Selected AI Technology

- **AI framework:** LangChain + LangGraph
- **LLM provider:** Volcengine Ark
- **Model:** `doubao-seed-2-1-pro-260628`
- **AI integration boundary:** Backend AI Service
- **Primary provider integration approach:** LangChain `ChatOpenAI` with `use_responses_api = true` through Ark's OpenAI-compatible Responses API
- **Fallback provider integration approach:** Use the Volcengine Ark Python SDK only if a required Responses API capability cannot be represented correctly through `ChatOpenAI`
- **Resume input approach:** Send the user-verified static `mei_chang_resume.md` resource as model text context
- **Recruiter artifact:** Retain the paired fixed `mei_chang_resume.pdf` for preview/download
- **Backend PDF extraction:** None at request time; the user supplies and verifies the fixed Markdown resource
- **RAG:** Not required for the MVP
- **Structured output:** Responses API `text.format.type = json_schema` with `strict = true`
- **Thinking mode:** Explicitly disabled for the strict structured matching workflow

Goal 7 must expose the selected integration through validated backend settings such as `ARK_API_KEY`, `ARK_BASE_URL`, `ARK_MODEL`, and a finite request-timeout setting. Only the API key is secret; no provider setting or credential is exposed to the frontend or committed with a real value.

Conceptually:

```text
LangChain
= reusable AI components and provider integration

LangGraph
= workflow and state orchestration
```

Ark exposes an OpenAI-compatible Responses API. `ChatOpenAI` should be configured with the API base URL and `use_responses_api = true` rather than the full operation URL:

```text
Base URL
https://ark.cn-beijing.volces.com/api/v3

Responses operation
https://ark.cn-beijing.volces.com/api/v3/responses
```

The preferred implementation keeps the LangChain-facing model interface standard and configures the Ark base URL, API key, model ID, and Responses API mode. LangChain converts the fixed résumé and dynamic workflow content to Responses API `input_text` and the strict schema to `text.format`. If an Ark-specific Responses API behavior is not represented correctly through that compatibility layer, the implementation may use the native Volcengine Ark Python SDK inside the same AI Service boundary without changing the frontend, backend API contracts, or LangGraph workflow design.

Goal 7 must verify the exact fixed Markdown plus strict production-shaped schemas through the primary `ChatOpenAI` Responses path with `doubao-seed-2-1-pro-260628` before the corrected adapter is considered complete. If that client path cannot represent a required Responses capability, use the native Ark SDK fallback; if both paths fail, stop and request a design decision rather than weakening validation, adding request-time extraction, streaming, or a public-API change.

The AI design should remain provider-replaceable behind the backend AI Service boundary.

## 3. Inputs and Outputs

### 3.1 Candidate Source

The MVP candidate resource is one approved, fixed pair: the recruiter-visible PDF and the user-verified Markdown used at runtime by the AI Service. The Markdown is the only candidate-fact input sent to the model and must not be edited independently without repeating user verification and updating its approved digest.

```text
User-verified Resume Markdown
        ↓
LangChain / Volcengine Ark Text Input
        ↓
Matching or Follow-up Workflow
```

The original `mei_chang_resume.pdf` remains the preview/download artifact and is not sent to Ark. The AI Service loads the exact UTF-8 `mei_chang_resume.md`, verifies its fixed filename and SHA-256 before any provider call, places the stable résumé text before dynamic JD or conversation text, and sends text-only Responses input. This creates no provider file resource.

No request-time extraction pipeline, provider-managed file lifecycle, résumé upload/management, or RAG knowledge base is required for the MVP.

### 3.2 Matching Analysis

Input:

```text
- jobDescription
- candidateResumeMarkdown
```

Internal structured output:

```text
EvidenceItem

- evidenceText: non-empty string
- sourceReference: non-empty string

MatchingAnalysisResult

- summary: non-empty string
- requirements[1..]
    - requirement: string
    - importance: required | preferred | unspecified
    - status: supported | partial | missing
    - evidence[]: EvidenceItem
    - explanation: string
    - missingInformation: string | null
```

`importance` is derived only from priority language in the job description. Use `unspecified` when the job description does not establish whether a requirement is required or preferred; the model must not invent priority.

Each `EvidenceItem` must contain a short, faithful résumé excerpt or close factual paraphrase and a recruiter-checkable locator using a visible heading from the approved Markdown. A source reference is not evidence by itself and must not point to a previous AI message or invent a PDF page number that is absent from the model input.

Matching-result invariants:

- `supported` requires one or more evidence items and `missingInformation = null`;
- `partial` requires one or more relevant evidence items and a non-empty `missingInformation` value that explains the unproven part;
- `missing` requires an empty evidence list and a non-empty `missingInformation` value;
- `explanation` must describe how the evidence or information gap leads to the status without adding facts absent from the résumé.

The AI returns structured meaning internally. The Pydantic model enforces these cross-field invariants after provider-level schema validation.

Before deterministic Markdown rendering, every provider-controlled string is normalized to one line and Markdown control characters are escaped. This prevents model text from creating headings, links, images, HTML-like content, or other presentation structure beyond the renderer-owned template. The strict schema and source-reference whitelist remain the semantic validation boundary.

The result is validated and then rendered into Markdown for the existing frontend/backend API.

### 3.3 Follow-up Question

Input:

```text
- currentQuestion
- candidateResumeMarkdown
- conversationHistory
```

`currentQuestion` is separate from previous conversation history.

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

Internal structured output:

```text
FollowUpResult

- answerability: answerable | insufficient_evidence | out_of_scope
- answer: non-empty string
- evidence[]: EvidenceItem
- missingInformation: string | null
```

Follow-up-result invariants:

- `answerable` requires one or more `EvidenceItem` values supporting the answer and `missingInformation = null`;
- `insufficient_evidence` must avoid new affirmative candidate claims and requires a non-empty `missingInformation` value; relevant partial résumé evidence may be returned when it helps explain the gap;
- `out_of_scope` requires an empty evidence list and `missingInformation = null`; `answer` must decline the unsupported request and may redirect the recruiter to candidate background, matching evidence, or information gaps;
- previous AI messages may be used to resolve conversational references but never as candidate evidence.

The structured result is validated and rendered into Markdown before being returned through the backend API.

## 4. AI Workflows

The MVP uses two core AI workflows.

### Workflow 1 — Generate Matching Report

```text
Job Description
+
Candidate Resume Markdown
        ↓
Generate Structured Matching Analysis
        ↓
Validate
        ↓
Render Markdown
        ↓
Return
```

The first version uses **one primary LLM attempt** for:

- Requirement understanding;
- Evidence matching;
- Supported / Partial / Missing classification;
- Explanation generation.

### Workflow 2 — Answer Follow-up Question

```text
Current Question
+
Candidate Resume Markdown
+
Conversation History
        ↓
Generate Structured Follow-up Result
        ↓
Validate
        ↓
Render Markdown
        ↓
Return
```

The first version uses **one primary LLM attempt** for:

- Determining answerability;
- Finding candidate evidence;
- Producing a grounded answer or limitation.

Logical responsibilities do not need to map one-to-one to LangGraph nodes or LLM calls.

Initial LangGraph shape:

```text
START
↓
Generate
↓
Validate
├── Valid ─────────────────────→ Render → END
├── Retryable + attempt remains → Generate
└── Non-retryable or exhausted ─→ AI Processing Error → END
```

Provider/network failures enter the same retry decision before validation. Nodes may use either LangChain components or normal Python functions.

## 5. State and Evidence Rules

### State Ownership

```text
Backend Database
= persistent conversation state

LangGraph State
= temporary state for one AI execution
```

The backend remains the source of truth for conversations.

LangGraph persistence/checkpointing is not required for the MVP.

### Evidence Rules

```text
User-verified Candidate Resume Markdown
= runtime factual candidate source paired with the recruiter-visible PDF

Conversation History
= interaction context
```

Previous AI messages must not become new factual evidence about the candidate.

Evidence classification means:

- **Supported** — candidate information directly supports the requirement;
- **Partial** — relevant evidence exists but does not fully establish the requirement;
- **Missing** — the available resume does not provide sufficient evidence.

`Missing` does not mean the candidate cannot satisfy the requirement.

It only means the available candidate information does not prove it.

## 6. Response Validation and Retry

The selected model uses structured response output.

Preferred response mode:

```text
text.format.type = json_schema
strict = true
```

Structured outputs are represented and validated with Pydantic schemas corresponding to `MatchingAnalysisResult` and `FollowUpResult`.

The provider-facing JSON Schemas must be concrete and compatible with strict mode: all object fields are declared, unexpected properties are rejected, enum values are closed, and intentionally absent values use the explicit nullable fields defined in Section 3 rather than omitted keys.

The AI system must validate structured outputs before they are returned to the backend workflow.

Validation should confirm at minimum:

- A response exists;
- The response matches the expected structured schema;
- Required fields are present;
- Required strings are trimmed and non-empty, and required result lists satisfy their minimum cardinality;
- Classification values are valid;
- Section 3 cross-field invariants hold;
- The result can be converted into frontend-renderable Markdown.

If the provider returns an invalid structured response:

```text
Invalid Output
↓
Limited Retry
↓
Valid?
├── Yes → Continue
└── No  → Return AI Processing Error
```

The MVP uses one unified retry budget for each matching or follow-up execution:

- Maximum provider attempts: **2 total** — one initial attempt and at most one retry;
- Retryable conditions: a transient connection/timeout failure, a provider rate-limit or temporary-service failure, or an invalid structured result;
- Non-retryable conditions: authentication/authorization failure, invalid request or unsupported-model/capability error, safety refusal, and any other permanent provider error;
- Library-level automatic retries must be disabled so they cannot multiply the workflow budget;
- Each provider attempt uses a finite backend-configured timeout. Goal 7 must validate the timeout against the fixed Markdown and deployment gateway before release;
- Exhaustion returns the existing safe AI-processing error. It must not persist an assistant message or expose raw provider details.

If and only if the first provider result fails parsing, strict schema validation, or Section 3 invariant validation, the second request adds one short generic correction instruction telling the model to return a complete result that satisfies the already supplied JSON Schema and field rules. The correction must not include the raw first response, validation exception text, field-level internal diagnostics, secrets, or user content beyond the original request. The original strict schema, invariant checks, source-heading whitelist, and model inputs remain unchanged.

When the first attempt instead fails because of an approved transient network, timeout, rate-limit, or temporary-service condition, the second attempt reuses the original request without the structured-output correction. Permanent failures do not retry. These branches share the same two-attempt ceiling; no failure sequence can create a third call.

A second provider call is a retry, not another workflow stage. No evaluator loop, background queue, or distributed retry infrastructure is added for the MVP.

Goal 7A may run one matching analysis and one follow-up with `doubao-seed-2-0-mini-260428`, after deterministic tests pass and the user separately approves up to four provider calls and their cost. The run must use the same fixed Markdown, prompts, strict schemas, invariants, source rules, thinking setting, and public API path as the Pro baseline. Its privacy-safe record contains only model/client identifiers, first-attempt validity, retry occurrence, total duration, schema/source and prohibited-behavior rule results, and a comparison with the 34.28-second Pro baseline. It must not contain the résumé, job description, question, prompt, raw provider payload/response, or generated Markdown. The result does not change the configured default model or `.env` without a separate user decision.

## 7. Backend Integration

The existing frontend/backend API contract remains unchanged.

### Matching Analysis

```text
Frontend
↓
POST /api/matching-analysis
↓
Backend creates conversation and stores JD
↓
Backend prepares AI request
↓
AI Service
↓
LangGraph / LangChain / Volcengine Ark
↓
Structured Result
↓
Validate + Render Markdown
↓
Backend stores AI message
↓
Frontend renders content
```

### Follow-up Question

```text
Frontend
↓
POST /api/conversations/{conversationId}/messages
↓
Backend stores current question
↓
Backend loads ordered conversation history
↓
Backend prepares AI request
↓
AI Service
↓
LangGraph / LangChain / Volcengine Ark
↓
Structured Result
↓
Validate + Render Markdown
↓
Backend stores AI message
↓
Frontend renders content
```

The AI system does not manage:

- Conversation persistence;
- Message IDs;
- Feedback;
- Tracking;
- HTTP behavior;
- Frontend state.

The “stores” steps in these diagrams occur inside the Service Layer's existing transaction. Provider retries happen before commit. A failed matching execution commits neither its new Conversation nor its messages, and a failed follow-up commits neither its new question nor answer; existing replay and rollback behavior remains unchanged.

## 8. AI Evaluation Strategy

Real AI integration should be evaluated before it is treated as ready.

The evaluation set should include representative job descriptions and follow-up questions covering:

- Correct evidence grounding;
- Supported evidence;
- Partial evidence;
- Missing information;
- Answerable follow-up questions;
- Candidate-related questions with insufficient evidence;
- Out-of-scope questions;
- Rejection of hiring recommendations;
- Rejection of candidate ranking or comparison;
- Rejection of future-performance prediction;
- No overall match score.

### Pass Principle

The real AI should pass the agreed guardrail and grounding cases before release.

At minimum:

```text
No invented candidate evidence
+
Correct handling of unknown information
+
Correct supported-scope behavior
+
No prohibited hiring judgment or scoring
```

The initial evaluation matrix must include at least one matching or follow-up case for every category listed above and must reuse the provider-neutral guardrail fixtures established during the Mock-AI phase where applicable.

The following are non-negotiable release criteria across the approved release evaluation set:

- Zero invented candidate evidence or source references;
- Zero hiring decisions, rankings/comparisons, future-performance predictions, or overall match scores;
- Every insufficient-evidence case states the information gap without converting absence of evidence into a negative candidate fact;
- Every out-of-scope case declines the unsupported request without speculative content;
- Every successful provider response passes the strict schema and Section 3 invariants before Markdown rendering.

Any violation of these hard guardrails blocks release. Numerical thresholds for graded quality measures such as classification accuracy, evidence relevance, and explanation usefulness are finalized in the AI Evaluation Goal after a baseline is measured and explicitly approved. Those graded thresholds are not an entry requirement for implementing the provider adapter, but they are required before the AI-enabled release is approved.

## 9. Evaluation-Driven Evolution

The MVP intentionally starts with two consolidated workflows and one primary LLM call per request.

Additional steps should be introduced only when evaluation identifies a real problem.

Examples:

```text
Poor evidence quality
→ Separate evidence retrieval / checking

Weak scope control
→ Separate scope classification

Unsupported conclusions
→ Add evaluator / retry loop

Candidate information becomes too large
→ Introduce RAG
```

Design principle:

> Start consolidated. Split the workflow only when evaluation shows that the additional separation improves reliability or product quality.

## 10. Logging and Tracing

The MVP uses three complementary debugging layers.

### Backend Structured Logs

Backend logs are the baseline debugging mechanism. Recommended fields include:

```text
request_id
conversation_id
workflow
model
duration_ms
retry_count
validation_status
error_type
```

Production logs should not contain resume content, raw job descriptions, follow-up question content, full prompts, API keys, or full model responses.

### Ark Request Correlation

Each provider request should include a generated `X-Client-Request-Id`. The same ID should be stored in backend logs so client-side activity can be correlated with Ark-side logs during troubleshooting.

### LangSmith

LangSmith may be used during development for LangChain/LangGraph tracing and prompt debugging. It is optional and must not be a production dependency. No self-hosted LangSmith deployment is required for the MVP. Production tracing should not send full real-user resume, JD, prompt, or model-response content to an external tracing service by default.

## 11. Finalized Implementation Decisions

The AI architecture is finalized for real-AI implementation.

```text
Provider
→ Volcengine Ark

Model
→ doubao-seed-2-1-pro-260628

Integration
→ LangChain ChatOpenAI
→ use_responses_api=true
→ Ark OpenAI-compatible Responses API

Native Ark SDK
→ fallback only

Resume input
→ user-verified fixed Markdown
→ text-only Responses input

Structured output
→ json_schema + strict=true

Schema validation
→ Pydantic

Invalid-output retry
→ 2 provider attempts total
→ one initial attempt + at most one retry
→ no stacked client retries

Compatibility gate
→ fixed repository Markdown and approved SHA-256
→ production-shaped matching and follow-up schemas
→ primary ChatOpenAI Responses path first
→ native Ark SDK fallback only if required

Model parameters
→ thinking disabled for strict structured matching
→ other provider defaults initially

Logging
→ backend structured logs
→ X-Client-Request-Id

Tracing
→ optional LangSmith in development
→ no production dependency
```

The following are intentionally deferred to implementation and evaluation because they are tuning decisions rather than architecture blockers:

- Detailed prompt wording;
- Fine-grained model parameters;
- Evaluation-case expansion beyond the required matrix;
- Numerical thresholds for graded AI-quality measures.

These items may evolve without redesigning the AI system unless evaluation shows that the current architecture is insufficient.
