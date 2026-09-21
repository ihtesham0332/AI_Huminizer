from typing import Dict, Any, Tuple
from app.utils.text import clean_text
from app.utils.errors import InputValidationError
from app.config.settings import get_settings

def validate_input(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """
    Skill 01: Input Validation
    Validates input text (empty, too long) and cleans it.
    
    Args:
        raw_text: The raw input text.
        
    Returns:
        A tuple of (validation_result_dict, cleaned_text).
        
    Raises:
        InputValidationError: If the text is empty, malformed, or exceeds the length limit.
    """
    settings = get_settings()
    
    if not isinstance(raw_text, str):
        raise InputValidationError(
            message="Input text must be a string.",
            context={"received_type": str(type(raw_text))}
        )
        
    cleaned = clean_text(raw_text)
    
    if not cleaned:
        raise InputValidationError(
            message="Input text is empty or contains only whitespace.",
            context={"received": raw_text}
        )
        
    if len(cleaned) > settings.MAX_INPUT_LENGTH:
        raise InputValidationError(
            message=f"Input text exceeds maximum length of {settings.MAX_INPUT_LENGTH} characters.",
            context={"length": len(cleaned), "max_length": settings.MAX_INPUT_LENGTH}
        )
        
    result = {
        "is_valid": True,
        "original_length": len(raw_text),
        "cleaned_length": len(cleaned)
    }
    
    return result, cleaned
