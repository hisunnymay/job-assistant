# Frontend Workspace Design Detour: Learning Summary

## Version Log

- **v1.0 — 2026-08-25:** Recorded the frontend information-architecture detour, its causes, the approved correction, and prevention rules.

## 1. Purpose

This note records why the first frontend structure could satisfy individual feature requirements while still feeling different from the intended product experience.

It is a retrospective learning record, not an authoritative specification. The current approved behavior is defined in `docs/04_Frontend_Technical_Design.md` v0.5.

## 2. What Happened

The first implementation organized the interface as one long page:

```text
Top Navigation
↓
Conversation
↓
Resume, Contact, and Feedback Sections
```

Later, the navigation was moved to the left and the input was anchored near the bottom. This improved the visual similarity to an assistant workspace, but the underlying information architecture was still unchanged: résumé and contact content remained supporting sections below the conversation.

The intended experience was different:

```text
Persistent Left Navigation
+
One Active Right-side Workspace View

Home | Conversation | Resume | Contact
```

Resume Preview and Contact Me should replace the conversation view rather than appear beside or below it. The product also needed a dedicated entrance page containing a brief introduction and the initial job-description input.

## 3. Why the Detour Happened

### 3.1 Capabilities Were Clear, but Their Spatial Relationship Was Not

The earlier frontend design clearly listed:

- Conversation;
- Resume Preview;
- Contact Me;
- Feedback.

However, it did not define whether these capabilities were:

- Separate workspace views;
- Sections on one page;
- Panels displayed simultaneously;
- Navigation destinations that replace each other.

Codex therefore made a valid implementation choice within the documented flexibility, but that choice did not match the intended product model.

### 3.2 “Keep Layout Flexible” Was Interpreted Too Broadly

Visual styling and component structure should remain flexible during MVP implementation. Information architecture and navigation behavior are different: they affect how users understand and move through the product.

The earlier design treated both as implementation details. This left a product-level decision unresolved:

> Is this a long feature page, or an assistant workspace with mutually exclusive views?

### 3.3 Validation Focused on Functionality More Than Product Structure

The implementation was tested for:

- Correct feature behavior;
- Responsive layout;
- Horizontal overflow;
- Frontend and backend validation.

Those checks could confirm that the page worked, but not that its overall interaction model matched the intended experience. A short visual review before implementation would have exposed the mismatch earlier.

## 4. Approved Correction

The reviewed demonstration established the following model:

```text
Left Navigation
├── Home
├── Job Matching
├── Resume Preview
└── Contact Me

Right Workspace
└── Exactly one active view
    ├── Entrance
    ├── Conversation
    ├── Resume Preview
    └── Contact Me
```

The key decisions are:

- Home introduces the product and collects the initial job description;
- Submitting a valid job description opens the Conversation View;
- Conversation content is displayed only in the right workspace;
- Resume Preview replaces the Conversation View;
- Contact Me replaces the Conversation View;
- Switching views does not intentionally clear the active conversation;
- Smaller screens may adapt the navigation presentation without changing these relationships.

These decisions were added to Frontend Technical Design v0.5 before implementation.

## 5. How to Prevent Similar Detours

### Learning 1: Separate Product Interaction Rules From Visual Implementation Details

The design should lock decisions that affect the user’s mental model:

- What are the primary views?
- Which views can appear simultaneously?
- What does navigation replace?
- What state should survive navigation?

It can still leave spacing, component libraries, styling, routing technique, and responsive details unresolved.

### Learning 2: Define a View-state Model for Workspace Products

Before coding a workspace-style interface, document the active-view states and transitions:

```text
Entrance --submit JD--> Conversation
Conversation --view resume--> Resume
Conversation --contact--> Contact
Resume or Contact --job matching--> Conversation
```

This small model prevents independent features from accidentally becoming unrelated page sections.

### Learning 3: Review One Visual Demonstration Before Structural UI Implementation

A demonstration should be required when a Goal introduces or changes:

- Page hierarchy;
- Primary navigation;
- Workspace replacement behavior;
- The main user journey.

The demonstration is not a pixel-perfect specification. Its purpose is to confirm information architecture before code makes the assumption expensive to reverse.

### Learning 4: Add Interaction Architecture to Goal Acceptance Criteria

Automated checks should continue to cover tests, type-checking, builds, responsiveness, and errors. Goal-level browser validation should also confirm product-structure expectations such as:

- The active navigation item matches the visible workspace;
- Resume and Contact do not remain stacked below Conversation;
- Only one right-side view is active;
- Navigation does not unexpectedly erase the conversation;
- The entrance-page submission opens the matching journey.

## 6. Final Learning

The detour was not caused by insufficient component detail. It was caused by leaving a user-visible relationship undefined.

The reusable principle is:

> Keep visual implementation flexible, but make navigation, view relationships, and state transitions explicit before coding.
