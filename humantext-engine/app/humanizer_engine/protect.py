"""Entity protection: mask facts the rewrite must never alter, restore afterwards."""
from __future__ import annotations
import re
from collections import Counter

_MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
_PATTERNS = [
    ("code",    r"```.*?```|`[^`\n]+`"),
    ("url",     r"https?://[^\s)>\]]+"),
    ("email",   r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    ("cite_n",  r"\[\d+(?:\s*[,–-]\s*\d+)*\]"),
    ("cite_a",  r"\((?:[A-Z][A-Za-z'’-]+)(?:\s+(?:et al\.|and|&)\s*[A-Z]?[A-Za-z'’-]*)?,?\s+\d{4}[a-z]?\)"),
    ("quote",   r"“[^”]+”|\"[^\"\n]+\""),
    ("money",   r"[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand|trillion|[kKmMbB]\b))?"),
    ("percent", r"\d+(?:\.\d+)?\s?%"),
    ("date",    rf"\b{_MONTH}\s+\d{{1,2}}(?:,\s*\d{{4}})?\b|\b\d{{4}}-\d{{2}}-\d{{2}}\b"),
    ("number",  r"\b\d[\d,]*(?:\.\d+)?\b"),
]
_MASK_RE = re.compile("|".join(f"(?P<{k}>{v})" for k, v in _PATTERNS), re.DOTALL)

PLACEHOLDER = "⟦E{}⟧"
# Tolerant matcher for placeholders an LLM may have slightly mangled.
_PH_LOOSE = re.compile(r"[⟦\[]{1,2}\s*E\s*(\d+)\s*[⟧\]]{1,2}")
_PH_STRICT = re.compile(r"⟦E(\d+)⟧")


class EntityMasker:
    def __init__(self) -> None:
        self.entities: dict[int, tuple[str, str]] = {}
        self._by_value: dict[str, int] = {}

    def mask(self, text: str) -> str:
        def repl(m: re.Match) -> str:
            val = m.group(0)
            if val not in self._by_value:
                idx = len(self.entities)
                self._by_value[val] = idx
                self.entities[idx] = (m.lastgroup or "x", val)
            return PLACEHOLDER.format(self._by_value[val])
        return _MASK_RE.sub(repl, text)

    @staticmethod
    def normalize(text: str) -> str:
        """Canonicalise mangled placeholders such as [[E3]] or ⟦ E3 ⟧."""
        return _PH_LOOSE.sub(lambda m: PLACEHOLDER.format(m.group(1)), text)

    @staticmethod
    def counts(text: str) -> Counter:
        return Counter(_PH_STRICT.findall(text))

    def unmask(self, text: str) -> str:
        text = self.normalize(text)
        return _PH_STRICT.sub(lambda m: self.entities[int(m.group(1))][1], text)

    @staticmethod
    def strip_placeholders(text: str) -> str:
        return _PH_STRICT.sub(" ", text)
