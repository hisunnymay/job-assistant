# AI Job Fit Assistant

A Chinese-language MVP that helps recruiters compare a job description with a predefined candidate résumé using evidence-based matching analysis.

## Project Status

Goal 7 adds a validated Volcengine Ark adapter behind the existing backend AI Service boundary while keeping the deterministic Mock AI Service as the local and automated-test default. The public matching and follow-up APIs remain unchanged. The paired PDF remains the recruiter preview/download artifact; the user-verified fixed Markdown is the runtime AI context. The corrected matching-plus-follow-up path passed the opt-in live test with `doubao-seed-2-1-pro-260628`; real runs require an uncommitted `ARK_API_KEY` with access to the configured model.

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
- Docker with Compose for the recommended local PostgreSQL setup;
- A Volcengine Ark API key only for explicit real-AI runs.

No AI provider account or API key is required for Mock mode or normal automated tests.

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

## AI Provider Modes

Mock mode is the safe default in `backend/.env.example`:

```dotenv
AI_PROVIDER=mock
```

For an explicit real-AI run, keep the key only in the ignored `backend/.env` file or the process environment and configure:

```dotenv
AI_PROVIDER=ark
ARK_API_KEY=replace-with-an-uncommitted-key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=doubao-seed-2-1-pro-260628
ARK_REQUEST_TIMEOUT_SECONDS=180
```

The Ark adapter uses the Responses API to send the user-verified `mei_chang_resume.md` as a stable UTF-8 text block before dynamic job or conversation content. It verifies the approved filename and SHA-256 before the provider call, requests strict internal JSON Schema through `text.format`, explicitly disables model thinking, validates the result with Pydantic, and renders only Markdown into the existing API `content` field. The request remains non-streaming. The API key is backend-only and must never be added to frontend variables, Compose build arguments, source control, logs, or persisted application data.

The primary `ChatOpenAI(use_responses_api=True)` path is covered by deterministic transport tests for the `/responses` endpoint, exact verified Markdown text, stable-before-dynamic ordering, strict schema, Ark thinking setting, correlation header, disabled library retries, and bounded workflow retries. The Pro live test completed matching plus follow-up in 34.28 seconds with two first-attempt provider successes, so no native Ark SDK fallback was added. Because provider access and service behavior can vary by account and deployment, rerun the opt-in test when validating another Ark environment. A sanitized integration reference is available at `history/provider_research/ark-responses-api.md`.

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
uv run mypy app tests
uv run ruff check .
```

Opt-in live Ark compatibility and public-API test:

```bash
cd backend
RUN_LIVE_ARK_TESTS=1 AI_PROVIDER=ark \
  uv run pytest -m live_ark tests/live/test_ark_integration.py
```

The live test is skipped during normal `pytest` runs. With `RUN_LIVE_ARK_TESTS=1`, missing Ark credentials fail configuration clearly. The test does not print submitted or generated content, and its isolated database records are removed by the test fixture.

After all deterministic Goal 7A validation passes and the user separately approves at most four provider calls and their account-billed cost, run the Mini comparison with an explicit process-only model override:

```bash
cd backend
RUN_LIVE_ARK_TESTS=1 \
RUN_GOAL_7A_MINI_VALIDATION=1 \
AI_PROVIDER=ark \
ARK_MODEL=doubao-seed-2-0-mini-260428 \
GOAL_7A_RESULT_PATH=../history/evaluation_runs/goal-07a-mini.json \
GOAL_7A_REVIEW_PATH=/tmp/goal-07a-mini-review.json \
uv run pytest -m live_ark tests/live/test_ark_integration.py
```

This performs one matching analysis and one follow-up through the same strict public-API path as Pro, with no more than four provider attempts. The repository result contains only privacy-safe model, attempt, duration, validation, rule, and baseline-comparison fields. The temporary review file contains the user-facing Markdown only for the required grounding review and must be removed after that review. The command does not edit `.env` or change the configured default model.

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
# Keep AI_PROVIDER=mock, or set Ark variables only in the ignored deploy/demo.env.
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
