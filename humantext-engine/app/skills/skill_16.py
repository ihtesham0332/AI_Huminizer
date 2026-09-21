from typing import Dict, Any, List
from pydantic import BaseModel, Field

class FactValidationResult(BaseModel):
    is_valid: bool = Field(description="True if all facts are preserved, False otherwise")
    missing_facts: List[str] = Field(default_factory=list, description="List of facts missing from the transformed text")

def validate_fact_preservation(facts_registry: Dict[str, Any], transformed_text: str) -> Dict[str, Any]:
    """
    Skill 16: Fact Preservation Validation
    Deterministically cross-references the original Facts Registry with the final text.
    
    Args:
        facts_registry: The generated Facts registry (from Skill 05).
        transformed_text: The final transformed text.
        
    Returns:
        A dictionary representing the FactValidationResult.
    """
    missing = []
    
    if not facts_registry:
        return FactValidationResult(is_valid=True, missing_facts=[]).model_dump()
        
    if not transformed_text:
        return FactValidationResult(is_valid=False, missing_facts=["All facts missing (empty text)"]).model_dump()
        
    for category, items in facts_registry.items():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "value" in item:
                    val = item["value"]
                    if val and val not in transformed_text:
                        missing.append(val)
                        
    is_valid = len(missing) == 0
    return FactValidationResult(is_valid=is_valid, missing_facts=missing).model_dump()
