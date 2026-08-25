# Frontend Technical Design

## Document Information


| Field             | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| Document Name     | AI Job Fit Assistant Frontend Technical Design                                         |
| Document Type     | Frontend Technical Design                                                              |
| Version           | v0.3                                                                                   |
| Status            | Draft                                                                                  |
| Related Documents | Product Requirement Document, Lightweight AI Design Decision, Backend Technical Design |




## 1. Frontend Design Goal

### 1.1 Frontend Responsibility

The frontend is responsible for providing the recruiter-facing experience of AI Job Fit Assistant.

The frontend should:

- Provide interfaces for recruiters to input job descriptions;
- Present AI-generated matching analysis results;
- Allow recruiters to view or download the candidate's resume independently;
- Support follow-up question interactions;
- Provide feedback, candidate contact, and owner contact entry points;
- Present clear interaction states during system processing.

The frontend should not:

- Implement AI reasoning logic;
- Determine candidate-job matching results;
- Interpret or modify AI-generated conclusions;
- Implement backend business logic.

The frontend focuses on presenting product information and backend-provided results while enabling recruiter interactions.

### 1.2 Design Principles



#### Clear AI Content Presentation

The frontend should help recruiters understand AI-generated content by:

- Presenting matching analysis clearly;
- Making important information easy to review;
- Separating AI-generated content from user actions.

The frontend should display AI outputs without adding unsupported interpretations.

#### Localization Compatibility

The frontend implementation should remain compatible with future multilingual support.

Requirements:

- Avoid hard-coded user-facing text inside components;
- Keep language configuration separable;
- Avoid architecture decisions that block future localization.

The MVP supports only one language and does not require a complete internationalization system.

#### UI Design Principles

The UI should:

- Prioritize readability of AI analysis;
- Make important actions easy to find;
- Avoid overwhelming recruiters with excessive information;
- Maintain a clear assistant-like interaction experience.



#### Flexible MVP Implementation

The design should provide enough guidance while allowing UI iteration during development.

The document should define:

- User experience;
- Frontend responsibilities;
- Information requirements.

The document should not restrict:

- Exact UI layout;
- Specific component implementation;
- Visual styling details.



## 2. Page Structure



### 2.1 Job Assistant Workspace Structure

The frontend is designed around a Job Assistant Workspace.

```text
Job Assistant Workspace

├── Conversation Area
│
│   ├── AI Output
│   │   ├── Initial Guidance
│   │   ├── Matching Analysis
│   │   └── Follow-up Answers
│   │
│   ├── User Input
│   │   ├── Job Description
│   │   └── Follow-up Questions
│   │
│   └── Contextual Action Area
│       ├── View Resume
│       ├── Contact Candidate
│       └── Submit Feedback
│
└── Navigation
    ├── Resume Preview
    └── Contact Me (Same as Contact Candidate for MVP but with different name)
```

The workspace should support the complete recruiter evaluation process without requiring users to switch between unrelated pages.

### 2.2 Core Components



#### Conversation Area

Responsible for supporting the main AI assistant interaction.

It includes:

- AI-generated messages;
- User inputs;
- Matching analysis;
- Follow-up question interactions.



#### Contextual Action Area

Responsible for providing actions related to the current evaluation context.

It includes:

- View Resume;
- Contact Candidate;
- Submit Feedback.

These actions become available after relevant information is presented, such as the matching analysis result.

#### Navigation

Responsible for providing independent access to major capabilities.

It includes:

- Resume Preview;
- Contact Me.

These capabilities can be accessed without going through the full conversation flow.

## 3. User Experience Design



### 3.1 Job Assistant Workspace Overview

The primary user journey:

```text
Enter Job Assistant

↓

Receive Initial Guidance

↓

Provide Job Description

↓

Receive Matching Analysis

↓

Review Analysis

↓

Optional Actions:
- View Resume
- Ask Follow-up Questions
- Submit Feedback
- Contact Candidate
```

The user can access Resume Preview and Contact Candidate either independently or from the matching analysis context.

### 3.2 Job Description Input

Purpose:

Allow recruiters to provide job requirements for candidate matching analysis.

User interaction:

1. Recruiter enters job description.
2. Frontend submits the input to backend.
3. Frontend displays processing status.
4. Frontend presents returned AI analysis.

Frontend responsibility:

- Collect user input;
- Submit the request;
- Display processing status.



### 3.3 Matching Analysis

