# 25. PERFORMANCE PLAN

## 1. Latency Budgets
*   **UI Render:** < 100ms
*   **Document Upload & Parsing:** < 2 seconds (for 10MB PDF).
*   **Fast Mode Transformation (1 Paragraph):** < 4 seconds.
*   **Deep Mode Transformation (1 Paragraph):** < 12 seconds.

## 2. Parallelization Strategy
The biggest bottleneck is sequential LLM calls.
*   *Bad:* Run Style Analysis -> Wait -> Run Fact Extraction -> Wait -> Generate.
*   *Good (Our approach):* Run Style Analysis, Fact Extraction, and Citation Extraction asynchronously via LangGraph concurrent branches. Await all -> Generate.

## 3. Caching Strategy
*   Use Redis to cache exact-match sentences.
*   If a user processes a document, realizes they forgot to change a setting, and re-processes it, the identical sentences should hit the Redis cache and return in 50ms, saving 100% of the API cost.

## 4. Autoscaling
*   Deploy FastAPI workers on AWS ECS Fargate or Kubernetes. Scale workers based on concurrent job queue depth in Redis (using Celery/RQ).
