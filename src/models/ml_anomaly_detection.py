"""
Machine Learning Anomaly Detection Engine.
Integrates XGBoost, LightGBM, Random Forest, and Isolation Forest for real-time fraud detection.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import logging
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (
    roc_auc_score, average_precision_score, precision_recall_fscore_support,
    classification_report, confusion_matrix
)
import joblib

logger = logging.getLogger(__name__)

# Check XGBoost
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False
    logger.warning("XGBoost is not installed.")

# Check LightGBM
try:
    import lightgbm as lgb
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False
    logger.warning("LightGBM is not installed.")


class AnomalyDetector:
    """
    Production-ready Anomaly Detector supporting supervised ensemble
    (XGBoost, LightGBM, Random Forest) and unsupervised anomaly detection (Isolation Forest).
    """

    def __init__(self,
                 contamination: float = 0.01,
                 tracking_uri: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        self.contamination = contamination
        self.tracking_uri = tracking_uri
        self.config = config or {}
        self.models: Dict[str, Any] = {}
        self.model_metrics: Dict[str, Any] = {}
        self.feature_importances: Dict[str, Any] = {}
        self.feature_names: List[str] = []

        # Model configs
        ml_cfg = self.config.get('ml_models', {})
        self.xgb_cfg = ml_cfg.get('xgboost', {})
        self.lgb_cfg = ml_cfg.get('lightgbm', {})
        self.rf_cfg = ml_cfg.get('random_forest', {})
        self.iso_cfg = ml_cfg.get('isolation_forest', {})

    def _get_feature_names(self, X: Any) -> List[str]:
        if isinstance(X, pd.DataFrame):
            return list(X.columns)
        return [f"feature_{i}" for i in range(X.shape[1])]

    def train_supervised_models(self,
                                X_train: Any,
                                y_train: Any,
                                X_test: Any,
                                y_test: Any) -> Dict[str, Any]:
        """
        Train supervised fraud detection classifiers and calculate validation metrics.
        """
        results = {}
        self.feature_names = self._get_feature_names(X_train)
        feature_names = self.feature_names

        # 1. XGBoost
        if XGB_AVAILABLE and self.xgb_cfg.get('enabled', True):
            logger.info("Training XGBoost Classifier...")
            n_est = self.xgb_cfg.get('n_estimators', 100)
            max_d = self.xgb_cfg.get('max_depth', 6)
            lr = self.xgb_cfg.get('learning_rate', 0.1)

            xgb_model = xgb.XGBClassifier(
                n_estimators=n_est,
                max_depth=max_d,
                learning_rate=lr,
                random_state=42,
                eval_metric='logloss',
                use_label_encoder=False
            )
            xgb_model.fit(X_train, y_train)

            # Evaluate
            y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            ap = average_precision_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            y_pred = (y_pred_proba >= 0.5).astype(int)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', zero_division=0)

            # Feature importance
            importances = xgb_model.feature_importances_
            feat_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values('importance', ascending=False)
            self.feature_importances['xgboost'] = feat_df

            results['xgboost'] = {
                'model': xgb_model,
                'best_threshold': 0.5,
                'metrics': {
                    'auc': round(float(auc), 4),
                    'average_precision': round(float(ap), 4),
                    'precision': round(float(prec), 4),
                    'recall': round(float(rec), 4),
                    'f1': round(float(f1), 4)
                }
            }
            self.models['xgboost'] = xgb_model
            logger.info(f"XGBoost trained - AUC: {auc:.4f}, Recall: {rec:.4f}, Precision: {prec:.4f}")

        # 2. Random Forest
        if self.rf_cfg.get('enabled', True):
            logger.info("Training Random Forest Classifier...")
            n_est = self.rf_cfg.get('n_estimators', 100)
            max_d = self.rf_cfg.get('max_depth', 10)

            rf_model = RandomForestClassifier(
                n_estimators=n_est,
                max_depth=max_d,
                random_state=42,
                class_weight='balanced'
            )
            rf_model.fit(X_train, y_train)

            y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            ap = average_precision_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            y_pred = (y_pred_proba >= 0.5).astype(int)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', zero_division=0)

            importances = rf_model.feature_importances_
            feat_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values('importance', ascending=False)
            self.feature_importances['random_forest'] = feat_df

            results['random_forest'] = {
                'model': rf_model,
                'best_threshold': 0.5,
                'metrics': {
                    'auc': round(float(auc), 4),
                    'average_precision': round(float(ap), 4),
                    'precision': round(float(prec), 4),
                    'recall': round(float(rec), 4),
                    'f1': round(float(f1), 4)
                }
            }
            self.models['random_forest'] = rf_model
            logger.info(f"Random Forest trained - AUC: {auc:.4f}, Recall: {rec:.4f}, Precision: {prec:.4f}")

        # 3. LightGBM
        if LGBM_AVAILABLE and self.lgb_cfg.get('enabled', True):
            logger.info("Training LightGBM Classifier...")
            n_est = self.lgb_cfg.get('n_estimators', 100)
            lr = self.lgb_cfg.get('learning_rate', 0.05)
            num_leaves = self.lgb_cfg.get('num_leaves', 31)

            lgb_model = lgb.LGBMClassifier(
                n_estimators=n_est,
                learning_rate=lr,
                num_leaves=num_leaves,
                random_state=42,
                verbose=-1
            )
            lgb_model.fit(X_train, y_train)

            y_pred_proba = lgb_model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            ap = average_precision_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 1.0
            y_pred = (y_pred_proba >= 0.5).astype(int)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', zero_division=0)

            results['lightgbm'] = {
                'model': lgb_model,
                'best_threshold': 0.5,
                'metrics': {
                    'auc': round(float(auc), 4),
                    'average_precision': round(float(ap), 4),
                    'precision': round(float(prec), 4),
                    'recall': round(float(rec), 4),
                    'f1': round(float(f1), 4)
                }
            }
            self.models['lightgbm'] = lgb_model
            logger.info(f"LightGBM trained - AUC: {auc:.4f}, Recall: {rec:.4f}, Precision: {prec:.4f}")

        self.model_metrics = results
        return results

    def train_unsupervised_models(self, X: Any) -> Dict[str, Any]:
        """
        Train unsupervised Isolation Forest for outlier/anomaly detection.
        """
        logger.info("Training Isolation Forest for unsupervised anomaly detection...")
        n_est = self.iso_cfg.get('n_estimators', 100)
        contam = self.iso_cfg.get('contamination', self.contamination)

        iso_model = IsolationForest(
            n_estimators=n_est,
            contamination=contam,
            random_state=42
        )
        iso_model.fit(X)
        self.models['isolation_forest'] = iso_model

        return {
            'isolation_forest': {
                'model': iso_model,
                'contamination': contam
            }
        }

    def train_advanced_models(self, X_train: Any, y_train: Any, X_test: Any, y_test: Any) -> Dict[str, Any]:
        """Placeholder / fallback for deep learning models."""
        return {}
