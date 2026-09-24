# UI/UX Specification
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document defines the layout and user experience patterns for the Next.js frontend.

## 1. Core Layout Structure
The main dashboard follows a professional, dense layout suited for editorial work, avoiding the overly-simplistic design of basic paraphrasing tools.

*   **Left Pane (Input):** The original document editor. Supports rich text (paste from Word/Docs) and file dropzones (PDF/DOCX).
*   **Right Pane (Output):** The generated humanized text. Includes tabs at the top for `Version 1`, `Version 2`, and `Version 3` (Multiple Candidates).
*   **Right Side-Panel (Controls):** 
    *   Humanization Mode Selector (Light, Balanced, Deep, Academic).
    *   Writing Profile Dropdown (e.g., "Use my Professional Profile").
    *   Protection Checkboxes (Preserve Numbers, Preserve Citations).
*   **Bottom Pane (Quality Report):** An expandable drawer showing the LangGraph evaluation metrics (Grammar Score, Readability Delta, Style Match %) and the "What Changed" explanation.

## 2. Interactive Features
*   **Inline Diff View:** A toggle button above the Output Pane that visually highlights additions in green and deletions in red, allowing the user to precisely track how the Agentic system altered the semantics.
*   **Paragraph-Level Controls:** Users can highlight a specific paragraph in the Output Pane and click a floating toolbar button to trigger localized actions: `Improve`, `Simplify`, `Make More Academic`.
*   **The "Scan for AI" Dashboard:** A dedicated modal that visualizes the `Burstiness` and `Perplexity` scores as an animated radial gauge, offering a transparent probability metric before export.

## 3. Writing Profile Wizard
*   A dedicated setup flow where users paste text samples.
*   The UI displays a dynamic "Analyzing your style..." animation.
*   Once complete, it renders a radar chart visualizing the user's stylistic fingerprint (Formality vs. Conversational, Simple vs. Complex Vocabulary) to prove the system understood their voice.

## 4. Design System (Obsidian Glass)
*   **Theme:** Dark mode by default, utilizing deep purples (`#1e1b4b`), soft neon accents (`#a855f7`), and frosted glassmorphism for panels (`backdrop-filter: blur`).
*   **Typography:** Inter (for clean UI elements) and Merriweather (for long-form reading in the text panes).
