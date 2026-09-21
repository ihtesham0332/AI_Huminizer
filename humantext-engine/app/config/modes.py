from enum import Enum

class RewriteMode(str, Enum):
    NATURAL_PROFESSIONAL = "natural_professional"
    ACADEMIC_NATURAL = "academic_natural"
    SIMPLE_CLEAR = "simple_clear"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    BUSINESS = "business"
    PERSONALIZED = "personalized"
    CUSTOM = "custom"

MODES_CONFIG = {
    RewriteMode.NATURAL_PROFESSIONAL: {"formality": "medium-high", "semantic_strictness": "high"},
    RewriteMode.ACADEMIC_NATURAL: {"formality": "high", "semantic_strictness": "highest"},
    RewriteMode.SIMPLE_CLEAR: {"formality": "low-medium", "semantic_strictness": "high"},
    RewriteMode.CONVERSATIONAL: {"formality": "low", "semantic_strictness": "medium"},
    RewriteMode.TECHNICAL: {"formality": "medium-high", "semantic_strictness": "highest"},
    RewriteMode.BUSINESS: {"formality": "medium", "semantic_strictness": "high"},
}
