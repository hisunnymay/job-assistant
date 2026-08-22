# 3. Major Turning Point 1: From Stakeholder Mapping to Actual User Definition

## 3.1 Initial Approach

At the beginning, we considered multiple roles involved in recruitment:

- HR / Recruiter;
- Hiring Manager;
- Product Leader / Role Owner.

This was a common product-thinking approach because in enterprise products, multiple stakeholders often influence usage and decision-making.

The initial assumption was:

> If a person is involved in the recruitment process, they may need to be represented as a user role.

This led to a broader user model.

---

# 3.2 Problem Identified

During the User and Scenario discussion, we identified a key distinction:

## Stakeholder ≠ User

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



# 3.3 Turning Point

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



# 3.4 Final Decision

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



# 3.5 Why This Change Was Important

This change simplified several downstream decisions.

## Before:

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



## After:

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



# 3.6 Could This Have Been Avoided Earlier?

Partially yes.

The unnecessary iteration came from using a traditional enterprise-product mindset.

A better early question would have been:

> "Who is the person performing the MVP action?"

instead of:

> "Who is related to this business process?"

A more efficient process:

Before creating User Definition:

## Step 1

List all stakeholders:

```
Recruiter
Hiring Manager
Candidate
Business Owner
```



## Step 2

Classify:


| Question                 | Example                |
| ------------------------ | ---------------------- |
| Uses the product?        | Recruiter              |
| Provides data?           | Candidate              |
| Receives indirect value? | Hiring Manager         |
| Owns business outcome?   | Product/Business Owner |




## Step 3

Only users enter User Journey.

---



# Learning 2: Define Users Based on Interaction, Not Organizational Roles

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



# Reflection

This was one of the more valuable changes in the PRD process.

Unlike the AI capability boundary issue, this was not mainly a documentation problem. It was a product strategy clarification.

The discussion helped answer:

> Are we building a recruitment platform?

No.

> Are we building a tool that helps recruiters evaluate one candidate faster?

Yes.

That narrower positioning made the rest of the PRD much easier.

---



