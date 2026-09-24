import re
from typing import Dict, Any, List

class EnhancedFactGuardian:
    """
    Extracts factual entities (numbers, dates) before generation and verifies them after.
    Adheres to Master Prompt Section 14.
    """
    def extract_facts(self, text: str) -> List[str]:
        # Extract years (e.g., 2026), percentages (87%), and currencies ($20)
        facts = re.findall(r'\b\d{4}\b|\b\d+%\b|\$\d+', text)
        return facts
        
    def verify_facts(self, original_text: str, generated_text: str) -> Dict[str, Any]:
        orig_facts = set(self.extract_facts(original_text))
        gen_facts = set(self.extract_facts(generated_text))
        
        missing = list(orig_facts - gen_facts)
        added = list(gen_facts - orig_facts)
        
        return {
            "facts_preserved": len(missing) == 0 and len(added) == 0,
            "altered_facts": missing + added
        }

class EnhancedCitationGuardian:
    """
    Extracts and protects citations.
    Adheres to Master Prompt Section 15.
    """
    def extract_citations(self, text: str) -> List[str]:
        # Extract basic APA style (Smith, 2023) or standard DOI URLs
        citations = re.findall(r'\([A-Za-z]+, \d{4}\)|10\.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.IGNORECASE)
        return citations
        
    def verify_citations(self, original_text: str, generated_text: str) -> Dict[str, Any]:
        orig_cites = set(self.extract_citations(original_text))
        gen_cites = set(self.extract_citations(generated_text))
        
        missing = list(orig_cites - gen_cites)
        
        return {
            "citations_preserved": len(missing) == 0,
            "altered_citations": missing
        }
