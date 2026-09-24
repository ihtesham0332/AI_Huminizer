# Current Architecture

## 1. Overview
The current platform (v3.0) is a containerized monorepo consisting of:
*   **Backend:** FastAPI + LangGraph (Python 3.11)
*   **Frontend:** Next.js (React 18) with an Obsidian Glass aesthetic
*   **Database:** PostgreSQL with `pgvector` (via Docker)
*   **Extensions:** Chrome Extension (Manifest V3), Discord Bot (discord.py)
*   **Mobile:** React Native (Expo) architecture stub
*   **Monetization/Auth:** Stripe Webhooks and NextAuth (Google)

## 2. Agentic Workflow (LangGraph)
Currently, the system uses a localized LangGraph orchestration:
*   `humanization_planner.py`: Configures the prompt based on `strength` (Ninja, Balanced, Ghost).
*   `Supervisor`: Coordinates the generation.
*   `FactGuardian` / `SemanticGuardian`: Extract facts and ensure meaning preservation.
*   `ThreadPoolExecutor`: Generates parallel candidates.

## 3. Deployment
Orchestrated via a root `docker-compose.yml` and `Makefile`.
