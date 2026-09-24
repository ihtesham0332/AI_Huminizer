from typing import Dict, Any, List

class StyleIntelligenceEngine:
    """
    Analyzes document language, content type, and stylistic characteristics.
    Adheres to Master Prompt Sections 5, 6, and 7.
    """
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Stub for language detection. 
        In production, use langdetect or an LLM call.
        """
        # Simplistic heuristic for Urdu/Hindi vs English
        if any(c in text for c in ['ہے', 'میں', 'کی']):
            return {"language": "ur", "confidence": 0.95, "script": "Arabic"}
            
        return {"language": "en", "confidence": 0.98, "script": "Latin"}
        
    def classify_content(self, text: str) -> Dict[str, Any]:
        """
        Classifies the document genre (Academic, Business, Casual).
        """
        text_lower = text.lower()
        if "abstract" in text_lower or "et al." in text_lower or "methodology" in text_lower:
            return {"content_type": "academic", "confidence": 0.89}
        elif "sincerely," in text_lower or "attached" in text_lower:
            return {"content_type": "email", "confidence": 0.92}
            
        return {"content_type": "general", "confidence": 0.60}
        
    def analyze_style_metrics(self, text: str) -> Dict[str, float]:
        """
        Calculates internal style metrics (formality, readability, etc).
        """
        words = text.split()
        avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
        
        # Simulated style calculation based on average word length
        formality = min(1.0, avg_word_len / 7.0)
        readability = max(0.1, 1.0 - formality)
        
        return {
            "formality": formality,
            "readability": readability,
            "sentence_variation": 0.5, # Placeholder for NLP parser
            "technicality": 0.4
        }


class PersonalWritingDNAEngine:
    """
    Creates and stores a Personal Writing DNA profile based on historical uploads.
    Adheres to Master Prompt Section 8 (Personal Writing DNA).
    """
    
    def __init__(self, style_engine: StyleIntelligenceEngine):
        self.style_engine = style_engine
        
    def build_profile(self, document_samples: List[str]) -> Dict[str, Any]:
        """
        Aggregates style metrics across multiple documents to build a baseline DNA profile.
        """
        if not document_samples:
            return {}
            
        aggregated_metrics = {"formality": 0.0, "readability": 0.0, "technicality": 0.0}
        
        for sample in document_samples:
            metrics = self.style_engine.analyze_style_metrics(sample)
            for k in aggregated_metrics.keys():
                aggregated_metrics[k] += metrics.get(k, 0.0)
                
        # Average the metrics
        count = len(document_samples)
        for k in aggregated_metrics.keys():
            aggregated_metrics[k] = round(aggregated_metrics[k] / count, 2)
            
        return {
            "version": "1.0",
            "dna_metrics": aggregated_metrics,
            "preferred_sentence_length": "medium",
            "tone": "conversational"
        }
