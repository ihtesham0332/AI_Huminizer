from pydantic import BaseModel, Field
from typing import Dict, List, Any

class WritingDNA(BaseModel):
    tone: Dict[str, Any] = Field(default_factory=lambda: {"dominant": "neutral", "range": ["neutral"]})
    formality: Dict[str, Any] = Field(default_factory=lambda: {"level": 0.5, "uses_contractions": True})
    directness: Dict[str, Any] = Field(default_factory=lambda: {"level": 0.5, "prefers_active_voice": True})
    sentence_length: Dict[str, Any] = Field(default_factory=lambda: {"avg": 15, "std_dev": 5, "range": [5, 30]})
    vocabulary: Dict[str, Any] = Field(default_factory=lambda: {"complexity": "moderate", "domain_terms": []})
    technicality: Dict[str, Any] = Field(default_factory=lambda: {"level": 0.5})
    paragraph_structure: Dict[str, Any] = Field(default_factory=lambda: {"avg_sentences": 4, "prefers_short": False})
    punctuation: Dict[str, Any] = Field(default_factory=lambda: {"uses_semicolons": False, "uses_dashes": False})
    transitions: Dict[str, Any] = Field(default_factory=lambda: {"frequency": "moderate", "preferred": []})
    first_person_usage: Dict[str, Any] = Field(default_factory=lambda: {"frequency": "rare", "prefers": "we"})
