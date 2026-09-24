import re
from typing import List, Dict, Any

class SentenceIntelligenceEngine:
    """
    Splits text into sentences and independently evaluates which sentences
    actually need humanization, saving massive API costs.
    Adheres to Master Prompt Section 11 & 12.
    """
    
    def __init__(self):
        # Basic heuristic thresholds
        self.complexity_threshold = 0.7
        self.formulaic_phrases = ["it is important to note", "in conclusion", "furthermore", "delve into", "tapestry"]

    def split_into_sentences(self, text: str) -> List[str]:
        """Splits text into sentences using basic regex."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def analyze_sentence(self, sentence: str, index: int) -> Dict[str, Any]:
        """
        Calculates independent scores for a single sentence.
        """
        words = sentence.split()
        if not words:
            return {"needs_rewrite": False}

        avg_word_len = sum(len(w) for w in words) / len(words)
        complexity = min(1.0, avg_word_len / 8.0)
        
        formulaic_pattern = 0.0
        for phrase in self.formulaic_phrases:
            if phrase in sentence.lower():
                formulaic_pattern = 0.8
                break

        # A sentence needs a rewrite if it's too complex or uses typical ChatGPT formulaic patterns
        needs_rewrite = bool(complexity > self.complexity_threshold or formulaic_pattern > 0.5)

        return {
            "sentence_id": index,
            "text": sentence,
            "complexity": round(complexity, 2),
            "formulaic_pattern": formulaic_pattern,
            "needs_rewrite": needs_rewrite
        }

    def selective_humanization_plan(self, text: str) -> Dict[str, Any]:
        """
        Creates a plan detailing exactly which sentences to send to the LLM.
        """
        sentences = self.split_into_sentences(text)
        analysis = []
        words_saved = 0
        words_to_process = 0
        
        for i, sentence in enumerate(sentences):
            res = self.analyze_sentence(sentence, i)
            analysis.append(res)
            
            if res["needs_rewrite"]:
                words_to_process += len(sentence.split())
            else:
                words_saved += len(sentence.split())
                
        total_words = words_to_process + words_saved
        savings_percentage = round((words_saved / total_words) * 100, 2) if total_words > 0 else 0
        
        return {
            "total_sentences": len(sentences),
            "sentences_to_rewrite": sum(1 for a in analysis if a["needs_rewrite"]),
            "words_to_process": words_to_process,
            "words_saved": words_saved,
            "savings_percentage": savings_percentage,
            "sentence_analysis": analysis
        }
