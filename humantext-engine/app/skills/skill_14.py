from typing import Dict, Any, List

def preserve_citations(facts_registry: Dict[str, Any], text: str) -> List[str]:
    """
    Skill 14: Citation Preservation
    Locks citations, references, URLs, and DOIs deterministically.
    
    Args:
        facts_registry: The generated Facts registry (from Skill 05).
        text: The full text.
        
    Returns:
        A list of citations/URLs that must be locked (preserved exactly).
    """
    locked_citations = []
    
    if not text or not facts_registry:
        return locked_citations
        
    citations = facts_registry.get("citations", [])
    urls = facts_registry.get("urls", [])
    
    for item in citations + urls:
        if isinstance(item, dict) and "value" in item:
            val = item["value"]
            if val and val in text and val not in locked_citations:
                locked_citations.append(val)
                
    return locked_citations
