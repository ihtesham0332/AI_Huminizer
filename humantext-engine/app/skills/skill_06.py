from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class StyleProfile(BaseModel):
    formality_score: float = Field(default=0.5, description="0.0 (very casual) to 1.0 (highly formal)")
    tone: List[str] = Field(default_factory=list, description="List of detected tones (e.g., academic, conversational)")
    voice: str = Field(default="neutral", description="Detected voice (e.g., active, passive, direct)")
    lexical_patterns: List[str] = Field(default_factory=list, description="Common lexical choices or repetitive patterns")

def analyze_style(cleaned_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 06: Style Analysis
    Detects formality, tone, voice, and lexical patterns. Hybrid LLM approach.
    
    Args:
        cleaned_text: The cleaned input text.
        llm_client: Optional LLM client to perform advanced style extraction.
        
    Returns:
        A dictionary representing the StyleProfile.
    """
    if not cleaned_text:
        return StyleProfile().model_dump()
        
    if llm_client is None:
        # Mock logic
        formality = 0.8 if "therefore" in cleaned_text.lower() else 0.4
        tone = ["academic"] if formality > 0.5 else ["conversational"]
        return StyleProfile(formality_score=formality, tone=tone, voice="active", lexical_patterns=[]).model_dump()
        
    try:
        response = llm_client.invoke({"text": cleaned_text})
        if hasattr(response, "model_dump"):
            return response.model_dump()
        elif isinstance(response, dict):
            return StyleProfile(**response).model_dump()
    except Exception:
        pass
        
    return StyleProfile().model_dump()
