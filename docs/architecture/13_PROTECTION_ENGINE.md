# 13. PROTECTION ENGINE (THE GUARDIANS)

The Protection Engine is the core technical differentiator of this platform. It guarantees that critical information is never altered by the generative LLM.

## 1. Fact Guardian
*   **Target:** Numbers, Dates, Currency, Percentages, Proper Nouns.
*   **Mechanism:** Uses fast regex and `spaCy` NER (Named Entity Recognition) to extract values.
*   **Ledger Example:** 
    *   Sentence: "Revenue grew 15% in Q3 2026."
    *   Extracted Facts: `["15%", "Q3", "2026"]`

## 2. Citation Guardian
*   **Target:** APA, MLA, IEEE in-text citations.
*   **Mechanism:** Regex patterns to match standard citation formats `(Author, Year)` or `[Number]`.
*   **Ledger Example:**
    *   Sentence: "This was proven by Smith et al. (2024)."
    *   Extracted Citations: `["Smith et al. (2024)"]`

## 3. Terminology Guardian
*   **Target:** User-defined glossary terms, Brand names.
*   **Mechanism:** Exact string matching (case-sensitive or insensitive based on settings).

## 4. Verification Loop
The extracted ledgers are passed forward to the `FactVerifierAgent` and `CitationVerifierAgent` in the Quality Phase. 
The LLM output is scanned. If ANY item from the original ledger is missing in the LLM output, the Verifier returns a `FAIL` signal, triggering the Revision Loop.

## 5. Logic Preservation (P2)
Future iterations will include contradiction detection, ensuring the LLM doesn't change "The model did not increase accuracy" to "The model increased accuracy".
