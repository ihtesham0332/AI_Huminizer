from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class Claim(BaseModel):
    id: str = Field(description="Unique identifier for the claim")
    text: str = Field(description="The core claim text")
    evidence_level: Optional[str] = Field(None, description="e.g., suggests, proves, shows")
    modality: Optional[str] = Field(None, description="e.g., may, must, will")
    scope: Optional[str] = Field(None, description="e.g., some, all, most")
    hedging: Optional[str] = Field(None, description="e.g., possibly, likely")

def extract_claims(cleaned_text: str, llm_client: Any = None) -> List[Dict[str, Any]]:
    """
    Skill 04: Claim Extraction
    Extracts claims with modality, hedging, and scope using an LLM.
    
    Args:
        cleaned_text: The cleaned input text.
        llm_client: An initialized LLM client or chain. If None, returns a mock list.
        
    Returns:
        A list of claims with their qualifiers as dictionaries.
    """
    if not cleaned_text:
        return []
        
    if llm_client is None:
        # Fallback or mock behavior when no LLM is provided
        return [
            {
                "id": "c1",
                "text": f"Mock claim for: {cleaned_text[:15]}",
                "evidence_level": "suggests",
                "modality": "may",
                "scope": "some",
                "hedging": "possibly"
            }
        ]
    
    try:
        response = llm_client.invoke({"text": cleaned_text})
        if isinstance(response, list) and all(hasattr(c, "model_dump") for c in response):
            claims = [c.model_dump() for c in response]
        elif hasattr(response, "claims"):
            claims = [c.model_dump() if hasattr(c, "model_dump") else c for c in response.claims]
        else:
            claims = response if isinstance(response, list) else [response]
    except Exception as e:
        claims = []

    return claims
