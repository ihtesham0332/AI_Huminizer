from typing import Dict, Any

class PromptBuilder:
    """
    Responsible for constructing the LLM prompts by injecting 
    the Personal Writing DNA and Guardian Constraints.
    """
    
    @staticmethod
    def build_generation_prompt(
        original_text: str, 
        dna_profile: Dict[str, Any], 
        facts: list, 
        citations: list,
        critique: str = None
    ) -> str:
        """
        Builds the system and user prompt for the model router.
        """
        
        prompt = "You are an expert editor. Rewrite the following text to improve flow and readability.\n\n"
        
        # Inject DNA Constraints
        prompt += "### STYLE CONSTRAINTS ###\n"
        prompt += "You MUST adopt the following stylistic fingerprint:\n"
        prompt += f"- Target Formality (1-10): {dna_profile.get('formality_score', 5)}\n"
        prompt += f"- Sentence Complexity: {dna_profile.get('complexity', 'medium')}\n"
        
        transitions = dna_profile.get('top_transitions', [])
        if transitions:
            prompt += f"- Preferred Transitions: {', '.join(transitions)}\n"
            
        # Inject Guardian Constraints
        prompt += "\n### INTEGRITY CONSTRAINTS ###\n"
        if facts:
            fact_list = ", ".join([f["value"] for f in facts])
            prompt += f"- YOU MUST RETAIN THE FOLLOWING EXACT NUMBERS AND DATES: {fact_list}\n"
            
        if citations:
            cite_list = ", ".join([c["value"] for c in citations])
            prompt += f"- YOU MUST RETAIN THE FOLLOWING EXACT CITATIONS: {cite_list}\n"
            
        # Revision Loop Logic
        if critique:
            prompt += f"\n### CRITICAL REVISION REQUIREMENT ###\n"
            prompt += f"Your previous attempt failed. Reason: {critique}\n"
            prompt += "Fix this error immediately in this generation.\n"
            
        prompt += f"\n### ORIGINAL TEXT ###\n{original_text}\n\n"
        prompt += "### REWRITTEN TEXT ###\n"
        
        return prompt
