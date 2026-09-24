# 06. FUNCTIONAL REQUIREMENTS

This document details the specific actions the system must perform to satisfy the Product Requirements.

## 1. Input Processing
*   **FR-1.1:** The user shall be able to upload `.txt`, `.docx`, `.pdf`, and `.md` files up to 30,000 words.
*   **FR-1.2:** The system shall parse the document into structured `Section`, `Paragraph`, and `Sentence` blocks.
*   **FR-1.3:** The system shall calculate word counts and estimate the cost (in credits) to process the document before execution.

## 2. Agentic Analysis & Protection
*   **FR-2.1:** The `FactGuardianAgent` shall extract all numerical values (e.g., "15%", "$5M", "2026") from a sentence.
*   **FR-2.2:** The `CitationGuardianAgent` shall extract all academic citations (e.g., "[Smith 2024]", "(Doe, 2023)").
*   **FR-2.3:** The `StyleAgent` shall calculate a Formality Score (1-10) and Readability Score (Flesch-Kincaid) for the document.

## 3. Selective Routing & Transformation
*   **FR-3.1:** The `CostControllerAgent` shall categorize each sentence's complexity.
*   **FR-3.2:** The `ModelRouterAgent` shall assign low-complexity sentences to a fast model (e.g., Gemini Flash or Llama 3) and high-complexity/academic sentences to a reasoning model (e.g., Claude 3.5 Sonnet / GPT-4o).
*   **FR-3.3:** The `HumanizerAgent` shall generate rewritten text that strictly adheres to the locked Facts and Citations.

## 4. Quality Verification
*   **FR-4.1:** The `QualityCriticAgent` shall compare the Original Sentence against the Generated Sentence.
*   **FR-4.2:** If a protected entity (Fact, Citation, Terminology) is missing in the generated output, the `QualityCriticAgent` SHALL trigger a `RevisionAgent` loop.
*   **FR-4.3:** The system shall abort the revision loop after `MAX_REVISION_LOOPS` (default 3) and gracefully fallback to the original sentence to prevent infinite loops.

## 5. User Output
*   **FR-5.1:** The system shall display a side-by-side diff of the Original vs. Humanized text.
*   **FR-5.2:** The system shall provide an `Explainability` tag for each changed sentence (e.g., "Improved tone", "Fixed grammar").
*   **FR-5.3:** The user shall be able to export the final text to `.docx` or `.txt`.
