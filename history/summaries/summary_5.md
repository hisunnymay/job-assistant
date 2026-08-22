# 6. Major Turning Point 4: From General Product Success to Measurable Validation Logic

## 6.1 Initial Approach

At the beginning, the validation goal was described in broader product language:

> Can this AI-assisted matching workflow improve recruitment communication efficiency?

This direction was reasonable because the product vision was not only about analysis, but also about helping candidates and recruiters communicate more effectively.

However, the phrase "communication efficiency" contained a hidden problem.

---

# 6.2 Problem Identified

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



# 6.3 Turning Point: Separating Product Influence from External Outcomes

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



# 6.4 Final Validation Logic

The validation goal was refined into:

> Validate whether an AI-assisted matching workflow can improve candidate evaluation efficiency and increase the likelihood of further recruiter communication.

The validation focuses on:

### 1. Usage Behavior

Question:

> Will recruiters use this AI-assisted workflow?

Signals:

- Page visits;
- JD submissions;
- Matching report generation.

---



### 2. Perceived Value

Question:

> Does the analysis help recruiters understand candidate fit?

Signals:

- Report feedback;
- Qualitative comments;
- Follow-up questions.

---



### 3. Communication Intention

Question:

> Does better understanding lead to further communication?

Signal:

- Contact CTA conversion rate.

---



# 6.5 Why Contact CTA Became the Key Metric

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



# 6.6 Risk Analysis Evolution

Another important improvement happened in MVP risk analysis.

Initially, risks were considered more like:

> What if the product does not work?

Later, we refined this into:

> If the MVP fails, can we understand why?

This changed risk analysis from prediction to diagnosis.

---



## Example: Low Contact Conversion

A low conversion rate could mean:

### Scenario A

The report is not useful.

Possible improvement:

- Improve evidence presentation;
- Improve analysis quality.

---



### Scenario B

The candidate does not match the role.

This is not necessarily a product failure.

The report may have successfully helped the recruiter make a decision.

---



### Scenario C

The recruiter does not trust this product/source.

Possible improvement:

- Improve credibility;
- Improve transparency.

---

Therefore, a good MVP should not only collect success signals.

It should collect enough context to interpret failure.

---



# 6.7 Could This Have Been Avoided Earlier?

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

## Hypothesis

AI matching helps recruiters evaluate candidates.

↓

## Observable behavior

Recruiter reviews report.

↓

## Metric

Report usage.

↓

## Interpretation

Are recruiters interested enough to use the tool?

---

Another example:

## Hypothesis

Better understanding increases communication.

↓

## Observable behavior

Recruiter clicks contact CTA.

↓

## Metric

CTA conversion rate.

↓

## Interpretation

Did understanding translate into action?

---



# Learning 5: Metrics Should Measure Controllable User Behavior, Not Final Business Outcomes

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



# Reflection

This was one of the more mature product discussions during the PRD process.

The important shift was:

From:

> "How do we prove this product succeeds?"

To:

> "What can this MVP realistically prove, and how do we interpret the result?"

That mindset prevents overclaiming and makes MVP results much more actionable.

