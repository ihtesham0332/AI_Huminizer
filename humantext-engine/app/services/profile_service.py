import uuid
from typing import List
from app.schemas.profile_schemas import WritingProfileCreate, WritingProfileDB

class ProfileService:
    """
    Mock service layer simulating a PostgreSQL + pgvector database for Writing Profiles.
    """
    def __init__(self):
        self._db = {}
        
    def analyze_samples(self, samples: List[str]) -> dict:
        """
        Simulates an LLM/Embedding model analyzing the text samples 
        to extract the stylistic DNA.
        """
        # In production, this would call `text-embedding-3-small` or an NLP heuristic
        return {
            "formality_score": 0.8,
            "vocabulary_complexity": 0.7,
            "preferred_transitions": ["Furthermore", "Consequently", "However"],
            "style_embedding": [0.012, -0.054, 0.103] * 512 # Mock 1536-dim vector
        }

    def create_profile(self, user_id: str, profile_in: WritingProfileCreate) -> WritingProfileDB:
        analysis = self.analyze_samples(profile_in.samples)
        
        new_profile = WritingProfileDB(
            id=str(uuid.uuid4()),
            user_id=user_id,
            profile_name=profile_in.profile_name,
            formality_score=analysis["formality_score"],
            vocabulary_complexity=analysis["vocabulary_complexity"],
            preferred_transitions=analysis["preferred_transitions"],
            style_embedding=analysis["style_embedding"]
        )
        
        self._db[new_profile.id] = new_profile
        return new_profile

    def get_profile(self, profile_id: str) -> WritingProfileDB:
        return self._db.get(profile_id)

# Singleton for testing
profile_db = ProfileService()
