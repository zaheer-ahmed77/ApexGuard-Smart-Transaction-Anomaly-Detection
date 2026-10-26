"""
SQLAlchemy models for Smart Transaction Anomaly Detection & AML Platform.
Includes User, TransactionRecord, and AuditLog.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from .db import Base


class User(Base):
    """User account model for authentication & authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), default="analyst")  # 'admin', 'analyst', 'compliance'
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


class TransactionRecord(Base):
    """Transaction audit and classification history record."""
    __tablename__ = "transactions"

    id = Column(String(64), primary_key=True, index=True)
    step = Column(Integer, default=1)
    type = Column(String(20), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    nameOrig = Column(String(50), index=True, nullable=False)
    oldbalanceOrg = Column(Float, default=0.0)
    newbalanceOrig = Column(Float, default=0.0)
    nameDest = Column(String(50), index=True, nullable=False)
    oldbalanceDest = Column(Float, default=0.0)
    newbalanceDest = Column(Float, default=0.0)

    # Classification & Risk Metrics
    is_fraud = Column(Boolean, default=False, index=True)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String(20), default="NORMAL", index=True) # NORMAL, LOW, MEDIUM, CRITICAL
    ml_score = Column(Float, default=0.0)
    rule_score = Column(Float, default=0.0)
    triggered_rules = Column(Text, default="[]")  # JSON string of rule names
    explanation = Column(Text, nullable=True)

    # Workflow & Audit Status
    status = Column(String(30), default="PENDING_REVIEW", index=True) # PENDING_REVIEW, CONFIRMED_FRAUD, CLEARED_NORMAL, FLAGGED
    reviewed_by = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class AuditLog(Base):
    """System-wide audit trail for compliance (FATF / GDPR / EU AI Act)."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    username = Column(String(50), nullable=True)
    action = Column(String(100), nullable=False) # LOGIN, PREDICTION, STATUS_CHANGE, BATCH_SCAN
    target_id = Column(String(64), nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
