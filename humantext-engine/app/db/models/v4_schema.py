import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    documents = relationship("Document", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    plan_tier = Column(String, default="FREE") # FREE, STUDENT, PRO, PRO_PLUS, ENTERPRISE
    credits_remaining = Column(Float, default=5000.0) # Internal credit system
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="subscription")

class UsageRecord(Base):
    __tablename__ = "usage_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    job_id = Column(String)
    credits_used = Column(Float)
    model_used = Column(String)
    tokens_processed = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="usage_records")

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    content_type = Column(String) # academic, blog, etc.
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"))
    content = Column(String) # Could be heavily compressed or stored in S3 at scale
    structural_metadata = Column(JSON) # JSON tree of paragraphs, citations, etc.
    version_number = Column(Integer)
    
    document = relationship("Document", back_populates="versions")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    original_text = Column(String)
    humanized_text = Column(String)
    user_rating = Column(Integer) # 1 to 5
    user_edits = Column(String) # What the user changed manually after generation
    
class CostRecord(Base):
    __tablename__ = "cost_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String)
    model_provider = Column(String)
    api_cost_usd = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
