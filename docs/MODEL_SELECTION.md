# Model Selection Strategy
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Local vs. Cloud Abstraction
The system utilizes a hybrid model approach. 

### Local Models (Ollama)
*   **Model:** `Qwen2.5:3b` or `Llama-3-8b-Instruct`.
*   **Use Case:** High-volume, low-complexity tasks requiring JSON output.
*   **Agents:** Input Analyzer, Style Analyzer, Grammar Checker, Readability Checker.

### Cloud Models (OpenAI / Anthropic / Gemini)
*   **Model:** `gpt-4o-mini` or `gemini-1.5-flash`.
*   **Use Case:** Creative generation requiring deep contextual understanding and natural phrasing.
*   **Agents:** Humanizer, Candidate Generator.

### Embedding Models
*   **Model:** `text-embedding-3-small` or `nomic-embed-text`.
*   **Use Case:** Semantic similarity comparisons and Writing Profile vectorization.
*   **Agents:** Semantic Checker.
