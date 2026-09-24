# ✨ HumanText Engine: The Agentic Anti-Detection Platform (v3.0)

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![LangGraph](https://img.shields.io/badge/LangGraph-AI-purple)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-orange)

**HumanText Engine** has evolved from a basic text rewriter into an enterprise-grade, multi-agent AI orchestration platform. Operating 100% locally for absolute data privacy, this system is engineered to not only bypass commercial AI detectors but to completely dominate competitor tools (like StealthWriter) through advanced linguistic frameworks, multi-agent reflection, and deep UI integrations.

---

## 🏗️ System Architecture: The LangGraph Brain

The core of the HumanText Engine is a cyclical state machine built on **LangGraph**. It abandons the traditional "single-prompt" approach in favor of a massive **Multi-Agent Workflow**:

1. **Input Analyzer**: Parses raw text, `.docx`, and `.pdf` files, dynamically detecting the language and extracting stylistic DNA (e.g., Academic vs. Casual).
2. **The Guardians (Fact & Citation)**: Critical factual data (numbers, dates, URLs) and academic citations (APA, IEEE) are extracted via Regex and locked into the LangGraph state. The LLM is strictly forbidden from altering them.
3. **Humanization Planner**: Determines the exact blueprint (e.g., "high sentence variation, low vocabulary change") based on the selected `strength` parameter (Ninja, Balanced, Ghost).
4. **Parallel Humanizer**: To reduce latency, `ThreadPoolExecutor` triggers multiple LLM generations simultaneously, yielding 3 distinct candidates.
5. **Quality Critic & Semantic Checker**: Evaluates all 3 candidates. If a candidate flips a negation ("does not") or loses a protected fact, the Critic rejects it and triggers a rewrite loop (max 3 iterations).

---

## ⚔️ Competitor Dominance (Phase 3 Features)

To beat existing tools on the market, we implemented a suite of advanced features:

- **Ninja vs Ghost Toggles:** Users can dynamically control the rewriting intensity via the API (`strength="light" | "aggressive"`).
- **Multiple Candidates:** The backend generates up to 3 variations, allowing the user to select their preferred phrasing.
- **Interactive "Deep Scan" Rewriting:** A micro-endpoint (`/api/v1/sentence`) allows users to send a single problematic sentence and instantly receive 3 localized, highly specific alternatives.
- **Personal Writing Profiles:** The system can analyze 3-5 writing samples to extract a user's unique stylistic vector (formality, vocabulary complexity) to enforce upon the generated output.

---

## 🌐 The Chrome Extension

HumanText is no longer confined to localhost. We built a lightweight **Manifest V3 Chrome Extension**.

*   **Functionality:** Highlight text on *any* webpage (Google Docs, Medium, ChatGPT), click the extension, select your rewrite strength (Ninja/Ghost), and instantly humanize the text via your local FastAPI server.
*   **Installation:** 
    1. Navigate to `chrome://extensions/`.
    2. Enable "Developer mode".
    3. Click "Load unpacked" and select the `humantext-extension` directory.

---

## 💻 Technology Stack

### Backend (`/humantext-engine`)
- **FastAPI**: Asynchronous web framework for high-throughput API routing.
- **LangGraph & LangChain**: State machine orchestration for the multi-agent cyclical workflow.
- **Ollama**: Local execution of quantized models (`qwen2.5:3b`) ensuring zero API costs.
- **PyTest**: Evaluation frameworks for mathematical A/B testing against baseline LLMs.

### Frontend (`/humantext-ui`)
- **Next.js 14 (App Router)**: React framework for the user interface.
- **AdvancedWorkspace.tsx**: A powerful React component featuring multi-candidate tabs, real-time job polling, and direct UI feedback from the Agentic Quality Critic.

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
pip install langgraph pypdf2 python-docx

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
*Developed by ihtesham0332. The ultimate anti-detection pipeline.*
