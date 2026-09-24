# 04. USER PROBLEMS

Our platform is being built to solve the following acute user problems that existing software fails to address.

## 1. "The AI destroyed my research data." (Factual Integrity)
**Persona:** Researchers, Students, Data Analysts, Financial Writers.
**Problem:** They paste a data-heavy report into an AI paraphraser to improve readability. The AI changes "decreased by 15%" to "significantly increased", ruining the document.
**Our Solution:** The *Fact Guardian* and *Numerical Integrity Engine* hard-lock statistics.

## 2. "It sounds like a teenager wrote it, not me." (Voice Mismatch)
**Persona:** Executives, Marketers, Authors.
**Problem:** Generic "humanizers" use colloquialisms (e.g., "dive in," "in today's fast-paced world," "moreover") that do not match the user's actual professional tone.
**Our Solution:** *Personal Writing DNA*. The system ingests 5 previous emails/reports from the user and maps their exact vocabulary, sentence length, and transition preferences.

## 3. "I lost all my academic citations." (Formatting Destruction)
**Persona:** Academics, PhD Students.
**Problem:** Current AI tools cannot distinguish between natural language and a `[Smith et al., 2023]` citation. They frequently delete or hallucinate citations during rewriting.
**Our Solution:** The *Citation Guardian* parses APA/MLA/IEEE formats, locks them, and re-inserts them post-generation.

## 4. "It costs too much to rewrite my 30,000-word thesis." (Cost & Over-processing)
**Persona:** Authors, Graduate Students.
**Problem:** Passing a 30,000-word document through GPT-4 or Claude Opus is extremely expensive. Most of the document is already well-written.
**Our Solution:** *Selective Rewriting Engine* + *Model Router*. We use a cheap, fast model to identify the 15% of sentences that actually need rewriting, and only send those to the expensive models, reducing costs by up to 85%.

## 5. "I don't know what it changed or why." (Lack of Explainability)
**Persona:** Editors, Compliance Officers.
**Problem:** Black-box outputs force users to do a manual diff to see what changed, creating anxiety about semantic drift.
**Our Solution:** *Explainability Engine*. A clean UI showing a side-by-side Diff, highlighting changes and providing a 1-sentence rationale (e.g., "Simplified complex passive voice").
