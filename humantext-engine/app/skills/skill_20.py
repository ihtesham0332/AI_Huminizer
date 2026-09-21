from typing import Dict, Any, List
from pydantic import BaseModel, Field

class RevisionPlan(BaseModel):
    instructions: List[str] = Field(default_factory=list, description="Specific instructions for the AI to fix the text")

def generate_revision_instructions(failed_validations: List[Dict[str, Any]], original_text: str, transformed_text: str, llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 20: Revision Instruction Generation
    Generates specific revision instructions if validation fails.
    
    Args:
        failed_validations: List of validation result dictionaries that failed.
        original_text: The original text.
        transformed_text: The current transformed text that failed validation.
        llm_client: Optional LLM client to generate the instructions.
        
    Returns:
        A dictionary representing the RevisionPlan.
    """
    if not failed_validations:
        return RevisionPlan(instructions=[]).model_dump()
        
    if llm_client is None:
        # Mock logic based on failed reasoning
        instructions = [f"Fix issue: {val.get('reasoning', 'Unknown')}" for val in failed_validations]
        return RevisionPlan(instructions=instructions).model_dump()
        
    try:
        response = llm_client.invoke({
            "failures": failed_validations, 
            "original": original_text, 
            "transformed": transformed_text
        })
        if hasattr(response, "model_dump"):
            return response.model_dump()
        elif isinstance(response, dict):
            return RevisionPlan(**response).model_dump()
    except Exception:
        pass
        
    return RevisionPlan(instructions=["Please revise the text."]).model_dump()
