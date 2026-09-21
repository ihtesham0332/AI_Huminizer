# HumanText Engine — Phase 2: Research the Space

**Project:** HumanText Engine
**Phase:** 2 of 17 — Research Questions, Literature Review, Competitor Analysis, Target Users, Document Types
**Depends on:** Phase 1 (Problem Definition)

---

## 2.1 Research Question Framework

Each RQ below is tagged by type so later phases know what kind of evidence answers it (experiment, literature, or engineering benchmark).

| ID | Research Question | Answered By |
|---|---|---|
| RQ1 | What linguistic features make generated text read as robotic or unnatural (sentence-length uniformity, repeated openers, discourse-marker density, nominalization, hedging patterns)? | Literature + corpus analysis (Phase 3/9) |
| RQ2 | Which transformation techniques (splitting, merging, reordering, lexical substitution, discourse-marker variation) most improve perceived naturalness? | Ablation experiments (Phase 15) |
| RQ3 | How can semantic meaning be preserved during aggressive rewriting? | Semantic Guardian design + NLI/entailment checks (Phase 7) |
| RQ4 | How can factual consistency (numbers, names, dates, entities, citations) be verified automatically? | Fact Guardian design (Phase 7) |
| RQ5 | How can a system learn an individual's writing style from a small sample set without copying phrases verbatim? | Writing DNA design (Phase 7) |
| RQ6 | Does a multi-agent architecture provide measurable quality gains over single-pass LLM rewriting? | Baseline comparison B vs F (Phase 10) |
| RQ7 | Does explicit planning before generation improve output quality vs. direct rewrite? | Ablation: planner on/off (Phase 15) |
| RQ8 | Does iterative critique-and-revision reduce semantic drift and factual errors? | Ablation: revision loop on/off (Phase 15) |
| RQ9 | Which models offer the best quality/cost/latency tradeoff for each subtask (analysis, rewrite, validation)? | Model benchmark (Phase 9) |
| RQ10 | Which automated metrics (BERTScore, NLI-based factuality, readability indices, LLM-judge scores) actually correlate with human quality judgments? | Human eval correlation study (Phase 10) |
| RQ11 | What are the known failure modes and limitations of current AI-text detectors (false positive/negative rates, domain sensitivity, length sensitivity)? | Literature review (this phase) + Detector research (Phase 10) |
| RQ12 | How should "naturalness" be evaluated as a writing-quality construct, independent of any single detector's score? | Naturalness framework (Phase 3) |
| RQ13 *(added)* | Does parallelizing independent analysis/validation agents reduce latency without harming quality vs. running them sequentially? | Concurrency experiment (Phase 6/15) |
| RQ14 *(added)* | What is the minimum agent count that captures most of the achievable quality gain (diminishing returns curve)? | Ablation study (Phase 15) |
| RQ15 *(added)* | What privacy risks does a persistent "Writing DNA" style profile introduce, and how should it be minimized/anonymized? | Privacy analysis (Phase 11) |

**Note on RQ11/Detector research:** this project studies detectors only as an *external measurement instrument* — the way a thermometer measures temperature without being the thing being optimized. See Rule enforced throughout: detector-avoidance is never a training or evaluation target.

---

## 2.2 Literature Review — Methodology and Seed Bibliography

**Methodology (must be followed once real research begins, not skipped):**
1. Search academic databases (ACL Anthology, arXiv cs.CL, Google Scholar, Semantic Scholar) for each RQ above.
2. Prefer peer-reviewed venues (ACL, EMNLP, NAACL, TACL) over preprints where possible; treat arXiv preprints as lower-confidence until verified.
3. For every source actually used in the final report, verify title/authors/year/venue/URL directly before citing — **never carry forward a citation from memory without verification.**
4. Record disagreements between sources explicitly rather than picking one silently.

**Seed research areas** (topics to search, not yet verified citations — each must be looked up and confirmed before appearing in the Phase 16 literature table):

