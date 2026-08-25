# AI Job Fit Assistant — Codex Guide

## Version Log

- **v0.2 — 2026-08-25:** Simplified the initial guide and aligned technology, document authority, project prohibitions, agent workflow, implementation records, and document-update rules.

## Project Goal

Build a Chinese-language, one-week MVP that helps a recruiter evaluate how the fixed candidate, Mei Chang, matches a supplied job description. Produce evidence-based analysis, identify unsupported or unknown information clearly, and help the recruiter decide whether to contact the candidate. Prioritize a complete core journey over production-scale infrastructure.

## Document Authority

- `docs/01_Product_Requirement_Document.md` owns product scope, behavior, priorities, and acceptance criteria.
- `docs/03_Lightweight_AI_Design_Decision.md` owns AI inputs, outputs, capabilities, and limitations.
- `docs/04_Frontend_Technical_Design.md` owns recruiter experience, UI behavior, frontend state, and presentation responsibilities.
- `docs/05_Backend_Technical_Design.md` owns backend architecture, persistence, workflows, AI integration, and API contracts. Section 5 is the authoritative MVP API contract.
- `planning/PLAN.md`, when created, owns goal order, task details, completion criteria, validation commands, dependencies, and status. It does not override `docs/`.
- `history/` contains analysis and implementation records. It is not authoritative for current product behavior or technical contracts.

This file provides operating rules and must not override the documents above. If authoritative documents conflict, stop and ask the user to resolve the conflict before changing behavior or an agreed interface.

## Project-wide Implementation Rules

- Implement only the approved PRD MVP scope.
- Use React, TypeScript, and Vite for the frontend; use Python and FastAPI for the backend.
- During the Demo phase, keep AI behavior mocked behind the AI Service boundary. Do not select or integrate a real AI provider or framework before the AI System Design is agreed.
- Choose the simplest implementation that completes the requested vertical slice.
- Preserve module and layer boundaries without adding abstractions that have no current use.
- Keep the AI provider replaceable behind the AI Service boundary.
- Keep the UI in Chinese and keep user-facing strings separable from components; do not build a full internationalization system for the MVP.
- Use one primary implementation agent by default. Use reviewer subagents only for bounded review or investigation at meaningful checkpoints; do not parallelize tightly coupled frontend and backend edits by default.

## Architecture Boundaries

Use a modular monolith with layered backend architecture:

```text
API Access Protection -> Controller -> Service -> AI Service / Repository
```

- The frontend owns interaction and presentation; it must not implement AI reasoning or backend workflows.
- Controllers own HTTP handling and basic request validation; they must not contain business logic, access persistence directly, or call AI providers.
- Services own business workflows and conversation context and coordinate the AI Service and repositories.
- The AI Service owns provider-specific handling and basic response validation; it must not load or persist conversations directly.
- Repositories hide persistence details from the rest of the application.

## Prohibited Changes

- Do not add multiple candidates, candidate comparison, résumé upload or management, ranking, an overall match score, hiring decisions, or performance prediction.
- Do not add open-ended chat, user accounts, or a broader recruitment-management workflow.
- Do not invent candidate evidence or present unknown or unsupported information as fact.
- Use the same predefined static résumé PDF for preview/download and AI context. Do not add backend PDF extraction, preprocessing, or a required text/Markdown mirror.
- Do not expose or persist raw prompts, raw provider responses, provider-specific payloads, secrets, or internal errors.
- Do not place AI reasoning or business workflow in the frontend or controller, and do not let the AI Service access persistence directly.
- Do not introduce microservices, distributed or event-driven infrastructure, multiple databases, complex retry systems, or speculative scaling work.
- Do not add streaming AI output or strict structured AI output unless the relevant design is updated and approved.

## Implementation Records

After completing a requested implementation goal, add a concise record under `history/implementation_logs/` containing:

- The completed goal and material behavior or files changed;
- Validation performed and its results;
- Problems fixed, approved deviations, and remaining known issues.

Do not record internal reasoning, every command, or conversation transcripts. Create the log folder when implementation begins.

## Document Update Rules

- Before changing this file or a finalized document under `docs/`, ask the user explicitly whether it should be updated and identify the affected document.
- After approval, update the document that owns the decision and add or update its Version Log with version, date, change, and reason.
- Do not let implementation silently change product behavior, AI capability boundaries, data ownership, persistence meaning, or API request, response, or error contracts.
- For an approved frontend-backend contract change, update Backend Technical Design Section 5 and the corresponding frontend integration assumptions together.
