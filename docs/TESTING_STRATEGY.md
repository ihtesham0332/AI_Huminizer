# Testing Strategy
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Unit Testing
*   **Framework:** `pytest`.
*   **Scope:** Pydantic schemas, isolated parser functions (PDF/DOCX extraction), and heuristic algorithms (e.g., Burstiness calculator).

## 2. Agent & Workflow Testing
*   **Mocking:** LLM calls inside agents will be mocked to return predictable JSON structures during CI/CD.
*   **LangGraph Testing:** The state machine will be tested by injecting predefined `HumanizationState` objects and asserting that the `Supervisor` routes to the correct node (e.g., verifying it routes to `Rewrite` if a mock Fact Check fails).

## 3. Adversarial Semantic Testing
Critical edge-case tests to ensure the AI does not hallucinate:
*   **Negation Reversal:** Input: "The treatment is not effective." Output must retain the negative.
*   **Number Alteration:** Input: "Increased by 95%." Output must not say "Increased by 90%."
*   **Citation Hallucination:** Input: "(Smith, 2023)." Output must retain the exact citation.
