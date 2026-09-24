# 22. PRIVACY DESIGN

We must offer privacy guarantees that generic LLM providers (like ChatGPT) do not.

## 1. Zero-Retention Mode
Users can toggle a "Privacy Mode: ON" switch in their dashboard.
When active:
*   Uploaded documents are processed entirely in RAM.
*   The final output is streamed back to the client.
*   Nothing is written to the PostgreSQL `documents` or `document_sentences` tables.
*   The system logs only metadata (e.g., "Job completed, 500 words") for billing purposes.

## 2. Model Provider Privacy
The `ModelRouter` ensures that when calling OpenAI or Anthropic APIs via our Enterprise accounts, the **"Zero Data Retention" (ZDR)** flag is active. This guarantees the LLM providers do not use our users' data to train their future models.

## 3. Local/Private Cloud Fallback
For enterprise clients with strict compliance (e.g., HIPAA), the architecture supports routing requests to a self-hosted Llama 3 instance or an isolated Azure OpenAI deployment, ensuring data never crosses the public internet.

## 4. Account Deletion
A "Delete Account" button triggers a cascading delete in the database, immediately purging the user's Writing DNA, documents, and subscription data.
