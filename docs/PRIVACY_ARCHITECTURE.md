# Privacy Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

## 1. Data Retention
*   **Ephemeral Processing:** Free-tier users' documents are processed in memory during the LangGraph execution and discarded immediately unless they explicitly click "Save to Library."
*   **Profile Deletion:** If a user deletes a Writing Profile, the associated vector embeddings in `pgvector` are hard-deleted.

## 2. Model Training
*   **Opt-In Policy:** User text is **never** used to fine-tune local or cloud models by default. An explicit opt-in is required in the settings panel.

## 3. Data Transparency
*   Users can request a full JSON export of all their stored data via a "Download My Data" button.
*   A "Delete Account" button triggers a cascading hard delete on the user's `user_id` across all relational and vector tables.
