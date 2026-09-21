# ✨ HumanText Engine

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![LangGraph](https://img.shields.io/badge/LangGraph-AI-purple)

**HumanText Engine** is an advanced, multi-agent AI orchestration system designed to completely humanize robotic, AI-generated text. Powered by local LLMs (Qwen 2.5) and orchestrated via LangGraph, this system is engineered to bypass all commercial AI detectors (Turnitin, GPTZero, Originality.ai) by injecting maximum burstiness, high lexical perplexity, and psychological writing frameworks.

## 🚀 Key Features (v1.0.0)

- **Local Privacy**: Runs 100% locally via Ollama. No data is sent to external servers.
- **LangGraph Multi-Agent Architecture**: Uses an Input Validator, Rewriter, Semantic Guardian, Fact Guardian, and a Revision Agent for deep quality control.
- **Detector Bypass Protocols**: Strict prompts enforce pacing variations (burstiness) and ban common AI vocabulary (perplexity).
- **Structural Preservation**: Perfectly maintains document outlines, markdown, and line breaks while only replacing words.
- **"Obsidian Glass" UI**: A breathtaking, highly responsive Next.js frontend built with pure Vanilla CSS, featuring live scoring rings and typewriter micro-animations.

## 📁 Repository Structure

The project is split into two independent services:

- `/humantext-engine`: The FastAPI & LangGraph backend.
- `/humantext-ui`: The Next.js 14 frontend.

## 🛠️ Installation & Setup

### 1. Backend (FastAPI + LangGraph)
Make sure you have Ollama installed and the `qwen2.5:3b` model downloaded (`ollama run qwen2.5:3b`).

```bash
cd humantext-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (Next.js)
```bash
cd humantext-ui
npm install
npm run dev
```
Navigate to [http://localhost:3000](http://localhost:3000) to use the UI.

## 🔮 Roadmap (v2.0)
- True Real-Time SSE Token Streaming
- Visual "Diff" Word-by-Word Highlighting
- Bypass Strength Slider
- PDF/Word Document Bulk Uploads
- Multi-Model LLM Routing

---
*Built for absolute text humanization perfection.*
