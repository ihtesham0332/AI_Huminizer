# ✨ HumanText Engine: The Agentic Anti-Detection Pipeline

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![LangGraph](https://img.shields.io/badge/LangGraph-AI-purple)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-orange)

**HumanText Engine** is an enterprise-grade, multi-agent AI orchestration system designed to completely humanize robotic, AI-generated text. Operating 100% locally for absolute data privacy, this system is engineered to bypass all commercial AI detectors (e.g., Turnitin, GPTZero, Originality.ai) by deploying advanced linguistic frameworks, deep psychological writing constraints, and multi-agent reflection.

---

## 🏗️ System Architecture

The core of the HumanText Engine is a cyclical state machine built on **LangGraph**. It abandons the traditional "single-prompt" approach in favor of an **Agentic Workflow**.

### The Multi-Agent Pipeline

1. **Input Validator Node**: Performs lexical analysis and sanitizes input data. Extracts hard constraints (markdown formatting, line breaks, bullet points) that the engine is strictly forbidden from altering.
2. **Rewriter Node (The Ghostwriter)**: The primary generative node powered by the local LLM. It is strictly constrained by our **Anti-Detection Protocol** (see below).
3. **Semantic Guardian Node**: A deterministic safety layer that calculates cosine similarity between the original text and the rewritten text using lightweight embedding models. Ensures the core meaning has not drifted.
4. **Fact Guardian Node**: Extracts named entities, numerical claims, and citations from the source text and cross-references them against the generated output to prevent LLM hallucinations.
5. **Quality Judge Node**: Evaluates the output against strict thresholds for `QualityScore` and `NaturalnessScore`. If the text scores below the threshold (e.g., `0.75`), it dynamically triggers the...
6. **Revision Agent Node**: Receives the specific critique from the Quality Judge and re-processes the text to fix the identified flaws, looping back through the Guardians until the thresholds are met or a maximum revision limit is reached.

---

## 🛡️ Anti-Detection Protocol

To consistently achieve 0% AI detection scores, the `Rewriter Node` executes deep psychological formatting constraints rather than simple synonym swapping:

- **Maximum Burstiness (Pacing Constraints):** The LLM is forced to violently shatter uniform sentence structures. It operates on a strict rhythm: a punchy 3-word sentence, followed by an elegant, multi-clause compound sentence, followed by a medium-length assertion.
- **Extreme Lexical Perplexity:** We utilize a massive blacklist of statistical AI trigger words (e.g., *"delve", "testament", "crucial", "multifaceted", "moreover", "tapestry", "realm", "underscore"*). 
- **Asymmetrical Idiomatics:** The LLM is instructed to utilize rhetorical imperfections—such as em-dashes (—) and colloquial transitions—to mimic authentic human train-of-thought writing.

---

## ⚡ True Real-Time Streaming (Server-Sent Events)

Version 2.0 abandons traditional synchronous HTTP polling. 

The backend utilizes LangGraph's `.astream_events()` asynchronous generator to intercept LLM tokens at the exact millisecond they are inferred by the GPU/CPU. These tokens are piped through FastAPI via **Server-Sent Events (SSE)** directly to the Next.js React DOM, resulting in zero perceived latency and a true "ChatGPT-like" streaming experience.

---

## 💻 Technology Stack

### Backend (`/humantext-engine`)
- **FastAPI**: Asynchronous web framework for high-throughput API routing and SSE streaming.
- **LangGraph**: State machine orchestration for the multi-agent cyclical workflow.
- **LangChain**: LLM abstraction layer and PromptTemplate management.
- **Ollama**: Local execution of quantized models (Qwen2.5:3b) to ensure 100% data privacy and zero API costs.
- **PyTest**: Suite of 120+ unit tests validating 20 distinct linguistic sub-skills (TTR, Flesch-Kincaid, Entropy).

### Frontend (`/humantext-ui`)
- **Next.js 14 (App Router)**: React framework for the user interface.
- **Vanilla CSS (Obsidian Glass Theme)**: Custom-built, zero-bloat design system utilizing glassmorphism, dynamic gradients, and animated SVG Data Dials (`ScoreDial.tsx`).
- **Native Browser Fetch API**: Utilized to read and parse the `text/event-stream` chunks natively without heavy third-party libraries.

---

## 🚀 Installation & Setup

### 1. Requirements
- Python 3.11+
- Node.js 18+
- Ollama (with `qwen2.5:3b` pulled locally: `ollama run qwen2.5:3b`)

### 2. Run the Backend API
```bash
cd humantext-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start the FastAPI server on port 8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Run the Frontend UI
```bash
cd humantext-ui
npm install

# Start the Next.js Dev Server on port 3000
npm run dev
```

Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)** to experience the HumanText Engine.

---
*Developed by ihtesham0332. Built for absolute text humanization perfection.*
