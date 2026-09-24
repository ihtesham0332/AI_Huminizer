# LangGraph Workflow
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document defines the stateful execution graph that powers the multi-agent system.

## 1. The State Schema
The LangGraph `State` object acts as the central memory for a single job.
```python
class HumanizationState(TypedDict):
    original_text: str
    metadata: dict              # From Input Analyzer
    protected_tokens: dict      # From Guardians
    style_profile: dict         # From Style Analyzer
    rewrite_plan: dict          # From Humanization Planner
    candidates: List[str]       # From Candidate Generator
    evaluations: List[dict]     # From Evaluators
    best_candidate: str
    iteration_count: int
    final_output: str
    change_summary: str
```

## 2. Graph Nodes & Edges

### Phase A: Ingestion (Sequential)
1.  **Node `analyze_input`**: Executes Input, Language, and Style analyzers.
2.  **Node `run_guardians`**: Executes Fact, Citation, and Tech-Term guardians. Populates `protected_tokens`.
3.  **Node `create_plan`**: Generates the strategic `rewrite_plan`.

### Phase B: Generation (Parallel)
4.  **Node `generate_candidates`**: Spawns 3 LLM calls in parallel to generate `Candidate A`, `Candidate B`, and `Candidate C`.

### Phase C: Evaluation (Parallel)
5.  **Node `evaluate_candidates`**: For each candidate, parallel branches execute:
    *   `SemanticCheck`
    *   `FactCheck`
    *   `GrammarCheck`
    *   `StyleCheck`

### Phase D: Critique & Routing (Conditional Edge)
6.  **Node `quality_critic`**: Reviews all evaluations. 
    *   *Condition:* If at least one candidate passes all critical Quality Gates -> **Route to `finalize`**.
    *   *Condition:* If all candidates fail AND `iteration_count < 3` -> Increment count, update `rewrite_plan` with critique feedback, **Route back to `generate_candidates`**.
    *   *Condition:* If all candidates fail AND `iteration_count == 3` -> **Route to `finalize`** with the least-flawed candidate and a warning flag.

### Phase E: Finalization
7.  **Node `finalize`**: Executes `Finalizer` and `Change Explanation Agent`. Sets `final_output`.
8.  **END**
