# 28. RISK REGISTER

| Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **LLM Provider Outage** | Critical | High | Implement Model Router with automatic fallback (e.g., Anthropic -> OpenAI). |
| **Runaway API Costs** | Critical | Medium | Cost Controller assigns strict budgets per job. Disable infinite revision loops (max 3). Implement Redis caching. |
| **Infinite LLM Loop** | High | Low | The `QualityCritic` might repeatedly reject a candidate. Solution: Hard cap `MAX_REVISION_LOOPS=3`. If it fails, fallback to original sentence. |
| **Complex PDF Parsing Fails** | Medium | High | Two-column academic PDFs often parse poorly. Solution: Use advanced layout-aware parsers (like PyMuPDF or unstructured.io) and warn users to review formatting. |
| **Fact Guardian Misses Data** | High | Low | If a fact is missed during extraction, it won't be protected. Solution: Continuous integration testing on a massive dataset of complex numerical/academic sentences. |
| **Slow Latency** | High | Medium | LangGraph execution takes too long. Solution: Stream (SSE) completed sentences to the frontend instantly while the rest of the document processes in the background. |
