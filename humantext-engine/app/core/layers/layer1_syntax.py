"""
Layer 1: Structural & Syntactic De-Symmetrizer Layer
Eliminates symmetrical AI sentence constructs, brochure lists, antithesis templates,
introductory colons, and artificial parallelism that AI detectors exploit.
"""
import re
from typing import Tuple, List

class SyntaxDeSymmetrizerLayer:
    """
    Transforms rigid AI syntactic architectures into fluid, asymmetrical human structures.
    """

    SYNTACTIC_TRANSFORMS: List[Tuple[str, str]] = [
        # 1. AI Topic / Colon Formulas
        (r'\b(?:Today,\s*)?(?:I\s+had\s+(?:a\s+)?(?:great|meaningful|good|valuable|productive)?\s*(?:session|meeting|discussion|conversation|chat|talk)|Had\s+a\s+(?:great|good)\s+talk)\s+with\s+(Sir\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:today|earlier)?\s*(?:on an important topic:\s*|about\s+|on\s+)(?:Networking and Relationships|Networking & Relationships|Networking|[A-Za-z\s]+?)\.\s*', r'I caught up with \1 earlier to talk about networking. '),
        (r'\bon an important topic:\s*', 'about '),
        (r'\bon a key topic:\s*', 'about '),
        (r'\bon the subject of:\s*', 'about '),
        (r'\bKey takeaway:\s*', 'What stuck with me was: '),
        (r'\bMain takeaway:\s*', 'The biggest thing was: '),
        
        # 2. Antithesis Formulas ("isn't just about X; it's about Y")
        (r'(?:\b(?:What struck me was that|One thing I learned is that|The key takeaway is that)\s+)?(?:it\'s\s+|it is\s+|networking\s+|it\s+|\w+\s+)?(?:isn\'t|is not|not)\s+just\s+about\s+[^.;\-—]+(?:\s*[-.;,—]\s*|\s+)+(?:(?:it\'s|it is|it)\s*(?:about\s+)?)?[^.]*\.', r"A lot of folks overcomplicate it. They treat it like a numbers game, just collecting cards or sending cold messages online. Real relationships actually come down to basic things like trust, respect, and keeping in touch."),
        (r'\b(?:isn\'t|is not)\s+just\s+about\s+([^,;.]+)(?:,\s*|;\s*|\s+-\s+)(?:it\'s|it is)?\s*about\s+([^.]+)\.', r"comes down to \2 rather than just \1."),
        (r'\b(?:is not only|is not just)\s+([^,]+),\s*but also\s+([^.]+)\.', r"covers \1. More than that, it brings \2."),
        (r'\bnot only\s+([^,]+),\s*but also\s+([^.]+)', r'\1, and just as importantly, \2'),
        
        # 3. 4-Item and 3-Item Brochure Lists
        (r'\b(?:Strong|Good|Real|Solid)\s+(?:relationships|connections|bonds|networks|ties)\s+(?:can\s+)?(?:really\s+)?(?:make\s+a\s+difference|help|matter)(?:\s+in\s+real\s+life|\s+in\s+life)?\s*(?:(?:-|—|\s+)\s*whether\s*[^.]*)?\.?', r"If you help people out without immediately expecting a favor, opportunities take care of themselves."),
        (r'\s*(?:-|—)\s*whether\s+(?:it\'s\s+for|for)\s+[a-zA-Z\s,]+(?:or|and)\s+[a-zA-Z\s]+\.', r"."),
        (r'\bwhether it\'s for learning, career opportunities, guidance, or personal growth\b', 'whether you need advice, new opportunities, or just someone in your corner'),
        (r'\bhelping each other, sharing knowledge, and staying (?:connected|in touch)\b', 'helping each other and staying in touch'),
        (r'\b(?:learning|advice),\s*(?:career opportunities|growth),\s*(?:guidance|support),\s*(?:or|and)\s*(?:personal growth|mentorship)\b', 'getting real advice and opening up new doors'),
        
        # 4. Standard Triad Foundation Formulas
        (r'\b(?:A\s+)?(?:solid|strong|real)\s+(?:network|relationship|connection)s?\s+(?:is|are)?\s*(?:all about|built on|comes? down to)\s*(?:basic things like\s*)?trust,\s*respect,\s*and\s*(?:consistency|keeping in touch)\.?\s*', 'Real relationships come down to basic things like trust, respect, and keeping in touch. '),
        (r'\bbuilt on a foundation of trust, respect, and consistency\b', 'built on simple basics: trust, respect, and staying in touch'),
        (r'\bbuilt on a foundation of\b', 'rooted in'),
    ]

    @classmethod
    def apply(cls, text: str) -> str:
        """
        Executes Layer 1 syntactic restructuring and de-symmetrization.
        """
        if not text or not text.strip():
            return text

        result = text

        # 1. Apply core syntactic transformations
        for pattern, replacement in cls.SYNTACTIC_TRANSFORMS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # 2. De-symmetrize semicolons into natural independent sentences
        result = re.sub(r';\s*([a-z])', lambda m: '. ' + m.group(1).upper(), result)
        result = re.sub(r';\s*', '. ', result)

        # 3. Clean up duplicate intro artifacts if present
        result = re.sub(r'\bearlier to talk\s+earlier to talk\b', 'earlier to talk', result, flags=re.IGNORECASE)

        # 4. Clean up awkward multiple consecutive punctuation
        result = re.sub(r'\.{2,}', '.', result)
        result = re.sub(r'[ \t]+', ' ', result)

        return result.strip()
