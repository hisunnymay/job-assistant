# Order
# 整体顺序
```text
1. Frontend Technical Design Outline
2. Backend Technical Design Outline
3. Review dependency between them
4. Write the documents
5. Confirm Frontend-Backend Integration Assumptions
6. Start vibe coding 
```
#  vibe coding 顺序
```text
### Step 1: Build the user flow skeleton

Frontend:

```
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

```
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
```
# Repo
``` text
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
