from typing import TypedDict, List, Optional, Dict, Any

class HumanizationState(TypedDict):
    original_text: str
    metadata: Dict[str, Any]             # From Input Analyzer
    protected_tokens: List[str]          # From Fact & Citation Guardians
    style_profile: Dict[str, Any]        # Style configuration
    strength: str                        # "light", "medium", or "aggressive"
    rewrite_plan: Dict[str, Any]         # From Humanization Planner
    candidates: List[str]                # From Candidate Generator
    evaluations: List[Dict[str, Any]]    # From Quality Critic
    best_candidate: Optional[str]
    iteration_count: int
    final_output: str
    change_summary: str
