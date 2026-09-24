from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid
from app.graph.workflow import build_humanization_graph

router = APIRouter()

# Initialize the LangGraph state machine once
humanization_app = build_humanization_graph()

# In-memory mock for Job status polling
JOB_STORE = {}

class AdvancedHumanizeRequest(BaseModel):
    text: str
    profile_id: str = None
    strength: str = "balanced"
    preserve_citations: bool = True

def process_langgraph_job(job_id: str, request: AdvancedHumanizeRequest):
    """Background task that runs the cyclical LangGraph workflow."""
    JOB_STORE[job_id]["status"] = "processing"
    
    initial_state = {
        "original_text": request.text,
        "style_profile": {"profile_id": request.profile_id} if request.profile_id else {},
        "strength": request.strength
    }
    
    try:
        # Execute the LangGraph workflow
        final_state = humanization_app.invoke(initial_state)
        
        JOB_STORE[job_id]["status"] = "completed"
        JOB_STORE[job_id]["result"] = {
            "final_output": final_state.get("final_output"),
            "change_summary": final_state.get("change_summary"),
            "candidates": final_state.get("candidates"),
            "evaluations": final_state.get("evaluations"),
            "iterations": final_state.get("iteration_count")
        }
    except Exception as e:
        JOB_STORE[job_id]["status"] = "failed"
        JOB_STORE[job_id]["error"] = str(e)

@router.post("/humanize/advanced")
async def start_advanced_humanization(request: AdvancedHumanizeRequest, background_tasks: BackgroundTasks):
    """
    Submits a document to the multi-agent QA platform.
    Returns a Job ID immediately for async polling.
    """
    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {"status": "queued"}
    
    background_tasks.add_task(process_langgraph_job, job_id, request)
    
    return {"job_id": job_id, "status": "queued", "message": "LangGraph agents dispatched."}

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
