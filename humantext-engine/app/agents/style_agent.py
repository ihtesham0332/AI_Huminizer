import re
from typing import Dict, Any

class StyleAgent:
    """
    Analyzes the input text for tone, formality, and readability.
    Does not use LLMs to save cost; uses deterministic NLP.
    """
    
    def __init__(self):
        self.formal_words = {"furthermore", "moreover", "consequently", "thus", "therefore", "utilize", "facilitate", "implement"}
        self.casual_words = {"like", "super", "really", "stuff", "things", "got", "gonna", "wanna"}
    
    def analyze_style(self, text: str) -> Dict[str, Any]:
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        
        if total_words == 0:
            return {"formality_score": 5, "readability": "unknown"}
            
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
        total_sentences = max(len(sentences), 1)
        
        avg_sentence_length = total_words / total_sentences
        
        formal_count = sum(1 for word in words if word in self.formal_words)
        casual_count = sum(1 for word in words if word in self.casual_words)
        
        # Formality 1-10
        base_formality = 5
        formality = base_formality + (formal_count * 0.5) - (casual_count * 0.5)
        
        if avg_sentence_length > 20:
            formality += 1
        elif avg_sentence_length < 10:
            formality -= 1
            
        formality = max(1, min(10, formality))
        
        readability = "Balanced"
        if avg_sentence_length > 25:
            readability = "Dense/Academic"
        elif avg_sentence_length < 12:
            readability = "Simple/Casual"
            
        return {
            "formality_score": round(formality, 1),
            "readability": readability,
            "avg_sentence_length": round(avg_sentence_length, 1)
        }
