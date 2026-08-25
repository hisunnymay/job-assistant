# Development Plan

## Implementation Phase (Vibe Coding)

### Step 1: Build the user flow skeleton

Frontend:

```text
Input JD page

↓

Loading state

↓

Report page

↓

Follow-up question area

↓

Contact CTA
```

Use mock data initially.

---

### Step 2: Build minimum backend

Replace mock data:

```text
Frontend
   |
   |
Backend API
   |
   |
AI capability
```

---

### Step 3: Iterate together

Example:

You discover:

"The report is too long."

Frontend:

- Need collapsible sections.

Backend/AI:

- Need shorter output.

Both change together.

---



## 3. Repository Structure

```text
ai-job-fit-assistant/

├── frontend/
│   ├── src/
│   └── ...

├── backend/
│   ├── api/
│   └── ...

├── docs/
│   ├── 00_Project_Alignment_Document.md
│   ├── 01_Product_Requirement_Document.md
│   ├── 03_Lightweight_AI_Design_Decision.md
│   ├── 04_Frontend_Technical_Design.md
│   └── 05_Backend_Technical_Design.md

└── README.md
```