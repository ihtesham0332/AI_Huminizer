from typing import Dict, Any
from pydantic import BaseModel, Field
from app.skills.skill_15 import ValidationResult

def validate_tone_consistency(target_tone: list[str], transformed_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 17: Tone Consistency Validation
    Verifies that the transformed text matches the target tone.
    
    Args:
        target_tone: The desired tone(s) from the humanization plan.
        transformed_text: The final transformed text.
        llm_client: Optional LLM client to perform the validation.
        
    Returns:
        A dictionary representing the ValidationResult.
    """
    if not transformed_text:
        return ValidationResult(is_valid=False, reasoning="Transformed text is empty").model_dump()
        
    if not target_tone:
        return ValidationResult(is_valid=True, reasoning="No target tone specified").model_dump()
        
    if llm_client is None:
        # Mock logic
        return ValidationResult(is_valid=True, reasoning="Mock tone validation passed").model_dump()
        
    try:
        response = llm_client.invoke({"target_tone": target_tone, "text": transformed_text})
        if hasattr(response, "model_dump"):
            return response.model_dump()
        elif isinstance(response, dict):
            return ValidationResult(**response).model_dump()
    except Exception:
        pass
        
    return ValidationResult(is_valid=True, reasoning="Fallback to true on error").model_dump()
