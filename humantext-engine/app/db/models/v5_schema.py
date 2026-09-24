from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # user, admin, team_owner
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    plan_name = Column(String, default="free") # free, pro, pro_plus, enterprise
    credit_balance = Column(Integer, default=100)
    word_balance = Column(Integer, default=5000)
    stripe_customer_id = Column(String, nullable=True)

class WritingProfile(Base):
    __tablename__ = "writing_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    profile_name = Column(String)
    dna_data = Column(JSONB) # Stores vocabulary, transitions, rules
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    title = Column(String)
    status = Column(String, default="queued") # queued, processing, completed, failed
    total_words = Column(Integer, default=0)
    cost_credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DocumentSentence(Base):
    __tablename__ = "document_sentences"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    sentence_index = Column(Integer)
    original_text = Column(String)
    final_text = Column(String, nullable=True)
    facts_extracted = Column(JSONB, nullable=True)
    citations_extracted = Column(JSONB, nullable=True)
    quality_score = Column(Float, nullable=True)
    explainability_tag = Column(String, nullable=True)
