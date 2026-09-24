# 08. TARGET ARCHITECTURE

The platform is designed as a modular, scalable SaaS architecture separating the heavy AI orchestration from the fast client-facing API.

## High-Level Components

### 1. Frontend (Next.js / React)
*   Provides the Dashboard, Document Workspace, Diff Viewer, and Billing UI.
*   Communicates with the Backend via REST APIs and Server-Sent Events (SSE) for streaming progress.

### 2. API Gateway & Backend (FastAPI / Python)
*   Handles Authentication, Rate Limiting, Subscription checks, and Job queuing.
*   Provides synchronous endpoints for short text and asynchronous Webhooks/Polling for large documents.

### 3. Agentic Orchestration Engine (LangGraph)
*   The core state machine. Coordinates the flow of data between dozens of specialized AI Agents (Guardians, Planners, Generators, Critics).

### 4. Model Router & LLM Gateway
*   Abstracts the actual LLM providers (OpenAI, Anthropic, Google, Groq).
*   Handles cost calculation, fallback logic, and token optimization.

### 5. Storage Layer
*   **PostgreSQL:** Relational data (Users, Subscriptions, Document Metadata, Writing DNA profiles).
*   **Redis:** Caching, Rate Limiting, Async Job Queues, LangGraph State Persistence.
*   **S3/Object Storage:** Raw PDF/DOCX file uploads and final exported files.

## Data Flow (Simplified)

```text
[User Browser] -> HTTP POST /humanize -> [FastAPI Router]
                                              |
                                     (Check Rate Limits & Credits)
                                              |
                                              v
                                      [LangGraph Orchestrator]
                                              |
     +----------------------------------------+----------------------------------------+
     |                                        |                                        |
[Fact Guardian]                        [Style Analyzer]                      [Citation Guardian]
     |                                        |                                        |
     +----------------------------------------+----------------------------------------+
                                              |
                                       [Model Router] -> (LLM API: Claude/GPT)
                                              |
                                     [Quality Critic] -> (Pass/Fail)
                                              |
                                   [FastAPI Response / SSE] -> [User Browser]
```
