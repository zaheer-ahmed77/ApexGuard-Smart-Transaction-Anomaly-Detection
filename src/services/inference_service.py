"""
Real-time Inference Service for Smart Transaction Anomaly Detection & AML.
Loads trained XGBoost, Random Forest, and Isolation Forest models + Rule Engine.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
import joblib

from src.models.rule_based_scenarios import AMLRuleEngine

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TransactionInferenceEngine:
    """
    Inference Engine orchestrating real Machine Learning and Rule-based models.
    """

    FEATURE_NAMES = [
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "orig_diff",
        "dest_diff",
        "error_orig",
        "error_dest",
        "is_orig_drained",
        "amount_to_oldbalance",
        "type_PAYMENT",
        "type_TRANSFER",
        "type_CASH_OUT",
        "type_CASH_IN",
        "type_DEBIT"
    ]

    def __init__(self, models_dir: Optional[str] = None):
        self.models_dir = Path(models_dir) if models_dir else (PROJECT_ROOT / "models")
        self.xgb_model = None
        self.rf_model = None
        self.iso_model = None
        self.metadata = {}
        self.rule_engine = AMLRuleEngine()
        self.load_models()

    def load_models(self):
        """Loads model weights from models/ directory."""
        xgb_path = self.models_dir / "xgboost_fraud_model.joblib"
        rf_path = self.models_dir / "random_forest_fraud_model.joblib"
        iso_path = self.models_dir / "isolation_forest_model.joblib"
        meta_path = self.models_dir / "model_metadata.json"

        if xgb_path.exists():
            try:
                self.xgb_model = joblib.load(xgb_path)
                logger.info(f"Loaded XGBoost model from {xgb_path}")
            except Exception as e:
                logger.warning(f"Failed to load XGBoost: {e}")

        if rf_path.exists():
            try:
                self.rf_model = joblib.load(rf_path)
                logger.info(f"Loaded Random Forest model from {rf_path}")
            except Exception as e:
                logger.warning(f"Failed to load RF: {e}")

        if iso_path.exists():
            try:
                self.iso_model = joblib.load(iso_path)
                logger.info(f"Loaded Isolation Forest model from {iso_path}")
            except Exception as e:
                logger.warning(f"Failed to load Isolation Forest: {e}")

        if meta_path.exists():
            try:
                with open(meta_path, 'r') as f:
                    self.metadata = json.load(f)
            except Exception:
                pass

    def extract_single_feature_vector(self, tx: Dict[str, Any]) -> np.ndarray:
        """Transforms a raw transaction dictionary into model feature array."""
        amount = float(tx.get('amount', 0.0))
        old_orig = float(tx.get('oldbalanceOrg', 0.0))
        new_orig = float(tx.get('newbalanceOrig', 0.0))
        old_dest = float(tx.get('oldbalanceDest', 0.0))
        new_dest = float(tx.get('newbalanceDest', 0.0))
        tx_type = str(tx.get('type', 'PAYMENT')).upper()

        orig_diff = old_orig - new_orig
        dest_diff = new_dest - old_dest
        error_orig = new_orig + amount - old_orig
        error_dest = old_dest + amount - new_dest
        is_orig_drained = 1 if (old_orig > 0 and new_orig == 0) else 0
        amount_to_oldbalance = amount / (old_orig + 1.0)

        type_payment = 1 if tx_type == 'PAYMENT' else 0
        type_transfer = 1 if tx_type == 'TRANSFER' else 0
        type_cash_out = 1 if tx_type == 'CASH_OUT' else 0
        type_cash_in = 1 if tx_type == 'CASH_IN' else 0
        type_debit = 1 if tx_type == 'DEBIT' else 0

        features = [
            amount,
            old_orig,
            new_orig,
            old_dest,
            new_dest,
            orig_diff,
            dest_diff,
            error_orig,
            error_dest,
            is_orig_drained,
            amount_to_oldbalance,
            type_payment,
            type_transfer,
            type_cash_out,
            type_cash_in,
            type_debit
        ]
        return pd.DataFrame([features], columns=self.FEATURE_NAMES)

    def predict(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes full composite AI inference on a single transaction:
        ML model + Isolation Forest + FATF AML rules.
        """
        features_2d = self.extract_single_feature_vector(tx)

        # 1. Rule Engine evaluation
        rule_eval = self.rule_engine.evaluate_transaction(tx)
        rule_score = rule_eval['rule_score']
        triggered_rules = rule_eval['triggered_rules']

        # 2. XGBoost ML evaluation
        ml_score = 0.0
        if self.xgb_model is not None:
            try:
                proba = self.xgb_model.predict_proba(features_2d)[0, 1]
                ml_score = float(proba)
            except Exception as e:
                logger.warning(f"XGBoost prediction failed: {e}")
                ml_score = rule_score
        else:
            ml_score = rule_score

        # 3. Isolation Forest evaluation
        iso_flag = 0
        iso_score = 0.0
        if self.iso_model is not None:
            try:
                # decision_function gives score (lower means more anomalous)
                raw_score = self.iso_model.decision_function(features_2d)[0]
                iso_score = float(np.clip(-raw_score * 2.0, 0.0, 1.0))
                iso_pred = self.iso_model.predict(features_2d)[0]
                iso_flag = 1 if iso_pred == -1 else 0
            except Exception:
                iso_score = 0.0

        # Composite Risk Calculation
        # XGBoost weight: 60%, Rule engine: 30%, Unsupervised Anomaly: 10%
        composite_score = (ml_score * 0.60) + (rule_score * 0.30) + (iso_score * 0.10)
        composite_score = min(max(composite_score, 0.0), 1.0)

        # Risk Tier
        if composite_score >= 0.70 or ml_score >= 0.80 or "RAPID_BALANCE_DRAINAGE" in triggered_rules:
            risk_level = "CRITICAL"
            is_fraud = True
        elif composite_score >= 0.40 or rule_eval['is_suspicious']:
            risk_level = "MEDIUM"
            is_fraud = True
        elif composite_score >= 0.20:
            risk_level = "LOW"
            is_fraud = False
        else:
            risk_level = "NORMAL"
            is_fraud = False

        # Build Explainability & Recommendations
        reasons = []
        if "LARGE_TRANSACTION_THRESHOLD" in triggered_rules:
            reasons.append(f"Transaction amount (${tx.get('amount', 0):,.2f}) exceeds FATF threshold.")
        if "STRUCTURING_SMURFING_SUSPECT" in triggered_rules:
            reasons.append(f"Amount (${tx.get('amount', 0):,.2f}) matches smurfing/structuring patterns just under $10,000.")
        if "RAPID_BALANCE_DRAINAGE" in triggered_rules:
            reasons.append("Origin account balance was completely emptied out immediately upon transfer/cash-out.")
        if ml_score >= 0.70:
            reasons.append(f"Supervised XGBoost fraud classifier assigned high anomaly probability ({ml_score*100:.1f}%).")
        if iso_flag == 1:
            reasons.append("Unsupervised Isolation Forest flagged behavioral vector as an outlier distribution.")

        explanation = " | ".join(reasons) if reasons else "Transaction patterns match legitimate customer financial profile."

        recommendations = []
        if risk_level == "CRITICAL":
            recommendations = [
                "Temporarily hold outbound fund settlement.",
                "Escalate to AML Compliance Officer for SAR (Suspicious Activity Report) review.",
                "Verify beneficiary identity and origin account KYC."
            ]
        elif risk_level == "MEDIUM":
            recommendations = [
                "Queue for manual review by Fraud Operations team.",
                "Cross-reference recent 72-hour transaction velocity for this account."
            ]
        else:
            recommendations = ["Auto-cleared: Proceed with real-time settlement."]

        return {
            'is_fraud': is_fraud,
            'risk_score': round(composite_score, 4),
            'risk_level': risk_level,
            'ml_score': round(ml_score, 4),
            'rule_score': round(rule_score, 4),
            'isolation_score': round(iso_score, 4),
            'triggered_rules': triggered_rules,
            'explanation': explanation,
            'recommendations': recommendations
        }


# Singleton instance
_inference_engine = None

def get_inference_engine() -> TransactionInferenceEngine:
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = TransactionInferenceEngine()
    return _inference_engine
