from typing import Dict, Any, List

def preserve_terminology(facts_registry: Dict[str, Any], text: str) -> List[str]:
    """
    Skill 13: Terminology Preservation
    Locks technical terms, defined terms, and jargon deterministically.
    
    Args:
        facts_registry: The generated Facts registry (from Skill 05).
        text: The full text.
        
    Returns:
        A list of terms that must be locked (preserved exactly).
    """
    locked_terms = []
    
    if not text or not facts_registry:
        return locked_terms
        
    # Extract entities and names from the facts registry as potential terminology
    entities = facts_registry.get("entities", [])
    names = facts_registry.get("names", [])
    
    for item in entities + names:
        if isinstance(item, dict) and "value" in item:
            val = item["value"]
            if val and val in text and val not in locked_terms:
                locked_terms.append(val)
                
    # A real implementation might also use spaCy or a predefined jargon dictionary here.
    return locked_terms
