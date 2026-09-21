from typing import Dict, Any, TypedDict, List, Optional
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    # Fallback mock for testing environment if langgraph is missing
    class StateGraph:
        def __init__(self, state_schema): pass
        def add_node(self, name, node): pass
        def add_edge(self, source, target): pass
        def set_entry_point(self, name): pass
        def add_conditional_edges(self, source, condition, mapping): pass
        def compile(self): return self
        def invoke(self, state): return state
    END = "__end__"

from app.graph.nodes import (
    input_validator_node, document_analyst_node, semantic_analyst_node,
    style_analyst_node, context_analyst_node, planner_node,
    rewriter_node, semantic_validator_node, fact_validator_node,
    style_critic_node, quality_judge_node, revision_agent_node
)

# Using TypedDict for LangGraph compatibility with our Pydantic StateSchema fields
class GraphState(TypedDict, total=False):
    request_id: str
    original_text: str
    document_type: str
    target_mode: str
    target_tone: Optional[str]
    status: str
    
    document_analysis: Dict[str, Any]
    semantic_analysis: Dict[str, Any]
    style_analysis: Dict[str, Any]
    context_analysis: Dict[str, Any]
    readability_analysis: Dict[str, Any]
    
    claims: List[Dict[str, Any]]
    facts: Dict[str, Any]
    entities: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]
    
    transformation_plan: Dict[str, Any]
    rewritten_text: Optional[str]
    
    semantic_score: Optional[float]
    factual_score: Optional[float]
    style_score: Optional[float]
    readability_score: Optional[float]
    naturalness_score: Optional[float]
    quality_score: Optional[float]
    
    validation_errors: List[str]
    revision_count: int
    revision_history: List[Dict[str, Any]]
    
    agent_metadata: Dict[str, Any]

def route_after_validation(state: GraphState) -> str:
    """Routes based on input validation."""
    if state.get("status") == "failed":
        return END
    return "analyze"

def route_after_judgment(state: GraphState) -> str:
    """Routes based on quality score and revision limits."""
    if state.get("status") == "completed":
        return END
    if state.get("revision_count", 0) >= 3: # MAX_REVISIONS
        state["status"] = "completed_with_warnings"
        return END
    return "revise"

def build_graph():
    """Builds the LangGraph orchestration workflow."""
    workflow = StateGraph(GraphState)
    
    # 1. Validation
    workflow.add_node("validate_input", input_validator_node)
    
    # 2. Parallel Analysis (Mocked as sequential due to pure functional setup here, 
    # but logically these form the 'analyze' stage)
    def parallel_analysis(state: GraphState):
        state.update(document_analyst_node(state))
        state.update(semantic_analyst_node(state))
        state.update(style_analyst_node(state))
        state.update(context_analyst_node(state))
        return state
        
    workflow.add_node("analyze", parallel_analysis)
    
    # 3. Planning & Rewriting
    workflow.add_node("plan", planner_node)
    workflow.add_node("rewrite", rewriter_node)
    
    # 4. Parallel Validation
    def parallel_validation(state: GraphState):
        state.update(semantic_validator_node(state))
        state.update(fact_validator_node(state))
        state.update(style_critic_node(state))
        return state
        
    workflow.add_node("validate_output", parallel_validation)
    
    # 5. Judgment & Revision
    workflow.add_node("judge", quality_judge_node)
    workflow.add_node("revise", revision_agent_node)
    
    # Build Edges
    workflow.set_entry_point("validate_input")
    workflow.add_conditional_edges("validate_input", route_after_validation, {"analyze": "analyze", END: END})
    workflow.add_edge("analyze", "plan")
    workflow.add_edge("plan", "rewrite")
    workflow.add_edge("rewrite", "validate_output")
    workflow.add_edge("validate_output", "judge")
    
    workflow.add_conditional_edges(
        "judge", 
        route_after_judgment, 
        {END: END, "revise": "revise"}
    )
    workflow.add_edge("revise", "plan") # Loop back to planner
    
    return workflow.compile()

app_graph = build_graph()
