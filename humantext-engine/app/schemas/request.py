from pydantic import BaseModel, Field
from typing import Optional

class HumanizeRequest(BaseModel):
    text: str = Field(..., description="The original text to be humanized", min_length=1)
    document_type: str = Field(default="general", description="e.g., academic, technical, business, casual")
    target_mode: str = Field(default="natural_professional", description="The Rewrite Mode to use")
    target_tone: Optional[str] = Field(default=None, description="Optional target tone (e.g., formal, conversational)")
    target_audience: Optional[str] = Field(default=None, description="Optional target audience")
