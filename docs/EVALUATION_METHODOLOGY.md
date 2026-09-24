# Evaluation Methodology
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Multi-Dimensional Quality Scoring
The platform does not rely on a single "AI Score". We evaluate success using a matrix:
1.  **Semantic Preservation Score:** Computed via cosine similarity between the embeddings of the original text and the humanized output (Target: > 0.95).
2.  **Factual Retention Rate:** Percentage of protected tokens (numbers/dates) successfully present in the final output (Target: 100%).
3.  **Readability Delta:** Difference in Flesch-Kincaid Grade Level before and after processing.
4.  **Style Match %:** Distance between the generated output's stylistic vector and the User's Writing Profile vector.

## 2. A/B Testing Framework
*   **Baseline:** Standard zero-shot LLM prompt ("Rewrite this to sound human").
*   **Variant:** Our full LangGraph Agentic Pipeline.
*   **Metric:** We will log the Semantic Preservation and Factual Retention of both approaches on a dataset of 500 academic paragraphs to prove the Agentic System's superiority.
