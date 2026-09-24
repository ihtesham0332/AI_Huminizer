# Data Model Architecture
**Version:** 1.0.0
**Project:** Agentic AI Text Humanization & Writing Intelligence Platform

This document outlines the PostgreSQL database schema and vector storage strategy.

## 1. Relational Entities (PostgreSQL)

### `users`
*   `id`: UUID (Primary Key)
*   `email`: String (Unique)
*   `password_hash`: String
*   `created_at`: Timestamp
*   `tier`: Enum (free, pro, enterprise)

### `documents`
*   `id`: UUID (Primary Key)
*   `user_id`: UUID (Foreign Key)
*   `title`: String
*   `original_text`: Text
*   `metadata`: JSONB (word count, language, content_type)
*   `created_at`: Timestamp

### `document_versions`
*   `id`: UUID (Primary Key)
*   `document_id`: UUID (Foreign Key)
*   `humanized_text`: Text
*   `change_summary`: Text
*   `created_at`: Timestamp
*   `is_favorite`: Boolean

### `evaluations` (Quality Assurance Scores)
*   `id`: UUID (Primary Key)
*   `version_id`: UUID (Foreign Key -> document_versions)
*   `semantic_score`: Float
*   `fact_preservation_score`: Float
*   `grammar_score`: Float
*   `readability_score`: Float
*   `style_match_score`: Float

### `humanization_jobs`
*   `id`: UUID (Primary Key)
*   `user_id`: UUID (Foreign Key)
*   `status`: Enum (queued, processing, completed, failed)
*   `progress`: Integer (0-100)
*   `result_version_id`: UUID (Foreign Key -> document_versions)

## 2. Vector Entities (pgvector)

### `writing_profiles`
*   `id`: UUID (Primary Key)
*   `user_id`: UUID (Foreign Key)
*   `profile_name`: String (e.g., "Academic Profile")
*   `style_metrics`: JSONB (formality, vocabulary complexity)
*   `style_embedding`: VECTOR(1536) (Captures the latent stylistic fingerprint of the user's uploaded samples).

## 3. Data Privacy & Storage Notes
*   Documents are stored encrypted at rest.
*   Users can trigger a cascade delete on their `user_id` to instantly wipe all `documents`, `document_versions`, and `writing_profiles` from the database.
