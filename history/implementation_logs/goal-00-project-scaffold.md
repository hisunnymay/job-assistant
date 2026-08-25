# Goal 0 — Project Scaffold and Validation Baseline

## Completed Scope

- Added a React, TypeScript, and Vite frontend shell with Chinese content kept outside components, typed environment configuration, and an npm lockfile.
- Added a FastAPI modular-monolith scaffold with explicit access, controller, service, AI Service, repository, configuration, and database boundaries.
- Added Pydantic Settings, SQLAlchemy with PostgreSQL through psycopg, a database initialization command, a health endpoint, and a uv lockfile for Python 3.12.
- Added safe frontend and backend `.env.example` files, a local PostgreSQL Compose service, validation configuration, tests, and local-run documentation.
- Kept real AI provider selection and integration deferred.

## Validation

- `cd frontend && npm run test` — passed, 2 tests.
- `cd frontend && npm run type-check` — passed.
- `cd frontend && npm run lint` — passed.
- `cd frontend && npm run build` — passed.
- `cd backend && uv run pytest` — passed, 2 tests.
- `cd backend && uv run mypy app` — passed.
- `cd backend && uv run ruff check .` — passed.
- FastAPI started successfully with Uvicorn; a real local HTTP request to `/health` returned `200` with `{"status":"ok"}`, and the endpoint also passed its FastAPI `TestClient` test.
- PostgreSQL 16 was started locally and `uv run python -m app.db.init_db` completed successfully against a newly created `job_assistant` database.

## Problems Fixed and Known Issues

- Added the repository root to pytest's import path after the initial test collection could not import the `app` package.
- Replaced the deprecated HTTPX compatibility path with Starlette's current `httpx2` TestClient dependency.
- Docker was not installed on the validation machine, so the committed Compose service was not started directly. Database initialization was instead verified against a clean local PostgreSQL 16 installation using the same connection settings.
- No known Goal 0 application issues remain.
