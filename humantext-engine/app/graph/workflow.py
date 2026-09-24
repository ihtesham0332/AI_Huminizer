from langgraph.graph import StateGraph, END
from app.graph.state import HumanizationState
from app.agents.input_analyzer import analyze_input_text
from app.guardians.fact_guardian import fact_guardian_node
from app.guardians.citation_guardian import citation_guardian_node
from app.agents.humanization_planner import plan_humanization_node
from app.agents.humanizer import humanizer_node
from app.agents.evaluators.quality_critic import quality_critic_node

def analyze_input_node(state: dict) -> dict:
    """Wrapper to run the Input Analyzer and store in metadata."""
    res = analyze_input_text(state["original_text"])
    return {"metadata": res.model_dump(), "iteration_count": state.get("iteration_count", 0)}

def evaluate_and_route(state: dict) -> str:
    """
    Conditional edge logic based on Quality Critic results.
    """
    if state.get("best_candidate"):
        return "finalize"
    
    if state.get("iteration_count", 0) >= 3:
        # Hard cap reached. Force finalize with the first candidate.
        print("WARNING: Max iterations reached. Forcing finalization.")
        return "finalize"
    
    # Needs a rewrite
    # Increment iteration count here, or in another node. Let's do it simply here via state update if possible, 
    # but routing doesn't update state. State update happens in nodes. 
    # For now, rely on `iteration_count` being updated in the `humanize` node or somewhere else.
    return "humanize"

def finalize_node(state: dict) -> dict:
    """Sets the final output and ends the loop."""
    best = state.get("best_candidate")
    if not best and state.get("candidates"):
        best = state["candidates"][0] # Fallback
        
    return {"final_output": best, "change_summary": "Processed via LangGraph."}

def build_humanization_graph():
    """Builds and compiles the state graph."""
    workflow = StateGraph(HumanizationState)

    # Add Nodes
    workflow.add_node("analyze_input", analyze_input_node)
    workflow.add_node("extract_facts", fact_guardian_node)
    workflow.add_node("extract_citations", citation_guardian_node)
    workflow.add_node("plan", plan_humanization_node)
    workflow.add_node("humanize", humanizer_node)
    workflow.add_node("critic", quality_critic_node)
    workflow.add_node("finalize", finalize_node)

    # Add Edges (Linear up to planning)
    workflow.set_entry_point("analyze_input")
    workflow.add_edge("analyze_input", "extract_facts")
    workflow.add_edge("extract_facts", "extract_citations")
    workflow.add_edge("extract_citations", "plan")
    
    # The Loop
    workflow.add_edge("plan", "humanize")
    workflow.add_edge("humanize", "critic")
    
    # Conditional Routing
    workflow.add_conditional_edges(
        "critic",
        evaluate_and_route,
        {
            "humanize": "humanize",
            "finalize": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    return workflow.compile()
