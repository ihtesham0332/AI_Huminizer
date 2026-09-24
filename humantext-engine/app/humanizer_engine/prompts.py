from __future__ import annotations
from .config import LevelSpec, TONES
from .models import Profile

SYSTEM = """You are an authentic, skilled human writer and line editor. You rewrite machine-drafted prose so it reads like genuine, natural human writing that scores 0% on all AI detectors (Quillbot, Turnitin, GPTZero, CopyLeaks).

STRICT HUMAN WRITING RULES:
1. Meaning & Entity Integrity: Preserve the core message exactly. Tokens like ⟦E12⟧ are protected entities (numbers, names, dates, citations). Copy each ⟦E#⟧ token exactly where it belongs without modifying or dropping it. Never invent new facts or numbers.
2. High Burstiness & Rhythm: Drastically vary sentence lengths. Real humans write with rhythmic contrast: include very short, punchy sentences (2-5 words, e.g., 'Most people overcomplicate it.', 'Trust is everything.') alongside natural conversational sentences. Vary how consecutive sentences begin.
3. Natural Contractions: Always use natural contractions (it's, don't, can't, wasn't, we're, I've) instead of stiff uncontracted phrasing.
4. Eliminate Formulaic AI Syntactic Patterns:
   - NEVER use introductory topic colons (e.g. 'on an important topic: Topic Name'). Say 'about [Topic]' instead.
   - NEVER use antithesis formulas (e.g. 'isn't just about X; it is about Y, Z, and W'). Say what it is directly or reframe the idea.
   - NEVER use 3- or 4-item brochure lists (e.g. 'whether it's for learning, career opportunities, guidance, or personal growth'). Real humans summarize the point in one natural thought.
   - NEVER write corporate gratitude closings (e.g. 'Thanks, [Name], for sharing your valuable knowledge and experience.'). Conclude naturally (e.g., 'Really enjoyed our chat—gave me a lot to think about.').
   - ABSOLUTELY NO HASHTAGS (#...) or social media tags anywhere.
5. Zero AI Stock Phrases: Never use words like 'delve', 'tapestry', 'testament', 'beacon', 'foster', 'enlightening', 'invaluable', 'robust', 'lifeline', 'pivotal', 'in essence', 'moreover', 'furthermore', 'in conclusion'.
6. Pure Output: Output ONLY the rewritten paragraph. No commentary, no preface, no markdown fences, no quotes."""


def build_user_prompt(paragraph: str, *, level: LevelSpec, tone: str, ops: list[str],
                      voice_hint: str, prev_ctx: str, next_ctx: str,
                      draft: str | None = None, issues: list[str] | None = None) -> str:
    parts = [f"Tone: {TONES.get(tone, TONES['standard'])}"]
    if voice_hint:
        parts.append(f"Match this writer's voice: {voice_hint}")
    parts.append(f"Rewrite strength: {level.name} (about {int(level.target_novelty*100)}% of the wording "
                 f"should change; meaning must not).")
    if ops:
        parts.append("Editing plan:\n" + "\n".join(f"- {o}" for o in ops))
    if prev_ctx:
        parts.append(f"Preceding paragraph (context only, do not rewrite):\n{prev_ctx}")
    if next_ctx:
        parts.append(f"Following paragraph (context only, do not rewrite):\n{next_ctx}")
    if draft is not None:
        parts.append("A previous attempt had these problems:\n" + "\n".join(f"- {i}" for i in (issues or [])))
        parts.append(f"Previous attempt:\n{draft}")
        parts.append("Fix only those problems and keep everything else that already works.")
        
    parts.append(
        "DEMONSTRATION OF AUTHENTIC HUMAN REWRITE (0% AI):\n"
        "AI Draft:\n"
        "\"Today, I had a great session with ⟦E0⟧ on an important topic: Productivity and Time. One thing I learned is that productivity isn't just about managing hours; it's about managing energy, setting boundaries, and staying focused. Good habits can really help in daily life—whether it's for work, study, health, or personal growth. True success is built on trust, respect, and consistency. Thanks, ⟦E0⟧, for sharing your valuable knowledge. #Productivity\"\n"
        "Humanized Version:\n"
        "\"Had a long chat with ⟦E0⟧ earlier about staying productive. Most people overcomplicate it. They treat it like a calendar puzzle, packing every minute with tasks. But real focus comes down to something simpler: protecting your energy and cutting out distractions. When you show up consistently each day, the bigger goals take care of themselves. Good conversation—definitely gave me plenty to think about.\""
    )
    
    parts.append(f"Original paragraph to rewrite:\n<<<PARAGRAPH\n{paragraph}\nPARAGRAPH>>>")
    return "\n\n".join(parts)
