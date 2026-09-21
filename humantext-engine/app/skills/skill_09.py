from typing import Dict, Any, List
from pydantic import BaseModel, Field

class Operation(BaseModel):
    action: str = Field(description="e.g., split_sentence, rewrite_paragraph, change_tone")
    target: str = Field(description="The specific paragraph or sentence index, or 'global'")
    instruction: str = Field(description="Detailed instruction for the transformation agent")

class TransformationPlan(BaseModel):
    operations: List[Operation] = Field(default_factory=list, description="Ordered list of transformation operations")
    global_constraints: List[str] = Field(default_factory=list, description="Rules to observe across all operations")

def generate_plan(analysis_results: Dict[str, Any], llm_client: Any = None) -> Dict[str, Any]:
    """
    Skill 09: Humanization Planning
    Generates a structured transformation plan based on all prior analysis results.
    
    Args:
        analysis_results: A dictionary containing all prior analysis (style, context, readability, etc.)
        llm_client: Optional LLM client to generate the plan.
        
    Returns:
        A dictionary representing the TransformationPlan.
    """
    if not analysis_results:
        return TransformationPlan().model_dump()
        
    if llm_client is None:
        # Mock logic
        plan = TransformationPlan(
            operations=[
                Operation(action="rewrite_paragraph", target="0", instruction="Simplify vocabulary")
            ],
            global_constraints=["Preserve facts"]
        )
        return plan.model_dump()
        
    try:
        response = llm_client.invoke({"analysis": analysis_results})
        if hasattr(response, "model_dump"):
            return response.model_dump()
        elif isinstance(response, dict):
            return TransformationPlan(**response).model_dump()
    except Exception:
        pass
        
    return TransformationPlan().model_dump()
