# 07. NON-FUNCTIONAL REQUIREMENTS

This document defines the system attributes such as performance, security, reliability, and cost.

## 1. Performance & Latency
*   **NFR-1.1:** The system must process a 500-word block in under 5 seconds (Fast Mode) or 15 seconds (Deep Mode).
*   **NFR-1.2:** The `DocumentIntelligenceEngine` must parse a 30,000-word PDF in under 10 seconds.
*   **NFR-1.3:** Agentic nodes that do not depend on each other (e.g., Fact Extraction, Citation Extraction, Style Analysis) MUST run in parallel using asynchronous LangGraph execution to reduce TTFT (Time to First Token).

## 2. Cost Optimization
*   **NFR-2.1:** The cost per 1,000 words processed in "Balanced Mode" must not exceed $0.02 in LLM API costs.
*   **NFR-2.2:** The system must utilize a Redis caching layer to instantly return results for previously processed exact-match sentences (saving 100% of LLM cost on cache hits).

## 3. Reliability & Availability
*   **NFR-3.1:** The `ModelRouterAgent` must support automatic fallback. If Provider A (e.g., Anthropic) is down or rate-limited, it must automatically route to Provider B (e.g., OpenAI/Gemini) without failing the user request.
*   **NFR-3.2:** Large document jobs (over 2,000 words) must run as background tasks (Async API). The user can safely close their browser while the job finishes.

## 4. Security & Privacy
*   **NFR-4.1:** All API endpoints must be protected by a Token-Bucket Rate Limiter to prevent malicious usage/DDoS.
*   **NFR-4.2:** "No-Retention Mode": When enabled by the user, the system MUST NOT persist the generated text to the PostgreSQL database. Memory must be flushed upon session end.
*   **NFR-4.3:** Multi-tenant data isolation: User A must never be able to query or retrieve User B's documents, profiles, or API keys.

## 5. Scalability
*   **NFR-5.1:** The backend must be stateless (except for Redis tracking) to allow horizontal scaling of the FastAPI workers.
*   **NFR-5.2:** WebSockets/Server-Sent Events (SSE) must be used to stream progress updates to the frontend for long-running LangGraph executions.
