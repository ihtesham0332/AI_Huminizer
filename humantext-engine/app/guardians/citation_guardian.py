import re
from typing import List

def extract_citations(text: str) -> List[str]:
    """
    Identifies and extracts academic citations (APA, MLA, IEEE, etc.)
    that must be preserved identically.
    """
    protected = set()
    
    # 1. Inline parenthetical citations: (Smith, 2023) or (Doe & Smith, 2020)
    parentheticals = re.findall(r'\([A-Z][a-zA-Z\s&.,]+,\s*(?:19|20)\d{2}[a-z]?\)', text)
    protected.update(parentheticals)
    
    # 2. Bracketed citations (IEEE style): [1], [4, 5], [10-15]
    brackets = re.findall(r'\[\d+(?:\s*,\s*\d+)*(?:\s*-\s*\d+)?\]', text)
    protected.update(brackets)
    
    return list(protected)

def citation_guardian_node(state: dict) -> dict:
    """LangGraph node to extract citations and add them to the state."""
    text = state.get("original_text", "")
    citations = extract_citations(text)
    
    # Merge with existing protected tokens
    current_protected = state.get("protected_tokens", [])
    current_protected.extend(citations)
    
    return {"protected_tokens": list(set(current_protected))}
