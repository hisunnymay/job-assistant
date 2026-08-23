# PRD Creation Retrospective: Process Review and Learning Summary

## Outline

- [1. Purpose of This Review](#1-purpose-of-this-review)
  - [1.1 Goal](#11-goal)
- [2. Starting Point: Initial Product Definition](#2-starting-point-initial-product-definition)
  - [2.1 Original Starting Point](#21-original-starting-point)
  - [2.2 Initial Challenges](#22-initial-challenges)
  - [2.3 Initial Assumption vs Final Understanding](#23-initial-assumption-vs-final-understanding)
  - [Learning 1: Define Document Boundaries Before Writing Detailed Features](#learning-1-define-document-boundaries-before-writing-detailed-features)
- [3. Major Turning Point 1: From Stakeholder Mapping to Actual User Definition](#3-major-turning-point-1-from-stakeholder-mapping-to-actual-user-definition)
  - [3.1 Initial Approach](#31-initial-approach)
  - [3.2 Problem Identified](#32-problem-identified)
  - [3.3 Turning Point](#33-turning-point)
  - [3.4 Final Decision](#34-final-decision)
  - [3.5 Why This Change Was Important](#35-why-this-change-was-important)
  - [3.6 Could This Have Been Avoided Earlier?](#36-could-this-have-been-avoided-earlier)
  - [Learning 2: Define Users Based on Interaction, Not Organizational Roles](#learning-2-define-users-based-on-interaction-not-organizational-roles)
  - [Reflection](#reflection)
- [4. Major Turning Point 2: From System Workflow to User Journey](#4-major-turning-point-2-from-system-workflow-to-user-journey)
  - [4.1 Initial Approach](#41-initial-approach)
  - [4.2 Problem Identified](#42-problem-identified)
  - [4.3 Turning Point](#43-turning-point)
  - [4.4 Final Decision](#44-final-decision)
  - [4.5 Why This Change Was Important](#45-why-this-change-was-important)
  - [4.6 Could This Have Been Avoided Earlier?](#46-could-this-have-been-avoided-earlier)
  - [Learning 3: In AI Products, Separate "Reasoning Process" from "User Value"](#learning-3-in-ai-products-separate-reasoning-process-from-user-value)
  - [Reflection](#reflection-1)
- [5. Major Turning Point 3: From Feature Expansion to MVP Validation Thinking](#5-major-turning-point-3-from-feature-expansion-to-mvp-validation-thinking)
  - [5.1 Initial Approach](#51-initial-approach)
  - [5.2 Problem Identified](#52-problem-identified)
  - [5.3 Turning Point: Defining the Validation Goal First](#53-turning-point-defining-the-validation-goal-first)
  - [5.4 Feature Evaluation Framework](#54-feature-evaluation-framework)
  - [5.5 Final MVP Philosophy](#55-final-mvp-philosophy)
  - [5.6 Could This Have Been Avoided Earlier?](#56-could-this-have-been-avoided-earlier)
  - [Learning 4: MVP Scope Should Be Defined by Validation Needs, Not Product Possibilities](#learning-4-mvp-scope-should-be-defined-by-validation-needs-not-product-possibilities)
  - [Reflection](#reflection-2)
- [6. Major Turning Point 4: From General Product Success to Measurable Validation Logic](#6-major-turning-point-4-from-general-product-success-to-measurable-validation-logic)
  - [6.1 Initial Approach](#61-initial-approach)
  - [6.2 Problem Identified](#62-problem-identified)
  - [6.3 Turning Point: Separating Product Influence from External Outcomes](#63-turning-point-separating-product-influence-from-external-outcomes)
  - [6.4 Final Validation Logic](#64-final-validation-logic)
  - [6.5 Why Contact CTA Became the Key Metric](#65-why-contact-cta-became-the-key-metric)
  - [6.6 Risk Analysis Evolution](#66-risk-analysis-evolution)
  - [6.7 Could This Have Been Avoided Earlier?](#67-could-this-have-been-avoided-earlier)
  - [Learning 5: Metrics Should Measure Controllable User Behavior, Not Final Business Outcomes](#learning-5-metrics-should-measure-controllable-user-behavior-not-final-business-outcomes)
  - [Reflection](#reflection-3)
- [7. Major Turning Point 5: Feature Boundary Refinement — Candidate Profile Data Source vs Resume Preview](#7-major-turning-point-5-feature-boundary-refinement-candidate-profile-data-source-vs-resume-preview)
  - [7.1 Initial Approach](#71-initial-approach)
  - [7.2 Problem Identified](#72-problem-identified)
  - [7.3 Turning Point](#73-turning-point)
  - [7.4 Final Decision](#74-final-decision)
  - [7.5 Why This Change Was Important](#75-why-this-change-was-important)
  - [7.6 Could This Have Been Avoided Earlier?](#76-could-this-have-been-avoided-earlier)
  - [Learning 6: In AI Products, Separate Data Source, User Interface, and Intelligence Layer](#learning-6-in-ai-products-separate-data-source-user-interface-and-intelligence-layer)
  - [Reflection](#reflection-4)
- [8. Process Retrospective: What Could Have Been Improved in the PRD Creation Process](#8-process-retrospective-what-could-have-been-improved-in-the-prd-creation-process)
  - [8.1 What Worked Well](#81-what-worked-well)
  - [8.2 What Caused Unnecessary Iterations](#82-what-caused-unnecessary-iterations)
  - [8.3 Issue 2: User Definition Started From Business Roles](#83-issue-2-user-definition-started-from-business-roles)
  - [8.4 Issue 3: PRD and AI Design Boundary Should Be Defined Earlier](#84-issue-3-prd-and-ai-design-boundary-should-be-defined-earlier)
  - [8.5 Improved Future PRD Creation Process](#85-improved-future-prd-creation-process)
- [9. Final Learning Summary](#9-final-learning-summary)
  - [Principle 1](#principle-1)
  - [Principle 2](#principle-2)
  - [Principle 3](#principle-3)
  - [Principle 4](#principle-4)
  - [Overall Retrospective Conclusion](#overall-retrospective-conclusion)

---

## 1. Purpose of This Review

### 1.1 Goal

This review aims to understand how the AI Job Fit Assistant PRD evolved from an initial product idea into a structured product requirement document, and extract reusable principles for future product design work.

The focus is not only the final PRD quality, but also:

- How decisions were made;
- Why certain directions changed;
- Which iterations were necessary;
- Which iterations could have been avoided with a better process.

The final PRD became the source of truth for:

- Product scope;
- User scenarios;
- Functional requirements;

while explicitly separating responsibilities from:

- AI System Design;
- Frontend Technical Design;
- Backend Technical Design.

---



## 2. Starting Point: Initial Product Definition



### 2.1 Original Starting Point

At the beginning, the product idea was already relatively clear:

> Build an AI-assisted job matching tool that helps recruiters understand how a candidate's experience matches a job requirement.

The original product concept focused on:

- Parsing Job Description;
- Understanding candidate experience;
- Matching requirements with evidence;
- Helping recruiters decide whether to continue communication.

This core idea remained stable throughout the PRD process.

The final PRD still describes the product as:

> "an AI-assisted job matching tool that helps recruiters quickly understand the relationship between job requirements and candidate experience." 

The biggest changes were not about **what the product is**, but about:

- How to define its boundaries;
- How to represent users;
- How to separate product requirements from implementation details.

---



### 2.2 Initial Challenges

The first version of thinking had several natural ambiguities caused by the nature of AI products.

Unlike traditional software, an AI product often has three different layers:

```
User Value Layer

        ↓

Product Feature Layer

        ↓

AI Capability Layer
```

At the beginning, these layers were not fully separated.

For example:

```
Job Requirement Analysis

Hard / Soft Requirement Classification

Requirement-Evidence Matching

Unknown Information Detection

Matching Report
```

were initially treated similarly.

However, later we recognized:

- The first four are **internal AI capabilities**;
- Matching Report is the **user-facing product output**.

This eventually led to the document boundary:

- PRD defines user-facing requirements;
- AI System Design defines Agent workflow and AI capability implementation.

This boundary is now explicitly reflected in the PRD:

> AI System Design defines AI capability design, Agent workflow, knowledge strategy, and AI-related implementation requirements. 

---



### 2.3 Initial Assumption vs Final Understanding



#### Initial Assumption

The product could be described by listing all capabilities involved in generating the result.

Example:

```
Input JD

↓

Analyze Requirements

↓

Classify Requirements

↓

Match Evidence

↓

Detect Missing Information

↓

Generate Report
```

This is a natural engineering-oriented view.

---



#### Final Understanding

A PRD should describe:

> What value the user receives.

Not:

> Every internal step required to create that value.

Therefore:

PRD:

```
Job Description Input

↓

Matching Report

↓

Communication Decision
```

AI Design:

```
Requirement Analysis

↓

Classification

↓

Evidence Matching

↓

Unknown Detection

↓

Report Generation
```

---



### Learning 1: Define Document Boundaries Before Writing Detailed Features

The biggest efficiency improvement for future PRDs would be:

Before writing the feature list, first answer:

#### Question:

"Is this document describing:

A. User value?

B. Product behavior?

C. System implementation?"

A simple classification table could prevent many iterations:


| Item                        | Belongs to      |
| --------------------------- | --------------- |
| User sees matching report   | PRD             |
| User clicks contact CTA     | PRD             |
| Agent extracts requirements | AI Design       |
| Prompt strategy             | AI Design       |
| Database storage            | Backend Design  |
| Component layout            | Frontend Design |


---

---

## 3. Major Turning Point 1: From Stakeholder Mapping to Actual User Definition

### 3.1 Initial Approach

At the beginning, we considered multiple roles involved in recruitment:

- HR / Recruiter;
- Hiring Manager;
- Product Leader / Role Owner.

This was a common product-thinking approach because in enterprise products, multiple stakeholders often influence usage and decision-making.

The initial assumption was:

> If a person is involved in the recruitment process, they may need to be represented as a user role.

This led to a broader user model.

---

### 3.2 Problem Identified

During the User and Scenario discussion, we identified a key distinction:

#### Stakeholder ≠ User

A stakeholder may:

- Care about the outcome;
- Influence decisions;
- Provide requirements;

but may not directly interact with the product.

The critical question became:

> Who actually uses this MVP?

For this product:

- Who inputs information?
- Who reads the output?
- Who asks questions?
- Who clicks the contact CTA?

The answer was:

> Recruiter.

The PRD eventually simplified the user scope:

> The MVP focuses on a single user role: Recruiter. 

(Exact line reference should be updated from the final User Definition section.)

---



### 3.3 Turning Point

The biggest realization was:

The MVP is not building a complete recruitment workflow system.

It is validating one specific hypothesis:

> Can AI-assisted candidate matching help recruiters better understand candidate fit and initiate further communication?

The product does not currently support:

- Hiring Manager approval;
- Candidate management;
- Internal recruitment collaboration;
- Multiple decision makers.

Therefore, introducing those roles created unnecessary complexity.

---



### 3.4 Final Decision

The final user model became:

```
Primary User:

Recruiter
```

Other roles were treated differently:


| Role           | Treatment                          |
| -------------- | ---------------------------------- |
| Recruiter      | Product user                       |
| Candidate      | Data subject / information source  |
| Hiring Manager | Future stakeholder, not MVP user   |
| Product Leader | Internal stakeholder, not MVP user |


This aligned with the MVP scope:

- Fixed candidate profile;
- Single recruiter workflow;
- Matching report as the core output.

The Project Alignment Document also established that the MVP focuses on a fixed candidate profile (Mei Chang) and a recruitment communication scenario. 

---



### 3.5 Why This Change Was Important

This change simplified several downstream decisions.

#### Before:

User Journey needed to answer:

```
Recruiter:
- What do they do?

Hiring Manager:
- What do they do?

Candidate:
- What do they do?

Product Owner:
- What do they do?
```

This created unnecessary branches.

---



#### After:

The journey became:

```
Recruiter receives candidate information

↓

Visits product

↓

Inputs Job Description

↓

Reviews Matching Report

↓

Decides whether to contact candidate
```

This directly maps to the MVP validation goal.

The MVP core workflow in the alignment document follows this simplified path:

> Recruiter receives candidate information → Visits AI Job Fit Assistant → Inputs Job Description → AI generates Matching Report → Recruiter reviews Matching Report → Recruiter decides whether to contact candidate. 

---



### 3.6 Could This Have Been Avoided Earlier?

Partially yes.

The unnecessary iteration came from using a traditional enterprise-product mindset.

A better early question would have been:

> "Who is the person performing the MVP action?"

instead of:

> "Who is related to this business process?"

A more efficient process:

Before creating User Definition:

#### Step 1

List all stakeholders:

```
Recruiter
Hiring Manager
Candidate
Business Owner
```



#### Step 2

Classify:


| Question                 | Example                |
| ------------------------ | ---------------------- |
| Uses the product?        | Recruiter              |
| Provides data?           | Candidate              |
| Receives indirect value? | Hiring Manager         |
| Owns business outcome?   | Product/Business Owner |




#### Step 3

Only users enter User Journey.

---



### Learning 2: Define Users Based on Interaction, Not Organizational Roles

For future PRDs:

Avoid:

> "Who is involved in the business process?"

Prefer:

> "Who performs actions inside this product?"

This is especially important for MVPs.

A narrow user definition:

- Reduces feature expansion;
- Makes user journey clearer;
- Improves validation accuracy.

---



### Reflection

This was one of the more valuable changes in the PRD process.

Unlike the AI capability boundary issue, this was not mainly a documentation problem. It was a product strategy clarification.

The discussion helped answer:

> Are we building a recruitment platform?

No.

> Are we building a tool that helps recruiters evaluate one candidate faster?

Yes.

That narrower positioning made the rest of the PRD much easier.

---

---

## 4. Major Turning Point 2: From System Workflow to User Journey

### 4.1 Initial Approach

In the early PRD drafts, we described the MVP workflow using the steps required for the Agent to generate the final output.

The workflow looked like:

```text
Job Description Input

↓

Job Requirement Analysis

↓

Candidate Information Matching

↓

Evidence-based Matching Report

↓

Further Communication
```

This was a reasonable description from a system perspective because these are indeed the logical steps required to produce the matching result.

The Project Alignment Document also described similar internal processing steps:

```text
AI analyzes requirements

↓

AI maps requirements to candidate evidence

↓

Recruiter reviews matching report
```

---



### 4.2 Problem Identified

The problem was not that the workflow was incorrect.

The problem was:

> The same workflow was trying to represent two different things.

It mixed:

#### User Journey

The question:

> What does the recruiter do?

Example:

```text
Recruiter enters JD

↓

Reviews report

↓

Decides whether to contact candidate
```

---



#### AI Workflow

The question:

> How does the Agent generate the report?

Example:

```text
JD

↓

Requirement Extraction

↓

Requirement Classification

↓

Evidence Matching

↓

Gap Detection

↓

Report Generation
```

---

The confusion happened because AI products naturally expose internal reasoning as part of their value proposition.

For traditional software:

```text
User clicks button

↓

System processes data

↓

User receives result
```

The separation is obvious.

For AI products:

```text
User enters request

↓

Agent reasons

↓

Agent generates answer
```

The reasoning process itself can look like a product feature.

---



### 4.3 Turning Point

The key question became:

> "Would the recruiter actually perform this step?"

For each step:

#### Job Requirement Analysis

Would recruiter do this?

No.

The recruiter provides the JD.

The Agent analyzes it.

---



#### Hard / Soft Requirement Classification

Would recruiter do this?

No.

It is an internal interpretation capability.

---



#### Requirement-Evidence Matching

Would recruiter do this?

No.

It is the core intelligence behind the report.

---



#### Unknown Information Detection

Would recruiter do this?

No.

It is another internal analysis capability.

---



#### Matching Report

Would recruiter interact with this?

Yes.

This is the actual product output.

---

This distinction allowed us to move:

From:

```text
Feature = every capability needed to generate result
```

To:

```text
Feature = user-visible capability that helps validate product value
```

---



### 4.4 Final Decision

The final PRD structure separated:

#### User-facing Product Flow

```text
Job Description Input

↓

Matching Report

↓

Ask Follow-up Questions (Optional)

↓

Contact Candidate
```

---



#### AI Internal Capability Flow

```text
Job Requirement Analysis

↓

Hard / Soft Requirement Classification

↓

Requirement-Evidence Matching

↓

Unknown Information Detection

↓

Matching Report Generation
```

---

This also affected the Feature List.

The initial feature list contained:

- Job Requirement Analysis;
- Hard / Soft Requirement Classification;
- Requirement-Evidence Matching;
- Unknown Information Detection;
- Matching Report.

The later understanding was:

The first four are not independent user features.

They are the internal capabilities required by the Matching Report.

The final PRD therefore positions Matching Report as the core user-facing capability.

---



### 4.5 Why This Change Was Important

This decision improved several later documents.

#### For PRD

The product requirement remains focused:

> What value does the recruiter receive?

---



#### For AI System Design

The Agent design becomes clearer:

> What capabilities are needed to generate that value?

---



#### For Frontend Design

The interface becomes clearer:

The frontend does not need pages for:

- Requirement Analysis;
- Evidence Matching;
- Unknown Detection.

It needs:

- Input;
- Report display;
- Follow-up interaction;
- Contact action.

---



### 4.6 Could This Have Been Avoided Earlier?

Partially yes.

This iteration could have been reduced by introducing a simple classification step before creating the Feature List.

For every candidate feature, ask:

#### Question 1

Does the user directly interact with it?

If yes:

→ Product Feature

---



#### Question 2

Does it describe how AI/system reaches the result?

If yes:

→ Technical Capability

---

Example:


| Item                  | Classification    |
| --------------------- | ----------------- |
| Job Description Input | Product Feature   |
| Matching Report       | Product Feature   |
| Resume Preview        | Product Feature   |
| Requirement Analysis  | AI Capability     |
| Evidence Matching     | AI Capability     |
| Prompt Strategy       | AI Implementation |


---



### Learning 3: In AI Products, Separate "Reasoning Process" from "User Value"

A common mistake in AI product documentation is:

> Treating the model's internal process as product functionality.

A better approach:

Start from:

```text
User Problem

↓

Desired User Outcome

↓

User-facing Capability

↓

Required AI Capability
```

not:

```text
AI Capability

↓

Expose Everything as Features
```

---



### Reflection

This was probably the most important structural improvement in the PRD process.

The final PRD became much cleaner because it stopped explaining:

> "How the AI works"

and focused on:

> "What the recruiter can accomplish with the AI."

This boundary will also be useful when creating the next documents:

- AI System Design explains the reasoning process;
- Frontend Design explains interaction;
- Backend Design explains data/system support.

---

---

## 5. Major Turning Point 3: From Feature Expansion to MVP Validation Thinking

### 5.1 Initial Approach

At the beginning of the project, the natural instinct was:

> Build enough capabilities to demonstrate what an AI recruitment assistant could do.

The initial MVP feature list contained many capabilities:

- Job Description Input;
- Job Requirement Analysis;
- Hard / Soft Requirement Classification;
- Candidate Knowledge Base;
- Requirement-Evidence Matching;
- Unknown Information Detection;
- Resume Preview;
- Contact CTA;
- Basic User Behavior Tracking.



This reflected a capability-oriented mindset:

```text
id="b0w9y7"
What can an AI recruitment assistant do?

↓

List all possible capabilities

↓

Build the demo
```

This is understandable because the product idea itself was AI-driven.

---

### 5.2 Problem Identified

The issue was:

A good demo and a good MVP are not always the same thing.

A demo asks:

> "Can we show interesting AI capabilities?"

An MVP asks:

> "Can we validate whether this product solves a meaningful problem?"

These are different objectives.

---

The key question became:

> What is the smallest product that can prove the core hypothesis?

The hypothesis was not:

> Can an LLM analyze a JD and resume?

That was already technically possible.

The real question was:

> Will recruiters find AI-assisted candidate-job fit analysis useful enough to take further action?

---

### 5.3 Turning Point: Defining the Validation Goal First

The MVP goal became more focused:

The product should validate:

1. Whether recruiters are willing to use an AI-assisted matching tool;
2. Whether the tool helps recruiters understand candidate fit;
3. Whether the tool improves recruitment communication conversion.



This changed the way features were evaluated.

Instead of asking:

> "Is this feature impressive?"

We started asking:

> "Does this feature help validate the MVP hypothesis?"

---

### 5.4 Feature Evaluation Framework

The new evaluation method became:

```text
Feature

↓

Does it support the validation goal?

↓

Is it required for MVP?

↓

Keep / Reduce / Remove
```

---

#### Example 1: Matching Report

Question:

Does it validate the hypothesis?

Yes.

Because it is the main mechanism through which recruiters understand candidate fit.

Decision:

✅ Core MVP feature.

---

#### Example 2: Ask Follow-up Questions

Question:

Does it help validate the hypothesis?

Partially.

It improves the experience, but the product can still validate the core idea without it.

Decision:

P1.

---

#### Example 3: Resume Preview

This was more subtle.

Initially it looked like an additional convenience feature.

Later we identified another value:

> It provides source transparency and helps recruiters verify AI analysis.

Therefore:

Decision:

Keep as P0.

---

#### Example 4: Multi-candidate comparison

Question:

Does it help validate the MVP hypothesis?

No.

The MVP is about:

```text
One candidate

+

One recruiter

+

One job requirement
```

Not:

```text
Candidate ranking system
```

Decision:

Excluded.

The Project Alignment Document explicitly excludes:

- Multi-candidate comparison;
- HR uploading other candidates' resumes;
- Automatic candidate screening. 

---

### 5.5 Final MVP Philosophy

The final MVP became:

```text
Recruiter

↓

Provide Job Description

↓

Review Matching Report

↓

Understand Candidate Fit

↓

Decide Whether to Contact Candidate
```

rather than:

```text
AI Recruitment Platform

↓

Many recruitment capabilities

↓

Complex workflow
```

---

### 5.6 Could This Have Been Avoided Earlier?

Yes, this was probably the biggest opportunity for process improvement.

The feature list was discussed before the validation framework was fully established.

A more efficient sequence would be:

#### Before listing features:

First define:

##### 1. Core hypothesis

Example:

> Recruiters need help understanding candidate-job fit.

##### 2. Success signal

Example:

> Recruiter views report and initiates communication.

##### 3. Minimum required capability

Example:

> Generate evidence-based matching report.

Only then:

derive features.

---

A better order:

```text
Problem

↓

Hypothesis

↓

Validation Method

↓

User Journey

↓

Features
```

Instead of:

```text
Idea

↓

Feature List

↓

Try to find validation purpose
```

---

### Learning 4: MVP Scope Should Be Defined by Validation Needs, Not Product Possibilities

Especially for AI products, there is a strong temptation to add capabilities because:

- They look impressive;
- They demonstrate model ability;
- They make the product feel more complete.

But the MVP should optimize for:

> Learning speed, not feature completeness.

A useful future checklist:

For every feature:

| Question | If No |
|-|-|
| Does it help test the core hypothesis? | Remove |
| Does the MVP fail without it? | Reduce priority |
| Does it create learning value? | Consider keeping |

---

### Reflection

This was an important shift from a technology-driven mindset to a product-driven mindset.

The product did not become less ambitious.

Instead, the ambition moved from:

> "Show everything AI can do"

to:

> "Prove one valuable behavior change."

That made the MVP achievable within the one-week constraint while preserving the foundation for future expansion.

---

---

## 6. Major Turning Point 4: From General Product Success to Measurable Validation Logic

### 6.1 Initial Approach

At the beginning, the validation goal was described in broader product language:

> Can this AI-assisted matching workflow improve recruitment communication efficiency?

This direction was reasonable because the product vision was not only about analysis, but also about helping candidates and recruiters communicate more effectively.

However, the phrase "communication efficiency" contained a hidden problem.

---

### 6.2 Problem Identified

The MVP could not actually measure the whole recruitment communication process.

Recruitment communication efficiency may include:

- Whether recruiters reply;
- How quickly they reply;
- Whether interviews are scheduled;
- Whether hiring progresses.

But the MVP only controls and observes part of the process:

```text id="u9d7xm"
Candidate Information

↓

AI Matching Analysis

↓

Recruiter Understanding

↓

Recruiter Decision to Contact
```

It does not control:

- Recruiter availability;
- Candidate quality;
- External communication channels;
- Hiring decisions.

Therefore, using a broad success statement created a measurement problem.

---



### 6.3 Turning Point: Separating Product Influence from External Outcomes

The key question became:

> What behavior can this MVP realistically influence and observe?

The answer:

The MVP can influence:

1. Whether recruiters use the matching report;
2. Whether recruiters better understand candidate-job fit;
3. Whether recruiters become more willing to initiate communication.

It cannot directly guarantee:

- Successful recruitment;
- Interview progression;
- Hiring outcomes.

---



### 6.4 Final Validation Logic

The validation goal was refined into:

> Validate whether an AI-assisted matching workflow can improve candidate evaluation efficiency and increase the likelihood of further recruiter communication.

The validation focuses on:

#### 1. Usage Behavior

Question:

> Will recruiters use this AI-assisted workflow?

Signals:

- Page visits;
- JD submissions;
- Matching report generation.

---



#### 2. Perceived Value

Question:

> Does the analysis help recruiters understand candidate fit?

Signals:

- Report feedback;
- Qualitative comments;
- Follow-up questions.

---



#### 3. Communication Intention

Question:

> Does better understanding lead to further communication?

Signal:

- Contact CTA conversion rate.

---



### 6.5 Why Contact CTA Became the Key Metric

Initially, a possible measurement was:

> Does the recruiter successfully communicate with the candidate?

However, that introduces too many external variables.

A more appropriate MVP metric became:

> Contact CTA Conversion Rate

Meaning:

```text id="2q9b6f"
Number of users who click Contact CTA

/

Number of users who view Matching Report
```

The important change:

The metric measures:

> Recruiter's willingness to continue communication.

Not:

> Recruitment success.

---



### 6.6 Risk Analysis Evolution

Another important improvement happened in MVP risk analysis.

Initially, risks were considered more like:

> What if the product does not work?

Later, we refined this into:

> If the MVP fails, can we understand why?

This changed risk analysis from prediction to diagnosis.

---



#### Example: Low Contact Conversion

A low conversion rate could mean:

##### Scenario A

The report is not useful.

Possible improvement:

- Improve evidence presentation;
- Improve analysis quality.

---



##### Scenario B

The candidate does not match the role.

This is not necessarily a product failure.

The report may have successfully helped the recruiter make a decision.

---



##### Scenario C

The recruiter does not trust this product/source.

Possible improvement:

- Improve credibility;
- Improve transparency.

---

Therefore, a good MVP should not only collect success signals.

It should collect enough context to interpret failure.

---



### 6.7 Could This Have Been Avoided Earlier?

Partially.

The main improvement would be:

Before defining metrics, create a validation chain:

```text id="qgl6nb"
Hypothesis

↓

Observable User Behavior

↓

Metric

↓

Possible Interpretation
```

Example:

#### Hypothesis

AI matching helps recruiters evaluate candidates.

↓

#### Observable behavior

Recruiter reviews report.

↓

#### Metric

Report usage.

↓

#### Interpretation

Are recruiters interested enough to use the tool?

---

Another example:

#### Hypothesis

Better understanding increases communication.

↓

#### Observable behavior

Recruiter clicks contact CTA.

↓

#### Metric

CTA conversion rate.

↓

#### Interpretation

Did understanding translate into action?

---



### Learning 5: Metrics Should Measure Controllable User Behavior, Not Final Business Outcomes

Especially for MVPs:

Avoid:

> Did the business succeed?

Prefer:

> Did users behave differently because of the product?

A useful framework:


| Level            | Example                              |
| ---------------- | ------------------------------------ |
| Product usage    | Did users use it?                    |
| Product value    | Did users find it useful?            |
| Behavior change  | Did users take desired action?       |
| Business outcome | Did the company achieve final goals? |


For an MVP, focus on the first three.

---



### Reflection

This was one of the more mature product discussions during the PRD process.

The important shift was:

From:

> "How do we prove this product succeeds?"

To:

> "What can this MVP realistically prove, and how do we interpret the result?"

That mindset prevents overclaiming and makes MVP results much more actionable.

---

## 7. Major Turning Point 5: Feature Boundary Refinement — Candidate Profile Data Source vs Resume Preview

### 7.1 Initial Approach

During the feature definition stage, we encountered an overlap:

- Candidate Profile Data Source;
- Resume Preview.

At first glance, both seemed to represent:

> Candidate information.

This created uncertainty:

- Are they the same feature?
- Should one be removed?
- Is resume access just another form of candidate data access?

This is a common ambiguity in AI products because the same information can exist in multiple layers.

---

### 7.2 Problem Identified

The key mistake was treating:

> "Information about the candidate"

as one single product concept.

However, candidate information has different roles.

The important distinction became:

#### Who uses the information and for what purpose?

---



#### Candidate Profile Data Source

Purpose:

> Provide information for AI analysis.

Relationship:

```text id="r7u5qf"
Candidate Information

↓

AI Processing

↓

Matching Report

↓

Follow-up Answers
```

The recruiter does not directly operate on this data source.

It is a system capability.

---



#### Resume Preview

Purpose:

> Allow recruiters to access the original candidate information.

Relationship:

```text id="1r5c7y"
Resume

↓

Recruiter View / Download
```

This is a user-facing capability.

---



### 7.3 Turning Point

The key question became:

> Is this information used by the AI, or viewed by the user?

This created the final separation:


| Capability                    | Role                       |
| ----------------------------- | -------------------------- |
| Candidate Profile Data Source | AI input/context           |
| Resume Preview                | Recruiter-facing reference |


---



### 7.4 Final Decision



#### F001 Candidate Profile Data Source

Position:

> A product/system capability that provides candidate information context required for AI-powered candidate-job fit analysis.

It may include:

- Resume content;
- Project experience;
- Other related candidate information.

Its purpose is:

- Generate Matching Report;
- Answer Follow-up Questions.

---



#### F004 Resume Preview

Position:

> A recruiter-facing feature that provides direct access to the original resume.

It supports:

- Reviewing background details;
- Verifying AI analysis;
- Downloading the resume when needed.

---

The relationship became:

```text id="r1x9p3"
              Candidate Profile Data Source
                         |
                         |
              AI Candidate-Job Analysis
                         |
                         ↓
                  Matching Report
                         |
              --------------------
              |                  |
              ↓                  ↓

      Follow-up Questions    Resume Preview
                             
                         Recruiter Reference
```

---



### 7.5 Why This Change Was Important

This clarification solved several future problems.

#### Frontend Design

Without this distinction, developers might ask:

> Where is the Candidate Profile page?

But the answer is:

There is no dedicated F001 page.

F001 is not a UI feature.

---



#### Backend Design

Backend can now distinguish:

##### Internal data:

```text id="n4c6v5"
Candidate Profile Data
```

from:

##### User-accessible resource:

```text id="s9dz8g"
Resume File / Resume View
```

---



#### AI Design

AI System Design can define:

- How candidate information is structured;
- How evidence is retrieved;
- How context is provided.

---



### 7.6 Could This Have Been Avoided Earlier?

Yes.

This issue came from a common AI product documentation problem:

> We started from data objects instead of user capabilities.

A better approach would be to classify every item before putting it into Feature List:

---



#### Classification Framework

For every item:

##### Question 1:

Does the user directly interact with it?

If yes:

→ User Feature

Example:

- Resume Preview;
- Contact CTA;
- Feedback.

---



##### Question 2:

Does the system need it to generate outputs?

If yes:

→ System Capability

Example:

- Candidate Profile Data Source;
- Knowledge Base;
- Retrieval Context.

---



##### Question 3:

Does it describe how AI reasons?

If yes:

→ AI Capability

Example:

- Requirement Classification;
- Evidence Matching.

---



### Learning 6: In AI Products, Separate Data Source, User Interface, and Intelligence Layer

A useful three-layer model:

```text id="v3yq8s"
Layer 1: User Experience

What can users see and do?

Examples:
- Report
- Resume
- Contact


Layer 2: Product Data

What information does the product manage?

Examples:
- Candidate profile
- JD
- Conversation history


Layer 3: Intelligence

How does AI process information?

Examples:
- Extraction
- Matching
- Reasoning
```

Many AI product requirements become confusing because these three layers are mixed together.

---



### Reflection

This was a smaller iteration compared with user definition or MVP scope, but it was important because it exposed a recurring challenge in AI product design:

Traditional software often separates:

- Data model;
- UI;
- Business logic.

AI products add another layer:

- Intelligence behavior.

The PRD becomes much clearer when these layers are explicitly separated.

---

---

## 8. Process Retrospective: What Could Have Been Improved in the PRD Creation Process

This section steps back from individual product decisions and reviews the **method we used to create the PRD**.

The goal is not to say "we should have avoided discussion". The discussions were valuable because they uncovered real product ambiguity.

The goal is:

> How can we reach the same quality faster in future projects?

---

### 8.1 What Worked Well

#### 1. We challenged assumptions instead of only editing documents

A strong part of the process was that we did not immediately optimize wording.

For example:

Instead of asking:

> "How should we describe Job Requirement Analysis?"

we asked:

> "Should Job Requirement Analysis even exist as a PRD feature?"

This changed the problem from:

```
Writing problem
```

to:

```
Product definition problem
```

This produced bigger improvements.

---

#### 2. We repeatedly returned to the core product hypothesis

Many decisions were evaluated against:

> Can this MVP validate whether AI-assisted matching helps recruiters understand candidate fit and initiate communication?

This prevented feature expansion.

The final MVP remained focused on:

- Input Job Description;
- Generate Matching Report;
- Support recruiter understanding;
- Enable communication action.

This aligns with the original MVP goal:

> Build a usable demo within one week and validate whether recruiters are willing to use an AI-assisted matching tool, understand candidate fit, and improve communication conversion. 

---

#### 3. We treated document boundaries as a product design problem

A common mistake is to treat documents as formatting.

In this process, the document structure itself became part of the product architecture:

```
PRD
 |
 ├── AI System Design
 ├── Frontend Technical Design
 └── Backend Technical Design
```

The final PRD explicitly defines these responsibilities:

- PRD: product requirements;
- AI System Design: AI capability design and Agent workflow;
- Frontend Technical Design: UI implementation;
- Backend Technical Design: system architecture and APIs.



This made later implementation planning easier.

---

### 8.2 What Caused Unnecessary Iterations

#### Issue 1: Feature List Was Defined Too Early

This was probably the biggest efficiency issue.

The initial thinking was closer to:

```
Product idea

↓

Possible features

↓

Write PRD
```

However, for AI products, a better order is:

```
Product problem

↓

Validation hypothesis

↓

User behavior

↓

Required capabilities

↓

Features
```

Because AI products often have many impressive capabilities that are not necessarily MVP requirements.

---

#### How to Improve

Before creating the Feature List, add a short "Capability Classification" step:

Example:

| Item | Category |
|-|-|
| Matching Report | User Feature |
| Resume Preview | User Feature |
| Contact CTA | User Feature |
| Requirement Analysis | AI Capability |
| Evidence Matching | AI Capability |
| Candidate Profile Data Source | System Capability |

This would have prevented several later discussions.

---

### 8.3 Issue 2: User Definition Started From Business Roles

Initial thinking:

```
Recruitment process participants

↓

Product users
```

Better approach:

```
People interacting with the product

↓

Product users
```

The distinction:

| Role | Should appear in User Definition? |
|-|-|
| Recruiter using assistant | Yes |
| Candidate whose information is analyzed | No |
| Hiring Manager not using MVP | No |

---

#### How to Improve

Before writing User Definition:

Create a simple table:

| Person | Uses Product? | Provides Data? | Receives Value? |
|-|-|-|-|
| Recruiter | Yes | Yes | Yes |
| Candidate | No | Yes | Indirect |
| Hiring Manager | No | No | Indirect |

Only the first category enters User Journey.

---

### 8.4 Issue 3: PRD and AI Design Boundary Should Be Defined Earlier

The biggest AI-product-specific challenge was:

> Internal reasoning looks like a product feature.

For example:

```
Requirement Analysis

Requirement Classification

Evidence Matching

Unknown Detection
```

These are valuable capabilities.

But they answer:

> How does AI work?

not:

> What does the user do?

---

#### How to Improve

Before writing PRD:

Create a two-column list:

#### Product Requirements

- User actions;
- User-visible outputs;
- User decisions.

#### AI Requirements

- Reasoning process;
- Prompt strategy;
- Retrieval;
- Evaluation.

Then write separate documents.

---

### 8.5 Improved Future PRD Creation Process

Based on this project, I would recommend the following process.

---

#### Phase 1: Product Foundation

##### Output:

Project Alignment Document

Define:

- Product vision;
- Problem;
- User;
- MVP goal;
- Non-goals.

Questions:

1. Who uses the product?
2. What problem are we validating?
3. What does success look like?

---

#### Phase 2: Validation Design

Before features:

Define:

```
Hypothesis

↓

Observable behavior

↓

Metric

↓

Interpretation
```

Example:

```
AI analysis improves understanding

↓

Recruiter reviews report

↓

Report usage + feedback

↓

Evaluate usefulness
```

---

#### Phase 3: Capability Mapping

Separate:

```
User Features

System Capabilities

AI Capabilities
```

Only user-facing capabilities enter PRD Feature List.

---

#### Phase 4: User Journey

Create:

```
User Goal

↓

User Action

↓

Product Response
```

Avoid including:

- AI workflow;
- Backend process.

---

#### Phase 5: Functional Requirements

For each feature:

Define:

1. Purpose;
2. User story;
3. Functional requirements;
4. Acceptance criteria.

---

#### Phase 6: Technical Design Documents

Generate:

##### AI System Design

Answers:

> How does AI generate the result?

##### Frontend Design

Answers:

> How does the user interact?

##### Backend Design

Answers:

> How does the system support it?

---

## 9. Final Learning Summary

After this PRD creation process, the most important principles are:

### Principle 1

**Start from validation, not features.**

Bad:

```
What can AI do?
```

Better:

```
What behavior do we need to validate?
```

---

### Principle 2

**Separate user value from system intelligence.**

Bad:

```
AI capability = feature
```

Better:

```
User outcome
    ↓
Product feature
    ↓
AI capability
```

---

### Principle 3

**Define users by interaction, not business relationship.**

Bad:

```
Everyone involved in the process
```

Better:

```
Everyone who performs actions in the product
```

---

### Principle 4

**Keep MVP focused on learning speed.**

The goal of an MVP is not:

> Show everything the technology can do.

The goal is:

> Learn whether the core assumption is true.

---

### Overall Retrospective Conclusion

The PRD creation process took longer than expected (around two days), but most additional iterations were not wasted editing work. They uncovered deeper product decisions:

- What the product actually is;
- Who the user actually is;
- What the MVP is actually validating;
- What belongs in PRD versus technical documents.

The biggest improvement for future projects would not be "write faster".

It would be:

> Spend more time on product boundaries before writing detailed sections.

Doing that earlier would likely reduce rewriting while preserving the same depth of thinking.
