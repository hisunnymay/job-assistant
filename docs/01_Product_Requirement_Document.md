# AI Job Fit Assistant Product Requirement Document (PRD)

---

# Document Information


| Field         | Description                  |
| ------------- | ---------------------------- |
| Document Name | AI Job Fit Assistant PRD     |
| Document Type | Product Requirement Document |
| Version       | v0.9                         |
| Status        | Approved                     |
| Owner         | Mei Chang                    |
| Last Updated  | 2026-09-01                   |
| Product Stage | MVP Planning                 |


---

## Related Documents

This document defines product requirements and serves as the source of truth for product scope, user scenarios, and functional requirements.

Related documents:


| Document                  | Purpose                                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| AI System Design          | Define AI capability design, Agent workflow, knowledge strategy, and AI-related implementation requirements |
| Frontend Technical Design | Define frontend implementation based on product requirements                                                |
| Backend Technical Design  | Define backend implementation based on product requirements and AI system requirements                      |


---



## Version Log

The Version Log records document changes and the reasons behind those changes.


| Version | Date       | Changes                                                           | Reason                                                           |
| ------- | ---------- | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| v0.9    | 2026-09-01 | Required an obvious persistent “测试模式” label after test-mode activation, with optional color styling as secondary reinforcement. | Ensure testers can immediately recognize the excluded analytics state without relying on color alone. |
| v0.8    | 2026-09-01 | Added the hidden three-click test-mode entry and exit behavior, whole-session metric exclusion, and a dashboard date-range filter. | Allow product testing without contaminating dashboard results and allow evaluators to inspect metrics for a defined period. |
| v0.7    | 2026-09-01 | Added the aggregate Data Dashboard, clarified that distinct-session metrics deduplicate by `sessionId` rather than person, and excluded test-mode sessions from product metrics. | Make MVP usage and conversion results visible while keeping metric interpretation accurate and preventing product testing from affecting reported results. |
| v0.6    | 2026-08-27 | Added an immediate, clearly labelled static example report and truthful elapsed-time guidance for real matching generation. | Let recruiters inspect report value without provider cost or persisted activity while setting accurate expectations for synchronous AI latency. |
| v0.1    | 2026-08-20 | Initial PRD structure created                                     | Establish product requirement documentation structure            |
| v0.2    | 2026-08-27 | Clarified that S001 requires centralized, cross-session event persistence and aggregate metric evaluation. | Ensure the tracking implementation can evaluate MVP usage and conversion rather than retaining data only in an individual browser. |
| v0.3    | 2026-08-27 | Defined Contact Conversion Rate using the generated-report session cohort. | Keep the MVP metric measurable with the approved S001 events and prevent contact-only sessions from inflating conversion. |




## Outline

