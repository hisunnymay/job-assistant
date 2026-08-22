# 4. Functional Requirements

## 4.1 Feature List

The MVP includes the following user-facing features:


| ID   | Feature                       | Priority | Description                                                                                                                                             |
| ---- | ----------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| F001 | Candidate Profile Data Source | P0       | Provide structured candidate information as the source for candidate-job fit analysis.                                                                  |
| F002 | Job Description Input         | P0       | Allow recruiters to provide job descriptions as the input for candidate-job matching analysis.                                                          |
| F003 | Matching Report               | P0       | Present evidence-based candidate-job fit analysis, including relevant candidate experience, supporting evidence, and identified information gaps.       |
| F004 | Resume Preview                | P0       | Allow recruiters to review candidate resume information and background details.                                                                         |
| F005 | Ask Follow-up Questions       | P1       | Allow recruiters to ask additional questions about candidate experience or background when the matching report does not provide sufficient information. |
| F006 | Contact CTA                   | P0       | Provide recruiters with a clear method to initiate further communication with the candidate.                                                            |
| F007 | Report Feedback               | P1       | Collect optional recruiter feedback on the usefulness and quality of the matching report.                                                               |


---



# 4.2 Feature Details



## F001 Candidate Profile Data Source



### Overview

Candidate Profile Data Source provides the structured candidate information required for candidate-job fit analysis.

In the MVP, the system uses a predefined candidate profile:

> Mei Chang

The candidate profile is not uploaded by recruiters in the MVP.

---



### User Story

As a recruiter,

I want the system to provide candidate background information,

so that I can understand the candidate’s experience in relation to a specific job requirement.

---



### Functional Requirements

The system should:

- Maintain structured candidate information required for analysis;
- Provide candidate information as the source for generating matching insights;
- Support candidate information beyond basic resume content when available.

---



### Acceptance Criteria

- The system has access to the predefined candidate profile;
- The candidate information can be used to generate a matching report;
- The system does not require recruiters to upload candidate resumes in the MVP.

---



# F002 Job Description Input



### Overview

Job Description Input allows recruiters to provide the target job requirements for candidate-job fit analysis.

---



### User Story

As a recruiter,

I want to provide a job description,

so that the system can analyze whether the candidate matches the role requirements.

---



### Functional Requirements

The system should:

- Allow recruiters to provide job description content;
- Accept unstructured job descriptions as input;
- Use the provided job description as the context for generating a matching report.

---



### Acceptance Criteria

- Recruiters can successfully submit a valid job description;
- The system can process the provided job description;
- The submitted job description is associated with the corresponding analysis session.

---



# F003 Matching Report



### Overview

Matching Report is the core product output of AI Job Fit Assistant.

It presents an evidence-based analysis of candidate-job fit by connecting job requirements with candidate experience.

The report should help recruiters understand:

- Relevant candidate experience;
- Supporting evidence;
- Areas where information is insufficient.

The report supports recruiter decision-making but does not make hiring decisions.

---



### User Story

As a recruiter,

I want to understand how a candidate’s experience matches a job requirement,

so that I can decide whether further communication with the candidate is valuable.

---



### Functional Requirements

The Matching Report should:

- Present the key job requirements evaluated during the analysis;
- Indicate the importance level of each requirement when applicable;
- Present the relationship between job requirements and candidate experience;
- Provide supporting evidence for identified matches;
- Clearly indicate areas where sufficient evidence is unavailable;
- Avoid unsupported conclusions;
- Present results in an understandable format.

The Matching Report should not:

- Provide a final hiring recommendation;
- Replace recruiter judgment;
- Generate unsupported candidate capability claims.

---



### Acceptance Criteria

- After submitting a valid job description, recruiters can access a matching report;
- The report presents the key requirements considered during the evaluation;
- The report indicates requirement importance when applicable;
- The report provides traceable connections between requirements and candidate information;
- The report distinguishes between:
  - Supported evidence;
  - Partial information;
  - Missing information;
- Recruiters can understand why the system reaches each conclusion.

---

分界线
分界线
分界线
分界线

---



# F004 Resume Preview



## Overview

Resume Preview allows recruiters to review the candidate’s background information when evaluating candidate-job fit.

The feature provides additional context beyond the matching report and helps recruiters better understand the candidate’s experience.

