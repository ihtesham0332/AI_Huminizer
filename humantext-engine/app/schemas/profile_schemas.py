from pydantic import BaseModel, Field
from typing import List, Optional

class WritingProfileBase(BaseModel):
    profile_name: str = Field(..., description="Name of the profile, e.g., 'Academic Voice'")
    formality_score: float = Field(0.5, description="0.0 = Casual, 1.0 = Highly Formal")
    vocabulary_complexity: float = Field(0.5, description="0.0 = Simple, 1.0 = Complex")
    preferred_transitions: List[str] = Field(default_factory=list)

class WritingProfileCreate(BaseModel):
    profile_name: str
    samples: List[str] = Field(..., description="3 to 5 writing samples from the user")

class WritingProfileDB(WritingProfileBase):
    id: str
    user_id: str
    # In a real pgvector implementation, this would be a List[float] representing the embedding
    style_embedding: Optional[List[float]] = None 
