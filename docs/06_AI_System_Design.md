# AI Job Fit Assistant AI System Design

## Document Information

| Field | Description |
| --- | --- |
| Document Name | AI Job Fit Assistant AI System Design |
| Document Type | AI System Design |
| Version | v0.4 |
| Status | Draft |
| Last Updated | 2026-08-27 |
| Related Documents | Product Requirement Document, Frontend Technical Design, Backend Technical Design, AI System Strategy Comparison, Implementation Plan |

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
- Invent candidate information.

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
- **Initial LLM provider:** Volcengine Ark
- **Initial model family:** Doubao
- **AI integration boundary:** Backend AI Service
- **Primary provider integration approach:** Use Ark's OpenAI-compatible API through LangChain when supported
- **Fallback provider integration approach:** Use the Volcengine Ark Python SDK inside the same AI Service / LangGraph boundary if provider-specific PDF or structured-output behavior requires it
- **Resume input approach:** Pass the original predefined PDF directly to the selected model
- **Preferred MVP PDF transport:** Send the fixed PDF as `file_data` when practical; `file_id` or `file_url` may be used later if needed
- **Backend PDF extraction:** Not required
- **RAG:** Not required for the MVP

Conceptually:

```text
LangChain
= reusable AI components and provider integration

LangGraph
= workflow and state orchestration
```

Ark exposes an OpenAI-compatible Chat Completions API:

```text
https://ark.cn-beijing.volces.com/api/v3/chat/completions
```

The preferred implementation is to keep the LangChain-facing model interface standard and configure the Ark base URL, API key, and model ID. If Ark-specific file or structured-output behavior is not represented correctly through that compatibility layer, the implementation may use the native Volcengine Ark Python SDK inside the same AI Service boundary without changing the frontend, backend API contracts, or LangGraph workflow design.

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

Ark supports PDF file input through `file_data`, `file_id`, or `file_url`. For the MVP's fixed two-page resume, `file_data` is the preferred starting approach because it avoids introducing a separate file-upload lifecycle.

No separate candidate text source, backend extraction pipeline, or RAG knowledge base is required for the MVP.

### 3.2 Matching Analysis

Input:

```text
- jobDescription
- candidateResumePdf
```

Internal structured output:

```text
MatchingAnalysisResult

- summary
- requirements[]
    - requirement
    - importance
    - status: supported | partial | missing
    - evidence[]
        - evidenceText
        - sourceReference
    - explanation
    - missingInformation
```

The AI returns structured meaning internally.

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

- answerability:
    - answerable
    - insufficient_evidence
    - out_of_scope
- answer
- evidence[]
- missingInformation
```

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

The first version uses **one primary LLM call** for:

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

The first version uses **one primary LLM call** for:

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
↓
Render
↓
END
```

Nodes may use either LangChain components or normal Python functions.

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

The selected Ark model should use structured response output when supported.

Preferred response mode:

```text
response_format.type = json_schema
```

Because Ark documents `json_schema` response formatting as model-dependent and currently beta, the exact Doubao model must be verified to support both:

- PDF document input;
- `response_format: json_schema`.

The AI system must validate structured outputs before they are returned to the backend workflow.

Validation should confirm at minimum:

- A response exists;
- The response matches the expected structured schema;
- Required fields are present;
- Classification values are valid;
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

The MVP should use only a **small bounded retry**, not complex retry infrastructure.

The exact retry count may be finalized during implementation.

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

Detailed numerical pass thresholds can be finalized in the AI Evaluation Goal after a baseline is measured.

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

## 10. Remaining Implementation Decisions

This document remains a draft. Real-AI implementation must not begin until the AI System Design is finalized and explicitly approved through the project document process.

The following decisions must be finalized before or during that approval:

- Exact Volcengine Ark / Doubao model;
- Confirmation that the selected model supports both PDF input and `json_schema` structured output;
- Whether the final integration uses LangChain's OpenAI-compatible client path or the native Volcengine Ark Python SDK;
- Model parameters;
- Exact bounded retry count;
- Concrete Python schema representation (`TypedDict`, Pydantic, dataclass, etc.);
- Detailed prompt wording;
- Logging / tracing implementation;
- Detailed numerical AI-evaluation thresholds.

Until those choices and this document are approved, the Demo phase continues to use the Mock AI Service behind the existing AI Service boundary.