| Area | What to search for | Why it matters here |
|---|---|---|
| Paraphrase generation & controlled paraphrasing | quality-controlled paraphrase generation, diverse paraphrasing models | Core technique for Rewrite Engine |
| Text style transfer | formality transfer, authorship style transfer, disentangled style/content representations | Style Analyst + Rewrite Engine design |
| Semantic similarity / entailment | sentence embeddings, natural language inference (NLI) as a consistency check | Semantic Guardian's core verification method |
| Factual consistency & hallucination detection | summarization factual-consistency metrics, hallucination detection in generated text | Fact Guardian design |
| Self-critique / iterative refinement in LLMs | self-refine loops, reflection-based revision | Justifies (or disproves) the Revision Agent |
| LLM-as-a-judge | using LLMs to score generated text against human preference | Quality Judge + evaluation framework |
| Multi-agent LLM systems | agentic workflows, tool-using agents, orchestration frameworks | Justifies (or disproves) the multi-agent architecture itself |
| Authorship attribution / stylometry | quantifiable stylistic fingerprinting features | Writing DNA feature design |
| Readability & discourse coherence metrics | readability formulas, coherence/cohesion measurement | Readability Analysis skill |
| AI-generated text detection | detector methodology, known false-positive/negative rates, robustness to paraphrase | RQ11, detector research (external eval only) |

**Literature table template** (to be populated during actual research, one row per verified source):

| Title | Authors | Year | Venue | URL/DOI | RQ Addressed | Method | Key Finding | Limitation | Relevance | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| *(fill during literature pass — do not invent entries)* | | | | | | | | | | |

Classify each populated row as: **foundational / highly relevant / supporting / controversial / outdated / engineering reference.**

---

## 2.3 Competitor Analysis

**Important caveat before reading this table:** the AI-humanizer market is heavily marketed with vendor-claimed "detection bypass rates" (e.g., "98% bypass," "100% human score"). These numbers come from vendor blogs and marketing comparison sites, are **not independently verified, not peer-reviewed, and are excluded from this project as evidence.** They are listed only so the gap analysis below is grounded in what's actually being sold — not as benchmarks HumanText Engine should chase.

| Product | Category | Known Features | Style/Tone Control | Personalization | API | Privacy Info | Pricing Model | Notable Limitation |
|---|---|---|---|---|---|---|---|---|
| QuillBot | Paraphraser + light humanizer | Multiple paraphrase modes (Standard, Fluency, Formal, Creative, etc.), grammar check, built-in AI detector | Mode-based, not personalized | None (no per-user style memory) | Yes (paid tiers) | Standard SaaS ToS | Freemium, ~$8–10/mo | Vendor's own comparisons note it does shallow, not deep structural, rewriting |
| Grammarly | Writing assistant | Grammar/clarity correction, tone detector, generative rewrite suggestions | Tone presets | Limited ("brand voice" for teams) | Yes (enterprise) | Enterprise-grade, SOC2 | Freemium/subscription | Optimized for correctness/clarity, not deep humanization |
| Wordtune | Rewrite/paraphrase assistant | Sentence-level rewrite suggestions, tone shift | Tone presets | None | Limited | Standard SaaS | Freemium/subscription | Sentence-level only; no document-level planning or fact-checking |
| Dedicated "AI humanizer" tools (Undetectable AI, GPTHumanizer-style products, and similar) | Detector-evasion focused | Bulk rewriting, "bypass rate" scoring against named detectors, multiple "modes" | Some tone/mode options | Rare | Some | Inconsistent/unclear | Marketing-stated bypass rates | Explicitly optimize for detector evasion; no published semantic/factual preservation guarantees; no independent quality evaluation |
| Originality.ai / GPTZero / Copyleaks / Turnitin's AI detector | AI-text **detectors** (not humanizers) | Classify text as AI vs. human-written | N/A | N/A | Yes (some) | Varies | Subscription | Published research shows detectors have real false-positive/negative rates and are sensitive to paraphrasing, domain, and text length — relevant to RQ11, not a humanization tool |

### Feature Gap
No reviewed competitor publishes a **semantic-preservation guarantee** or a **fact-consistency check** as a first-class, measurable feature. Rewriting is treated as a black box.

