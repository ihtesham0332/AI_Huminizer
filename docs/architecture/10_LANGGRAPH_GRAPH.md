# 10. LANGGRAPH GRAPH

This defines the exact state machine and node transitions for the core LangGraph workflow.

## State Schema
```python
class HumanizerState(TypedDict):
    original_text: str
    mode: str
    budget: dict
    facts: list
    citations: list
    style_profile: dict
    candidates: list
    final_output: str
    quality_report: dict
    revision_count: int
```

## Node Execution Flow

```text
START
  │
  ▼
[DocumentParserNode]
  │
  ▼
[Parallel Analysis & Protection]
  ├── [StyleAnalyzerNode]
  ├── [FactGuardianNode]
  └── [CitationGuardianNode]
  │
  ▼
[CostControllerNode]
  │
  ▼
[ModelRouterNode]
  │
  ▼
[GenerationNode] (Creates Candidates)
  │
  ▼
[Parallel Verification]
  ├── [FactVerifierNode]
  ├── [SemanticVerifierNode]
  └── [CitationVerifierNode]
  │
  ▼
[QualityCriticNode]
  │
  ├──► IF "FAIL" AND revision_count < MAX
  │      │
  │      ▼
  │    [RevisionNode] ──► (Back to GenerationNode)
  │
  └──► IF "PASS" OR revision_count == MAX
         │
         ▼
       [ExplanationNode]
         │
         ▼
        END
```

## Critical Edges
1.  **Conditional Routing at Quality Critic:** The loop between `QualityCriticNode` -> `RevisionNode` -> `GenerationNode` is the defining feature of our Integrity Engine. It forces the LLM to fix its own mistakes regarding facts/citations.
2.  **Parallel Execution:** The Analysis nodes and Verification nodes must be executed in parallel branches to maintain low latency.
