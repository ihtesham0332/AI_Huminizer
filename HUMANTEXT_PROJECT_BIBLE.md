# 📖 HumanText Engine — Complete Project Bible

> **PURPOSE OF THIS FILE:** This is the **single source of truth** for the entire HumanText Engine project. Read this file before creating ANY skill, agent, graph node, or API endpoint. It consolidates all 3 research phases + the 50-part Master Prompt into one easy-to-read reference so that **no context is lost** between sessions.

**Last Updated:** 2026-09-21
**Project:** HumanText Engine — Advanced Multi-Agent Natural Text Transformation System
**Stack:** Python 3.12+ · FastAPI · LangGraph · Pydantic v2 · spaCy · sentence-transformers

---

## TABLE OF CONTENTS

1. [Project Identity](#1-project-identity)
2. [Operating Rules (NEVER BREAK)](#2-operating-rules-never-break)
3. [What Is Text Humanization](#3-what-is-text-humanization)
4. [Success Criteria](#4-success-criteria)
5. [How Humanization Differs From Other Tasks](#5-how-humanization-differs-from-other-tasks)
6. [Research Questions (RQ1–RQ15)](#6-research-questions)
7. [Competitor Analysis](#7-competitor-analysis)
8. [Target Users](#8-target-users)
9. [Document Types & Transformation Policies](#9-document-types--transformation-policies)
10. [12 Naturalness Dimensions](#10-12-naturalness-dimensions)
11. [14 Linguistic Features](#11-14-linguistic-features)
12. [20 Skills Catalog](#12-20-skills-catalog)
13. [12 Agents Catalog](#13-12-agents-catalog)
14. [Semantic Guardian](#14-semantic-guardian)
15. [Fact Guardian](#15-fact-guardian)
16. [Writing DNA](#16-writing-dna)
17. [8 Rewrite Modes](#17-8-rewrite-modes)
18. [LangGraph Architecture](#18-langgraph-architecture)
19. [State Schema](#19-state-schema)
20. [FastAPI Endpoints](#20-fastapi-endpoints)
21. [Technology Stack](#21-technology-stack)
22. [Repository Structure](#22-repository-structure)
23. [Credential Management](#23-credential-management)
24. [Build Order (50 Steps)](#24-build-order-50-steps)
25. [Quick Reference Checklists](#25-quick-reference-checklists)

---

## 1. PROJECT IDENTITY

**Name:** HumanText Engine
**Goal:** Transform robotic, generic, repetitive, unnatural text into natural, fluent, readable, context-appropriate, stylistically consistent writing — while **preserving original meaning, facts, claims, numbers, dates, names, entities, citations, technical terminology, logical relationships, uncertainty, qualifications, user intent, and document purpose.**

**What this project is NOT:**
- ❌ NOT an "AI detector bypass" tool
- ❌ NOT a simple paraphraser
- ❌ NOT a grammar checker
- ❌ NOT optimized against any specific detector

**What this project IS:**
- ✅ Natural language transformation with semantic preservation
- ✅ Factual consistency guaranteed
- ✅ Context-appropriate style adaptation
- ✅ Measurable quality with 12 named dimensions
- ✅ Multi-agent architecture with LangGraph orchestration
- ✅ Professional FastAPI service

---

## 2. OPERATING RULES (NEVER BREAK)

> ⚠️ **EVERY skill, agent, prompt, and test MUST comply with ALL five rules below. No exceptions.**

### Rule 1 — Research Before Architecture
Do not assume an architecture. Research the problem first. Compare alternatives. Explain why the final choice was selected.

### Rule 2 — Evidence Before Claims
For every important technical claim: find reliable evidence, prefer primary research, prefer peer-reviewed papers. **Do not invent citations. Do not fabricate benchmark results.**

### Rule 3 — Do Not Over-Agentize
Do NOT create an AI agent merely because it is possible. For every proposed agent ask:
1. Does it require reasoning?
2. Does it have an independent responsibility?
3. Can it be implemented more reliably as deterministic code?
4. Can another existing agent handle it?
5. Does it provide measurable value?

**Use normal Python/NLP functions where they are better than agents.**

### Rule 4 — Preserve Meaning Above Everything
The system must **NEVER** sacrifice semantic accuracy to make text appear more natural. A rewrite that sounds better but changes the original meaning = **FAILURE**.

### Rule 5 — No Unsupported Information
The rewrite system must NOT:
- Invent facts or statistics
- Invent citations
- Change numbers, dates, or names
- Remove important qualifiers
- Reverse or strengthen/weaken claims
- Add unsupported information

---

## 3. WHAT IS TEXT HUMANIZATION

> Text humanization is the controlled transformation of writing so that its surface form — sentence structure, lexical choices, rhythm, discourse flow, and stylistic register — matches patterns typical of natural human-authored text, **without altering the semantic content, factual claims, or communicative intent of the source.**

It sits at the intersection of three sub-problems:

| Sub-Problem | What It Does |
|---|---|
| **Surface-form normalization** | Reduce statistically unnatural patterns (repetitive openers, uniform sentence length, over-used discourse markers, excessive hedging/nominalization) |
| **Style adaptation** | Shift register, tone, and voice toward a target profile (document type, audience, or individual Writing DNA) |
| **Semantic-preserving generation** | Produce new surface text constrained to encode the same propositional content, modality, and qualifications as the source |

**Critical:** Detector evasion is a possible *side effect* of good humanization, but it is **never the target**. Detection is treated as an *external, secondary evaluation signal*.

---

## 4. SUCCESS CRITERIA

A transformation succeeds **only if ALL of the following hold simultaneously:**

| # | Criterion | Status |
|---|---|---|
| 1 | Meaning, facts, numbers, dates, names, entities, citations, technical terms are **unchanged** | ✅ Required |
| 2 | Modality, hedging, and uncertainty levels are **unchanged** ("may" cannot become "will") | ✅ Required |
| 3 | Scope qualifiers are **unchanged** ("some workplaces" cannot become "all workplaces") | ✅ Required |
| 4 | Output reads as natural, fluent, and appropriately styled for the target document type/audience | ✅ Required |
| 5 | Structural variation exists where the original was repetitive or robotic | ✅ Required |
| 6 | Output evades any specific AI-text detector | ❌ NOT required, NEVER optimized for |

---

## 5. HOW HUMANIZATION DIFFERS FROM OTHER TASKS

| Task | Relation to HumanText Engine |
|---|---|
| **Paraphrasing** | A *technique* we use, not the goal itself |
| **Rewriting** | Broader superset; we are a constrained form of rewriting |
| **Text Simplification** | A possible *mode* (Mode 3: Simple & Clear), not the whole system |
| **Grammar Correction** | A prerequisite quality check, not a rewrite goal |
| **Style Transfer** | A *core mechanism* inside our style adaptation layer |
| **Text Normalization** | A deterministic preprocessing step |
| **Text Polishing** | Overlaps with "light" humanization mode |
| **Personalized Writing** | A *specialization* (our Writing DNA subsystem) |
| **Controlled Generation** | The generation *paradigm* our Rewrite Engine is built on |
| **Human Editing** | The gold-standard reference behavior we approximate |
| **AI Detection** | An *external evaluation lens*, explicitly NOT our optimization target |

**Identity:** The combination of (a) aggressive surface-level rewriting capability and (b) a hard, verifiable semantic/factual preservation guarantee — no single adjacent task provides both.

---

## 6. RESEARCH QUESTIONS

| ID | Question | Answered By |
|---|---|---|
| RQ1 | What linguistic features make generated text read as robotic? | Literature + corpus analysis |
| RQ2 | Which transformation techniques improve perceived naturalness? | Ablation experiments |
| RQ3 | How can semantic meaning be preserved during aggressive rewriting? | Semantic Guardian + NLI checks |
| RQ4 | How can factual consistency be verified automatically? | Fact Guardian design |
| RQ5 | How can a system learn an individual's writing style? | Writing DNA design |
| RQ6 | Does multi-agent architecture provide measurable gains over single-pass? | Baseline comparison |
| RQ7 | Does planning before generation improve quality? | Ablation: planner on/off |
| RQ8 | Does iterative revision reduce semantic drift? | Ablation: revision on/off |
| RQ9 | Which models offer best quality/cost/latency tradeoff? | Model benchmark |
| RQ10 | Which automated metrics correlate with human judgments? | Human eval correlation |
| RQ11 | What are the limitations of AI-text detectors? | Literature review |
| RQ12 | How should naturalness be evaluated independently? | Naturalness framework |
| RQ13 | Does parallelizing agents reduce latency without quality loss? | Concurrency experiment |
| RQ14 | What is the minimum agent count for quality gain? | Ablation study |
| RQ15 | What privacy risks does Writing DNA introduce? | Privacy analysis |

---

## 7. COMPETITOR ANALYSIS

| Competitor | Category | Key Gap vs. HumanText Engine |
|---|---|---|
| **QuillBot** | Paraphraser | Shallow rewriting, no fact-checking, no personalization |
| **Grammarly** | Writing assistant | Correctness-focused, not deep humanization |
| **Wordtune** | Rewrite assistant | Sentence-level only, no document-level planning |
| **AI humanizer tools** | Detector-evasion | No semantic preservation guarantee, no evaluation |
| **AI detectors** | Classification | Measurement tools, not humanizers |

**Our Advantages:**
1. Verifiable semantic/factual preservation
2. Published evaluation methodology
3. Per-document-type transformation policies
4. Genuine personalization (Writing DNA)

---

## 8. TARGET USERS

| User | Core Need | Strictness Level |
|---|---|---|
| **Students** | Natural academic prose, same argument/citations | HIGH fidelity |
| **Researchers** | Publication-quality writing, zero factual drift | HIGHEST fidelity |
| **Engineers** | Clear, natural technical writing | HIGH terminology preservation |
| **Marketers** | Engaging, on-brand natural copy | MEDIUM fidelity, HIGH tone |
| **Business professionals** | Professional but natural tone | MEDIUM-HIGH fidelity |
| **Organizations** | Consistent natural voice at scale | HIGH consistency, HIGH privacy |

**Design consequence:** The system MUST support per-user-type transformation policies. A single "humanize" button with one fixed strategy is insufficient.

---

## 9. DOCUMENT TYPES & TRANSFORMATION POLICIES

| Document Type | Key Policy |
|---|---|
| **Academic** | Preserve hedging/modality exactly; formal register; citation format untouched |
| **Technical** | Preserve terminology and precision; avoid simplifying away accuracy |
| **Business** | Natural but respectful tone; preserve action items, dates, figures |
| **Email** | Shorter sentences, natural greeting/sign-off, tone-sensitive |
| **Report** | Structured narrative flow; preserve data points exactly |
| **Blog** | More stylistic freedom, higher lexical variation allowed |
| **Social media** | Very short-form, high informality tolerance |
| **Essay** | Balance natural voice with argument structure preservation |
| **Casual** | Highest tolerance for colloquialism, contractions |
| **Creative** | Style transformation central; factual constraints relaxed except stated facts |

**Rule:** Each document type requires a distinct transformation policy. A single global rewriting strategy CANNOT serve all types.

---

## 10. 12 NATURALNESS DIMENSIONS

> Every skill, agent, evaluator, and metric MUST map to one or more of these dimensions.

| # | Dimension | Measurement Signal | Hard/Soft |
|---|---|---|---|
| 1 | **Fluency** | Grammar-error rate, LLM-judge fluency score | Soft |
| 2 | **Readability** | Flesch-Kincaid, avg sentence/word length | Soft |
| 3 | **Coherence** | Discourse-structure analysis, LLM-judge score | Soft |
| 4 | **Cohesion** | Discourse-marker analysis, reference tracking | Soft |
| 5 | **Lexical variation** | Type-token ratio, repeated-word detection | Soft |
| 6 | **Sentence variation** | Length variance, opener repetition rate | Soft |
| 7 | **Appropriate informality** | Contraction rate vs. document type | Soft |
| 8 | **Appropriate formality** | Formality markers vs. document type | Soft |
| 9 | **Personal voice** | Style-similarity score against Writing DNA | Soft |
| 10 | **Contextual appropriateness** | Document-type-policy conformance | Soft |
| 11 | **Discourse quality** | Discourse-marker appropriateness, logic consistency | Soft |
| 12 | **Semantic fidelity** | NLI/entailment checks, fact-diff checks | **HARD** |

> ⚠️ **Dimension 12 is a HARD CONSTRAINT.** A rewrite that improves dimensions 1–11 while degrading dimension 12 is a FAILED rewrite. Dimensions 1–11 are optimized WITHIN the space of outputs that pass dimension 12.

---

## 11. 14 LINGUISTIC FEATURES

> These are the concrete signals that feed the naturalness dimensions. Skills 02, 06, and 08 compute these.

| Feature | Robotic Pattern | Natural Pattern |
|---|---|---|
| **Sentence length** | Uniform length throughout | Mix of short and long |
| **Clause depth** | Uniformly simple or over-nested | Varies with content complexity |
| **Vocabulary frequency** | Overuse of "Moreover," "Furthermore" | Broader, context-appropriate vocabulary |
| **Lexical diversity** | Low type-token ratio | Higher diversity appropriate to genre |
| **Repetition** | Same template reused repeatedly | Varied structures |
| **Discourse markers** | Overused, mechanically inserted | Used only where logical relation exists |
| **Punctuation** | Only periods/commas | Natural dashes, semicolons, question marks |
| **Active/passive voice** | All-active or all-passive | Ratio matches genre convention |
| **Nominalization** | High ("utilization" vs. "use") | Verbs used directly where natural |
| **Hedging density** | Absent or excessive/uniform | Matches evidentiary strength |
| **Excessive formality** | "Utilize," "in order to" everywhere | Formality matched to document type |
| **Sentence openings** | Repeated ("This," "Additionally,") | Openers vary naturally |
| **Paragraph length** | Uniform throughout | Varies with idea density |
| **Pronoun usage** | Impersonal ("It can be seen that...") | Direct pronoun use where genre allows |

> ⚠️ **Context-dependence rule:** None of these features has a single "correct" value. Each is evaluated relative to the document type's expected range. More variation ≠ always better.

---

## 12. 20 SKILLS CATALOG

> Every skill is a reusable, testable function. Some are deterministic (Python/NLP), some require LLM. Each skill maps to specific naturalness dimensions.

### Analysis Skills (Skills 01–08)

| Skill | Purpose | LLM? | Key Inputs | Key Outputs | Dimensions |
|---|---|---|---|---|---|
| **01 Input Validation** | Validate input (empty, too long, malformed, language) | No | Raw text | Validation result, cleaned text | Gate |
| **02 Document Analysis** | Sentence/paragraph stats, structural features | No | Cleaned text | Sentence lengths, paragraph lengths, structure map | 2, 5, 6 |
| **03 Semantic Analysis** | Extract core meaning, propositions, entailment structure | Yes | Cleaned text | Propositions, meaning graph | 12 |
| **04 Claim Extraction** | Extract claims with modality, hedging, scope | Yes | Cleaned text | Claims list with qualifiers | 12 |
| **05 Fact Extraction** | Extract numbers, dates, names, entities, citations | Hybrid | Cleaned text | Facts registry | 12 |
| **06 Style Analysis** | Formality, tone, voice, lexical patterns | Hybrid | Cleaned text | Style profile | 7, 8, 9, 10 |
| **07 Context Analysis** | Detect document type, audience, purpose, register | Yes | Cleaned text | Context profile | 10 |
| **08 Readability Analysis** | Flesch-Kincaid, sentence complexity, vocabulary level | No | Cleaned text | Readability scores | 2 |

### Transformation Skills (Skills 09–14)

| Skill | Purpose | LLM? | Key Inputs | Key Outputs | Dimensions |
|---|---|---|---|---|---|
| **09 Humanization Planning** | Structured transformation plan (JSON operations) | Yes | All analysis results | Operations plan | All |
| **10 Sentence Transformation** | Split, merge, reorder, restructure sentences | Yes | Plan + sentences | Transformed sentences | 1, 5, 6 |
| **11 Paragraph Transformation** | Paragraph-level flow, transitions, structure | Yes | Plan + paragraphs | Transformed paragraphs | 3, 4, 11 |
| **12 Discourse Optimization** | Discourse markers, coherence, argument flow | Yes | Plan + full text | Optimized text | 3, 4, 11 |
| **13 Terminology Preservation** | Lock technical terms, defined terms, jargon | No | Facts registry + text | Locked terms list | 12 |
| **14 Citation Preservation** | Lock citations, references, URLs, DOIs | No | Facts registry + text | Locked citations list | 12 |

### Validation Skills (Skills 15–20)

| Skill | Purpose | LLM? | Key Inputs | Key Outputs | Dimensions |
|---|---|---|---|---|---|
| **15 Semantic Validation** | NLI-based: does rewrite preserve meaning? | Yes | Original + rewrite | Semantic score (0–1), drift details | 12 |
| **16 Fact Validation** | Compare extracted facts before/after rewrite | Hybrid | Original facts + rewrite facts | Fact score, discrepancies list | 12 |
| **17 Style Validation** | Does rewrite match target mode/profile? | Yes | Rewrite + target style | Style conformance score | 7, 8, 9, 10 |
| **18 Naturalness Evaluation** | Score against 12 naturalness dimensions | Yes | Rewrite + document type | Per-dimension scores | 1–11 |
| **19 Quality Evaluation** | Composite quality score, pass/fail gate | Hybrid | All validation scores | Quality verdict + score | All |
| **20 Revision** | Targeted revision based on validation failures | Yes | Rewrite + failure list | Revised text | All |

---

## 13. 12 AGENTS CATALOG

> Agents are thin orchestration wrappers around skills. They add reasoning, error handling, and structured output.

| # | Agent | Skills Used | Model Tier | Parallel Group |
|---|---|---|---|---|
| 1 | **Input Validator** | Skill 01 | None (deterministic) | — |
| 2 | **Document Analyst** | Skill 02, 08 | Light | Analysis ⚡ |
| 3 | **Semantic Analyst** | Skill 03, 04 | Strong | Analysis ⚡ |
| 4 | **Style Analyst** | Skill 06 | Light | Analysis ⚡ |
| 5 | **Context Analyst** | Skill 07 | Light | Analysis ⚡ |
| 6 | **Planner** | Skill 09 | Strong | — |
| 7 | **Rewriter** | Skills 10, 11, 12, 13, 14 | Strong | — |
| 8 | **Semantic Validator** | Skill 15 | Strong | Validation ⚡ |
| 9 | **Fact Validator** | Skill 16 | Light | Validation ⚡ |
| 10 | **Style Critic** | Skill 17 | Light | Validation ⚡ |
| 11 | **Quality Judge** | Skills 18, 19 | Strong | — |
| 12 | **Revision Agent** | Skill 20 | Strong | — |

**⚡ = runs in parallel** with other agents in the same group.

---

## 14. SEMANTIC GUARDIAN

> The **highest-priority subsystem**. Enforces Rule 4 (Preserve Meaning Above Everything).

**What it extracts and protects:**

| Element | Example | Must Be Preserved Exactly |
|---|---|---|
| Evidence level | "suggests," "shows," "proves" | ✅ |
| Modality | "may," "could," "will," "must" | ✅ |
| Scope | "some," "all," "most," "few" | ✅ |
| Hedging | "possibly," "potentially," "arguably" | ✅ |
| Negations | "not," "never," "none" | ✅ |
| Causal relations | "because," "due to," "leads to" | ✅ |
| Uncertainty | "unclear," "uncertain," "debatable" | ✅ |

**Example:**
```
Original: "The study suggests that AI may improve productivity in some workplaces."

PROTECTED:
  evidence_level = "suggests"
  modality       = "may"
  scope          = "some workplaces"
  claim          = "AI may improve productivity"

FORBIDDEN: "AI definitely improves productivity everywhere."
```

---

## 15. FACT GUARDIAN

> Protects all factual elements from deletion, alteration, invention, or contradiction.

**What it checks:**

| Element | Check Type |
|---|---|
| Numbers/percentages | Exact match |
| Dates | Exact match |
| Names/people | Exact match |
| Organizations | Exact match |
| Locations | Exact match |
| Technical terms | Exact match |
| Citations/references | Exact match |
| URLs | Exact match |
| Measurements/units | Exact match |

**Failure types:** Deletion · Alteration · Invention · Contradiction · Unsupported strengthening

---

## 16. WRITING DNA

> Personalization system. Learns style from samples WITHOUT copying phrases.

**Schema:**
```json
{
  "writing_dna": {
    "tone": {"dominant": "analytical", "range": ["formal", "neutral"]},
    "formality": {"level": 0.75, "uses_contractions": false},
    "directness": {"level": 0.8, "prefers_active_voice": true},
    "sentence_length": {"avg": 18, "std_dev": 7, "range": [5, 42]},
    "vocabulary": {"complexity": "moderate", "domain_terms": ["API", "latency"]},
    "technicality": {"level": 0.7},
    "paragraph_structure": {"avg_sentences": 4, "prefers_short": false},
    "punctuation": {"uses_semicolons": true, "uses_dashes": true},
    "transitions": {"frequency": "moderate", "preferred": ["however", "specifically"]},
    "first_person_usage": {"frequency": "rare", "prefers": "we"}
  }
}
```

**Privacy rules:** No verbatim phrase copying · Model characteristics only · Support deletion · Multi-tenant isolation

---

## 17. 8 REWRITE MODES

| Mode | Target | Formality | Semantic Strictness |
|---|---|---|---|
| 1 Natural Professional | Business docs | Medium-high | High |
| 2 Academic Natural | Papers, essays | High | Highest |
| 3 Simple & Clear | General audience | Low-medium | High |
| 4 Conversational | Blog, casual | Low | Medium |
| 5 Technical | Docs, specs | Medium-high | Highest |
| 6 Business | Email, reports | Medium | High |
| 7 Personalized | Writing DNA match | Varies | High |
| 8 Custom Style | User-defined | User-defined | User-defined |

---

## 18. LANGGRAPH ARCHITECTURE

```
START
  ↓
Input Validation (Agent 1)
  ↓ (fail → Error)
Parallel Analysis ⚡ (Agents 2, 3, 4, 5)
  ├── Document Analyst  →  Skills 02, 08
  ├── Semantic Analyst  →  Skills 03, 04, 05
  ├── Style Analyst     →  Skill 06
  └── Context Analyst   →  Skill 07
  ↓ (all complete)
Planner (Agent 6)  →  Skill 09
  ↓
Rewriter (Agent 7)  →  Skills 10, 11, 12, 13, 14
  ↓
Parallel Validation ⚡ (Agents 8, 9, 10)
  ├── Semantic Validator  →  Skill 15
  ├── Fact Validator      →  Skill 16
  └── Style Critic        →  Skill 17
  ↓ (all complete)
Quality Judge (Agent 11)  →  Skills 18, 19
  ├── PASS → ✅ Final Output
  └── FAIL → Revision Agent (Agent 12)  →  Skill 20
               ↓ (max 3 loops)
             Quality Judge
               ├── PASS → ✅ Final Output
               └── MAX → ⚠️ Best-Effort Output
```

---

## 19. STATE SCHEMA

**Immutable (set once):**
`request_id` · `original_text` · `document_type` · `target_audience` · `target_tone` · `target_style` · `target_mode` · `writing_dna_profile`

**Mutable (agent-written):**
`document_analysis` · `semantic_analysis` · `style_analysis` · `context_analysis` · `readability_analysis` · `claims` · `facts` · `entities` · `constraints` · `transformation_plan` · `rewritten_text` · `semantic_score` · `factual_score` · `style_score` · `readability_score` · `naturalness_score` · `quality_score` · `validation_errors` · `revision_count` · `revision_history`

**Metadata:**
`status` · `agent_metadata` · `model_metadata` · `token_usage` · `latency` · `total_cost`

---

## 20. FASTAPI ENDPOINTS

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/humanize` | Main humanization — full pipeline |
| `POST` | `/api/v1/analyze` | Analysis only — no rewrite |
| `POST` | `/api/v1/writing-dna` | Create/update Writing DNA profile |
| `GET` | `/api/v1/writing-dna/{id}` | Get Writing DNA profile |
| `DELETE` | `/api/v1/writing-dna/{id}` | Delete Writing DNA profile |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/modes` | List rewrite modes |

---

## 21. TECHNOLOGY STACK

| Technology | Purpose |
|---|---|
| **Python 3.12+** | Language |
| **FastAPI** | API framework |
| **Pydantic v2** | Validation/schemas |
| **pydantic-settings** | Config (.env) |
| **LangGraph** | Orchestration |
| **LangChain** | LLM interface |
| **LangSmith** | Observability |
| **spaCy** | NLP (tokenization, NER, parsing) |
| **NLTK** | Linguistics (readability) |
| **sentence-transformers** | Embeddings (semantic similarity) |
| **pytest** | Testing |
| **uvicorn** | ASGI server |

---

## 22. REPOSITORY STRUCTURE

```
humantext-engine/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/settings.py
│   ├── schemas/ (request.py, response.py, state.py)
│   ├── skills/ (skill_01 through skill_20)
│   ├── agents/ (12 agent files)
│   ├── guardians/ (semantic_guardian.py, fact_guardian.py)
│   ├── writing_dna/profile.py
│   ├── graph/ (nodes.py, edges.py, workflow.py)
│   ├── prompts/v1/ (analyst, planner, rewriter, validator, judge)
│   ├── models/router.py
│   ├── evaluation/ (metrics.py, human_eval.py, llm_judge.py)
│   ├── services/humanize.py
│   ├── api/v1/endpoints/ (humanize, analyze, writing_dna, health)
│   └── utils/ (text.py, logging.py, errors.py)
├── tests/ (unit, integration, graph, evaluation)
├── research/
├── data/datasets/
├── .env.example  ← credentials template
├── .gitignore    ← .env is NEVER committed
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 23. CREDENTIAL MANAGEMENT

> ⚠️ **ZERO hardcoded credentials. EVER.**

```python
# app/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    LANGSMITH_API_KEY: str = ""
    PRIMARY_MODEL: str = "gpt-4o"
    ANALYSIS_MODEL: str = "gpt-4o-mini"
    SEMANTIC_THRESHOLD: float = 0.85
    FACT_THRESHOLD: float = 0.95
    MAX_REVISIONS: int = 3
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
```

---

## 24. BUILD ORDER (50 STEPS)

| Step | What It Builds |
|---|---|
| 1 | `pyproject.toml` + `requirements.txt` + `.env.example` + `.gitignore` |
| 2 | `app/config/settings.py` |
| 3 | `app/schemas/state.py` |
| 4 | `app/utils/errors.py` + `logging.py` |
| 5 | `app/utils/text.py` |
| 6 | Skill 01: Input Validation |
| 7 | Skill 02: Document Analysis |
| 8 | Skill 03: Semantic Analysis |
| 9 | Skill 04: Claim Extraction |
| 10 | Skill 05: Fact Extraction |
| 11 | Skill 06: Style Analysis |
| 12 | Skill 07: Context Analysis |
| 13 | Skill 08: Readability Analysis |
| 14 | Skill 09: Humanization Planning |
| 15 | Skill 10: Sentence Transformation |
| 16 | Skill 11: Paragraph Transformation |
| 17 | Skill 12: Discourse Optimization |
| 18 | Skill 13: Terminology Preservation |
| 19 | Skill 14: Citation Preservation |
| 20 | All Versioned Prompts |
| 21 | Skill 15: Semantic Validation |
| 22 | Skill 16: Fact Validation |
| 23 | Skill 17: Style Validation |
| 24 | Skill 18: Naturalness Evaluation |
| 25 | Skill 19: Quality Evaluation |
| 26 | Skill 20: Revision |
| 27 | Semantic Guardian + Fact Guardian |
| 28 | Writing DNA system |
| 29 | Model Router |
| 30 | 8 Rewrite Modes |
| 31 | Agent 1: Input Validator |
| 32 | Agents 2–5: Parallel Analysis |
| 33 | Agent 6: Planner |
| 34 | Agent 7: Rewriter |
| 35 | Agents 8–10: Parallel Validation |
| 36 | Agent 11: Quality Judge |
| 37 | Agent 12: Revision Agent |
| 38 | LangGraph Workflow |
| 39 | API Schemas |
| 40 | Humanize Service |
| 41 | POST /api/v1/humanize |
| 42 | POST /api/v1/analyze |
| 43 | Writing DNA API endpoints |
| 44 | Health + Router + FastAPI main |
| 45 | Evaluation Metrics |
| 46 | LLM-as-Judge |
| 47 | Human Eval Framework |
| 48 | Unit Tests |
| 49 | Integration + Graph Tests |
| 50 | Final Documentation + Diagrams |

---

## 25. QUICK REFERENCE CHECKLISTS

### ✅ Before Writing ANY Skill
- [ ] Read this file's section for that skill (Section 12)
- [ ] Identify which naturalness dimensions it maps to
- [ ] Define Pydantic input/output models
- [ ] Determine if LLM is required or deterministic is better (Rule 3)
- [ ] Plan failure modes and error handling
- [ ] Write test alongside

### ✅ Before Writing ANY Agent
- [ ] Confirm justified (Rule 3 — all 5 questions answered)
- [ ] List which skills it uses
- [ ] Define structured output schema
- [ ] Define retry strategy and timeout
- [ ] Determine model tier (light vs. strong)

### ✅ Before Writing ANY Prompt
- [ ] Include: role, objective, context, input, constraints, prohibited behavior, output schema
- [ ] Use structured JSON output
- [ ] Version the prompt (prompts/v1/)
- [ ] Never put entire workflow in one prompt

### ✅ Before ANY Rewrite
- [ ] Extract claims/facts BEFORE rewriting
- [ ] Lock terminology and citations BEFORE rewriting
- [ ] Validate semantics AFTER rewriting
- [ ] Validate facts AFTER rewriting
- [ ] Dimension 12 (semantic fidelity) is a HARD gate

---

> **📌 HOW TO USE THIS FILE:** Before starting any step, Ctrl+F to the relevant section. Every decision traces back to this document. If something contradicts this document, **this document wins.**
