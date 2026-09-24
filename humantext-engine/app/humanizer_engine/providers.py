from __future__ import annotations
import hashlib
import os
import random
import re
from typing import Protocol

from .lexicon import STOCK_REPLACEMENTS, TRANSITIONS
from .segment import split_sentences


class Provider(Protocol):
    name: str
    async def complete(self, system: str, user: str, *, temperature: float,
                       max_tokens: int, seed: int = 0) -> str: ...


class AnthropicProvider:
    """Production provider. Set ANTHROPIC_API_KEY. Model is configurable."""
    def __init__(self, model: str = "claude-sonnet-5", api_key: str | None = None) -> None:
        import anthropic
        self.name = f"anthropic:{model}"
        self.model = model
        self._client = anthropic.AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    async def complete(self, system, user, *, temperature, max_tokens, seed=0) -> str:
        resp = await self._client.messages.create(
            model=self.model, max_tokens=max_tokens, temperature=min(temperature, 1.0),
            system=system, messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


class OllamaProvider:
    """Local provider using Ollama (llama3.1:8b 4-bit quantized, with fallbacks)."""
    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        self.model = model or os.getenv("OLLAMA_PRIMARY_MODEL", "llama3.1:8b")
        self.fallback_models = [os.getenv("OLLAMA_FALLBACK_MODEL", "qwen2.5:7b"), "qwen2.5:3b"]
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.name = f"ollama:{self.model}"

    async def complete(self, system: str, user: str, *, temperature: float, max_tokens: int, seed: int = 0) -> str:
        import httpx
        models_to_try = [self.model] + [m for m in self.fallback_models if m != self.model]
        last_err = None
        async with httpx.AsyncClient(base_url=self.base_url, timeout=120.0) as client:
            for m in models_to_try:
                try:
                    payload = {
                        "model": m,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user}
                        ],
                        "options": {
                            "temperature": min(max(temperature, 0.1), 1.0),
                            "top_p": 0.92,
                            "seed": seed
                        },
                        "stream": False
                    }
                    res = await client.post("/api/chat", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        content = data.get("message", {}).get("content", "").strip()
                        if content:
                            return content
                except Exception as e:
                    last_err = e
                    continue
        if last_err:
            raise last_err
        return ""



def _match_case(src: str, repl: str) -> str:
    if not repl:
        return repl
    return repl[0].upper() + repl[1:] if src[:1].isupper() else repl


class MockProvider:
    """Deterministic rule-based rewriter for tests, CI, and offline demos.

    NOT a quality model: it applies the same lexicon edits and structural moves the
    planner asks an LLM to make, so the *pipeline* can be exercised end to end.
    """
    name = "mock"

    _SPLIT = re.compile(r",\s+(and|but|while|which)\s+|;\s+")

    async def complete(self, system, user, *, temperature, max_tokens, seed=0) -> str:
        m = re.search(r"<<<PARAGRAPH\n(.*?)\nPARAGRAPH>>>", user, re.DOTALL)
        para = m.group(1) if m else user
        rng = random.Random(int(hashlib.md5(f"{para}{temperature}{seed}".encode()).hexdigest(), 16))
        # 1. stock phrase replacement (longest first)
        for k in sorted(STOCK_REPLACEMENTS, key=len, reverse=True):
            pat = re.compile(re.escape(k), re.IGNORECASE)
            para = pat.sub(lambda mm: _match_case(mm.group(0), STOCK_REPLACEMENTS[k]), para)
        sents = split_sentences(para)
        out = []
        for s in sents:
            # 2. drop leading transitions
            s = re.sub(r"^(?:%s),?\s+" % "|".join(re.escape(t) for t in TRANSITIONS), "", s, flags=re.IGNORECASE)
            s = s[:1].upper() + s[1:] if s else s
            # 3. sometimes split long sentences at a conjunction
            if len(s.split()) > 22 and rng.random() < 0.7:
                parts = self._SPLIT.split(s, maxsplit=1)
                if len(parts) >= 2:
                    head = parts[0].rstrip(",;") + "."
                    tail_words = parts[-1]
                    conj = parts[1] if len(parts) == 3 else ""
                    tail = (conj.capitalize() + " " + tail_words).strip() if conj in ("but",) else tail_words
                    s = head + " " + tail[:1].upper() + tail[1:]
            out.append(s)
        text = " ".join(out)
        text = re.sub(r"\s+([,.;!?])", r"\1", text)
        text = re.sub(r"\.\.+", ".", text)
        return text.strip()
