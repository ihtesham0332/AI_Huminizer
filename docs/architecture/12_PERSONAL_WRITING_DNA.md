# 12. PERSONAL WRITING DNA ENGINE

This engine extracts the user's personal stylistic fingerprint, preventing the output from sounding like generic AI text.

## 1. Data Ingestion
The user uploads 3 to 5 examples of their past writing (e.g., previous essays, emails, or blog posts). 
The system stores this as a raw "Corpus" for the user.

## 2. Extraction Vector
The `StyleAnalyzerAgent` runs over the corpus to extract the following vectors:
1.  **Vocabulary Profile:** Over-indexed words (e.g., does the user prefer "utilize" or "use"? "Therefore" or "So"?).
2.  **Sentence Length Distribution:** (e.g., 20% short, 60% medium, 20% long).
3.  **Syntactic Patterns:** Average clauses per sentence, use of passive vs. active voice.
4.  **Formality Level:** Measured from 1 (Casual) to 10 (Academic).
5.  **Punctuation Habits:** Frequency of em-dashes, semicolons, exclamation marks.

## 3. Storage
The DNA Profile is stored in PostgreSQL as a structured JSON object, tied to the `user_id`.
Users can have multiple profiles (e.g., `dna_academic`, `dna_marketing`).

## 4. Application
During the `GenerationNode` phase, the LLM prompt is dynamically injected with the user's DNA:
> *System: Write the following text. You must adopt the following style constraints:*
> *- Formality: 7/10*
> *- Preferred transitions: "Furthermore", "However"*
> *- Max sentence length: 25 words*
> *- Voice: Active, slightly academic*

## 5. Feedback Loop
If a user consistently manually edits the AI output to remove a specific word (e.g., "delve"), the Feedback Engine updates the DNA Profile's "Avoided Words" list automatically.
