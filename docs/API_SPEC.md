# API Specification
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document outlines the core RESTful endpoints for the backend service. All endpoints fall under `/api/v1/`.

## 1. Humanization & Processing
**`POST /api/v1/humanize`**
*   **Description:** Submits a document for full agentic humanization. For large documents, this is asynchronous.
*   **Payload:** `{"text": "...", "profile_id": "uuid", "strength": "balanced", "preserve_citations": true}`
*   **Response:** `{"job_id": "uuid", "status": "queued"}`

**`GET /api/v1/jobs/{job_id}`**
*   **Description:** Polls the status of the LangGraph workflow.
*   **Response:** `{"status": "processing", "current_agent": "QualityCritic", "progress": 75}`

**`POST /api/v1/analyze`**
*   **Description:** Synchronous endpoint to get the diagnostic breakdown (Input Analyzer, Style Analyzer) without rewriting the text.
*   **Response:** `{"word_count": 500, "content_type": "academic", "detected_facts": ["2026", "GPT-5"]}`

## 2. Writing Profiles
**`POST /api/v1/style-profile`**
*   **Description:** Upload 3-5 writing samples to generate a new vector-based writing profile.
*   **Payload:** `{"name": "Academic", "samples": ["text1", "text2", "text3"]}`
*   **Response:** `{"profile_id": "uuid", "metrics": {"formality": 0.8}}`

**`GET /api/v1/style-profile`**
*   **Description:** Retrieve all writing profiles for the authenticated user.

## 3. Document Management
**`GET /api/v1/documents`**
*   **Description:** Retrieve paginated list of user documents.

**`GET /api/v1/documents/{document_id}/versions`**
*   **Description:** Retrieve all humanized iterations of a specific document, including their QA Evaluation scores.

## 4. MCP Integration (Machine Context Protocol)
**`POST /api/v1/mcp/execute`**
*   **Description:** A dedicated standardized endpoint for agent-to-agent communication, allowing external LLMs to trigger tools like `humanize_text` or `check_grammar` directly on this platform.
