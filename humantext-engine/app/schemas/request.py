from pydantic import BaseModel, Field
from typing import Optional

class HumanizeRequest(BaseModel):
    text: str = Field(..., description="The original text to be humanized", min_length=1)
    document_type: str = Field(default="general", description="e.g., academic, technical, business, casual")
    target_mode: str = Field(default="natural_professional", description="The Rewrite Mode to use")
    bypass_strength: str = Field(default="standard", description="standard, high, extreme")
    target_tone: Optional[str] = Field(default=None, description="Optional target tone (e.g., formal, conversational)")
    target_audience: Optional[str] = Field(default=None, description="Optional target audience")

class SentenceRewriteRequest(BaseModel):
    sentence: str = Field(..., description="The specific sentence to rewrite", min_length=1)
    context: Optional[str] = Field(default="", description="The surrounding paragraph context")
    tone: str = Field(default="clear", description="The tone for the rewrite")

class ScanRequest(BaseModel):
    text: str = Field(..., description="The text to scan for AI probability")
