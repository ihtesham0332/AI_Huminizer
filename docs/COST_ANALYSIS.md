# Cost Analysis
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Model Call Breakdown per Job
Assuming a 500-word document:
1.  **Analyzers:** 3 calls -> Local Qwen2.5 ($0)
2.  **Guardians:** 2 calls -> Local Qwen2.5 ($0)
3.  **Candidate Generation:** 3 calls -> Cloud Model (e.g., GPT-4o-mini) -> ~$0.005
4.  **Quality Assurance:** 4 calls -> Local Qwen2.5 ($0)
5.  **Critic/Finalizer:** 1 call -> Local Qwen2.5 ($0)

*Total Expected Cost per Job:* ~$0.005.

## 2. Infrastructure Costs
*   **PostgreSQL + pgvector:** Managed database (e.g., Supabase or AWS RDS) ~ $20/month.
*   **Redis:** For rate limiting and Celery queues ~ $10/month.
*   **API Gateway & Compute:** Vercel (Frontend) + DigitalOcean/AWS (FastAPI/LangGraph Workers) ~ $40/month.

## 3. Caching Strategy
*   Identical paragraphs bypass the entire LangGraph engine and hit the database cache, dropping the LLM cost for that segment to $0.
