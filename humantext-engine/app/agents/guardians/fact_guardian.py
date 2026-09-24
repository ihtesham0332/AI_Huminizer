import re
from typing import List, Dict, Any

class FactGuardianAgent:
    """
    Extracts all numerical values, dates, and percentages to lock them
    before generation. This is a core component of the Protection Engine.
    """
    
    def __init__(self):
        # Regex patterns for facts
        self.patterns = {
            "percentage": r'\b\d+(?:\.\d+)?\s*%',
            "currency": r'(?:\$|€|£|¥)\s*\d+(?:\.\d+)?(?:k|m|b|K|M|B)?',
            "year": r'\b(19|20)\d{2}\b',
            "decimal": r'\b\d+\.\d+\b',
            "large_number": r'\b\d{1,3}(?:,\d{3})+\b'
        }
    
    def extract_facts(self, text: str) -> List[Dict[str, str]]:
        facts = []
        for fact_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                facts.append({
                    "type": fact_type,
                    "value": match.group(),
                    "position": match.span()
                })
        
        return facts

    def verify(self, original_facts: List[Dict[str, str]], generated_text: str) -> Dict[str, Any]:
        """
        Runs after generation to ensure facts weren't dropped.
        """
        missing_facts = []
        for fact in original_facts:
            # We strip spaces for loose matching of things like $ 500 vs $500
            val = fact["value"].replace(" ", "")
            gen_clean = generated_text.replace(" ", "")
            if val not in gen_clean:
                missing_facts.append(fact["value"])
                
        if missing_facts:
            return {
                "status": "FAIL",
                "missing": missing_facts,
                "message": f"CRITICAL: The LLM dropped the following facts: {', '.join(missing_facts)}"
            }
            
        return {"status": "PASS", "missing": [], "message": "All facts preserved."}
