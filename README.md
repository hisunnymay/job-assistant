# AI Job Fit Assistant

A Chinese-language MVP that helps recruiters compare a job description with a predefined candidate résumé using evidence-based matching analysis.

## Project Status

Goal 6 provides a validated recruiter journey, automated browser coverage, and a provider-neutral single-host Docker demo bundle protected by gateway-level HTTP Basic Authentication. Matching reports still use the deterministic backend Mock AI Service; no real AI provider or API key is used during this Demo phase.

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

The health endpoint is available at `http://localhost:8000/health`. The MVP uses `POST /api/matching-analysis`, `POST /api/conversations/{conversationId}/messages`, `GET /api/resume`, `POST /api/feedback`, and `POST /api/tracking-events` on the same backend origin.

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
npm run test:e2e
```

The end-to-end command starts an isolated PostgreSQL container, backend, and frontend, runs the desktop and compact-browser journeys, and removes the isolated container afterward. Install the Playwright browser once with `npx playwright install chromium` if it is not already available.

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

## Protected Demo Bundle

The demo bundle runs PostgreSQL, the FastAPI backend, the built frontend, and an Nginx gateway on one Docker host. The gateway protects both the UI and API with HTTP Basic Authentication. Local development remains unprotected.

From the repository root:

```bash
cp deploy/demo.env.example deploy/demo.env
# Replace POSTGRES_PASSWORD with a long URL-safe random value.
DEMO_USERNAME=demo DEMO_PASSWORD='choose-a-separate-demo-password' \
  bash scripts/prepare-demo-auth.sh
docker compose --env-file deploy/demo.env -f compose.demo.yaml up --build --wait
```

Open `http://localhost:8080` (or the configured `DEMO_PORT`) and sign in with the generated demo credentials. Verify service health through the protected gateway:

```bash
curl --user demo:'choose-a-separate-demo-password' http://localhost:8080/health
```

Stop the bundle without deleting its database volume:

```bash
docker compose --env-file deploy/demo.env -f compose.demo.yaml down
```

The bundle is deployment preparation only. It does not select a hosting provider, create external resources, or configure production HTTPS; those remain deployment-time decisions.

## Tracking Metrics and Retention

Run the internal aggregate report from `backend/` with an inclusive start and exclusive end timestamp:

```bash
uv run python -m app.commands.tracking_report \
  --start 2026-08-01T00:00:00Z \
  --end 2026-09-01T00:00:00Z
```

The JSON result contains total and distinct-session counts for all six S001 events and the distinct-session Contact Conversion Rate. It contains no job description, résumé, feedback, contact, prompt, IP-address, or user-agent content.

Delete events older than the approved 90-day retention period:

```bash
uv run python -m app.commands.cleanup_tracking_events
```

Both commands use the backend's configured `DATABASE_URL`. The metrics command is an internal evaluator tool; the MVP does not expose event-level analytics or a recruiter-facing Dashboard.

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
- [Goal 5 Implementation Record](history/implementation_logs/goal-05-tracking-and-guardrails.md)
- [Goal 6 Implementation Record](history/implementation_logs/goal-06-demo-readiness.md)

Read `AGENTS.md` before implementation. Implement only the explicitly requested Goal from `planning/PLAN.md`.