In the MVP, the resume belongs to the predefined candidate MeiChang's profile.

---



## User Story

As a recruiter,

I want to review the candidate’s resume information,

so that I can obtain additional context when evaluating candidate-job fit.

---



## Functional Requirements

The Resume Preview should:

- Provide access to candidate resume information;
- Allow recruiters to review candidate background details;
- Support deeper understanding of candidate experience beyond the matching report.

The Resume Preview should not:

- Allow recruiters to upload other candidates’ resumes in the MVP;
- Replace the matching report as the primary evaluation interface.

---



## Acceptance Criteria

- Recruiters can access the candidate resume information and download it;
- Resume information is consistent with the predefined candidate profile;
- Recruiters can navigate between the matching report and resume information.

---



# F005 Ask Follow-up Questions



## Overview

Ask Follow-up Questions allows recruiters to request additional information when the matching report does not fully answer their questions.

This feature provides a limited conversational capability to support recruiter exploration.

The MVP does not provide an open-ended recruitment chatbot.

---



## User Story

As a recruiter,

I want to ask additional questions about the candidate,

so that I can clarify information gaps before deciding whether to contact the candidate.

---



## Supported Question Scope

The follow-up question capability is limited to candidate-related information and matching analysis.

The Agent may answer questions related to:

- Candidate experience and background information;
- Evidence behind matching results;
- Clarification of identified information gaps;
- Additional context available in the candidate profile.

---



## Out-of-Scope Questions

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



## Functional Requirements

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



## Acceptance Criteria

- Recruiters can access the contact CTA after reviewing the matching report;
- Recruiters can copy or use the provided contact information;
- Recruiters can enter their name;
- The system generates a personalized greeting template with the provided name.

---



# F006 Contact CTA



## Overview

Contact CTA provides recruiters with a clear action path to initiate further communication with the candidate.

The feature helps reduce friction during the transition from candidate evaluation to communication by providing convenient contact methods and a predefined greeting template.

The CTA represents the final conversion step of the MVP workflow.

---



## User Story

As a recruiter,

I want to easily contact the candidate after understanding the matching results,

so that I can continue the recruitment communication process.

---



## Functional Requirements

The Contact CTA should:

- Provide a clear contact action after reviewing the matching report;
- Allow recruiters to obtain the candidate’s contact method;
- Support conversion tracking.

---



## Acceptance Criteria

- Recruiters can access the contact action after reviewing candidate information;
- The contact action provides a valid communication method;
- Contact CTA interactions can be tracked by the system.

---



# F007 Report Feedback



## Overview

Report Feedback allows recruiters to provide feedback on the usefulness and quality of the matching report.

The feedback helps evaluate whether the product provides valuable insights and identifies areas for improvement.

---



## User Story

As a recruiter,

I want to provide feedback on the matching report,

so that the product can improve future candidate-job fit analysis.

---



## Functional Requirements

The system should:

- Allow recruiters to submit feedback after reviewing the matching report;
- Associate feedback with the corresponding analysis session;
- Support qualitative feedback collection.

Feedback may include:

- Whether the report was useful;
- Whether evidence provided was sufficient;
- What additional information was needed.

---



## Acceptance Criteria

- Recruiters can submit feedback voluntarily;
- Feedback is stored together with the corresponding analysis context;
- Feedback can be used for future product evaluation.

---



# 4.3 System Requirements



## S001 User Behavior Tracking



## Overview

User Behavior Tracking collects interaction data required to evaluate MVP usage and conversion performance.

This capability supports product iteration by helping understand how recruiters interact with the product.

---



## Functional Requirements

The system should track key user interactions, including:

- Page visits;
- Job description submissions;
- Matching report generation;
- Resume preview views;
- Contact CTA clicks;
- Feedback submissions.

---



## Acceptance Criteria

- User interactions can be recorded;
- Events can be associated with the corresponding user session;
- Tracking data can support MVP success metric evaluation.

---



# S002 Conversation Logging



## Overview

Conversation Logging stores recruiter-agent interaction records for AI evaluation, product optimization, and future improvement.

This capability is intended for internal analysis and is not directly visible to recruiters.

---



## Functional Requirements

The system should store relevant conversation information, including:

- Recruiter questions;
- Agent responses;
- Related analysis context;
- Session information;
- Associated feedback when available.

---

