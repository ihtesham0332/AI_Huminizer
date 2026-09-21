# HumanText Engine — Phase 3: Define "Natural Writing"

**Project:** HumanText Engine
**Phase:** 3 of 17 — Naturalness Framework + Linguistic Analysis
**Depends on:** Phase 1 (Problem Definition), Phase 2 (Research Questions)

---

## 3.1 Why "Human-Like" Is Not an Acceptable Definition

"Make it sound human-like" is not measurable, not testable, and not implementable as a target. It gives every downstream component (planner, rewrite engine, validators, evaluators) nothing concrete to check against. This phase replaces it with a set of **named, individually measurable dimensions**. Every later evaluation metric (Phase 10) and every validator agent (Phase 5/6) must map back to one or more of these dimensions — nothing is scored against a vague "naturalness feeling."

---

## 3.2 The Naturalness Dimension Set

| # | Dimension | Definition | How It's Measured (signal type) | Failure Looks Like |
|---|---|---|---|---|
| 1 | **Fluency** | Sentences are grammatically well-formed and read smoothly aloud | Grammar-error rate, LLM-judge fluency score | Awkward phrasing, garbled syntax |
| 2 | **Readability** | Text is appropriately easy or hard to read for its audience | Readability formulas (e.g., Flesch-Kincaid), avg sentence/word length | Needlessly dense or oversimplified for the audience |
| 3 | **Coherence** | Ideas follow a logical order; the argument/narrative makes sense as a whole | Discourse-structure analysis, LLM-judge coherence score | Ideas jump around, conclusions don't follow from setup |
| 4 | **Cohesion** | Sentences/paragraphs connect smoothly via appropriate linking devices | Discourse-marker analysis, pronoun/reference tracking | Choppy, disconnected sentences; missing transitions |
| 5 | **Lexical variation** | Vocabulary isn't repetitive; word choice varies appropriately | Type-token ratio, repeated-word/phrase detection | Same words/phrases repeated unnaturally often |
| 6 | **Sentence variation** | Sentence length/structure/openings vary appropriately rather than being uniform | Sentence-length variance, opener-word repetition rate | Every sentence is the same length or starts the same way |
| 7 | **Appropriate informality** | Casual register is used where the context calls for it | Contraction rate, informal-marker presence vs. document type | Text is stiffly formal in a casual context (or vice versa) |
| 8 | **Appropriate formality** | Formal register is used where the context calls for it | Formality-marker presence vs. document type | Slang/casual tone in an academic/business context |
| 9 | **Personal voice** | Text reflects a consistent, identifiable authorial perspective when one is requested (Writing DNA) | Style-similarity score against reference samples | Text reads generically, with no individual voice |
| 10 | **Contextual appropriateness** | Style, tone, and structure fit the stated document type and audience | Document-type-policy conformance check | An email reads like a research abstract, or vice versa |
| 11 | **Discourse quality** | Argument structure, causal/contrastive relations, and transitions are logically sound and clearly signposted | Discourse-marker appropriateness, logical-relation consistency | Contradictions or unclear cause/effect chains |
| 12 | **Semantic fidelity** | The rewrite communicates exactly the same claims, facts, modality, and scope as the original | NLI/entailment checks, fact-diff checks (Phase 7 Guardians) | Meaning drift, invented/altered facts, changed hedging |

**Governing rule:** dimension 12 (semantic fidelity) is a **hard constraint**, not a score to be traded off against the others. A rewrite that improves dimensions 1–11 while degrading dimension 12 is a failed rewrite by definition (see Phase 1, Rule 4). Dimensions 1–11 are optimized *within* the space of outputs that pass dimension 12, never instead of it.

---

## 3.3 Context-Dependence — Why More Variation Isn't Always "Better"

A common mistake is treating high lexical/sentence variation as an unconditional good. It is not. Naturalness is **context-relative**:

- A legal contract or technical spec is *supposed* to have repetitive, precise terminology — synonym-swapping a defined term ("the Licensee") for variety would harm accuracy, not naturalness.
- Short, choppy sentences are natural in a text message but unnatural in an academic essay.
- Passive voice is often flagged as "robotic," but it is the *correct, natural* choice in many scientific and procedural contexts ("the sample was heated to 80°C").

