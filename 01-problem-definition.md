# HumanText Engine — Phase 1: Problem Definition

**Project:** HumanText Engine
**Phase:** 1 of 17 — Define the Research Problem
**Status:** Foundation document. All later phases (agents, skills, LangGraph design, evaluation, etc.) build on the definitions here.

---

## 1.1 What Is Text Humanization?

**Working definition (for this project):**

> Text humanization is the controlled transformation of writing so that its surface form — sentence structure, lexical choices, rhythm, discourse flow, and stylistic register — matches patterns typical of natural human-authored text, **without altering the semantic content, factual claims, or communicative intent of the source.**

From an NLP perspective, humanization sits at the intersection of three sub-problems:

1. **Surface-form normalization** — reducing statistically "unnatural" patterns (repetitive sentence openers, uniform sentence length, over-use of certain discourse markers, excessive hedging or nominalization).
2. **Style adaptation** — shifting register, tone, and voice toward a target profile (a document type, an audience, or an individual author's "writing DNA").
3. **Semantic-preserving generation** — producing new surface text that is constrained to encode the same propositional content, modality, and qualifications as the source.

Critically, humanization is **not** defined by "does it fool an AI detector." Detector evasion is a possible *side effect* of good humanization, but it is not the target. A rewrite is only successful if a careful human reader would judge it as natural, coherent, and equivalent in meaning to the original — regardless of what any detector says.

**Why this distinction matters for the project:** if the system is optimized against a detector, it will overfit to that detector's blind spots and will not generalize; it may also drift toward factual or semantic distortion since detectors do not measure meaning. The project therefore treats detection as an *external, secondary evaluation signal* (see Phase 10), never as a loss function or success criterion.

---

## 1.2 How Humanization Differs From Adjacent Tasks

Humanization overlaps with several established NLP tasks but is not identical to any of them. Below is the reference comparison table used throughout the rest of the project to keep scope boundaries clear.

| Task | Primary Goal | Changes Meaning? | Changes Surface Form? | Target-Style Aware? | Preserves Author Voice? | Relation to Humanization |
|---|---|---|---|---|---|---|
| **Paraphrasing** | Say the same thing differently | No (ideally) | Yes | No | No | A *technique* humanization uses, not the goal itself |
| **Rewriting (general)** | Improve or restructure text | Sometimes | Yes | Rarely | No | Broader/vaguer superset; humanization is a constrained form of rewriting |
| **Text Simplification** | Reduce reading difficulty (vocab, syntax) | Slight (simplification loss) | Yes | No | No | A possible *mode* (Mode 3: Simple & Clear), not the whole system |
| **Grammar Correction** | Fix errors | No | Minimal, localized | No | Yes | A prerequisite/adjacent quality check, not a rewrite goal |
| **Style Transfer** | Shift stylistic attributes (formality, sentiment, persona) | Should not, but risk exists | Yes | Yes | Sometimes | A *core mechanism* inside humanization (style adaptation layer) |
| **Text Normalization** | Standardize format (dates, units, casing) | No | Minimal | No | N/A | A deterministic preprocessing step, not a rewriting concern |
| **Text Polishing** | Light surface cleanup (word choice, flow) | No | Minor | No | Sometimes | Overlaps with "light" humanization mode |
| **Personalized Writing** | Generate/adapt text to match one person's style | No (ideally) | Yes | Yes (one person) | Yes | A *specialization* of humanization (Writing DNA subsystem) |
| **Controlled Generation** | Generate text under explicit constraints (length, keywords, tone) | Depends on constraints | Yes (generation, not edit) | Yes | No | The generation *paradigm* the Rewrite Engine is built on |
| **Human Editing** | A person manually revises text | No (ideally) | Yes | Sometimes | Sometimes | The gold-standard reference behavior the system tries to approximate |
| **AI-Generated Text Detection** | Classify text as AI- or human-authored | N/A (classification, not generation) | N/A | N/A | N/A | An *external evaluation lens*, explicitly NOT the optimization target |
| **HumanText Engine (this project)** | Transform unnatural text into natural, style-appropriate, **meaning-preserving** text | **No — hard constraint** | Yes, extensively | Yes (mode + Writing DNA) | Yes (when Writing DNA is used) | The umbrella task; draws technique from all rows above but is governed by the semantic-preservation constraint above everything |

**Key takeaway for scope control:** every technique borrowed from the rows above (paraphrasing engines, style-transfer models, simplification heuristics) is a *component*, never the *whole system*. The system's identity is defined by the combination of (a) aggressive surface-level rewriting capability and (b) a hard, verifiable semantic/factual preservation guarantee — a combination that no single row above provides alone.

---

## 1.3 What "Success" Means (Preview — formalized in Phase 3 & 10)

A transformation is only a success if **all** of the following hold simultaneously:

- ✅ Meaning, facts, numbers, dates, names, entities, citations, and technical terms are unchanged
- ✅ Modality, hedging, and uncertainty levels are unchanged (a "may" cannot become a "will")
- ✅ Scope qualifiers are unchanged ("some workplaces" cannot become "all workplaces")
- ✅ The output reads as natural, fluent, and appropriately styled for the target document type/audience
- ✅ Structural variation exists (sentence length, openings, discourse markers) where the original was repetitive or robotic
- ❌ It is **not** required, and never optimized for, that the output evade any specific AI-text detector

This definition is the constitution the rest of the project (skills, agents, guardians, evaluation) is built to enforce.

---

## Next Phase

**Phase 2 — Research the Space:** research questions (RQ1–RQ12+), literature review, competitor analysis, target users, and document types.

Say **"do phase 2"** (or "next phase") when ready, or **"store it"** if you want this phase saved/combined into the running project file now.
