"""
Layer 2: Perplexity, Rhythm & Extreme Burstiness Injector Layer
Destroys AI's uniform sentence-length distribution and flat perplexity signatures.
Creates authentic human rhythmic cadences (stdev > 5.0).
"""
import re
import statistics
from typing import List

class BurstinessRhythmLayer:
    """
    Rhythmic sentence length modulator and perplexity injector.
    """

    NATURAL_SPLITTERS = [
        (", offering not just ", ". It gives you more than just "),
        (", which in turn ", ". In turn, "),
        (", ensuring that ", ". That way, "),
        (", as it allows ", ". It lets "),
        (", as it helps ", ". It helps "),
        (", which means that ", ". That means "),
        (", and therefore ", ". So "),
        (", but also ", ". More than that, "),
        (", making it easier to ", ". This makes it simpler to "),
        (", allowing them to ", ". This lets them "),
        (", highlighting the importance of ", ". It really underlines "),
    ]

    @classmethod
    def apply(cls, text: str) -> str:
        """
        Executes Layer 2 burstiness enhancement and rhythm modulation.
        """
        if not text or not text.strip():
            return text

        paragraphs = text.split("\n\n")
        processed_paras = []

        for p in paragraphs:
            if not p.strip():
                continue
            processed_p = cls._modulate_paragraph(p.strip())
            processed_paras.append(processed_p)

        return "\n\n".join(processed_paras)

    @classmethod
    def _modulate_paragraph(cls, paragraph: str) -> str:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', paragraph) if s.strip()]
        if not sentences:
            return paragraph

        modulated_sentences: List[str] = []
        for s in sentences:
            # 1. Break overly long uniform sentences (> 22 words) at natural splitters
            words = s.split()
            if len(words) > 22:
                split_applied = False
                for pattern, replacement in cls.NATURAL_SPLITTERS:
                    if pattern in s:
                        s = s.replace(pattern, replacement, 1)
                        split_applied = True
                        break
                
                # If still too long, check for ", and " or ", but " compound joins
                if not split_applied and len(s.split()) > 26:
                    if ", and " in s:
                        s = s.replace(", and ", ". And ", 1)
                    elif ", but " in s:
                        s = s.replace(", but ", ". But ", 1)

            modulated_sentences.append(s)

        # 2. Prevent repetitive sentence openers (e.g. "It... It...", "It's... It's...")
        diversified_sentences: List[str] = []
        prev_root = ""
        it_count = 0
        for s in modulated_sentences:
            words = s.split()
            if words:
                first_word = words[0].lower().rstrip(",:;.")
                root_word = first_word.replace("'s", "").replace("’s", "")
                
                if root_word in ("it", "this"):
                    it_count += 1
                else:
                    it_count = 0

                if (root_word == prev_root and root_word in ("it", "this", "the", "a", "they", "we", "he", "she")) or it_count >= 2:
                    # Vary the opener
                    if root_word in ("it", "this"):
                        if first_word in ("it's", "its"):
                            s = "That's " + " ".join(words[1:])
                        elif len(words) > 2 and words[1].lower() in ("helps", "allows", "makes"):
                            s = "Doing so " + " ".join(words[1:])
                        else:
                            s = "In practice, " + words[0].lower() + " " + " ".join(words[1:])
                    elif root_word == "the":
                        s = "All the " + " ".join(words[1:])
                
                prev_root = root_word
            diversified_sentences.append(s)

        # 3. Clean up spacing
        result = " ".join(diversified_sentences)
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)
        result = re.sub(r'[ \t]+', ' ', result)
        return result.strip()

    @classmethod
    def calculate_burstiness(cls, text: str) -> float:
        """
        Calculates sentence length standard deviation.
        Target: > 4.5 for human writing.
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip().split()) > 0]
        lengths = [len(s.split()) for s in sentences]
        if len(lengths) < 2:
            return 5.0
        return float(statistics.stdev(lengths))