Purpose:

Provide recruiters with AI-generated candidate-job fit analysis.

User interaction:

1. Recruiter submits job description.
2. AI generates matching analysis.
3. Frontend displays the analysis result.
4. Recruiter can continue evaluation through available actions.

Frontend responsibility:

- Render AI-generated analysis;
- Provide contextual actions;
- Avoid modifying or interpreting AI conclusions.

Available actions:

- View Resume;
- Contact Candidate;
- Submit Feedback;
- Ask Follow-up Questions through the conversation input.



### 3.4 Resume Preview

Purpose:

Provide recruiters with direct access to the candidate's original resume file.

User interaction:

Recruiters can:

- Open Resume Preview independently;
- Open Resume Preview from matching analysis context;
- View the original resume;
- Download the resume when supported.

Frontend responsibility:

- Provide entry points for accessing Resume Preview;
- Display the candidate's original resume file;
- Support resume viewing and downloading.



### 3.5 Follow-up Questions

Purpose:

Allow recruiters to ask additional questions after reviewing the matching analysis.

User interaction:

1. Recruiter enters a follow-up question.
2. Frontend sends the question to backend.
3. Frontend displays AI response.

Frontend responsibility:

- Provide question input;
- Display user questions;
- Display AI answers.

The frontend does not determine whether a question is within supported scope.

### 3.6 Feedback

Purpose:

Collect optional recruiter feedback after reviewing matching analysis.

User interaction:

1. Recruiter selects feedback entry.
2. Recruiter submits feedback.
3. Frontend displays submission status.

Frontend responsibility:

- Provide feedback entry;
- Submit feedback information;
- Display feedback submission result.



### 3.7 Contact Candidate (Contact Me)

Purpose:

Allow recruiters to access candidate contact information.

User interaction:

Recruiters can:

- Access contact information independently through navigation;
- Access contact action after reviewing matching analysis.

Frontend responsibility:

- Provide contact entry points;
- Allow recruiters to optionally provide their name for contact initiation;
- Display candidate contact information.



## 4. Frontend Behavior and Data Requirements



### 4.1 Data Requirements and Sources

The frontend requires backend-provided information for:


| Scenario            | Required Data                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| Initial Guidance    | Frontend static/configured content                                                                           |
| Matching Analysis   | Backend-provided AI-generated content                                                         |
| Follow-up Questions | Backend-provided AI-generated answers                                                                                   |
| Resume Preview      | Backend-provided candidate resume file                                                                      |
| Contact Candidate   | Frontend static content |
| Feedback            | Backend-provided submission result/status                                                             |


For MVP:

- Candidate information comes from predefined candidate data;
- Resume information belongs to the predefined candidate;
- AI-generated content is returned as text/Markdown.



### 4.2 Loading and Processing States

The MVP uses synchronous request-response interaction.

The frontend should provide:

- Processing status during AI generation;
- Clear feedback while waiting for backend responses;
- Result display after processing completes.



### 4.3 Error Handling

The frontend should handle:

- Invalid user input;
- Failed backend requests;
- AI processing failures;
- Missing information scenarios.

Errors should be displayed clearly without exposing unnecessary technical details.

### 4.4 User Behavior Tracking

Frontend should provide tracking events for:

- Page visits;
- Job description submission;
- Resume preview click;
- Contact CTA click;
- Feedback submission.

Tracking implementation details are not defined in MVP.

### 4.5 Future Improvements

Streaming AI Response

The MVP uses synchronous response handling for implementation simplicity.

Future iterations may introduce streaming output to:

- Reduce perceived waiting time;
- Provide a more natural AI assistant experience.



## 5. Frontend-Backend Integration Assumptions



### 5.1 Communication Principles

Frontend and backend responsibilities are separated as follows:

Frontend:

- Handles user interaction;
- Presents information;
- Manages UI states.

Backend:

- Provides required data;
- Handles business workflow;
- Manages AI processing.

The frontend consumes backend capabilities and does not implement business logic.

### 5.2 Data Format Assumptions

The frontend assumes:

- AI-generated content should be provided in a frontend-renderable format;
- MVP may use text/Markdown rendering;
- Structured output formats can be introduced in future iterations if required.



### 5.3 Unresolved Decisions

The following decisions can be finalized during implementation:

- Frontend framework and component library;
- Detailed UI layout;
- Resume Preview implementation method;
- Frontend state management approach.

