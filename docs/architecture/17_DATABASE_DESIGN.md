# 17. DATABASE DESIGN

The platform uses PostgreSQL (via SQLAlchemy) as the primary data store.

## Core Tables

### 1. `users`
*   `id` (UUID)
*   `email`
*   `hashed_password`
*   `role` (user, admin, team_owner)

### 2. `subscriptions`
*   `id` (UUID)
*   `user_id` (FK)
*   `plan_name` (free, pro, enterprise)
*   `credit_balance` (Integer)
*   `word_balance` (Integer)
*   `stripe_customer_id`

### 3. `writing_profiles` (DNA)
*   `id` (UUID)
*   `user_id` (FK)
*   `profile_name` (e.g., "Academic", "LinkedIn")
*   `dna_data` (JSONB - stores vocabulary, transition preferences, formatting rules)

### 4. `documents`
*   `id` (UUID)
*   `user_id` (FK)
*   `title`
*   `status` (queued, processing, completed, failed)
*   `total_words`
*   `cost_credits`

### 5. `document_sentences`
*   `id` (UUID)
*   `document_id` (FK)
*   `original_text` (Text)
*   `final_text` (Text)
*   `facts_extracted` (JSONB)
*   `citations_extracted` (JSONB)
*   `quality_score` (Float)
*   `explainability_tag` (String)

## Indexing Strategy
*   Index on `user_id` for all multi-tenant queries to ensure fast Dashboard loads.
*   Index on `document_id` in `document_sentences` for quick assembly of the final text.
