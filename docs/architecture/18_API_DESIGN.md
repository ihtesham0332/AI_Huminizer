# 18. API DESIGN

The API is built using FastAPI (Python) and follows RESTful principles.

## Core Endpoints

### 1. Document Processing
*   `POST /api/v1/analyze`
    *   *Input:* Text or File.
    *   *Output:* Document metadata, word count, estimated cost, extracted facts.
*   `POST /api/v1/humanize` (Sync)
    *   *Input:* Text snippet, `mode` (fast/balanced/deep), `profile_id`.
    *   *Output:* Humanized text, Diff, Quality Scorecard.
*   `POST /api/v1/jobs` (Async)
    *   *Input:* Large PDF/DOCX file.
    *   *Output:* `job_id`.

### 2. Job Polling & Streaming
*   `GET /api/v1/jobs/{job_id}`
    *   *Output:* Current status (Analyzing, Protecting, Generating, Verifying).
*   `GET /api/v1/jobs/{job_id}/events` (Server-Sent Events)
    *   *Output:* Real-time stream of completed sentences to the UI.

### 3. Profiles & Settings
*   `POST /api/v1/profiles`
    *   *Input:* 5 text samples.
    *   *Output:* Generated Writing DNA Profile (JSON).
*   `GET /api/v1/profiles`
    *   *Output:* List of user's profiles.

## MCP Server (Model Context Protocol)
We will expose an `mcp_server.py` allowing local AI tools (like Claude Desktop) to call our internal engines programmatically.
*   *Exposed Tools:* `analyze_text`, `humanize_text`, `check_facts`.
