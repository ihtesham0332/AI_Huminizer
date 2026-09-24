# Functional Requirements
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document outlines the specific functional behavior the system must exhibit.

## 1. Document & Input Analysis
*   **FR-1.01:** The system MUST parse `.txt`, `.md`, `.docx`, and `.pdf` files.
*   **FR-1.02:** The `Input Analyzer Agent` MUST output a JSON object containing: word count, language, content type, and flags for tables/citations/technical terms.
*   **FR-1.03:** The `Language Agent` MUST identify the specific input language (English, Urdu, Roman Urdu, Arabic, Hindi) and enforce language-specific grammatical and readability rules.

## 2. Fact & Semantic Protection
*   **FR-2.01:** The `Fact Guardian` MUST extract all numbers, percentages, dates, proper nouns, and URLs into a protected token registry before humanization.
*   **FR-2.02:** The `Citation Guardian` MUST identify and lock APA, MLA, Chicago, and inline citations.
*   **FR-2.03:** The `Semantic Verification Agent` MUST compare the semantic representation of the original text with the humanized text to ensure claims and negations are not altered.

## 3. Humanization & Candidate Generation
*   **FR-3.01:** The `Humanization Planner` MUST generate a structured rewrite plan (e.g., {"sentence_variation": "high", "vocabulary_change": "low"}) before text generation begins.
*   **FR-3.02:** The `Candidate Generator` MUST generate exactly three (3) parallel humanized candidates (e.g., Professional, Academic, Conversational).
*   **FR-3.03:** The `Supervisor` MUST route all three candidates to the `Quality Critic` for evaluation.

## 4. Quality Assurance Loop
*   **FR-4.01:** The system MUST execute Semantic Check, Fact Check, Citation Check, Grammar Check, and Readability Check in parallel (via LangGraph branches).
*   **FR-4.02:** If any critical check (Semantic, Fact, Citation) fails, the `Supervisor` MUST trigger a rewrite.
*   **FR-4.03:** The system MUST halt the rewrite loop after a configurable maximum of 3 iterations to prevent infinite looping.
*   **FR-4.04:** The `Change Explanation Agent` MUST generate a summary of structural changes (e.g., "3 passive constructions improved") upon successful completion.

## 5. Personal Writing Profiles
*   **FR-5.01:** The system MUST allow users to upload 3 to 5 reference documents.
*   **FR-5.02:** The system MUST extract a numerical "Style Profile" capturing formality, technicality, directness, and vocabulary complexity.
*   **FR-5.03:** The user MUST be able to apply this profile to any future humanization job.

## 6. Output & Export
*   **FR-6.01:** The UI MUST display a side-by-side comparison of the Original vs. Humanized text.
*   **FR-6.02:** The system MUST allow the user to export the humanized text to `.txt`, `.docx`, and `.pdf`.
