# AI Job Fit Assistant Technology Strategy Comparison

## Document Information

- **Version:** v0.2
- **Status:** Approved
- **Last Updated:** 2026-08-25
- **Purpose:** Compare frontend and backend technology choices for MVP speed and future flexibility.

## Version Log

- **v0.1 — 2026-08-25:** Created the initial frontend and backend technology comparison.
- **v0.2 — 2026-08-25:** Approved React, TypeScript, and Vite for the frontend and Python with FastAPI for the backend.

## Rating Guide

- `🔀` — Flexibility. More `🟢` means greater flexibility.
- `🤖` — Flexibility for future AI development. More `🟢` means greater flexibility.
- `⏳` — Relative implementation time. More `🟠` means more time required.
- Ratings are relative comparisons, not calendar estimates.

## Frontend Comparison

### React + TypeScript + Vite

- `🔀` 🟢🟢🟢🟢🟢
- `⏳` 🟠🟠
- Provides more freedom to choose libraries and architecture as the interface grows.

### Vue + TypeScript + Vite

- `🔀` 🟢🟢🟢🟢
- `⏳` 🟠
- Provides a more cohesive structure and may be slightly faster for a simple interface.

**Frontend decision:** Use **React + TypeScript + Vite**. It requires slightly more initial setup but offers greater long-term UI flexibility.

## Backend Comparison

### Node.js + TypeScript + Fastify

- `🔀` 🟢🟢🟢🟢🟢
- `🤖` 🟢🟢🟢🟢
- `⏳ MVP` 🟠
- `⏳ Future AI` 🟠🟠🟠

### Node.js + TypeScript + NestJS

- `🔀` 🟢🟢🟢🟢🟢
- `🤖` 🟢🟢🟢🟢
- `⏳ MVP` 🟠🟠🟠
- `⏳ Future AI` 🟠🟠🟠

### Python + FastAPI

- `🔀` 🟢🟢🟢🟢
- `🤖` 🟢🟢🟢🟢🟢
- `⏳ MVP` 🟠🟠
- `⏳ Future AI` 🟠

### Java + Spring Boot

- `🔀` 🟢🟢🟢🟢🟢
- `🤖` 🟢🟢🟢
- `⏳ MVP` 🟠🟠🟠🟠
- `⏳ Future AI` 🟠🟠🟠🟠

### C++

- `🔀` 🟢🟢
- `🤖` 🟢🟢
- `⏳ MVP` 🟠🟠🟠🟠🟠
- `⏳ Future AI` 🟠🟠🟠🟠🟠

## Selected Strategy

- **Frontend:** React + TypeScript + Vite.
- **Backend:** Python + FastAPI.
- **Demo stage:** Keep AI behavior mocked behind an AI Service interface.
- **Later AI stage:** Replace the mock with direct model calls, LangChain, LangGraph, or another implementation only after completing the AI System Design.
- **Resume handling:** Continue passing the static candidate PDF through the AI Service boundary; do not add backend PDF extraction for the MVP.

This combination adds a small amount of initial backend work compared with using TypeScript everywhere, but preserves stronger flexibility for future AI development without requiring a backend-language migration.

## References

- [React documentation](https://react.dev/learn)
- [Vue documentation](https://vuejs.org/guide/extras/ways-of-using-vue.html)
- [FastAPI documentation](https://fastapi.tiangolo.com/features/)
- [LangChain Python integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)
- [LangChain JavaScript integrations](https://docs.langchain.com/oss/javascript/integrations/providers/overview)
