import re
from typing import List

def extract_protected_facts(text: str) -> List[str]:
    """
    Identifies and extracts critical factual data (numbers, percentages, years)
    that must not be altered during the humanization process.
    """
    protected = set()
    
    # 1. Percentages (e.g., "95%", "3.14 %")
    percentages = re.findall(r'\b\d+(?:\.\d+)?\s*%', text)
    protected.update(percentages)
    
    # 2. Years (e.g., "2023", "1999")
    for match in re.finditer(r'\b(19|20)\d{2}\b', text):
        protected.add(match.group(0))
        
    # 3. Currency (e.g., "$500", "€1.2M")
    currencies = re.findall(r'[$€£]\s*\d+(?:\.\d+)?[kKmMbB]?', text)
    protected.update(currencies)
    
    # 4. URLs and Emails
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    protected.update(urls)
    protected.update(emails)
    
    return list(protected)

def fact_guardian_node(state: dict) -> dict:
    """LangGraph node to extract facts and add them to the state."""
    text = state.get("original_text", "")
    facts = extract_protected_facts(text)
    
    # Merge with existing protected tokens
    current_protected = state.get("protected_tokens", [])
    current_protected.extend(facts)
    
    return {"protected_tokens": list(set(current_protected))}
