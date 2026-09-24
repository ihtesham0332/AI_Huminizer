from typing import Dict, Any, List
import re

class DNAExtractorAgent:
    """
    Analyzes a user's past writing samples to extract their unique stylistic fingerprint.
    In a full production environment, this would use a Tier 1 LLM (Gemini 1.5 Flash) 
    to extract deeper semantic patterns, but we implement a deterministic baseline here.
    """
    
    def __init__(self):
        # A list of common transitional phrases to scan for
        self.transitions = [
            "furthermore", "moreover", "however", "therefore", "thus", 
            "in conclusion", "to summarize", "on the other hand", "specifically",
            "for example", "for instance", "as a result", "consequently"
        ]
        
    def extract_dna(self, text_samples: List[str]) -> Dict[str, Any]:
        combined_text = " ".join(text_samples).lower()
        words = re.findall(r'\b\w+\b', combined_text)
        sentences = re.split(r'[.!?]+', combined_text)
        
        total_words = len(words)
        total_sentences = max(len(sentences), 1)
        
        # 1. Preferred Transitions
        found_transitions = {}
        for transition in self.transitions:
            count = combined_text.count(transition)
            if count > 0:
                found_transitions[transition] = count
                
        # Sort transitions by frequency
        sorted_transitions = sorted(found_transitions.items(), key=lambda item: item[1], reverse=True)
        top_transitions = [t[0] for t in sorted_transitions[:3]]
        
        # 2. Sentence Complexity
        avg_sentence_length = total_words / total_sentences
        complexity = "medium"
        if avg_sentence_length > 25:
            complexity = "high"
        elif avg_sentence_length < 12:
            complexity = "low"
            
        # 3. Formality Heuristic
        formal_markers = combined_text.count("utilize") + combined_text.count("implement") + combined_text.count("facilitate")
        casual_markers = combined_text.count("like") + combined_text.count("really") + combined_text.count("stuff")
        
        formality_score = 5 + (formal_markers * 0.5) - (casual_markers * 0.5)
        formality_score = max(1, min(10, formality_score))
        
        return {
            "top_transitions": top_transitions,
            "complexity": complexity,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "formality_score": round(formality_score, 1),
            "preferred_voice": "passive" if "is driven by" in combined_text else "active"
        }
