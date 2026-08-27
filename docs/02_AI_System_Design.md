# AI Job Fit Assistant AI System Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant AI System Design |
| Document Type | AI System Design |
| Version | v1.1 |
| Status | Final |
| Last Updated | 2026-08-27 |
| Related Documents | Product Requirement Document, Frontend Technical Design, Backend Technical Design, AI System Strategy Comparison, Implementation Plan |

## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
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
- **Primary provider integration approach:** LangChain `ChatOpenAI` through Ark's OpenAI-compatible API
- **Fallback provider integration approach:** Use the Volcengine Ark Python SDK only if a required Ark-specific capability cannot be used correctly through the OpenAI-compatible path
- **Resume input approach:** Pass the original predefined PDF directly to the model
- **MVP PDF transport:** `file_data` using Base64-encoded PDF content
- **Backend PDF extraction:** Not required
- **RAG:** Not required for the MVP
- **Structured output:** `response_format.type = json_schema` with `strict = true`

Goal 7 must expose the selected integration through validated backend settings such as `ARK_API_KEY`, `ARK_BASE_URL`, `ARK_MODEL`, and a finite request-timeout setting. Only the API key is secret; no provider setting or credential is exposed to the frontend or committed with a real value.

Conceptually:

```text
LangChain
= reusable AI components and provider integration

LangGraph
= workflow and state orchestration
```

Ark exposes an OpenAI-compatible Chat Completions API. `ChatOpenAI` should be configured with the API base URL rather than the full operation URL:

```text
Base URL
https://ark.cn-beijing.volces.com/api/v3

Chat Completions operation
https://ark.cn-beijing.volces.com/api/v3/chat/completions
```

The preferred implementation is to keep the LangChain-facing model interface standard and configure the Ark base URL, API key, and model ID. If Ark-specific file or structured-output behavior is not represented correctly through that compatibility layer, the implementation may use the native Volcengine Ark Python SDK inside the same AI Service boundary without changing the frontend, backend API contracts, or LangGraph workflow design.

The selected model `doubao-seed-2-1-pro-260628` is selected on the basis that it supports direct PDF input, `json_schema` structured output with `strict = true`, and using both capabilities in the same Chat Completions request. Goal 7 must verify that exact combination with the repository's fixed PDF and production-shaped schemas through the primary `ChatOpenAI` path before the adapter is considered complete. If the compatibility path fails, use the native Ark SDK fallback; if both paths fail, stop and request a design decision rather than adding extraction or changing the public API.

The AI design should remain provider-replaceable behind the backend AI Service boundary.

## 3. Inputs and Outputs

### 3.1 Candidate Source

The only factual candidate source for the MVP is the predefined candidate resume PDF.

```text
Predefined Resume PDF
        ↓
LangChain / Volcengine Ark PDF Input
        ↓
Matching or Follow-up Workflow
```

The original PDF is passed to Volcengine Ark in a provider-supported file format.

The approved Ark transport accepts direct PDF input through `file_data`, `file_id`, or `file_url`, subject to the Goal 7 compatibility gate for the exact model and client path. For the MVP's fixed two-page résumé, `file_data` is selected because it avoids introducing a separate file-upload lifecycle. The request includes the stable filename `mei_chang_resume.pdf` and a `data:application/pdf;base64,...` value; it does not create a provider-side file resource.

No separate candidate text source, backend extraction pipeline, or RAG knowledge base is required for the MVP.

### 3.2 Matching Analysis

Input:

```text
- jobDescription
- candidateResumePdf
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

Each `EvidenceItem` must contain a short, faithful résumé excerpt or close factual paraphrase and a recruiter-checkable locator such as page plus visible section heading. A source reference is not evidence by itself and must not point to a previous AI message.

Matching-result invariants:

- `supported` requires one or more evidence items and `missingInformation = null`;
- `partial` requires one or more relevant evidence items and a non-empty `missingInformation` value that explains the unproven part;
- `missing` requires an empty evidence list and a non-empty `missingInformation` value;
- `explanation` must describe how the evidence or information gap leads to the status without adding facts absent from the résumé.

The AI returns structured meaning internally. The Pydantic model enforces these cross-field invariants after provider-level schema validation.

The result is validated and then rendered into Markdown for the existing frontend/backend API.

### 3.3 Follow-up Question

Input:

```text
- currentQuestion
- candidateResumePdf
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
Candidate Resume PDF
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
Candidate Resume PDF
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
Candidate Resume PDF
= factual candidate source of truth

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
response_format.type = json_schema
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
- Each provider attempt uses a finite backend-configured timeout. Goal 7 must validate the timeout against the fixed PDF and deployment gateway before release;
- Exhaustion returns the existing safe AI-processing error. It must not persist an assistant message or expose raw provider details.

A second provider call is a retry, not another workflow stage. No evaluator loop, background queue, or distributed retry infrastructure is added for the MVP.

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
→ Ark OpenAI-compatible API

Native Ark SDK
→ fallback only

Resume input
→ direct PDF
→ file_data for MVP

Structured output
→ json_schema + strict=true

Schema validation
→ Pydantic

Invalid-output retry
→ 2 provider attempts total
→ one initial attempt + at most one retry
→ no stacked client retries

Compatibility gate
→ fixed repository PDF
→ production-shaped matching and follow-up schemas
→ primary ChatOpenAI path first
→ native Ark SDK fallback only if required

Model parameters
→ provider defaults initially

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
