import re
from typing import List, Dict, Any

class CitationGuardianAgent:
    """
    Extracts academic citations (APA, MLA, IEEE) to lock them
    before generation. Part of the Protection Engine.
    """
    
    def __init__(self):
        self.patterns = {
            "ieee": r'\[\d+(?:,\s*\d+)*\]', # e.g. [1], [1, 2]
            "apa_author_year": r'(?:\b[A-Z][A-Za-z\s]+(?:et al\.)?\s*\(\d{4}\))|\([A-Za-z\s]+(?:et al\.)?,\s*\d{4}\)', # e.g. (Smith, 2023) or John (2024)
            "footnote": r'\b\S+?(?:”|"|\')?\[\d+\]' # word"[1]
        }
        
    def extract_citations(self, text: str) -> List[Dict[str, str]]:
        citations = []
        for cite_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                citations.append({
                    "type": cite_type,
                    "value": match.group(),
                    "position": match.span()
                })
        return citations
        
    def verify(self, original_citations: List[Dict[str, str]], generated_text: str) -> Dict[str, Any]:
        missing_citations = []
        for cite in original_citations:
            val = cite["value"]
            # Handle slight spacing changes in APA citations
            val_clean = re.sub(r'\s+', '', val)
            gen_clean = re.sub(r'\s+', '', generated_text)
            
            if val_clean not in gen_clean:
                missing_citations.append(val)
                
        if missing_citations:
            return {
                "status": "FAIL",
                "missing": missing_citations,
                "message": f"CRITICAL: The LLM dropped the following citations: {', '.join(missing_citations)}"
            }
            
        return {"status": "PASS", "missing": [], "message": "All citations preserved."}
