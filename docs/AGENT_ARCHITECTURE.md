# Agent Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document defines the specialized micro-agents that constitute the intelligence of the platform.

## 1. Orchestration
*   **Supervisor Agent:** The central brain. Determines which agents run in parallel, evaluates Quality Gates, and decides whether a rewrite cycle is necessary.

## 2. Analyzers
*   **Input Analyzer:** Detects language, word count, and document structure.
*   **Language Agent:** Enforces language-specific grammar and readability indices.
*   **Content Classifier:** Categorizes text (Academic, Blog, Email) to set base context.
*   **Style Analyzer:** Extracts the numerical Style Profile (formality, vocabulary complexity).
*   **AI Pattern Analyzer:** Flags repetitive structures, unnatural symmetry, and generic transitions.

## 3. The Guardians (Protection)
*   **Fact Guardian:** Extracts numbers, dates, proper nouns, and URLs into a protected registry.
*   **Citation Guardian:** Locks APA, MLA, Chicago, and inline citations.
*   **Technical-Term Guardian:** Protects user-defined jargon (e.g., "LangGraph", "RAG").

## 4. Generators
*   **Humanization Planner:** Creates the strategic blueprint (e.g., "High vocabulary variation, Low structural change").
*   **Candidate Generator:** Generates 3 parallel variations (A, B, C) based on the Planner's blueprint.
*   **Humanizer:** The core rewriting engine that applies the target voice while avoiding protected tokens.

## 5. Evaluators (Quality Assurance)
*   **Semantic Checker:** Uses embeddings to ensure core claims and negations are preserved.
*   **Fact/Citation Checker:** Verifies 100% inclusion of all items protected by the Guardians.
*   **Grammar/Readability/Style Checkers:** Evaluates output against baseline requirements and the User's Writing Profile.
*   **Quality Critic:** Aggregates scores from all checkers and outputs a PASS/FAIL boolean with reasoning.

## 6. Finalization
*   **Finalizer:** Selects the best candidate (if multiple pass) and performs minor formatting cleanup.
*   **Change Explanation Agent:** Generates the transparent "What Changed and Why" report for the user.
