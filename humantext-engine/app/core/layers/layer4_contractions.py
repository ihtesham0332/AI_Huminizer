"""
Layer 4: Universal Natural Contraction Enforcer Layer
Replaces stiff, uncontracted machine phrasing with fluid, natural human contractions.
"""
import re
from typing import List, Tuple

class ContractionsEnforcerLayer:
    """
    Enforces natural spoken contractions across all eligible verb forms.
    """

    CONTRACTION_RULES: List[Tuple[str, str]] = [
        # Negations
        (r'\bis not\b', "isn't"),
        (r'\bare not\b', "aren't"),
        (r'\bwas not\b', "wasn't"),
        (r'\bwere not\b', "weren't"),
        (r'\bcannot\b', "can't"),
        (r'\bcan not\b', "can't"),
        (r'\bcould not\b', "couldn't"),
        (r'\bdo not\b', "don't"),
        (r'\bdoes not\b', "doesn't"),
        (r'\bdid not\b', "didn't"),
        (r'\bwill not\b', "won't"),
        (r'\bwould not\b', "wouldn't"),
        (r'\bshould not\b', "shouldn't"),
        (r'\bmust not\b', "mustn't"),
        (r'\bhave not\b', "haven't"),
        (r'\bhas not\b', "hasn't"),
        (r'\bhad not\b', "hadn't"),

        # Pronoun + Auxiliaries
        (r'\bit is\b', "it's"),
        (r'\bthat is\b', "that's"),
        (r'\bthere is\b', "there's"),
        (r'\bwhat is\b', "what's"),
        (r'\bwho is\b', "who's"),
        (r'\bhere is\b', "here's"),
        (r'\bI am\b', "I'm"),
        (r'\bwe are\b', "we're"),
        (r'\bthey are\b', "they're"),
        (r'\byou are\b', "you're"),
        (r'\bI have\b', "I've"),
        (r'\bwe have\b', "we've"),
        (r'\bthey have\b', "they've"),
        (r'\byou have\b', "you've"),
        (r'\bI would\b', "I'd"),
        (r'\bwe would\b', "we'd"),
        (r'\bthey would\b', "they'd"),
        (r'\byou would\b', "you'd"),
        (r'\bI will\b', "I'll"),
        (r'\bwe will\b', "we'll"),
        (r'\bthey will\b', "they'll"),
        (r'\byou will\b', "you'll"),
        (r'\bit will\b', "it'll"),
        (r'\bthat will\b', "that'll"),
    ]

    @classmethod
    def apply(cls, text: str) -> str:
        """
        Executes Layer 4 contraction enforcement.
        Preserves capitalisation when matched at sentence start.
        """
        if not text or not text.strip():
            return text

        result = text
        for pattern, replacement in cls.CONTRACTION_RULES:
            # Match case-insensitively and preserve starting capital if applicable
            def replace_with_case(match):
                word = match.group(0)
                if word[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement

            result = re.sub(pattern, replace_with_case, result, flags=re.IGNORECASE)

        return result
