from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class ContextProfile(BaseModel):
    document_type: str = Field(default="unknown", description="e.g., email, essay, report, casual")
    audience: str = Field(default="general", description="e.g., peers, general public, experts")
    purpose: str = Field(default="inform", description="e.g., inform, persuade, entertain")
    text_register: str = Field(default="neutral", alias="register", description="e.g., formal, informal, technical")

def analyze_context(cleaned_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 07: Context Analysis
    Detects document type, audience, purpose, and register using an LLM.
    
    Args:
        cleaned_text: The cleaned input text.
        llm_client: Optional LLM client to perform extraction.
        
    Returns:
        A dictionary representing the ContextProfile.
    """
    if not cleaned_text:
        return ContextProfile().model_dump(by_alias=True)
        
    if llm_client is None:
        # Mock logic
        doc_type = "email" if "dear" in cleaned_text.lower() else "unknown"
        return ContextProfile(document_type=doc_type).model_dump(by_alias=True)
        
    try:
        response = llm_client.invoke({"text": cleaned_text})
        if hasattr(response, "model_dump"):
            return response.model_dump(by_alias=True)
        elif isinstance(response, dict):
            return ContextProfile(**response).model_dump(by_alias=True)
    except Exception:
        pass
        
    return ContextProfile().model_dump(by_alias=True)
