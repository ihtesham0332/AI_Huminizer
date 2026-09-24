# System Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document outlines the high-level technical architecture of the platform.

## 1. High-Level Architecture Overview
The platform utilizes a modern, decoupled 3-tier architecture, heavily leaning on Python for AI orchestration and React for user interaction.

*   **Tier 1: Presentation Layer (Frontend)**
    *   **Framework:** Next.js (React), TypeScript, Tailwind CSS.
    *   **Responsibility:** Handles user authentication, document uploading, writing profile management, and renders the real-time side-by-side interactive dashboard.
*   **Tier 2: Application & AI Layer (Backend)**
    *   **Framework:** FastAPI (Python 3.11+).
    *   **Orchestration:** LangGraph for stateful, multi-agent cyclical workflows.
    *   **Responsibility:** Manages job queues, executes the Agentic Workflow, enforces QA gates, and interfaces with the LLM Abstraction Layer.
*   **Tier 3: Data & State Layer (Database)**
    *   **Primary Database:** PostgreSQL.
    *   **Vector Store:** `pgvector` extension for PostgreSQL (used for storing and retrieving user Writing Profiles and stylistic embeddings).
    *   **Responsibility:** Persists user data, document version history, evaluation metrics, and protected token registries.

## 2. LLM Abstraction Layer
The system MUST NOT be hard-coded to a single provider. The backend utilizes an abstract `LLMRouter` that dispatches tasks based on cost and complexity:
*   **Fast/Cheap Tasks:** (e.g., Grammar Checking, Content Classification) -> Routed to local models like `Qwen2.5:3b` or `Llama-3-8b` via Ollama.
*   **Heavy/Reasoning Tasks:** (e.g., Deep Semantic Humanization, Quality Critic) -> Routed to premium models like `GPT-4o` or `Claude-3.5-Sonnet`.
*   **Vectorization:** Routed to dedicated embedding models (`text-embedding-3-small`).

## 3. Asynchronous Job Processing
Due to the cyclical nature of the LangGraph workflow, humanization requests for documents over 500 words cannot be processed synchronously.
*   The API accepts the document and immediately returns a `job_id`.
*   A background worker (Celery or FastAPI BackgroundTasks) executes the LangGraph state machine.
*   The Frontend polls `/api/v1/jobs/{job_id}` or listens via Server-Sent Events (SSE) for real-time status updates (e.g., "Fact Guardian scanning...", "Critic evaluating Candidate A...").
