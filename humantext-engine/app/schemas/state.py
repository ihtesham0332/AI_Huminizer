from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class WritingDNAProfile(BaseModel):
    tone: Dict[str, Any] = Field(default_factory=dict)
    formality: Dict[str, Any] = Field(default_factory=dict)
    directness: Dict[str, Any] = Field(default_factory=dict)
    sentence_length: Dict[str, Any] = Field(default_factory=dict)
    vocabulary: Dict[str, Any] = Field(default_factory=dict)
    technicality: Dict[str, Any] = Field(default_factory=dict)
    paragraph_structure: Dict[str, Any] = Field(default_factory=dict)
    punctuation: Dict[str, Any] = Field(default_factory=dict)
    transitions: Dict[str, Any] = Field(default_factory=dict)
    first_person_usage: Dict[str, Any] = Field(default_factory=dict)

class AgentMetadata(BaseModel):
    agent_name: str
    status: str
    latency_ms: float = 0.0
    error: Optional[str] = None

class StateSchema(BaseModel):
    # Immutable (set once)
    request_id: str
    original_text: str
    document_type: str
    target_audience: Optional[str] = None
    target_tone: Optional[str] = None
    target_style: Optional[str] = None
    target_mode: str
    writing_dna_profile: Optional[WritingDNAProfile] = None

    # Mutable (agent-written)
    document_analysis: Dict[str, Any] = Field(default_factory=dict)
    semantic_analysis: Dict[str, Any] = Field(default_factory=dict)
    style_analysis: Dict[str, Any] = Field(default_factory=dict)
    context_analysis: Dict[str, Any] = Field(default_factory=dict)
    readability_analysis: Dict[str, Any] = Field(default_factory=dict)
    
    claims: List[Dict[str, Any]] = Field(default_factory=list)
    facts: Dict[str, Any] = Field(default_factory=dict)
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)
    
    transformation_plan: Dict[str, Any] = Field(default_factory=dict)
    rewritten_text: Optional[str] = None
    
    semantic_score: Optional[float] = None
    factual_score: Optional[float] = None
    style_score: Optional[float] = None
    readability_score: Optional[float] = None
    naturalness_score: Optional[float] = None
    quality_score: Optional[float] = None
    
    validation_errors: List[str] = Field(default_factory=list)
    revision_count: int = 0
    revision_history: List[Dict[str, Any]] = Field(default_factory=list)

    # Metadata
    status: str = "initialized"
    agent_metadata: Dict[str, AgentMetadata] = Field(default_factory=dict)
    model_metadata: Dict[str, Any] = Field(default_factory=dict)
    token_usage: Dict[str, int] = Field(default_factory=dict)
    latency: float = 0.0
    total_cost: float = 0.0