### Research Gap
None of the reviewed products publish methodology, evaluation datasets, or human-evaluation studies. "Bypass rate" and "human score" numbers are unverifiable marketing metrics, not research-grade evaluation.

### Engineering Gap
No visible planning stage, no multi-stage validation, no user-controllable modes tied to *document type* (academic vs. business vs. email) rather than generic "tones."

### Opportunity for HumanText Engine
1. Make semantic/factual preservation a *verifiable, reported* property, not an assumption.
2. Publish an evaluation methodology (human eval + LLM-judge + automated metrics) instead of vendor-claimed detector-bypass percentages.
3. Support per-document-type transformation policies (Phase 8) rather than one-size-fits-all "tone" sliders.
4. Offer genuine personalization (Writing DNA) rather than static tone presets.

---

## 2.4 Target Users

| User | Problem | Expected Input | Desired Output | Style Requirements | Privacy Requirements | Evaluation Criteria |
|---|---|---|---|---|---|---|
| **Students** | Draft reads stiff/AI-flavored, worried about academic-integrity flags | Essay/report draft | Natural academic prose, same argument/citations | Academic register, no informal slang | High — no long-term retention of submitted essays | Meaning preserved, no invented citations, natural readability |
| **Researchers** | Need clear, natural prose without altering findings/numbers | Paper section, abstract | Publication-quality technical writing | Technical, precise, hedge-preserving | High — confidentiality of unpublished results | Zero factual/numeric drift, terminology preserved |
| **Engineers/technical writers** | Docs read like generated boilerplate | READMEs, specs, technical docs | Clear, natural technical writing | Technical, concise | Medium | Terminology preserved, structure logical |
| **Marketers/content writers** | Generic-sounding AI copy | Blog posts, ad copy | Engaging, on-brand natural copy | Brand voice, conversational | Medium | Naturalness, engagement, brand-tone match |
| **Business professionals** | Emails/reports sound robotic or overly formal | Emails, memos, reports | Professional but natural tone | Business-appropriate, respectful | Medium-high (may contain confidential business info) | Tone appropriateness, clarity, no info leakage |
| **Organizations (teams)** | Need consistent natural voice across many authors/documents | Bulk documents | Consistent natural style at scale | Org-wide style guide + individual Writing DNA option | High — multi-tenant isolation required | Consistency, throughput, cost per document |

**Explicit design consequence:** the system must support *per-user-type transformation policies* (Phase 8) — a single "humanize" button with one fixed strategy is insufficient, since a researcher's fidelity requirements (near-zero tolerance for hedging changes) differ sharply from a marketer's (tone/engagement over precision).

---

## 2.5 Document Types

| Document Type | Distinct Transformation Needs |
|---|---|
| Academic | Preserve hedging/modality exactly; formal register; citation format untouched |
| Technical | Preserve terminology and precision; avoid "simplifying away" technical accuracy |
| Business/professional | Natural but respectful tone; preserve action items, dates, figures exactly |
| Email | Shorter sentences, natural greeting/sign-off conventions, tone-sensitive |
| Report | Structured, natural narrative flow; preserve data points and figures exactly |
| Blog | More stylistic freedom, higher lexical variation allowed |
| Social media | Very short-form, high informality tolerance, platform-length constraints |
| Essay | Balance natural voice with argument structure preservation |
| Casual | Highest tolerance for colloquialism, contractions, informal discourse markers |
| Creative | Style transformation is central; factual constraints mostly relaxed except stated facts |

**Conclusion:** each document type requires a distinct **transformation policy** (allowed operations, allowed formality range, strictness of the Fact/Semantic Guardians). This directly motivates the "Mode" system in Phase 8 (Rewrite Engine) — a single global rewriting strategy cannot serve academic and social-media text with the same rules.

---

## Next Phase

**Phase 3 — Define "Natural Writing":** measurable naturalness dimensions (fluency, cohesion, lexical variation, etc.) and linguistic pattern research (sentence length, hedging, passive voice, discourse markers).

Say **"do phase 3"** / **"next phase"** to continue, or **"store it"** to save/combine what's been produced so far.