**Design consequence:** naturalness targets for each dimension must be parameterized by **document type and mode** (Phase 2.5 / Phase 8), not fixed globally. The system needs a per-document-type policy that defines acceptable ranges for sentence-length variance, formality, contraction rate, etc. — not one universal "natural" target vector.

---

## 3.4 Linguistic Analysis — Features Relevant to Robotic vs. Natural Text

This is the feature inventory the **Document Analysis**, **Style Analysis**, and **Readability Analysis** skills (Phase 4) are built to compute. These are the concrete, measurable signals that feed the naturalness dimensions above.

| Feature | What It Captures | Typical "Robotic" Pattern | Typical "Natural" Pattern |
|---|---|---|---|
| Sentence length | Words per sentence | Uniform length across the whole document | Mix of short and long sentences |
| Clause depth | Syntactic complexity per sentence | Either uniformly simple or uniformly over-nested | Varies with content complexity |
| Vocabulary frequency | Common vs. rare word usage | Overuse of a narrow set of "safe" words/transitions ("Moreover," "Furthermore," "In conclusion") | Broader, context-appropriate vocabulary |
| Lexical diversity | Type-token ratio across the document | Low diversity, repeated phrasing | Higher diversity appropriate to length/genre |
| Repetition | Repeated words, phrases, or sentence templates | Same structural template reused sentence after sentence | Varied structures |
| Transition/discourse-marker frequency | Rate of words like "however," "therefore," "additionally" | Overused, mechanically inserted at every paragraph | Used only where a real logical relation exists |
| Punctuation patterns | Variety and appropriateness of punctuation | Minimal punctuation variety (only periods/commas) | Natural use of dashes, semicolons, question marks where fitting |
| Active/passive voice ratio | Balance of voice | Either all-active or all-passive regardless of context | Ratio matches genre convention (e.g., passive is fine in methods sections) |
| Nominalization rate | Turning verbs into abstract nouns ("utilization" vs. "use") | High nominalization, inflating simple ideas | Verbs used directly where natural |
| Hedging/qualifier density | Frequency of "may," "could," "it is possible that" | Either absent (overclaiming) or excessive/uniform (formulaic hedging) | Matches the actual evidentiary strength of the claim |
| Excessive formality | Overly stiff phrasing regardless of context | "Utilize" instead of "use," "in order to" instead of "to," everywhere | Formality matched to document type |
| Sentence openings | Variety of how sentences begin | Repeated openers ("This," "Additionally," "It is important to note") | Openers vary naturally |
| Paragraph length | Words/sentences per paragraph | Uniform paragraph length throughout | Varies with idea density |
| Pronoun usage | Use of "I," "we," "you," "it" | Impersonal/avoidant ("It can be seen that...") when a direct voice fits | Direct pronoun use where genre allows |
| Rhetorical structure | How claims, evidence, and conclusions are organized | Formulaic templates (claim → generic support → generic conclusion, repeated identically) | Structure adapts to the actual content |

**Important caveat carried over from Phase 3.3:** none of these features has a single "correct" target value — each is evaluated *relative to the document type's expected range*, not against a universal robotic/natural threshold.

---

## 3.5 How This Feeds the Rest of the Project

- **Phase 4 (Skills):** Document Analysis, Style Analysis, and Readability Analysis skills compute the Section 3.4 features directly.
- **Phase 5/6 (Agents/Graph):** the Style Critic and Naturalness Evaluation agents score outputs against the Section 3.2 dimension set, parameterized by document type.
- **Phase 7 (Guardians):** Semantic Fidelity (dimension 12) is enforced by the Semantic Guardian and Fact Guardian as a hard gate, separate from the "soft" style dimensions.
- **Phase 8 (Rewrite Modes):** each of the 8 rewrite modes defines a target range for the Section 3.4 features (e.g., Academic Natural mode expects higher formality and lower contraction rate than Conversational mode).
- **Phase 10 (Evaluation):** every automated/human/LLM-judge metric in the evaluation framework must be traceable to one of the 12 dimensions above — no metric is added "because it's easy to compute" without a mapped dimension.

---

## Next Phase

**Phase 4 — Design the Skills Catalog:** all 20 deterministic/LLM skills, each with purpose, inputs, outputs, implementation approach, and failure modes.

Say **"do phase 4"** / **"next phase"** to continue, or **"store it"** to save/combine what's been produced so far.
