# 21. SECURITY DESIGN

Security is paramount, especially when handling proprietary corporate or academic documents.

## 1. Input Sanitization & Threat Protection
*   **Prompt Injection:** User text is never directly appended to a system prompt. It is strictly passed as a data variable within the LLM API call to prevent jailbreaks (e.g., "Ignore all previous instructions...").
*   **Malware Scanning:** Uploaded PDF/DOCX files are verified via MIME-type checking and bounded by a strict size limit (e.g., 10MB) before parsing.

## 2. API Security
*   **Rate Limiting:** A Token Bucket rate limiter (e.g., `slowapi`) protects endpoints. Free users: 10 req/min. Pro users: 60 req/min.
*   **Authentication:** JWT (JSON Web Tokens) are used for all stateless API requests.
*   **API Keys:** Developer API keys are hashed in the database using bcrypt. Only the user sees the raw key once.

## 3. Data Isolation
*   PostgreSQL Row-Level Security (RLS) or strict ORM filters (`where user_id == current_user.id`) ensures tenant isolation. User A cannot access User B's documents.

## 4. Secret Management
*   AWS Systems Manager (SSM) Parameter Store or HashiCorp Vault is used to inject production secrets (`DATABASE_URL`, `OPENAI_API_KEY`) into the Docker containers at runtime. Secrets are never committed to `.env` files in git.
