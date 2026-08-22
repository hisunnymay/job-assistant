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

Validate whether an AI-assisted matching workflow can improve recruitment communication efficiency.

The MVP aims to verify:

- Whether recruiters are willing to engage with an AI-assisted matching report during candidate evaluation;
- Whether evidence-based candidate analysis provides useful insights for understanding candidate-job fit;
- Whether the product increases the probability of further communication.
---

# 2.2 Success Metrics

The MVP focuses on validating user behavior and product value perception rather than optimizing recruitment outcomes.

---

## Primary Success Metric

### Contact Conversion Rate

Definition:

```text
Number of users who click contact CTA

/

Number of users who view the matching report
```

Purpose:

Measure whether the product successfully helps users move from understanding candidate information to initiating further communication.

---

## Supporting Metrics

### Product Usage Metrics

| Metric | Purpose |
|---|---|
| Page visits | Measure product exposure |
| JD submissions | Measure user willingness to use the core feature |
| Matching reports generated | Measure successful completion of the main workflow |
| Resume preview views | Measure candidate information exploration |
| Contact CTA clicks | Measure conversion behavior |

---

### User Feedback Metrics

| Metric | Purpose |
|---|---|
| Report Feedback | Measure whether recruiters find the matching analysis useful |

The product collects optional feedback after users review the matching report.

Feedback helps evaluate:

- Whether users understand the value of the analysis;
- Whether the evidence provided is useful;
- What additional information users need before making contact.

---

# 2.3 MVP Scope

The MVP focuses on validating the following core workflow:

```text
Job Description Input

↓

Job Requirement Analysis

↓

Candidate Information Matching

↓

Evidence-based Matching Report (Optinal)

↓

Further Communication
```

The MVP also includes a lightweight feedback loop to collect user insights for future iteration.

---

## Included Features

| Feature | Priority | Description |
|---|---|---|
| Candidate Profile Data Source | P0 | Provide structured candidate information as the source for candidate-job fit analysis. |
| Job Description Input | P0 | Allow recruiters to provide job descriptions for matching analysis. |
| Matching Report | P0 | Present evidence-based analysis of candidate-job fit, including matching insights and missing information. |
| Resume Preview | P0 | Allow recruiters to review candidate background information. |
| Ask Follow-up Questions | P1 | Allow recruiters to ask additional questions when the matching report does not provide sufficient information. |
| Contact CTA | P0 | Provide a clear method for recruiters to initiate further communication. |
| Basic User Behavior Tracking | P0 | Track key user interactions to evaluate MVP usage and conversion performance. |
| Report Feedback | P1 | Collect optional feedback on the usefulness of the matching report. |



## Out of Scope

The MVP intentionally does not include:

| Excluded Capability | Reason |
|-|-|
| Multi-candidate analysis | MVP focuses on validating matching analysis for a single candidate profile |
| Candidate resume upload | MVP uses a predefined candidate profile |
| Open-ended recruitment assistant | MVP focuses on structured matching analysis rather than general conversation |
| Automated hiring decisions | The product supports recruiter judgment rather than replacing it |
| Full multilingual support | Localization is reserved for future iterations |


# 2.4 MVP Constraints

The MVP is designed under the following constraints:

| Constraint | Description |
|---|---|
| Development Timeline | Target completion within one week |
| Candidate Scope | Initial version supports one fixed candidate profile |
| User Scope | Initial users are recruiters evaluating one candidate |
| Product Scope | Focus on matching analysis and communication conversion |
| Language Support | MVP supports a single language experience. The product design should remain compatible with future localization. |


# 2.5 MVP Success Risks

The MVP aims to validate whether an AI-assisted matching workflow can improve recruitment communication efficiency.

However, MVP outcomes may be affected by factors beyond product capability. The following risks should be considered when evaluating MVP results.

| Risk | Description | Potential Mitigation |
|---|---|---|
| Low Recruiter Engagement | Recruiters may not open or interact with the AI Job Fit Assistant after receiving the product link. This may indicate insufficient motivation, unclear value proposition, or high interaction cost. | Optimize recruiter outreach messaging, reduce access friction, and improve the explanation of product value. |
| Low Conversion After Product Usage | Recruiters may review the matching report but not initiate further communication with the candidate. | Analyze feedback and interaction data to identify whether the issue is caused by insufficient candidate information, requirement mismatch, or other external factors. |
| Insufficient Candidate Information Coverage | The available candidate information may not contain enough evidence to answer recruiter questions or demonstrate relevant experience. | Improve candidate profile completeness and collect additional information based on identified information gaps. |
| Limited Trust in AI-generated Analysis | Recruiters may hesitate to rely on AI-assisted analysis if the reasoning is unclear or unsupported. | Provide evidence-based explanations, highlight information sources, and avoid unsupported conclusions. |
| External Recruitment Factors | Recruitment outcomes may be affected by factors unrelated to the product, such as position status, candidate pool, company hiring decisions, or recruiter workload. | Consider external factors when interpreting MVP results and avoid attributing all outcomes to product performance. |

