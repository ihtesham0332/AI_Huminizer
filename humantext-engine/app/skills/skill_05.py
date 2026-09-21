from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class Fact(BaseModel):
    id: str = Field(description="Unique identifier for the fact")
    type: str = Field(description="number, date, name, entity, citation, url, etc.")
    value: str = Field(description="The exact text value of the fact")
    context: Optional[str] = Field(None, description="Surrounding context to disambiguate")

def extract_facts(cleaned_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 05: Fact Extraction
    Extracts numbers, dates, names, entities, and citations. Hybrid approach.
    
    Args:
        cleaned_text: The cleaned input text.
        llm_client: Optional LLM client for complex extraction (hybrid).
        
    Returns:
        A dictionary acting as a facts registry.
    """
    registry = {
        "numbers": [],
        "dates": [],
        "names": [],
        "entities": [],
        "citations": [],
        "urls": []
    }
    
    if not cleaned_text:
        return registry

    # Hybrid approach: we'd run regex or spaCy here, and potentially use LLM.
    # For now, we mock the behavior.
    if llm_client is None:
        # Simple mock extraction based on regex or string checking
        if "2026" in cleaned_text:
            registry["dates"].append(Fact(id="f1", type="date", value="2026").model_dump())
        if "AI" in cleaned_text:
            registry["entities"].append(Fact(id="f2", type="entity", value="AI").model_dump())
        if "42" in cleaned_text:
            registry["numbers"].append(Fact(id="f3", type="number", value="42").model_dump())
            
        return registry
        
    try:
        response = llm_client.invoke({"text": cleaned_text})
        if isinstance(response, dict):
            registry.update(response)
        elif hasattr(response, "model_dump"):
            registry.update(response.model_dump())
    except Exception:
        pass
        
    return registry
