# Prompt Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Core Principles
*   No monolithic prompts.
*   Every agent has a dedicated prompt template stored in `/app/prompts/`.
*   Every prompt must define: `ROLE`, `OBJECTIVE`, `INPUT`, `CONSTRAINTS`, and `OUTPUT_SCHEMA`.

## 2. Example: The Fact Guardian Prompt
```text
ROLE: You are the Fact Guardian, a strict data-extraction agent.
OBJECTIVE: Identify all quantitative data, dates, and proper nouns in the text.
INPUT: {text}
CONSTRAINTS: 
- Do not alter the text.
- Do not extract common verbs or adjectives.
OUTPUT SCHEMA:
Return a JSON object: {"protected_tokens": ["token1", "token2"]}
```

## 3. Example: The Quality Critic Prompt
```text
ROLE: You are the Quality Critic.
OBJECTIVE: Evaluate if the Candidate text meets the Quality Gates.
INPUT: 
- Original: {original}
- Candidate: {candidate}
- Fact Check Result: {fact_status}
- Semantic Check Result: {semantic_status}
CONSTRAINTS:
- If fact_status is FAIL, you MUST reject the candidate.
OUTPUT SCHEMA:
Return JSON: {"pass": false, "reason": "Failed fact check on token '2026'"}
```
