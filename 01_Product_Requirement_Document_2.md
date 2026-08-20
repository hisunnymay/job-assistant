# 2. Product Goals and Scope

## 2.1 Product Goals

AI Job Fit Assistant aims to improve the efficiency of candidate-job matching during the early recruitment stage.

The product goals are defined from three perspectives:

---

## User Goal

Help recruiters quickly understand whether a candidate’s experience aligns with a job requirement.

The product should enable recruiters to:

- Identify relevant candidate experience;
- Understand the evidence behind matching results;
- Discover missing information that requires further communication.

---

## Candidate Goal

Help candidates communicate their capabilities more effectively beyond traditional resume limitations.

The product should enable candidates to:

- Provide richer context around their experience;
- Highlight relevant evidence related to a specific role;
- Improve the efficiency of recruitment communication.

---



## Product Validation Goal

Validate whether an AI-assisted matching workflow can improve recruitment communication efficiency.

The MVP aims to verify:

- Whether recruiters are willing to use an AI-generated matching report;
- Whether evidence-based candidate analysis helps recruiters understand candidate fit;
- Whether the product increases the probability of further communication.

---



# 2.2 Success Metrics

The MVP focuses on validating user behavior rather than optimizing recruitment outcomes.

The primary success metric is:

## Contact Conversion Rate

Definition:

```text
Number of users who click contact CTA

/

Number of users who view the matching report
```

This metric measures whether the product successfully helps move users from understanding candidate information to initiating further communication.

---



## Supporting Metrics



### Product Usage Metrics


| Metric                     | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| Page visits                | Measure product exposure                           |
| JD submissions             | Measure user willingness to use the core feature   |
| Matching reports generated | Measure successful completion of the main workflow |
| Resume preview views       | Measure candidate information exploration          |
| Contact CTA clicks         | Measure conversion behavior                        |


---



### User Feedback Metrics

Qualitative feedback may be collected to understand:

- Whether users understand the matching report;
- Whether the evidence provided is useful;
- Which information users still need before contacting the candidate.

---



# 2.3 MVP Scope

The MVP focuses on validating the following core workflow:

```text
Job Description Input

↓

Requirement Analysis

↓

Candidate Experience Matching

↓

Matching Report

↓

Further Communication
```

---



## Included Features



### Job Description Analysis

The system allows users to input a job description and understand the key requirements of the role.

---



### Candidate Matching Analysis

The system analyzes the relationship between job requirements and candidate experience.

The output should include:

- Matching requirements;
- Supporting candidate evidence;
- Missing information.

---



### Candidate Information Overview

Users can view additional candidate information, including:

- Resume information;
- Project experience;
- Relevant background information.

---



### Contact Conversion

The product provides a clear way for interested users to contact the candidate.

---



### Basic User Behavior Tracking

The product tracks key user interactions to evaluate MVP effectiveness.

---



# 2.4 Non-goals

The following capabilities are intentionally excluded from the MVP.

---



## General Recruitment Platform

The MVP does not aim to build a complete recruitment platform.

Excluded:

- Candidate database management;
- Recruitment workflow management;
- Interview scheduling;
- Hiring pipeline management.

---



## Automated Hiring Decision

The product does not make hiring decisions.

The product provides structured information to support human judgment.

---



## Multi-candidate Recruitment Analysis

The MVP only analyzes a fixed candidate profile.

Excluded:

- Uploading multiple resumes;
- Comparing multiple candidates;
- Ranking candidates.

---



## Open-ended Recruitment Assistant

The MVP does not provide a general-purpose conversational assistant.

Excluded:

- Free-form recruiter conversations;
- General recruiting advice;
- Autonomous interview preparation.

---



## Full Multilingual Support

The MVP does not implement complete multilingual functionality.

However, the product should remain compatible with future localization.

---



# 2.5 MVP Constraints

The MVP is designed under the following constraints:


| Constraint           | Description                                             |
| -------------------- | ------------------------------------------------------- |
| Development Timeline | Target completion within one week                       |
| Candidate Scope      | Initial version supports one fixed candidate profile    |
| User Scope           | Initial users are recruiters evaluating one candidate   |
| Product Scope        | Focus on matching analysis and communication conversion |


