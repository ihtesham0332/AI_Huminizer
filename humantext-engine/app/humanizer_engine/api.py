from __future__ import annotations
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import TONES
from .pipeline import HumanizerEngine
from .providers import AnthropicProvider, MockProvider


class HumanizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=60_000)
    level: int = Field(3, ge=1, le=5)
    tone: str = "standard"
    voice_sample: str | None = Field(None, max_length=20_000)


def create_app(engine: HumanizerEngine | None = None) -> FastAPI:
    if engine is None:
        provider = AnthropicProvider() if os.environ.get("ANTHROPIC_API_KEY") else MockProvider()
        engine = HumanizerEngine(provider)
    app = FastAPI(title="Humanizer Engine", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "provider": engine.provider.name}

    @app.post("/v1/humanize")
    async def humanize(req: HumanizeRequest):
        if req.tone not in TONES:
            raise HTTPException(422, f"tone must be one of {sorted(TONES)}")
        res = await engine.humanize(req.text, level=req.level, tone=req.tone, voice_sample=req.voice_sample)
        return res.to_dict()

    return app
