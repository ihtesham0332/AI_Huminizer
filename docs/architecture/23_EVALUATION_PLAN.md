# 23. EVALUATION PLAN

Our core product metric is NOT an "AI Detection Bypass Score". Our North Star is **Accepted Quality Improvements**.

## 1. Golden Dataset
We will curate a dataset of 500 paragraphs split across:
*   Academic (Heavily cited, formal)
*   Technical (Code snippets, specific jargon)
*   Business (Emails, reports, metrics)
*   Creative (Blogs, marketing)

## 2. Automated Metrics
Every time we change an LLM prompt or upgrade a model, we run the Golden Dataset through the pipeline and measure:
*   **Semantic Preservation Rate:** (Target > 95%) Measured by semantic similarity embeddings.
*   **Fact Preservation Rate:** (Target 100%) Measured by the FactGuardian comparing input/output integers and dates.
*   **Citation Preservation Rate:** (Target 100%)
*   **Cost Efficiency:** (Target < $0.05 per 1k words).

## 3. Human Blind Testing
A/B testing where human reviewers are presented with outputs from WriteHuman, Undetectable, and HumanText (Our Platform). They rate them on:
1.  Naturalness
2.  Preservation of the original meaning.
