# 03. COMPETITOR GAP ANALYSIS

This document analyzes the specific failures and gaps in existing writing tools and how our Agentic Architecture will solve them.

| Feature | Competitor | Evidence | Current implementation | User value | Observed limitation | Severity | Our proposed solution | Est. Eng. Complexity | Est. AI Cost | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Meaning Drift** | StealthWriter | User Reviews | Brute-force synonym swapping | High | Changes logic, numbers, negations | CRITICAL | **Fact & Logic Guardians** validating output pre-delivery | High | Medium | P0 |
| **Generic Voice** | Phrasly / WriteHuman | Output testing | Uses generic "make it casual" prompts | High | Sounds like a different generic AI | HIGH | **Personal Writing DNA** extraction and style mapping | Very High | High | P1 |
| **Weak Explanation** | Undetectable AI | Product UX | Outputs text with no diff/reason | Medium | User must manually read both versions to spot errors | HIGH | **Explainability Engine & Diff Viewer** | Medium | Low | P1 |
| **Over-Processing** | ChatGPT / Quillbot | Architecture | Sends entire doc through LLM | Medium | Destroys good sentences, wastes compute | CRITICAL | **Selective Rewriting Engine** (only process bad sentences) | High | Very Low (Saves $) | P0 |
| **Cost / Economics** | All | Pricing Pages | Fixed word bundles | Low | High API costs for vendor, rigid limits for user | HIGH | **Cost-Aware Model Router** (uses cheap models for simple tasks) | High | Very Low (Saves $) | P0 |
| **Consistency** | All | Output testing | Paragraphs drift in tone | High | Chapter 5 tone differs from Chapter 1 | HIGH | **Document Intelligence Engine** (global state memory) | Medium | Low | P1 |

### Deep Dive: Gap A - Meaning Drift
*   **The Problem:** When instructed to "humanize" or "paraphrase", LLMs will frequently change `$500` to `five hundred dollars` (acceptable) or worse, `$50` or `a large sum of money` (unacceptable). They will also drop crucial academic citations.
*   **The Solution:** Our `EnhancedFactGuardian` explicitly extracts `[numbers, dates, citations, entities]` using fast regex/NER *before* the LLM call, and explicitly checks that they exist in the LLM output *after* the call. If they are missing, a `TargetedRevisionAgent` is fired.
