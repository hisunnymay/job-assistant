# AI Job Fit Assistant AI System Strategy Comparison

## Document Information

- **Version:** v0.1
- **Status:** Approved
- **Last Updated:** 2026-08-27
- **Purpose:** Compare AI system implementation frameworks and define the selected framework strategy for the AI Job Fit Assistant.

## Version Log

- **v0.1 — 2026-08-27:** Created the initial AI system framework comparison and selected LangChain + LangGraph.

## AI System Approach

The AI system uses a **Structured LLM Pipeline** rather than a fully autonomous agent architecture.

The expected matching workflow is:

```text
Job Description
↓
Requirement Extraction
↓
Candidate Evidence Matching
↓
Supported / Partial / Missing Classification
↓
Evidence-grounded Matching Report
```

For follow-up questions:

```text
Recruiter Question
↓
Scope Check
↓
Evidence Lookup
↓
Answer or "Information Unavailable"
```

The implementation framework should therefore support:

- Deterministic workflow orchestration;
- Structured outputs;
- Conditional routing;
- Shared state and context management;
- Evidence-grounded generation;
- Clear handling of unsupported or out-of-scope questions;
- Future expansion without requiring a full architecture replacement.

## AI Framework Comparison

| Framework | Flexibility | Time Cost | Scale Cost | Engineering Complexity | Choose? |
|---|---:|---:|---:|---:|---|
| **Dify** ⭐ | ⭐⭐⭐⭐ | ⏱️ | 💰💰 | 🧩 | **✅ Recommended for MVP** — fastest way to build your structured pipeline while still supporting branching, structured outputs, APIs, and follow-up conversations. |
| **LangChain + LangGraph** | ⭐⭐⭐⭐⭐ | ⏱️⏱️⏱️ | 💰💰 | 🧩🧩🧩 | **🟡 Strong alternative** — choose if long-term flexibility and code-level control matter more than MVP speed. |
| **OpenAI Agents SDK** | ⭐⭐⭐⭐ | ⏱️⏱️ | 💰💰 | 🧩🧩 | **🟡 Possible** — lightweight and clean if you mainly use OpenAI, but your system doesn't really require agent-oriented abstractions. |
| **PydanticAI + Pydantic Graph** | ⭐⭐⭐⭐⭐ | ⏱️⏱️⏱️ | 💰💰 | 🧩🧩🧩 | **🟡 Not for MVP** — excellent type safety and Python integration, but requires more implementation than necessary right now. |
| **LlamaIndex Workflows** | ⭐⭐⭐⭐ | ⏱️⏱️⏱️ | 💰💰💰 | 🧩🧩🧩 | **❌ Not for MVP** — particularly valuable for document/RAG-heavy systems, while your current candidate knowledge is very small. |
| **Flowise** | ⭐⭐⭐⭐ | ⏱️ | 💰💰 | 🧩 | **❌ Prefer Dify** — similar low-code advantages, but there is no clear advantage over Dify for the current workflow. |

## Selected AI Framework

**Decision:** Use **LangChain + LangGraph**.

Dify would be the fastest option if the only objective were to deliver the MVP as quickly as possible.

However, this project also aims to provide hands-on experience with a code-native LLM framework and to preserve stronger long-term control over AI workflow behavior.

For these reasons, LangChain + LangGraph is selected.

## Why LangChain + LangGraph

### 1. Good Fit for a Structured LLM Pipeline

The AI system does not require an open-ended autonomous agent.

Instead, it follows an explicit sequence:

```text
Extract Requirements
→ Match Candidate Evidence
→ Classify Evidence Coverage
→ Generate Report
```

LangGraph can represent these steps as workflow nodes and transitions.

This makes the execution path easier to understand, debug, validate, and extend.

### 2. Strong Code-level Control

The product requires the AI system to:

- Ground conclusions in candidate evidence;
- Distinguish supported, partial, and missing information;
- Avoid unsupported conclusions;
- Reject or redirect out-of-scope follow-up questions.

Using LangChain + LangGraph keeps these rules in application code.

This provides direct control over:

- Prompts;
- Structured output schemas;
- Context passed to each step;
- Validation between nodes;
- Conditional routing;
- Error handling;
- Logging;
- Evaluation.

### 3. Natural Fit with Python + FastAPI

The selected backend technology is **Python + FastAPI**.

LangChain and LangGraph integrate naturally with the Python ecosystem, so the AI workflow can live behind the existing AI Service boundary.

The intended architecture is:

```text
Frontend
↓
FastAPI Backend
↓
AI Service
↓
LangGraph Workflow
↓
LangChain Components
↓
LLM Provider
```

This avoids introducing a separate low-code runtime and keeps the AI implementation inside the backend codebase.

### 4. Better Long-term Flexibility

The MVP currently supports:

- One predefined candidate;
- One job description at a time;
- A structured matching report;
- Limited follow-up questions.

Future versions may add:

- Resume upload;
- Larger candidate profiles;
- Retrieval / RAG;
- Multiple candidates;
- More complex workflow branches;
- Additional model providers;
- AI evaluation and observability.

LangChain provides reusable LLM integrations and abstractions.

LangGraph provides workflow orchestration, state management, branching, and more complex execution control.

Together, they provide a reasonable path for future expansion without replacing the core AI framework.

### 5. Higher Learning and Interview Value

This project is also intended to provide practical experience with LangChain and LangGraph.

Implementing the workflow directly provides hands-on experience with:

- Prompt orchestration;
- Structured outputs;
- State management;
- Conditional routing;
- Context management;
- Retrieval integration;
- Guardrails;
- LLM evaluation;
- Failure handling.

This additional learning value justifies the higher implementation time compared with Dify.

## Why Not Dify

Dify remains a strong choice for a fast MVP.

Its main advantage is implementation speed.

However, it is not selected because this project places additional value on:

- Learning LangChain and LangGraph directly;
- Keeping workflow logic in code;
- Maintaining stronger implementation transparency;
- Preserving long-term customization flexibility;
- Integrating the AI workflow directly into the Python backend.

The trade-off is therefore:

```text
Dify
= Faster MVP
+ Lower initial engineering complexity

LangChain + LangGraph
= More implementation effort
+ More code-level control
+ More learning value
+ Better long-term flexibility
```

For this project, the second trade-off is preferred.

## Selected Strategy

- **AI architecture:** Structured LLM Pipeline.
- **AI framework:** LangChain + LangGraph.
- **Workflow orchestration:** LangGraph.
- **LLM components and integrations:** LangChain.
- **Backend integration:** Python + FastAPI.
- **Candidate source for MVP:** One predefined candidate profile.
- **AI boundary:** Keep AI behavior behind the backend AI Service interface.
- **Current retrieval strategy:** Direct candidate-context injection; no RAG required for the initial fixed-profile MVP.
- **Future evolution:** Add retrieval, additional workflow nodes, richer candidate sources, and AI evaluation only when product requirements justify them.

## References

- [LangChain Documentation](https://docs.langchain.com/)
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [Dify Documentation](https://docs.dify.ai/)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [LlamaIndex Workflows](https://docs.llamaindex.ai/)
- [Flowise Documentation](https://docs.flowiseai.com/)
