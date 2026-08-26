# AI Job Fit Assistant

A Chinese-language MVP that helps recruiters compare a job description with a predefined candidate résumé using evidence-based matching analysis.

## Project Status

Goal 4 provides the integrated matching journey plus approved résumé preview/download, static candidate contact actions, and report-linked feedback persistence. Matching reports still use the deterministic backend Mock AI Service; no real AI provider or API key is used during this Demo phase.

## Repository Structure

```text
job-assistant/
├── AGENTS.md             # Codex implementation rules
├── frontend/             # React + TypeScript + Vite application
├── backend/              # FastAPI modular-monolith backend
├── compose.yaml          # Local PostgreSQL service
├── docs/                 # Active source-of-truth documents
├── planning/PLAN.md      # Goal order, scope, and validation
└── history/              # Analysis and implementation records
```

## Prerequisites

- Node.js supported by the current Vite release and npm;
- [uv](https://docs.astral.sh/uv/) for Python 3.12 and backend dependencies;
- Docker with Compose for the recommended local PostgreSQL setup.

No AI provider or API key is required during the Demo phase.

## Local Setup

Start PostgreSQL from the repository root:

```bash
docker compose up -d database
```

Initialize and run the backend:

```bash
cd backend
cp .env.example .env
uv sync
uv run python -m app.db.init_db
uv run uvicorn app.main:app --reload
```

The health endpoint is available at `http://localhost:8000/health`. Goal 4 uses `POST /api/matching-analysis`, `GET /api/resume`, and `POST /api/feedback` on the same backend origin.

In another terminal, run the frontend:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Vite prints the local frontend URL when it starts.

## Validation

Frontend:

```bash
cd frontend
npm run test
npm run type-check
npm run lint
npm run build
```

Backend:

```bash
cd backend
uv run pytest
uv run mypy app
uv run ruff check .
```

Database initialization:

```bash
cd backend
uv run python -m app.db.init_db
```

## Active Documents

- [Product Requirement Document](docs/01_Product_Requirement_Document.md)
- [Lightweight AI Design Decision](docs/03_Lightweight_AI_Design_Decision.md)
- [Frontend Technical Design](docs/04_Frontend_Technical_Design.md)
- [Backend Technical Design](docs/05_Backend_Technical_Design.md)
- [Implementation Plan](planning/PLAN.md)

## Supporting Records

- [Implementation Strategy](history/strategy_analysis/01_Implementation_Strategy.md)
- [Technology Strategy Comparison](history/strategy_analysis/02_Technology_Strategy_Comparison.md)
- [Goal 0 Implementation Record](history/implementation_logs/goal-00-project-scaffold.md)
- [Goal 2 Implementation Record](history/implementation_logs/goal-02-matching-vertical-slice.md)
- [Goal 4 Implementation Record](history/implementation_logs/goal-04-supporting-actions.md)

Read `AGENTS.md` before implementation. Implement only the explicitly requested Goal from `planning/PLAN.md`.
