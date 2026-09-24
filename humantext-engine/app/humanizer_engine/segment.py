from __future__ import annotations
import re

_ABBR = {"mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "etc", "fig", "no", "st", "inc", "ltd", "cf"}
_BOUNDARY = re.compile(r'[.!?]["\')\]”’]*\s+(?=[A-Z0-9"\'(\[“⟦])')
_WORD = re.compile(r"⟦E\d+⟧|[\w][\w’'-]*")


def split_paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in parts if p.strip()]


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    out, start = [], 0
    for m in _BOUNDARY.finditer(text):
        before = text[start:m.start() + 1]
        last = re.findall(r"([A-Za-z.]+)\.$", before)
        tok = last[-1].lower().strip(".") if last else ""
        if tok in _ABBR or (len(tok) == 1 and tok.isalpha()) or "." in tok:
            continue
        out.append(text[start:m.end()].strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return out


def words(text: str) -> list[str]:
    return _WORD.findall(text)


def is_structural(paragraph: str) -> bool:
    """Headings, list items, tables, code: never rewritten."""
    p = paragraph.lstrip()
    if p.startswith(("#", "|", ">", "```", "- ", "* ", "+ ")):
        return True
    if re.match(r"^\d+[.)]\s", p):
        return True
    lines = [l for l in paragraph.splitlines() if l.strip()]
    return len(lines) > 1 and all(re.match(r"^\s*([-*+]|\d+[.)])\s", l) for l in lines)
