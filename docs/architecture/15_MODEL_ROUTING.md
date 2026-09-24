# 15. MODEL ROUTING

The platform abstracts LLM APIs behind a Model Router, allowing dynamic switching based on cost, complexity, and availability.

## 1. The Router Abstraction
The codebase will not contain hardcoded `openai.ChatCompletion.create()` calls in business logic.
Instead, agents use: `router.invoke(prompt, tier="advanced")`

## 2. Model Tiers
*   **Tier 1 (Fast & Cheap):** Used for grammar, simple classification, and pattern extraction.
    *   *Models:* Gemini 1.5 Flash, Llama 3 (8B), Claude 3 Haiku.
*   **Tier 2 (Balanced):** Used for standard sentence rewriting and tone adjustment.
    *   *Models:* GPT-4o-mini, Claude 3.5 Sonnet.
*   **Tier 3 (Advanced):** Used for deep semantic verification, contradiction detection, and academic rewriting.
    *   *Models:* GPT-4o, Claude 3 Opus, Gemini 1.5 Pro.

## 3. Health & Fallback
The router monitors HTTP 429 (Rate Limit) and 500 (Server Error) responses from providers.
If OpenAI is down, a request meant for GPT-4o will automatically and silently failover to Claude 3.5 Sonnet, ensuring 99.9% uptime for the user.

## 4. Privacy Mode Routing
If a user selects "Enterprise Private Mode", the router will restrict all API calls to a designated Private Cloud endpoint (e.g., Azure OpenAI or AWS Bedrock) or a locally hosted Llama 3 instance, bypassing public APIs entirely.
