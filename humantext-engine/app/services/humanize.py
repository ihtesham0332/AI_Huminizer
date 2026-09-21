from typing import Dict, Any
import uuid
from app.graph.workflow import app_graph
from app.schemas.request import HumanizeRequest
from app.schemas.response import HumanizeResponse

def run_humanize_workflow(request: HumanizeRequest) -> HumanizeResponse:
    """
    Service layer that initializes state and runs the LangGraph workflow.
    """
    req_id = str(uuid.uuid4())
    
    # Initialize state
    initial_state = {
        "request_id": req_id,
        "original_text": request.text,
        "document_type": request.document_type,
        "target_mode": request.target_mode,
        "target_tone": request.target_tone,
        "status": "initialized",
        
        "document_analysis": {},
        "semantic_analysis": {},
        "style_analysis": {},
        "context_analysis": {},
        "readability_analysis": {},
        
        "claims": [],
        "facts": {},
        "entities": [],
        "constraints": [],
        
        "transformation_plan": {},
        "rewritten_text": None,
        
        "semantic_score": None,
        "factual_score": None,
        "style_score": None,
        "readability_score": None,
        "naturalness_score": None,
        "quality_score": None,
        
        "validation_errors": [],
        "revision_count": 0,
        "revision_history": [],
        "agent_metadata": {}
    }
    
    # Execute Graph
    final_state = app_graph.invoke(initial_state)
    
    # Map to Response
    return HumanizeResponse(
        request_id=req_id,
        original_text=final_state.get("original_text", request.text),
        humanized_text=final_state.get("rewritten_text") or final_state.get("original_text", ""),
        quality_score=final_state.get("quality_score", 0.0),
        naturalness_score=final_state.get("naturalness_score", 0.0),
        status=final_state.get("status", "unknown"),
        metadata={
            "revision_count": final_state.get("revision_count", 0),
            "latency": final_state.get("latency", 0.0)
        }
    )
