# 30. MVP SCOPE

Based on the Priority Matrix, the Minimum Viable Product (MVP) will strictly focus on the **P0 Core Features** to prove the architecture works and solves the "Meaning Drift" and "Cost" gaps of existing competitors.

## In Scope for MVP
1.  **Backend:** FastAPI server with PostgreSQL (Users, Subscriptions, Documents).
2.  **AI Engine:** LangGraph implementation featuring:
    *   `FactGuardian` and `CitationGuardian`
    *   `CostController` (Selective rewriting logic)
    *   `ModelRouter` (OpenAI & Anthropic)
    *   `QualityCritic` (Verification loop)
3.  **Frontend:** Next.js Dashboard.
    *   Upload text/DOCX.
    *   Select Mode (Fast/Balanced/Deep).
    *   Side-by-side Diff Viewer showing changes.
4.  **Billing:** Basic Stripe integration (Credit system).

## Out of Scope for MVP (Deferred to V2)
1.  Personal Writing DNA (Complex to build UI for immediately).
2.  Enterprise Team features (Brand voice, SSO).
3.  Browser Extensions (Chrome).
4.  Local/Private cloud deployment.

## Next Steps
This concludes Phase 1 (Deep Audit & Architecture). 
Upon approval of these 30 documents, we will move to Phase 2 and begin writing the backend infrastructure and core LangGraph agents.
