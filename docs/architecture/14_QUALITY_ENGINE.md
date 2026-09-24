# 14. QUALITY ENGINE (THE CRITIC)

The Quality Engine acts as an independent judge, evaluating the output of the Generation Engine before it is shown to the user.

## 1. The Quality Gate
The Quality Gate is a decisive LangGraph node. It aggregates the results from the various Verifier Agents (Semantic, Fact, Citation, Grammar).
If the aggregate score is below the threshold, or if a hard constraint (Fact missing) is violated, the Gate closes.

## 2. Hard Failures (Triggers Revision)
*   `fact_changed = FAIL`
*   `citation_dropped = FAIL`
*   `protected_term_altered = FAIL`
*   `meaning_reversed = FAIL`

## 3. Soft Failures (Generates Warning)
*   `slightly_too_formal = WARN`
*   `readability_degraded = WARN`
*   `grammar_error_introduced = WARN`

## 4. Targeted Revision
If a Hard Failure occurs, the `QualityCriticAgent` generates a specific feedback prompt.
*   *Bad Prompt:* "Try again."
*   *Targeted Prompt:* "The previous attempt dropped the figure '$5M'. Rewrite the sentence again, ensuring all facts are preserved."

## 5. The Scorecard
When the text successfully passes the gate, the Quality Engine generates a final Scorecard JSON, which is displayed in the UI next to the Diff Viewer:
*   Semantic Preservation: 98%
*   Fact Integrity: 100%
*   Style Match: 92%
