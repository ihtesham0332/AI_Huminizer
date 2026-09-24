from langgraph.graph import StateGraph, START, END
from app.graph.v5_state import HumanizerState
from app.graph.v5_nodes import (
    analyze_node,
    planning_node,
    generate_node,
    critique_node,
    route_after_critique,
    finalize_node
)

def compile_humanizer_graph():
    """
    Compiles the Master LangGraph state machine.
    """
    workflow = StateGraph(HumanizerState)

    # Add Nodes
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("plan", planning_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("critique", critique_node)
    workflow.add_node("finalize", finalize_node)

    # Define Edges
    workflow.add_edge(START, "analyze")
    workflow.add_edge("analyze", "plan")
    workflow.add_edge("plan", "generate")
    workflow.add_edge("generate", "critique")

    # Conditional Routing based on Quality Critic
    workflow.add_conditional_edges(
        "critique",
        route_after_critique,
        {
            "generate": "generate", # Failed, loop back
            "finalize": "finalize"  # Passed, move forward
        }
    )
    
    workflow.add_edge("finalize", END)

    # Compile the graph
    app = workflow.compile()
    return app

# Expose a singleton instance for the FastAPI router
humanizer_app = compile_humanizer_graph()
