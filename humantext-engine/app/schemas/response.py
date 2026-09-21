from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class HumanizeResponse(BaseModel):
    request_id: str
    original_text: str
    humanized_text: str
    quality_score: float
    naturalness_score: float
    status: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
