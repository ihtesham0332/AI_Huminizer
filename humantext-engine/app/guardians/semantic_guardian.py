from typing import Dict, Any
from app.skills.skill_15 import validate_source_integrity

def enforce_semantic_preservation(original_semantics: Dict[str, Any], transformed_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Semantic Guardian
    Enforces Rule 4: Preserve Meaning Above Everything.
    Acts as a strict wrapper around Skill 15.
    """
    result = validate_source_integrity(original_semantics, transformed_text, llm_client)
    
    # Guardian logic: if it fails, it raises an exception or forces a fallback
    # For this architecture, we return the result for the LangGraph to handle
    return result
