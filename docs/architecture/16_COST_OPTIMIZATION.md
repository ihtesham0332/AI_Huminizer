# 16. COST OPTIMIZATION (SELECTIVE REWRITING)

To maintain high gross margins while processing massive documents, the platform employs a strict Cost Optimization architecture.

## 1. The Selective Rewriting Engine
**Problem:** Sending a 10,000-word document through GPT-4o costs roughly $0.15 just in API fees. Most of those sentences are already well-written.
**Solution:** 
1.  The `HumanizationPlannerAgent` (using a fast Tier 1 model) scores every sentence in the document for "Need".
2.  Sentences scoring > 8/10 are passed straight through to the output (Cost: $0).
3.  Only sentences scoring < 8/10 are sent to the Generation Engine (Tier 2/3 models).
**Result:** API costs are reduced by 60-80% per document.

## 2. The Budget Controller
Every incoming API request is assigned a `budget` by the `CostControllerAgent` based on the user's subscription tier.
*   *Free User:* 1 Candidate, Tier 1 model, Max 1 Revision Loop.
*   *Pro User:* 2 Candidates, Tier 2 model, Max 3 Revision Loops.
*   *Deep Mode (Premium):* 3 Candidates, Tier 3 model, Max 3 Revision Loops, full Semantic Verification.

## 3. Prompt Compression
System prompts are aggressively optimized to minimize input tokens. Context is narrowed. The Grammar Agent does not need to see the entire document, only the surrounding paragraph.

## 4. Redis Caching
A hash of `[original_text + mode + user_dna_id]` is checked in Redis before any LLM call. If a user tries to rewrite the exact same sentence twice with the same settings, it returns instantly with zero API cost.
