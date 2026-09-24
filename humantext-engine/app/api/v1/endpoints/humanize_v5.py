from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.graph.compiler import humanizer_app

router = APIRouter()

class HumanizeV5Request(BaseModel):
    text: str
    mode: str = "balanced" # fast, balanced, deep, ghost, creative
    length: str = "maintain" # maintain, condense, expand
    profile_id: Optional[str] = None
    profile_instructions: Optional[str] = None

class HumanizeV5Response(BaseModel):
    original_text: str
    humanized_text: str
    facts_protected: List[str]
    citations_protected: List[str]
    quality_score: int
    revision_loops: int

@router.post("/humanize/v5", response_model=HumanizeV5Response)
async def run_humanizer(request: HumanizeV5Request):
    """
    The main V5 endpoint that triggers the LangGraph swarm.
    """
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Initialize State
    initial_state = {
        "original_text": request.text,
        "mode": request.mode,
        "length": request.length,
        "profile_instructions": request.profile_instructions,
        "revision_count": 0
    }

    try:
        # Run the graph (this is synchronous for the MVP, 
        # in production with large docs we'd use .astream)
        final_state = humanizer_app.invoke(initial_state)
        
        # Extract results
        facts = [f["value"] for f in final_state.get("facts", [])]
        citations = [c["value"] for c in final_state.get("citations", [])]
        
        quality_report = final_state.get("quality_report", {})
        passed = quality_report.get("passed", False)
        
        return HumanizeV5Response(
            original_text=final_state["original_text"],
            humanized_text=final_state["final_output"],
            facts_protected=facts,
            citations_protected=citations,
            quality_score=99 if passed else 50,
            revision_loops=final_state["revision_count"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {str(e)}")
