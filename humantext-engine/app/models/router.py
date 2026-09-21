def get_model_for_task(task_type: str) -> str:
    """
    Routes the task to the appropriate model tier.
    """
    strong_tasks = ["planning", "rewriting", "semantic_validation", "revision", "quality_judgment"]
    light_tasks = ["document_analysis", "style_analysis", "context_analysis", "fact_validation", "style_validation"]
    
    if task_type in strong_tasks:
        return "gpt-4o"
    return "gpt-4o-mini"
