# 5. Major Turning Point 3: From Feature Expansion to MVP Validation Thinking

## 5.1 Initial Approach

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

# 5.2 Problem Identified

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

# 5.3 Turning Point: Defining the Validation Goal First

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

# 5.4 Feature Evaluation Framework

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

## Example 1: Matching Report

Question:

Does it validate the hypothesis?

Yes.

Because it is the main mechanism through which recruiters understand candidate fit.

Decision:

✅ Core MVP feature.

---

## Example 2: Ask Follow-up Questions

Question:

Does it help validate the hypothesis?

Partially.

It improves the experience, but the product can still validate the core idea without it.

Decision:

P1.

---

## Example 3: Resume Preview

This was more subtle.

Initially it looked like an additional convenience feature.

Later we identified another value:

> It provides source transparency and helps recruiters verify AI analysis.

Therefore:

Decision:

Keep as P0.

---

## Example 4: Multi-candidate comparison

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

# 5.5 Final MVP Philosophy

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

# 5.6 Could This Have Been Avoided Earlier?

Yes, this was probably the biggest opportunity for process improvement.

The feature list was discussed before the validation framework was fully established.

A more efficient sequence would be:

## Before listing features:

First define:

### 1. Core hypothesis

Example:

> Recruiters need help understanding candidate-job fit.

### 2. Success signal

Example:

> Recruiter views report and initiates communication.

### 3. Minimum required capability

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

# Learning 4: MVP Scope Should Be Defined by Validation Needs, Not Product Possibilities

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

# Reflection

This was an important shift from a technology-driven mindset to a product-driven mindset.

The product did not become less ambitious.

Instead, the ambition moved from:

> "Show everything AI can do"

to:

> "Prove one valuable behavior change."

That made the MVP achievable within the one-week constraint while preserving the foundation for future expansion.

---

