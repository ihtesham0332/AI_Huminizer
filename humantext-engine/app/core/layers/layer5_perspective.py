"""
Layer 5: Pragmatic Perspective & Anti-Corporate Normalizer Layer
Removes robotic corporate flattery, gratitude boilerplate, social media hashtags,
and artificial closing formulas.
"""
import re
from typing import List, Tuple

class PragmaticPerspectiveLayer:
    """
    Normalizes tone to an authentic, grounded human perspective.
    """

    PRAGMATIC_PATTERNS: List[Tuple[str, str]] = [
        # Gratitude boilerplate
        (r'\b(?:Thanks|Thank you),\s*(?:Sir\s+|Mr\.\s+|Dr\.\s+)?([A-Za-z\s]+?),\s*for\s+[^.]*\.', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'\bThanks,\s*(.*?),\s*for (?:sharing\s+your\s+)?(?:valuable\s*)?(?:insights|knowledge|wisdom|thoughts)\s*(?:and\s*(?:experience|advice))?\.\s*', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'\bReally appreciated (.*?)\s*taking the time to share practical advice today\s*-\s*definitely gave me plenty to think about\.\s*', r'Really enjoyed the conversation - definitely gave me a lot to think over.'),
        (r'\bI am deeply grateful to\s+([^.]+)\.', r'Huge thanks to \1 for the chat.'),
        (r'\bI\'m deeply grateful to\s+([^.]+)\.', r'Huge thanks to \1 for the chat.'),
        (r'\bI\'m really grateful to\s+([^.]+)\.', r'Big thanks to \1.'),
        (r'\bdeeply grateful\b', 'really thankful'),

        # Artificial closers & slogans
        (r'\bHere’s to building a network that not only supports but also propels us forward\b', 'Looking forward to putting this into practice'),
        (r'\bHere\'s to building a network that not only supports but also propels us forward\b', 'Looking forward to putting this into practice'),
        (r'\bHis insights have been invaluable and have left a lasting impression\b', 'His advice really stuck with me and gave me a lot to think about'),
        (r'\bleft a lasting impression\b', 'really stuck with me'),
        (r'\bleft a lasting impact\b', 'gave me plenty to think about'),
        (r'\bThese good relationships can be incredibly valuable in various aspects of life\b', 'Having good relationships around you pays off in every area of life'),
        (r'\bcan be incredibly valuable in various aspects of life\b', 'makes a huge difference in both life and work'),
    ]

    @classmethod
    def apply(cls, text: str) -> str:
        """
        Executes Layer 5 pragmatic perspective normalization.
        """
        if not text or not text.strip():
            return text

        result = text.strip()

        # 1. Normalize unicode quotes, dashes, apostrophes to clean standard forms
        result = result.replace('’', "'").replace('‘', "'").replace('`', "'")
        result = result.replace('“', '"').replace('”', '"')
        result = result.replace('—', ' - ').replace('–', ' - ').replace('\ufffd', ' - ')

        # 2. Strip AI markdown fences or conversational prefaces
        result = re.sub(r'^(?:Here is (?:the )?(?:rewritten|humanized) (?:version|text|paragraph):?|Humanized (?:version|text):?)\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'^```(?:markdown)?\s*', '', result)
        result = re.sub(r'\s*```$', '', result)

        # 3. Strip all trailing and inline hashtags (#Word)
        result = re.sub(r'#\w+', '', result).strip()

        # 4. Strip standard AI closing boilerplate
        result = re.sub(r'(?:In closing|In summary|In conclusion),\s*I would like to emphasize.*$', '', result, flags=re.IGNORECASE | re.MULTILINE).strip()

        # 5. Apply pragmatic tone patterns
        for pattern, replacement in cls.PRAGMATIC_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # 6. Clean up residual introductory filler and deduplicate identical/redundant statements
        result = re.sub(r'\bWhat struck me was that\s+(A\s+lot of folks\b)', r'\1', result, flags=re.IGNORECASE)
        
        # Deduplicate sentences that express the exact same point redundantly
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', result) if s.strip()]
        deduped = []
        for s in sentences:
            s_lower = s.lower()
            if not any(s_lower == x.lower() or ('trust, respect' in s_lower and 'trust, respect' in x.lower()) for x in deduped):
                deduped.append(s)
        
        result = " ".join(deduped)
        return result.strip()
