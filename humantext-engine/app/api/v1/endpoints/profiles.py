from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.agents.dna_extractor import DNAExtractorAgent
# In production, we would inject the DB session here
# from app.db.session import get_db

router = APIRouter()
dna_extractor = DNAExtractorAgent()

class ProfileCreateRequest(BaseModel):
    profile_name: str
    samples: List[str]

class ProfileResponse(BaseModel):
    profile_name: str
    dna_data: Dict[str, Any]

@router.post("/profiles", response_model=ProfileResponse)
async def create_profile(request: ProfileCreateRequest):
    """
    Generates a new Personal Writing DNA profile from text samples.
    """
    if len(request.samples) < 1:
        raise HTTPException(status_code=400, detail="At least one text sample is required.")
        
    if len(request.samples) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 text samples allowed.")
        
    # Run the DNA Extractor
    dna_data = dna_extractor.extract_dna(request.samples)
    
    # In production:
    # 1. Fetch user_id from JWT token
    # 2. Insert into PostgreSQL: 
    # db.add(WritingProfile(user_id=user_id, profile_name=request.profile_name, dna_data=dna_data))
    
    return ProfileResponse(
        profile_name=request.profile_name,
        dna_data=dna_data
    )

@router.get("/profiles", response_model=List[ProfileResponse])
async def get_profiles():
    """
    Returns all Writing DNA profiles for the authenticated user.
    """
    # Mock response for architecture skeleton
    mock_dna = {
        "top_transitions": ["furthermore", "thus"],
        "complexity": "high",
        "avg_sentence_length": 24.5,
        "formality_score": 8.0,
        "preferred_voice": "active"
    }
    
    return [
        ProfileResponse(profile_name="Academic Thesis", dna_data=mock_dna)
    ]
