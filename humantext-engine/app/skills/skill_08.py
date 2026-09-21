from typing import Dict, Any
from pydantic import BaseModel, Field

class ReadabilityScore(BaseModel):
    flesch_kincaid_grade: float = Field(default=0.0, description="Flesch-Kincaid Grade Level")
    flesch_reading_ease: float = Field(default=0.0, description="Flesch Reading Ease score")
    sentence_complexity: float = Field(default=0.0, description="Average words per sentence")
    vocabulary_level: float = Field(default=0.0, description="Type-token ratio or similar metric")

def analyze_readability(cleaned_text: str) -> Dict[str, Any]:
    """
    Skill 08: Readability Analysis
    Calculates readability scores (Flesch-Kincaid, complexity) deterministically.
    
    Args:
        cleaned_text: The cleaned input text.
        
    Returns:
        A dictionary representing the ReadabilityScore.
    """
    if not cleaned_text:
        return ReadabilityScore().model_dump()
        
    # In a real environment, we'd use `textstat` here.
    # For now, we simulate basic metrics deterministically based on length.
    words = cleaned_text.split()
    sentences = max(1, cleaned_text.count('.') + cleaned_text.count('!') + cleaned_text.count('?'))
    
    avg_words_per_sentence = len(words) / sentences
    unique_words = len(set(w.lower() for w in words))
    ttr = unique_words / len(words) if words else 0.0
    
    # Mocked flesch kincaid for demonstration
    fk_grade = min(12.0, avg_words_per_sentence * 0.5) 
    fk_ease = max(0.0, 100.0 - (fk_grade * 5))
    
    return ReadabilityScore(
        flesch_kincaid_grade=fk_grade,
        flesch_reading_ease=fk_ease,
        sentence_complexity=avg_words_per_sentence,
        vocabulary_level=ttr
    ).model_dump()
