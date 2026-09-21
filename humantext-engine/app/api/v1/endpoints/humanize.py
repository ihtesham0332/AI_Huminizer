from fastapi import APIRouter, HTTPException
from app.schemas.request import HumanizeRequest
from app.schemas.response import HumanizeResponse
from app.services.humanize import run_humanize_workflow
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/humanize", response_model=HumanizeResponse, summary="Humanize Text")
async def humanize_text(request: HumanizeRequest):
    """
    Transforms robotic/AI text into natural text using the LangGraph orchestration.
    """
    try:
        response = run_humanize_workflow(request)
        return response
    except Exception as e:
        logger.error(f"Humanization failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during humanization")
