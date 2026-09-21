from typing import Dict, Any
from app.skills.skill_16 import validate_fact_preservation

def enforce_fact_preservation(facts_registry: Dict[str, Any], transformed_text: str) -> Dict[str, Any]:
    """
    Fact Guardian
    Enforces Rule 5: No Unsupported Information.
    Acts as a strict wrapper around Skill 16.
    """
    result = validate_fact_preservation(facts_registry, transformed_text)
    return result
