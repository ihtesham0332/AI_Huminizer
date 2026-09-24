# Current Problems (Gap Analysis against Master Prompt)

While the v3.0 platform is robust, it lacks the following enterprise-grade requirements specified in the V4 Master Prompt:

## 1. Engine Modularity
*   **Current:** We have a few guardians and a supervisor.
*   **Missing:** 25 distinct modular engines (Document, Language, Style, Protection, Caching, Feedback, etc.).

## 2. Document Parsing
*   **Current:** Only supports raw string text.
*   **Missing:** DOCX, PDF, Markdown parsing while preserving structure (headings, tables).

## 3. Advanced Context & Caching
*   **Current:** No Redis cache. Every request hits the LLM.
*   **Missing:** Redis caching based on document hash to save costs.

## 4. Cost Optimization & Model Routing
*   **Current:** Hardcoded to local Ollama (Qwen2.5).
*   **Missing:** Dynamic `ModelRouter` to swap between Cheap, Medium, and Strong models based on task complexity.

## 5. Database Completeness
*   **Current:** Basic pgvector profile stub.
*   **Missing:** Comprehensive schema (Subscriptions, UsageRecords, Documents, Candidates, Feedback).

## 6. Granular Quality Control
*   **Current:** Basic Guardian pass/fail.
*   **Missing:** Targeted Revision (rewriting *only* the failed sentence instead of the whole text).
