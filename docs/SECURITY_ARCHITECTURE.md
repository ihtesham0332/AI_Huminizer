# Security Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Authentication & Authorization
*   **Auth Provider:** NextAuth.js (Frontend) issuing JWTs verified by FastAPI Middleware (Backend).
*   **Role-Based Access:** Basic users, Pro users, and Admins. Rate limits differ by role.

## 2. API Security
*   **Rate Limiting:** IP-based and User-ID-based sliding window rate limits (e.g., 50 requests/min) implemented via Redis to prevent DDOS and LLM cost-exhaustion.
*   **Input Validation:** Strict Pydantic models. Max character limit enforced at the API gateway (e.g., 50,000 chars) before memory allocation.
*   **Injection Protection:** Sanitization of input text to prevent prompt-injection attacks against the LangGraph agents.

## 3. Secret Management
*   No hardcoded secrets. `.env` files are excluded via `.gitignore`.
*   PostgreSQL and Redis credentials must be rotated.

## 4. File Handling Security
*   Uploaded PDFs and DOCX files are stored temporarily in `/tmp` during parsing and deleted immediately after text extraction using a `finally` block.
*   No execution of uploaded files is permitted.