- [Document Information](#document-information)
  - [Related Documents](#related-documents)
  - [Version Log](#version-log)
- [1. Product Overview](#1-product-overview)
  - [1.1 Product Introduction](#11-product-introduction)
  - [1.2 Product Background](#12-product-background)
  - [1.3 User Problem](#13-user-problem)
  - [1.4 Product Opportunity](#14-product-opportunity)
- [2. Product Goals and Scope](#2-product-goals-and-scope)
  - [2.1 Product Goals](#21-product-goals)
  - [2.2 Success Metrics](#22-success-metrics)
  - [2.3 MVP Scope](#23-mvp-scope)
  - [2.4 MVP Constraints](#24-mvp-constraints)
  - [2.5 MVP Success Risks](#25-mvp-success-risks)
- [3. User and Scenario](#3-user-and-scenario)
  - [3.1 User Definition](#31-user-definition)
  - [3.2 User Scenario](#32-user-scenario)
  - [3.3 User Journey](#33-user-journey)
- [4. Functional Requirements](#4-functional-requirements)
  - [4.1 Feature List](#41-feature-list)
  - [4.2 Feature Details](#42-feature-details)
  - [4.3 System Requirements](#43-system-requirements)
- [5. Future Product Evolution](#5-future-product-evolution)
  - [Phase 1: Conversion Optimization](#phase-1-conversion-optimization)
  - [Phase 2: Product Transparency and Continuous Improvement](#phase-2-product-transparency-and-continuous-improvement)
  - [Phase 3: General Recruitment Assistant](#phase-3-general-recruitment-assistant)

---



# 1. Product Overview



## 1.1 Product Introduction

AI Job Fit Assistant is an AI-assisted job matching tool that helps recruiters quickly understand the relationship between job requirements and candidate experience.

The product analyzes job descriptions and candidate information, identifies relevant job requirements, maps requirements to supporting evidence from candidate experience, and provides structured matching insights.

The product aims to reduce the information gap between recruiters and candidates during the initial screening stage by improving the efficiency of understanding candidate capabilities and job fit.

---



## 1.2 Product Background

Recruitment decisions require understanding whether a candidate’s experience aligns with the requirements of a specific role.

However, current recruitment workflows often rely on manually comparing:

- Job descriptions;
- Candidate resumes;
- Project experiences;
- Additional candidate information.

This creates challenges for both recruiters and candidates.

---



### Candidate-side Challenge

Traditional resumes mainly present:

- Employment history;
- Project descriptions;
- Responsibilities;
- Skills.

However, many job requirements involve contextual capabilities that are difficult to represent through concise resume descriptions, including:

- Problem-solving approaches;
- Product thinking;
- Technical understanding;
- Decision-making process;
- Experience applying skills in specific scenarios.

As a result, candidates may have relevant experience that is not effectively recognized during initial screening.

---



### Recruiter-side Challenge

Recruiters need to determine whether a candidate is worth further communication within a limited amount of time.

However, job requirements and candidate experience are usually represented as unstructured information.

Recruiters need to manually complete:

```text
Job Requirements

↓

Candidate Experience

↓

Evidence of Capability Match
```

This process requires significant time and depends on individual interpretation.

---



## 1.3 User Problem

The product focuses on improving the efficiency of understanding candidate-job fit during the early recruitment stage.

### Recruiter Problem

Recruiters need to quickly evaluate whether a candidate matches a specific role, but existing workflows require manually interpreting the relationship between job requirements and candidate experience.

Key problems:

- Relevant candidate experience may not be obvious from resumes;
- Candidate information may lack sufficient context;
- Manual comparison between JD and resume is time-consuming;
- Missing information is difficult to identify before communication.

Desired outcome:

Recruiters can quickly understand:

- Which job requirements have supporting evidence;
- Which requirements are partially supported;
- Which information requires further confirmation.

---



### Candidate Problem

Candidates need to communicate their capabilities effectively, but traditional resumes have limited space and context.

Key problems:

- Important project context may be omitted;
- Complex experiences are difficult to summarize;
- Relevant experience may not be recognized by recruiters.

Desired outcome:

Candidates can provide additional context to help recruiters better understand their experience.

---



## 1.4 Product Opportunity

The product opportunity is to use AI capabilities to transform unstructured recruitment information into structured matching insights.

Input:

```text
Job Description

+

Candidate Information
```

Output:

```text
Evidence-based Candidate Matching

+

Information Gaps
```

The product helps recruiters reduce the effort required to understand candidate-job fit while allowing candidates to better communicate their relevant experience.

---



# 2. Product Goals and Scope



## 2.1 Product Goals

AI Job Fit Assistant aims to improve the efficiency of candidate-job matching during the early recruitment stage.

The product goals are defined from three perspectives:

---



### User Goal

Help recruiters quickly understand whether a candidate’s experience aligns with a job requirement.

The product should enable recruiters to:

- Identify relevant candidate experience;
- Understand the evidence behind matching results;
- Discover missing information that requires further communication.

---



### Candidate Goal

Help candidates communicate their capabilities more effectively beyond traditional resume limitations.

The product should enable candidates to:

- Provide richer context around their experience;
- Highlight relevant evidence related to a specific role;
- Improve the efficiency of recruitment communication.

---



### Product Validation Goal

Validate whether an AI-assisted matching workflow can improve the efficiency of candidate evaluation and increase the likelihood of further recruiter communication.

The MVP aims to verify:

- Whether recruiters are willing to engage with an AI-assisted matching report during candidate evaluation;
- Whether evidence-based candidate analysis provides useful insights for understanding candidate-job fit;
- Whether the product increases the probability of further communication.

---



## 2.2 Success Metrics

The MVP focuses on validating user behavior and product value perception rather than optimizing recruitment outcomes.

---



### Primary Success Metric



#### Contact Conversion Rate

Definition:

```text
Number of distinct sessions with both a contact CTA click and a generated matching report

/

Number of distinct sessions with a generated matching report
```

Because the MVP has no user accounts, a distinct pseudonymous tracking session is used as the measurable proxy for a user in this calculation. “Distinct” means deduplicated by `sessionId`, not by person. Repeated qualifying events within the same tracking session count once for the relevant side of the conversion calculation, while the same person may be counted again if they start another tracking session.

Both the numerator and denominator use the generated-report session cohort from the same evaluation period; contact-only sessions outside that cohort remain visible in event totals but do not count as converted sessions. Sessions explicitly designated as test mode must be excluded from the Contact Conversion Rate and all supporting product metrics.

Purpose:

Measure whether the product helps users transition from understanding candidate-job fit to taking further communication actions.

---



### Supporting Metrics



#### Product Usage Metrics


| Metric                     | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| Page visits                | Measure product exposure                           |
| JD submissions             | Measure user willingness to use the core feature   |
| Matching reports generated | Measure successful completion of the main workflow |
| Resume preview views       | Measure candidate information exploration          |
| Contact CTA clicks         | Measure conversion behavior                        |


---



#### User Feedback Metrics


| Metric          | Purpose                                                      |
| --------------- | ------------------------------------------------------------ |
| Report Feedback | Measure whether recruiters find the matching analysis useful |


The product collects optional feedback after users review the matching report.

Feedback helps evaluate:

- Whether users understand the value of the analysis;
- Whether the evidence provided is useful;
- What additional information users need before making contact.

---



## 2.3 MVP Scope

The MVP focuses on validating the following core workflow:

```text
Recruiter Provides Job Description

↓

Recruiter Reviews AI-assisted Matching Report

↓

Ask Follow-up Questions (Optional)

↓

Recruiter Decides Whether to Contact Candidate
```

The MVP also includes a lightweight feedback loop to collect user insights for future iteration.

---



### Included Features


| Feature                       | Priority | Description                                                                                                    |
| ----------------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| Candidate Resume Data Source | P0       | Provide the predefined candidate resume as the source for candidate-job fit analysis.                          |
| Job Description Input         | P0       | Allow recruiters to provide job descriptions for matching analysis.                                            |
| Matching Report               | P0       | Present evidence-based analysis of candidate-job fit, including matching insights and missing information.     |
| Resume Preview                | P0       | Allow recruiters to review candidate background information.                                                   |
| Ask Follow-up Questions       | P1       | Allow recruiters to ask additional questions when the matching report does not provide sufficient information. |
| Contact CTA                   | P0       | Provide a clear method for recruiters to initiate further communication.                                       |
| Basic User Behavior Tracking  | P0       | Track key user interactions to evaluate MVP usage and conversion performance.                                  |
| Report Feedback               | P1       | Collect optional feedback on the usefulness of the matching report.                                            |




### Out of Scope

The MVP intentionally does not include:


| Excluded Capability              | Reason                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------- |
| Multi-candidate analysis         | MVP focuses on validating matching analysis for a single candidate profile   |
| Candidate resume upload          | MVP uses a predefined candidate profile                                      |
| Open-ended recruitment assistant | MVP focuses on structured matching analysis rather than general conversation |
| Automated hiring decisions       | The product supports recruiter judgment rather than replacing it             |
| Full multilingual support        | Localization is reserved for future iterations                               |




## 2.4 MVP Constraints

The MVP is designed under the following constraints:


| Constraint           | Description                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Development Timeline | Target completion within one week                                                                                |
| Candidate Scope      | Initial version supports one fixed candidate profile                                                             |
| User Scope           | Initial users are recruiters evaluating one candidate                                                            |
| Product Scope        | Focus on matching analysis and communication conversion                                                          |
| Language Support     | MVP supports a single language experience. The product design should remain compatible with future localization. |




## 2.5 MVP Success Risks

The MVP aims to validate whether an AI-assisted matching workflow can improve candidate evaluation efficiency and increase the likelihood of further recruiter communication.

However, MVP outcomes may be affected by factors beyond product capability. The following risks should be considered when evaluating MVP results.


| Risk                                        | Description                                                                                                                                                                                         | Potential Mitigation                                                                                                                                                  |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Low Recruiter Engagement                    | Recruiters may not open or interact with the AI Job Fit Assistant after receiving the product link. This may indicate insufficient motivation, unclear value proposition, or high interaction cost. | Optimize recruiter outreach messaging, reduce access friction, and improve the explanation of product value.                                                          |
| Low Conversion After Product Usage          | Recruiters may review the matching report but not initiate further communication with the candidate.                                                                                                | Analyze feedback and interaction data to identify whether the issue is caused by insufficient candidate information, requirement mismatch, or other external factors. |
| Insufficient Candidate Information Coverage | The available candidate information may not contain enough evidence to answer recruiter questions or demonstrate relevant experience.                                                               | Improve candidate profile completeness and collect additional information based on identified information gaps.                                                       |
| Limited Trust in AI-generated Analysis      | Recruiters may hesitate to rely on AI-assisted analysis if the reasoning is unclear or unsupported.                                                                                                 | Provide evidence-based explanations, highlight information sources, and avoid unsupported conclusions.                                                                |
| External Recruitment Factors                | Recruitment outcomes may be affected by factors unrelated to the product, such as position status, candidate pool, company hiring decisions, or recruiter workload.                                 | Consider external factors when interpreting MVP results and avoid attributing all outcomes to product performance.                                                    |




# 3. User and Scenario



## 3.1 User Definition



### User Role: Recruiter

The MVP focuses on a single user role: **Recruiter**.

A Recruiter is responsible for evaluating whether a candidate is suitable for a specific job opportunity during the early recruitment stage.

The Recruiter may include different recruitment-related stakeholders, such as HR professionals or hiring decision participants, who share the same product goal:

> Understand candidate-job fit and decide whether further communication is valuable.

---



## 3.2 User Scenario



### Scenario: Recruiter Evaluates Candidate-Job Fit



### Context

A Recruiter receives information about a candidate and needs to evaluate whether the candidate’s experience matches the requirements of a specific role. The MVP is accessed through recruiter outreach scenarios where recruiters receive candidate information and voluntarily visit the AI Job Fit Assistant.

The Recruiter needs to understand the relationship between:

```text
Job Requirements

+

Candidate Experience

↓

Candidate-Job Fit
```

---



### Current Problem

The evaluation process often requires manually comparing:

- Job descriptions;
- Candidate resumes;
- Project experiences;
- Additional candidate information.

This process can be time-consuming and may cause relevant candidate experience to be overlooked.

---



### Desired Outcome

The Recruiter can quickly understand:

- Which job requirements have supporting candidate evidence;
- Which requirements are partially supported;
- Which information requires further clarification.

Based on this understanding, the Recruiter can decide whether to initiate further communication with the candidate.

---



## 3.3 User Journey

The MVP user journey focuses on the Recruiter evaluation workflow.


| Stage                              | User Action                                                          | Product Purpose                                                                                |
| ---------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Preview Example Report (Optional)  | Open the pre-checked report for the fixed candidate and example job description | Understand the output format immediately without starting an AI analysis or saved conversation |
| Input Job Description              | Provide target job requirements                                      | Enable role-specific candidate-job fit analysis                                                |
| Review Matching Report             | Review requirement-evidence matching results generated by the system | Help the Recruiter understand candidate fit and identify information gaps                      |
| Ask Follow-up Questions (Optional) | Ask additional questions about candidate experience or background    | Provide further clarification when the matching report does not contain sufficient information |
| Contact Candidate                  | Initiate further communication with the candidate                    | Complete the recruitment communication flow                                                    |
| Provide Feedback (Optional)        | Submit feedback on the usefulness of the analysis                    | Support product evaluation and future iteration                                                |


---



# 4. Functional Requirements



## 4.1 Feature List

The MVP includes the following features and system capabilities:


| ID   | Feature                       | Priority | Description                                                                                                                                             |
| ---- | ----------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| F001 | Candidate Resume Data Source | P0       | Provide the predefined candidate resume required for AI-powered candidate-job fit analysis.                                                             |
| F002 | Job Description Input         | P0       | Allow recruiters to provide job descriptions as the input for candidate-job matching analysis.                                                          |
| F003 | Matching Report               | P0       | Present evidence-based candidate-job fit analysis, including relevant candidate experience, supporting evidence, and identified information gaps.       |
| F004 | Resume Preview                | P0       | Allow recruiters to review and download candidate resume information.                                                                                   |
| F005 | Ask Follow-up Questions       | P1       | Allow recruiters to ask additional questions about candidate experience or background when the matching report does not provide sufficient information. |
| F006 | Contact CTA                   | P0       | Provide recruiters with a clear method to initiate further communication with the candidate.                                                            |
| F007 | Report Feedback               | P1       | Collect optional recruiter feedback on the usefulness and quality of the matching report.                                                               |
| F008 | Data Dashboard                | P1       | Present aggregate MVP usage and contact-conversion metrics in a read-only dashboard.                                                                     |


---



## 4.2 Feature Details



### F001 Candidate Resume Data Source

#### Overview

Candidate Resume Data Source provides the candidate information used by the AI system for candidate-job fit analysis and follow-up question answering.

In the MVP, the system uses the predefined resume of "Mei Chang" as the only candidate information source. Recruiters should be clearly informed of this limitation before using the analysis result.

---



#### User Story

As a recruiter,
I want the system to analyze candidate information in the context of a job requirement,
so that I can understand the candidate’s experience through matching insights.

---



#### Functional Requirements

The system should:

- Maintain access to the predefined candidate resume required for AI analysis;
- Use the candidate resume as the candidate information source for Matching Report generation;
- Use the candidate resume as candidate context for follow-up question answering.

---



#### Acceptance Criteria

- The system has access to the predefined candidate resume;
- The candidate resume can be used to generate a matching report and answer follow-up questions;
- The candidate resume is not exposed as an editable user input in the MVP.

---



### F002 Job Description Input



#### Overview

Job Description Input allows recruiters to provide the target job requirements for candidate-job fit analysis.

---



#### User Story

As a recruiter,

I want to provide a job description,

so that the system can analyze whether the candidate matches the role requirements.

---



#### Functional Requirements

The system should:

- Allow recruiters to provide job description content;
- Accept unstructured job descriptions as input;
- Use the provided job description as the context for generating a matching report.

---



#### Acceptance Criteria

- Recruiters can successfully submit a valid job description;
- The system can process the provided job description;
- The submitted job description is associated with the corresponding analysis session.

---



### F003 Matching Report



#### Overview

Matching Report is the core product output of AI Job Fit Assistant.

It presents an evidence-based analysis of candidate-job fit by connecting job requirements with candidate experience.

The report should help recruiters understand:

- Relevant candidate experience;
- Supporting evidence;
- Areas where information is insufficient.

The report supports recruiter decision-making but does not make hiring decisions.

---



#### User Story

As a recruiter,

I want to understand how a candidate’s experience matches a job requirement,

so that I can decide whether further communication with the candidate is valuable.

---



#### Functional Requirements

The Matching Report should:

- Present the key job requirements evaluated during the analysis;
- Indicate the importance level of each requirement when applicable;
- Present the relationship between job requirements and candidate experience;
- Provide supporting evidence for identified matches;
- Clearly indicate areas where sufficient evidence is unavailable;
- Avoid unsupported conclusions;
- Present results in an understandable format.
- Offer a clearly labelled, human-checked static example report for the fixed candidate and example job description from the Entrance View;
- Reuse the normal report presentation for the example while explaining that recruiters must submit their own job description to generate a formal report and enable follow-up questions;
- During formal report generation, show the typical `30–60` second range, a real elapsed-second count, and an additional truthful note after 60 seconds without showing a fabricated percentage or unverifiable backend stage.

Opening the static example report must not call the AI provider, create a Conversation, or count as `matching_report_generated`.

The Matching Report should not:

- Provide a final hiring recommendation;
- Replace recruiter judgment;
- Generate unsupported candidate capability claims.

---



#### Acceptance Criteria

- After submitting a valid job description, recruiters can access a matching report;
- The report presents the key requirements considered during the evaluation;
- The report indicates requirement importance when applicable;
- The report provides traceable connections between requirements and candidate information;
- The report distinguishes between:
  - Supported evidence;
  - Partial information;
  - Missing information;
- Recruiters can understand why the system reaches each conclusion.
- Recruiters can open the labelled example report immediately and cannot ask follow-up questions in example mode;
- Example viewing creates no Conversation and no generated-report tracking event;
- Formal generation stops and resets its elapsed-time display on success, failure, retry restart, and page departure while preserving accessible loading and existing recovery behavior.

---



### F004 Resume Preview



#### Overview

Resume Preview provides recruiters with direct access to the candidate's original resume file and allows them to review or download the resume independently.
Recruiters can access the resume independently or from the matching analysis context when additional background information is needed.
In the MVP, the resume belongs to the predefined candidate MeiChang's profile.

---



#### User Story

As a recruiter,

I want to review the candidate’s resume information,

so that I can obtain additional context when evaluating candidate-job fit.

---



#### Functional Requirements

The Resume Preview should:

- Provide access to the predefined candidate resume;
- Allow recruiters to view candidate background information independently;
- Allow recruiters to navigate from the matching report to the resume when additional context is needed;
- Maintain consistency between resume information and the candidate profile used for analysis.

The Resume Preview should not:

- Allow recruiters to upload other candidates’ resumes in the MVP;
- Replace the matching report as the primary evaluation interface.

---



#### Acceptance Criteria

- Recruiters can access the candidate resume information and download the resume file;
- Resume information is consistent with the predefined candidate profile;
- Recruiters can navigate between the matching report and resume information.

---



### F005 Ask Follow-up Questions



#### Overview

Ask Follow-up Questions allows recruiters to request additional information when the matching report does not fully answer their questions.

This feature provides a limited conversational capability to support recruiter exploration.

The MVP does not provide an open-ended recruitment chatbot.

---



#### User Story

As a recruiter,

I want to ask additional questions about the candidate,

so that I can clarify information gaps before deciding whether to contact the candidate.

---



#### Supported Question Scope

The follow-up question capability is limited to candidate-related information and matching analysis.

The Agent may answer questions related to:

- Candidate experience and background information;
- Evidence behind matching results;
- Clarification of identified information gaps;
- Additional context available in the candidate profile.

---



#### Out-of-Scope Questions

The Agent should not answer any questions beyond the supported scope.

For out-of-scope questions, the Agent should:

- Clearly state that the requested information or judgment is not supported;
- Avoid generating speculative answers;
- Redirect the conversation to supported topics when appropriate.

Examples of out-of-scope questions include, but are not limited to:

- Hiring recommendations;
- Candidate ranking or comparison;
- Prediction of future performance;
- Personal judgments about the candidate;
- Information not contained in the available candidate profile.

---



#### Functional Requirements

- Allow recruiters to ask additional questions after reviewing the matching report;
- Maintain the context of the current candidate-job fit analysis during follow-up conversations;
- Answer questions related to candidate experience, background information, matching evidence, and identified information gaps;
- Clearly indicate when requested information is unavailable or outside the supported scope;
- Avoid generating unsupported conclusions or making hiring recommendations.

---



#### Acceptance Criteria

- Recruiters can ask additional questions;
- Questions are answered based on available candidate information;
- Unsupported questions are rejected or redirected;
- The Agent maintains analysis boundaries.

---



### F006 Contact CTA



#### Overview

Contact CTA provides recruiters with a clear action path to initiate further communication with the candidate.

The feature helps reduce friction during the transition from candidate evaluation to communication by providing convenient contact methods and a predefined greeting template.

The CTA represents the final conversion step of the MVP workflow.

---



#### User Story

As a recruiter,

I want to easily contact the candidate after understanding the matching results,

so that I can continue the recruitment communication process.

---



#### Functional Requirements

The Contact CTA should:

- Provide a clear contact action after reviewing the matching report;
- Provide the candidate’s available contact method;
- Provide a predefined greeting template for initial communication;

The greeting template should:

- Support dynamic information insertion based on recruiter input;
- Allow recruiters to provide their name;
- Automatically include the recruiter’s name in the greeting template.

Example:

> Hi, I’m {Recruiter Name}. I learned about your background through AI Job Fit Assistant and found your experience relevant to our current opportunity. I would love to connect and discuss further.

The system should not:

- Automatically send messages on behalf of recruiters;
- Generate misleading statements about the recruitment process;
- Pretend to be an official company communication channel unless configured.

---



#### Acceptance Criteria

- Recruiters can access the contact action after reviewing candidate information;
- The contact action provides a valid communication method;
- Contact CTA interactions can be tracked by the system.

---



### F007 Report Feedback



#### Overview

Report Feedback allows recruiters to provide feedback on the usefulness and quality of the matching report.

The feedback helps evaluate whether the product provides valuable insights and identifies areas for improvement.

---



#### User Story

As a recruiter,

I want to provide feedback on the matching report,

so that the product can improve future candidate-job fit analysis.

---



#### Functional Requirements

The system should:

- Allow recruiters to submit feedback after reviewing the matching report;
- Associate feedback with the corresponding analysis session;
- Support qualitative feedback collection.

Feedback may include:

- Whether the report was useful;
- Whether evidence provided was sufficient;
- What additional information was needed.

---



#### Acceptance Criteria

- Recruiters can submit feedback voluntarily;
- Feedback should be associated with the corresponding matching report for future product evaluation;
- Feedback can be used for future product evaluation.

---



### F008 Data Dashboard



#### Overview

The Data Dashboard provides a read-only view of aggregate MVP usage and contact-conversion performance. It helps evaluate whether recruiters use the core workflow and proceed from reviewing a generated matching report to initiating contact.

The dashboard displays aggregate metrics only. It must not expose individual tracking events, infer personal identity, or display job descriptions, resume content, follow-up questions, feedback comments, contact information, prompts, provider payloads, or other user-entered content.

---



#### User Story

As a product evaluator,

I want to view the product's core usage and contact-conversion metrics,

so that I can evaluate MVP adoption and whether generated matching reports lead to further communication.

---



#### Functional Requirements

The system should:

- Provide a Data Dashboard entry in the persistent workspace navigation;
- Present Contact Conversion Rate as the primary metric, including its percentage, numerator, denominator, and a concise definition;
- Calculate Contact Conversion Rate according to Section 2.2 using distinct pseudonymous tracking sessions. “Distinct” means deduplicated by `sessionId`, not by person;
- Present total counts for page visits, job description submissions, matching reports generated, resume preview views, Contact CTA clicks, and feedback submissions;
- Use the same reporting period and authoritative centralized tracking source for all displayed metrics;
- Provide start-date and end-date controls that allow the evaluator to define the reporting period;
- Treat both selected calendar dates as inclusive in the timezone displayed by the dashboard;
- Apply the selected date range to the primary metric, its numerator and denominator, and all six supporting metrics together;
- Default to all available tracking data within the approved retention period and provide a reset action that restores this default;
- Prevent applying a date range when the start date is later than the end date and explain the validation error clearly;
- Display the reporting period and latest data-update time, including timezone;
- Provide a concise definition for each metric;
- Test-mode sessions must not contribute to dashboard metrics.
- Display clear loading, empty, and retrieval-failure states without affecting the recruiter-facing matching workflow;
- Preserve the active conversation when the user enters or leaves the dashboard.

The initial dashboard does not require:

- Week-over-week or other period comparisons;
- Trend charts;
- Event-level drill-down;
- Data export;
- Real-time automatic refresh.

---



#### Acceptance Criteria

- The dashboard displays Contact Conversion Rate and all six supporting usage metrics from centrally persisted tracking data;
- The Contact Conversion Rate numerator and denominator deduplicate qualifying events by `sessionId`, not by inferred person identity or raw event count;
- Repeated qualifying events within one non-test session count once for the relevant side of the Contact Conversion Rate calculation;
- Supporting metric cards display total accepted event counts for the reporting period, so their values may differ from the distinct-session numerator and denominator;
- Events from test-mode sessions do not contribute to the primary metric, its numerator or denominator, or any supporting metric;
- A zero denominator produces a valid empty or zero-rate presentation rather than an invalid numeric value;
- All displayed metrics use the same reporting period and show the latest update time with timezone;
- Selecting and applying a valid date range updates the primary metric, its numerator and denominator, and all six supporting metrics consistently;
- The selected start and end dates are both included in the calculation according to the dashboard's displayed timezone;
- Resetting the date filter restores all available tracking data within the approved retention period;
- An invalid date range cannot be applied and does not replace the last valid dashboard result;
- The dashboard exposes aggregate values only and does not reveal individual events or user-entered or candidate content;
- Loading, no-data, and retrieval-failure states are understandable and recoverable;
- No week-over-week comparison value, direction indicator, or comparison calculation is displayed in the initial dashboard.

---



## 4.3 System Requirements



### S001 User Behavior Tracking



#### Overview

User Behavior Tracking centrally collects interaction data required to evaluate MVP usage and conversion performance across recruiter sessions and browser instances.

This capability supports product iteration by helping understand how recruiters interact with the product. Browser-local data alone is not an authoritative analytics source because it cannot support aggregate MVP evaluation.

---



#### Functional Requirements

The system should track key user interactions, including:

- Page visits;
- Job description submissions;
- Matching report generation;
- Resume preview views;
- Contact CTA clicks;
- Feedback submissions.

Each event should include a pseudonymous tracking-session identifier and timestamp. Events created after a Conversation exists should also include the corresponding Conversation identifier.

Events must be sent to and persist in a centralized backend-owned store so authorized MVP evaluators can aggregate behavior across sessions. Tracking must not include job descriptions, resume content, follow-up questions, feedback comments, contact data, prompts, provider payloads, or other user-entered content.

The standalone Entrance View provides a hidden test-mode entry through the visible “AI” portion of the product title. Selecting “AI” three consecutive times within two seconds designates the current tracking session as test mode. The click sequence resets when the two-second window expires.

After activation, the interface must display a persistent, clearly visible “测试模式” text label next to the product identity and provide an explicit exit action. The product-title styling may also change color as secondary reinforcement, but color alone must not communicate the state. The label remains visible in the Entrance View and persistent workspace navigation. Test mode remains active for the current browser-tab session across navigation and page refresh. Exiting test mode removes the label, restores the normal product-title styling, and starts a new non-test tracking session so later production activity is not associated with the excluded test session.

Test-mode designation applies to every event associated with that session's `sessionId`, including events accepted before test mode was activated. Events associated with a test-mode session must not contribute to the primary success metric, any supporting product metric, or any dashboard date range.

Test mode changes analytics classification only. It must not silently change AI-provider behavior, conversation or feedback persistence, matching behavior, or another recruiter-facing workflow.

---



#### Acceptance Criteria

- Every required interaction is persisted in the centralized tracking store with its event name, event identifier, timestamp, and pseudonymous tracking-session identifier;
- Events can be associated with the corresponding Conversation when one exists without treating the Conversation identifier as the tracking-session identifier;
- Authorized evaluators can run a documented aggregate report across sessions to calculate the supporting usage metrics and the distinct-session Contact Conversion Rate defined in Section 2.2;
- Distinct-session metrics deduplicate qualifying events by `sessionId`, not by inferred person identity;
- Events from sessions explicitly designated as test mode do not contribute to the Contact Conversion Rate or supporting product metrics;
- Selecting the “AI” title text three consecutive times within two seconds on the Entrance View activates test mode for the current tracking session;
- Activating test mode immediately displays a persistent “测试模式” text label next to the product identity; color may reinforce but must not be the only indicator;
- The test-mode label remains visible across navigation and refresh until the user exits test mode or the browser-tab session ends;
- Exiting test mode removes the label and restores the normal product-title styling;
- Activating test mode excludes all events associated with the current `sessionId`, including events accepted earlier in that session, from every dashboard date range;
- Exiting test mode creates a new non-test tracking session before later trackable activity is recorded;
- Test mode does not change AI execution, business-data persistence, or recruiter-facing workflow behavior;
- Clearing one browser's local data does not remove events already accepted by the centralized store;
- Tracking payloads exclude user-entered and candidate content, and tracking failures do not prevent completion of the recruiter journey;
- Tracking data is retained only for the approved MVP evaluation period defined in the Backend Technical Design.

---



### S002 Conversation Logging



#### Overview

Conversation Logging stores recruiter-agent interaction records for AI evaluation, product optimization, and future improvement.

This capability is intended for internal analysis and is not directly visible to recruiters.

---



#### Functional Requirements

The system should store relevant conversation information, including:

- Recruiter questions;
- Agent responses;
- Related analysis context;
- Session information;
- Associated feedback when available.

---



# 5. Future Product Evolution

The MVP focuses on validating the core workflow of helping recruiters understand candidate-job fit through evidence-based matching analysis.

Future product evolution will focus on improving conversion effectiveness, increasing product transparency, and expanding the product into a broader recruitment assistant.

---



## Phase 1: Conversion Optimization



### Goal

Improve the effectiveness of the recruitment communication flow and increase the likelihood of recruiter engagement.

### Potential Features


| Feature                        | Description                                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Matching Visualization         | Provide more intuitive visual representations of candidate-job fit analysis.                                           |
| Requirement Coverage Charts    | Visualize the proportion of job requirements supported by candidate evidence.                                          |
| Enhanced Follow-up Capability  | Improve follow-up interactions by providing richer context exploration while maintaining controlled answer boundaries. |
| Missing Information Collection | Collect recruiter-requested information gaps to improve candidate profile completeness.                                |
| Feedback-driven Optimization   | Use recruiter feedback and interaction data to improve matching report quality and product effectiveness.              |


---



## Phase 2: Product Transparency and Continuous Improvement



### Goal

Demonstrate continuous product iteration and improve transparency of product development.

### Potential Features


| Feature                      | Description                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------- |
| Product Updates              | Display product changes and iteration history.                                    |
| Roadmap Display              | Provide visibility into planned future improvements and feature directions.       |
| Product Design Documentation | Provide access to product decisions, design rationale, and related documentation. |


---



## Phase 3: General Recruitment Assistant



### Goal

Expand the product from a single-candidate validation scenario into a broader recruitment assistance tool.

### Potential Features


| Feature                  | Description                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------- |
| Resume Upload            | Allow recruiters to upload candidate resumes for analysis.                              |
| Multi-candidate Analysis | Support analysis across multiple candidates.                                            |
| Candidate Comparison     | Enable comparison between candidates based on job requirements and supporting evidence. |
| Interview Assistance     | Provide support for interview preparation and candidate evaluation workflows.           |
