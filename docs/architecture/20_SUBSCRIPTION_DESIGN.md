# 20. SUBSCRIPTION DESIGN

The economic model is based on "Internal Credits" rather than hard API calls, allowing us to absorb model pricing changes without redesigning user plans.

## The Dual-Wallet System
Users have a dual wallet: **Words** and **Credits**.
*   1 Credit = 1 standard AI operation.

## Tiered Subscription Plans

### 1. Free Tier ($0)
*   **Words/Month:** 5,000
*   **Features:** Basic Analysis, 1 Candidate generation, Fast Mode only.
*   **Limits:** No PDF uploads, No Writing DNA.

### 2. Professional Tier ($19/mo)
*   **Words/Month:** 150,000
*   **Features:** Balanced/Deep Modes, Personal Writing DNA, Multiple Candidates, Fact/Citation Guardians.
*   **Cost Control:** "Selective Rewriting" is enabled, meaning their 150k words stretches much further because we don't bill them for sentences we don't change.

### 3. Pro+ Tier ($49/mo)
*   **Words/Month:** 500,000
*   **Features:** Advanced Semantic Verification, Document-Level Consistency, API Access, Priority Queue.

## Failed Job Accounting
If a job fails due to an Anthropic/OpenAI 500 error or a timeout, the `UsageService` automatically intercepts the failure and **refunds** the credits to the user's wallet. Users are never billed for partial or failed generations.
