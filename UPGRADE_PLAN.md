# Upgrade Plan (v4.0 Enterprise Transition)

Based on the 54-point Master Prompt, here is the high-level roadmap to transition to v4.0:

## Phase A: Infrastructure & Database Evolution
1.  Stand up **Redis** in `docker-compose.yml` for caching and rate limiting.
2.  Expand **PostgreSQL** schema to support `Document`, `UsageRecord`, `Feedback`, and `CostRecord`.
3.  Implement the **Model Router** abstraction to easily swap between Local, OpenAI, and Anthropic.

## Phase B: Intelligence Engines (The Brains)
4.  Build the **Document Intelligence Engine** (PDF/DOCX parsing).
5.  Build the **Language & Content Classifiers**.
6.  Build the **Style Intelligence Engine** (Formality, Readability metrics).

## Phase C: Targeted Transformation (Cost Savings)
7.  Implement **Selective Humanization** (only send flagged sentences to the LLM).
8.  Implement **Targeted Revision** (if a fact changes, rewrite *only* that sentence, not the whole document).

## Phase D: Advanced Guardians
9.  Enhance the **Fact & Citation Guardians** to output structured JSON blocking policies.
10. Implement the **Quality Critic** engine for final pass/fail decisions.

## Phase E: Dashboard & API Polish
11. Update the Next.js UI to include the advanced **Quality Dashboard** and detailed **Diff Views**.
12. Implement the **Internal Credit System** for Stripe billing.
