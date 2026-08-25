# Lightweight AI Design Decision

## Document Information

| Field | Description |
|---|---|
| Document Name | Lightweight AI Design Decision |
| Document Type | AI Design Decision |
| Version | v0.2 |
| Status | Finalized |
| Owner | Mei Chang |
| Last Updated | 2026-08-25 |
| Related Documents | AI Job Fit Assistant PRD |


## Version Log

| Version | Date | Change | Reason |
| --- | --- | --- | --- |
| v0.1 | 2026-08-20 | Created the lightweight AI capability definition. | Establish the MVP AI scope and integration boundaries. |
| v0.2 | 2026-08-25 | Marked the reviewed AI design as finalized. | Prepare the approved design baseline for implementation planning. |


---

# 1. AI Capability Definition


## 1.1 AI Goal

The AI capability aims to help recruiters understand the relationship between job requirements and candidate experience by generating evidence-based candidate-job fit analysis.

The AI capability supports the MVP workflow by generating Matching Report content and answering follow-up questions based on available candidate information.


---

## 1.2 AI Input

The AI capability receives different inputs depending on the scenario.


### Matching Report Generation

Input:

- Job Description
- Candidate Resume


### Follow-up Question Answering

Input:

- Job Description
- Candidate Resume
- Existing Matching Report Context
- Recruiter Questions


---

## 1.3 AI Output

The AI capability provides the following outputs:


### Matching Report Content

The AI generates analysis content that helps recruiters understand:

- Relationship between job requirements and candidate experience;
- Supporting evidence from candidate experience;
- Areas where sufficient information is unavailable.


### Follow-up Answer Content

The AI provides answers based on available candidate information and existing analysis context.

Follow-up answers may include:

- Additional explanation of matching results;
- Clarification of candidate experience;
- Explanation of identified information gaps;
- Indication that requested information is unavailable or unsupported;
- Redirection to supported topics when appropriate.


The MVP does not require a strict structured output format. AI-generated content can be rendered as text/Markdown.


---

## 1.4 AI Capability Scope

The AI capability supports:

- Analyzing job requirements;
- Matching requirements with candidate evidence;
- Identifying information gaps;
- Generating Matching Report content;
- Answering follow-up questions within supported scope.

The AI capability should avoid:

- Making hiring decisions;
- Ranking candidates;
- Predicting future performance;
- Providing unsupported conclusions.


---

# 2. Integration Impact


## 2.1 Frontend Impact

Frontend should support:

- Providing job description input;
- Displaying Matching Report content;
- Displaying follow-up answers;
- Supporting recruiter interaction with AI-generated content.


The frontend is responsible for presenting AI-generated results and user interactions. It does not implement AI analysis logic.


---

## 2.2 Backend Impact

Backend should support:

- Managing communication between application and AI capability;
- Providing required input context for AI processing;
- Managing Matching Report generation requests;
- Maintaining follow-up conversation context;
- Returning AI-generated content to frontend.


The MVP does not require defining:
- Specific AI implementation framework;
- Fixed AI output schema;
- Detailed AI workflow architecture.

These decisions can be made during implementation based on development needs.
