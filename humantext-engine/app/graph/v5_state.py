from typing import TypedDict, List, Dict, Any, Optional

class HumanizerState(TypedDict):
    """
    The core state object that gets passed around the LangGraph nodes.
    Defined in ULTIMATE MASTER PROMPT - 10. LANGGRAPH GRAPH.
    """
    original_text: str
    mode: str # fast, balanced, deep
    length: str # maintain, condense, expand
    profile_instructions: Optional[str]
    budget: Dict[str, Any]
    facts: List[Dict[str, str]]
    citations: List[Dict[str, str]]
    style_profile: Dict[str, Any]
    candidates: List[str]
    final_output: Optional[str]
    quality_report: Dict[str, Any]
    revision_count: int
