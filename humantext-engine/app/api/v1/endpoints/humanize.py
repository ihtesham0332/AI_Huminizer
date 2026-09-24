from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional

# Import V4 Engines
from app.engine.document_intelligence import DocumentIntelligenceEngine
from app.engine.style_intelligence import StyleIntelligenceEngine
from app.engine.sentence_intelligence import SentenceIntelligenceEngine
from app.engine.cost_controller import CostControllerAgent
from app.engine.quality_critic import QualityCriticEngine, QualityGate
from app.engine.enhanced_guardians import EnhancedFactGuardian, EnhancedCitationGuardian

from app.graph.nodes import HumanizationState, create_supervisor
from app.models.router import get_model
from langchain_core.messages import HumanMessage

from app.schemas.request import SentenceRewriteRequest, ScanRequest
from app.services.stream import stream_humanize_workflow
from app.services.sentence_rewriter import rewrite_sentence
from app.services.detector import scan_text
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Instantiate V4 Engines
doc_engine = DocumentIntelligenceEngine()
style_engine = StyleIntelligenceEngine()
sentence_engine = SentenceIntelligenceEngine()
cost_agent = CostControllerAgent(user_plan="PRO")
fact_guardian = EnhancedFactGuardian()
citation_guardian = EnhancedCitationGuardian()
critic_engine = QualityCriticEngine()
quality_gate = QualityGate(critic=critic_engine)

class HumanizeRequest(BaseModel):
    text: str
    strength: str = "balanced"
    language: Optional[str] = "en"

class HumanizeResponse(BaseModel):
    original_text: str
    humanized_text: str
    candidates: List[str]
    v4_metadata: dict

@router.post("/humanize/scan", summary="Scan text for AI probability")
async def scan_ai_probability(request: ScanRequest):
    try:
        return scan_text(request)
    except Exception as e:
        logger.error(f"AI Scanning failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during scanning")

@router.post("/humanize/sentence", summary="Rewrite a single sentence (3 Variations)")
async def humanize_sentence(request: SentenceRewriteRequest):
    try:
        return rewrite_sentence(request)
    except Exception as e:
        logger.error(f"Sentence rewriting failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during sentence rewrite")

@router.post("/humanize", response_model=HumanizeResponse, summary="Humanize Text (Synchronous)")
async def humanize_text(request: HumanizeRequest):
    """
    Transforms robotic/AI text into natural text completely synchronously.
    """
    try:
        response = run_humanize_workflow(request)
        return response
    except Exception as e:
        logger.error(f"Humanization failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during humanization")

@router.post("/humanize/stream", summary="Humanize Text (Real-Time SSE Stream)")
async def humanize_text_stream(request: HumanizeRequest):
    """
    Transforms robotic/AI text into natural text and streams tokens back to the client in real-time.
    """
    try:
        return StreamingResponse(
            stream_humanize_workflow(request),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Streaming failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during streaming")
