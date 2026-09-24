# HUMANTEXT MASTER PLAN: Agentic Writing Intelligence Platform

*This document serves as the master blueprint for transitioning the HumanText Engine from a basic text rewriter into a professional-grade, multi-agent Quality Assurance and Personal Writing Intelligence Platform.*

## 📌 Phase 1: Research & Documentation (Milestone 1 & 2)

Before writing any new code, we must generate the 20 foundational documents requested in the Master Prompt. These will be stored in a new `docs/` directory.

### The 20 Required Documents:
1. `docs/COMPETITIVE_RESEARCH.md`
2. `docs/REQUIREMENTS_SPEC.md`
3. `docs/FUNCTIONAL_REQUIREMENTS.md`
4. `docs/NON_FUNCTIONAL_REQUIREMENTS.md`
5. `docs/SYSTEM_ARCHITECTURE.md`
6. `docs/AGENT_ARCHITECTURE.md`
7. `docs/LANGGRAPH_WORKFLOW.md`
8. `docs/DATA_MODEL.md`
9. `docs/API_SPEC.md`
10. `docs/UI_UX_SPEC.md`
11. `docs/SECURITY_ARCHITECTURE.md`
12. `docs/PRIVACY_ARCHITECTURE.md`
13. `docs/EVALUATION_METHODOLOGY.md`
14. `docs/TESTING_STRATEGY.md`
15. `docs/DEVELOPMENT_ROADMAP.md`
16. `docs/RISK_ANALYSIS.md`
17. `docs/COST_ANALYSIS.md`
18. `docs/MODEL_SELECTION.md`
19. `docs/PROMPT_ARCHITECTURE.md`
20. `docs/RESEARCH_CONTRIBUTION.md`

---

## 🏗️ Phase 2: Core Architecture & Parsers (Milestone 3)

### Input/Document Analyzer
- **Agents Built:** `Input Analyzer`, `Language Agent`, `Content Classifier`, `Style Analyzer`, `AI Pattern Analyzer`.
- **Infrastructure:** File parsing (DOCX, PDF, Markdown) with formatting preservation.
- **Goal:** Extract structured JSON representing the document's DNA (word count, language, style metrics).

---

## 🛡️ Phase 3: Protection & Planning (Milestone 5 & 10)

### Fact & Citation Protection
- **Agents Built:** `Fact Guardian`, `Citation Guardian`, `Technical-Term Guardian`.
- **Goal:** Extract and protect numbers, URLs, dates, and technical terminology (e.g., "LangGraph") before any humanization occurs.

### Humanization Planner
- **Agents Built:** `Humanization Planner`.
- **Goal:** Determines *what* should change (e.g., "high sentence variation, low vocabulary change") based on the Style Profile.

---

## 🧠 Phase 4: The Multi-Agent Engine (Milestone 4, 6, 8)

### Parallel Generation & Evaluation
- **Agents Built:** `Humanizer`, `Candidate Generator`, `Quality Critic`, `Finalizer`, `Supervisor`.
- **Goal:** Generate 3 distinct candidates (e.g., Professional, Academic, Conversational).
- **LangGraph Workflow:** The `Supervisor` routes the candidates to parallel evaluation nodes.

### Quality Assurance (Milestone 7)
- **Agents Built:** `Semantic Checker`, `Grammar Checker`, `Readability Checker`, `Style Checker`.
- **Goal:** Verify that negations, numbers, and core claims remain identical. If a candidate fails, the Supervisor triggers a rewrite (max 3 iterations).

---

## 👤 Phase 5: Personalization & UX (Milestone 9, 11)

### Personal Writing Profiles
- **Goal:** Allow users to upload 3-5 writing samples. Store their stylistic DNA (using `pgvector` or local embeddings) to align output generation to their exact voice.

### Frontend Overhaul
- **Goal:** Update the React/Next.js UI to support:
  - Multi-candidate selection tabs.
  - Granular checkboxes (Preserve Numbers, Preserve Citations).
  - Advanced Quality Reports (Before/After metrics).
  - Version History.

---

## ⚙️ Phase 6: Enterprise Infrastructure (Milestone 12, 13, 14)

### Production Hardening
- **Database:** PostgreSQL for User, Document, and Profile storage.
- **API:** RESTful endpoints for all tools (`/analyze`, `/humanize`, `/grammar`).
- **Security:** Rate limiting, auth, and temporary file cleanup.
- **Evaluation:** A robust testing framework for A/B testing baseline LLMs vs the Agentic System.

---

## 🔄 Execution Strategy

We will execute this strictly one milestone at a time. 
For each milestone, we will:
1. Explain the objective & architecture.
2. List files to create/change.
3. Implement.
4. Run tests & show results.
5. Fix problems & update docs.
6. Await user approval before proceeding to the next milestone.
