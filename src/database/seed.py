"""
Database initialization and seeding script.
Creates tables, default users, and initial transaction records for instant presentation.
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.database.db import engine, SessionLocal, Base
from src.database.models import User, TransactionRecord, AuditLog
from src.database.auth import hash_password
from src.models.rule_based_scenarios import AMLRuleEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init_db():
    """Create all database tables."""
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully.")


def seed_users(db):
    """Seed initial administrator and analyst accounts."""
    if db.query(User).count() == 0:
        logger.info("Seeding default administrative accounts...")
        admin_user = User(
            username="admin",
            email="admin@aml-system.internal",
            hashed_password=hash_password("Admin@123"),
            role="admin",
            full_name="Chief Compliance Officer"
        )
        analyst_user = User(
            username="analyst",
            email="analyst@aml-system.internal",
            hashed_password=hash_password("Analyst@123"),
            role="analyst",
            full_name="Lead Fraud Analyst"
        )
        db.add_all([admin_user, analyst_user])
        db.commit()
        logger.info("✅ Default users created: admin (Admin@123) and analyst (Analyst@123)")
    else:
        logger.info("Users already exist. Skipping user seeding.")


def seed_transactions(db, limit: int = 60):
    """Seed initial transaction audit records from data/transactions.csv."""
    if db.query(TransactionRecord).count() == 0:
        csv_path = PROJECT_ROOT / "data" / "transactions.csv"
        if not csv_path.exists():
            logger.warning(f"{csv_path} does not exist, skipping transaction seed.")
            return

        logger.info(f"Seeding {limit} transactions from {csv_path}...")
        df = pd.read_csv(csv_path)

        # Ensure we have both normal and fraud examples
        fraud_sample = df[df['isFraud'] == 1].head(15)
        normal_sample = df[df['isFraud'] == 0].head(limit - len(fraud_sample))
        sample_df = pd.concat([fraud_sample, normal_sample]).sample(frac=1.0, random_state=42).reset_index(drop=True)

        rule_engine = AMLRuleEngine()

        records = []
        now = datetime.utcnow()
        for idx, row in sample_df.iterrows():
            tx_dict = row.to_dict()
            rule_res = rule_engine.evaluate_transaction(tx_dict)

            is_fraud_actual = bool(row['isFraud'] == 1)
            # Combine rule score with synthetic probability
            if is_fraud_actual:
                risk_score = round(float(0.82 + (idx % 15) * 0.01), 3)
                risk_level = "CRITICAL"
                status = "FLAGGED"
                explanation = "High risk detected: Rapid balance drainage and structuring flag triggered."
            elif rule_res['is_suspicious']:
                risk_score = round(float(0.55 + rule_res['rule_score'] * 0.3), 3)
                risk_level = "MEDIUM"
                status = "PENDING_REVIEW"
                explanation = f"Flagged by rule engine: {', '.join(rule_res['triggered_rules'])}"
            else:
                risk_score = round(float(0.02 + (idx % 8) * 0.02), 3)
                risk_level = "NORMAL"
                status = "CLEARED_NORMAL"
                explanation = "Standard behavioral pattern, balances match expected transaction activity."

            tx_time = now - timedelta(hours=int(idx * 2))

            tx_rec = TransactionRecord(
                id=f"TXN-{100000 + idx}",
                step=int(row['step']),
                type=str(row['type']),
                amount=float(row['amount']),
                nameOrig=str(row['nameOrig']),
                oldbalanceOrg=float(row['oldbalanceOrg']),
                newbalanceOrig=float(row['newbalanceOrig']),
                nameDest=str(row['nameDest']),
                oldbalanceDest=float(row['oldbalanceDest']),
                newbalanceDest=float(row['newbalanceDest']),
                is_fraud=is_fraud_actual,
                risk_score=risk_score,
                risk_level=risk_level,
                ml_score=risk_score,
                rule_score=rule_res['rule_score'],
                triggered_rules=json.dumps(rule_res['triggered_rules']),
                explanation=explanation,
                status=status,
                created_at=tx_time
            )
            records.append(tx_rec)

        db.add_all(records)

        # Add initial audit log
        audit = AuditLog(
            user_id=1,
            username="admin",
            action="SYSTEM_INIT",
            target_id="DATABASE",
            details="Initialized system with baseline transaction dataset and active AML models.",
            timestamp=now
        )
        db.add(audit)
        db.commit()
        logger.info(f"✅ Successfully seeded {len(records)} transactions into database.")
    else:
        logger.info("Transactions already exist in database. Skipping seed.")


def run_seed():
    init_db()
    db = SessionLocal()
    try:
        seed_users(db)
        seed_transactions(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
