# 09. AGENT ARCHITECTURE

The system is powered by a multi-agent swarm, managed by a LangGraph Supervisor. Each agent has a specific, narrow responsibility to reduce hallucination and ensure predictability.

## 1. Analysis Agents (The "Understand" Phase)
*   **RequestClassifierAgent:** Determines the user's intent (e.g., "Make this academic" vs "Make this a casual email").
*   **DocumentParserAgent:** Breaks raw text/PDFs into a structured hierarchy of sentences and paragraphs.
*   **StyleAgent:** Analyzes the input text for tone, formality, and readability.

## 2. Guardian Agents (The "Protect" Phase)
*   **FactGuardianAgent:** Uses strict extraction to find numbers, dates, and currency. Creates a locked ledger of facts.
*   **CitationGuardianAgent:** Uses regex/extraction to find academic references.
*   **TerminologyGuardianAgent:** Checks the text against the user's "Brand Voice" or "Do Not Touch" dictionary.

## 3. Planning & Cost Agents (The "Optimize" Phase)
*   **CostControllerAgent:** Looks at the user's credit balance and the document complexity to set a budget (e.g., `max_candidates=2`, `model=standard`).
*   **HumanizationPlannerAgent:** Decides *which* sentences need rewriting and which can be skipped (Selective Rewriting).
*   **ModelRouterAgent:** Physically selects the LLM provider for the specific node execution based on the Cost Controller's budget.

## 4. Generation Agents (The "Transform" Phase)
*   **CandidateGeneratorAgent:** Actually writes the new text. Can run 1-3 times in parallel depending on the budget to create A/B/C options.

## 5. Verification Agents (The "Critique" Phase)
*   **SemanticVerifierAgent:** Ensures the core meaning of the candidate matches the original.
*   **FactVerifierAgent:** Cross-references the generated text against the ledger created by the `FactGuardianAgent`.
*   **QualityCriticAgent:** The final judge. If any verifier fails, the Critic rejects the candidate.
*   **RevisionAgent:** If the Critic rejects the text, this agent takes the failure reason (e.g., "You dropped the $500 figure") and prompts the Generator to try again.

## 6. Finalization
*   **ExplanationAgent:** Generates the short 1-sentence reason for *why* the text was changed, which is shown in the UI.
