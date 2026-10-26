"""
Model diagnostics for anomaly detection models (overfitting/underfitting evaluation).
"""

import numpy as np
from typing import Dict, Any, Optional
from sklearn.metrics import roc_auc_score, accuracy_score


class ModelDiagnostics:
    """
    Evaluates trained models for generalization, train vs test performance gap, and stability.
    """

    def __init__(self, auc_threshold_gap: float = 0.05):
        self.auc_threshold_gap = auc_threshold_gap

    def check_overfitting(self, model: Any, X_train: Any, y_train: Any, X_test: Any, y_test: Any, model_name: str) -> Dict[str, Any]:
        """
        Calculates performance gap between train and test sets to detect overfitting.
        """
        try:
            train_proba = model.predict_proba(X_train)[:, 1]
            test_proba = model.predict_proba(X_test)[:, 1]

            train_auc = roc_auc_score(y_train, train_proba) if len(np.unique(y_train)) > 1 else 1.0
            test_auc = roc_auc_score(y_test, test_proba) if len(np.unique(y_test)) > 1 else 1.0

            gap = float(train_auc - test_auc)
            is_overfitting = gap > self.auc_threshold_gap

            if gap > 0.10:
                severity = 'High'
                status = 'Overfitting Detected'
            elif gap > self.auc_threshold_gap:
                severity = 'Moderate'
                status = 'Slight Overfitting'
            else:
                severity = 'Low'
                status = 'Well Generalizing'

            return {
                'model_name': model_name,
                'overfitting_status': status,
                'overfitting_severity': severity,
                'performance_gaps': {
                    'auc': round(gap, 4),
                    'train_auc': round(float(train_auc), 4),
                    'test_auc': round(float(test_auc), 4)
                }
            }
        except Exception as e:
            return {
                'model_name': model_name,
                'overfitting_status': 'Unable to calculate',
                'overfitting_severity': 'None',
                'performance_gaps': {'error': str(e)}
            }

    def generate_diagnostic_report(self, diagnostic_results: Dict[str, Any]) -> str:
        """
        Generates readable ASCII diagnostic report.
        """
        lines = [
            "===========================================================",
            "             MODEL DIAGNOSTICS & AUDIT REPORT              ",
            "==========================================================="
        ]
        for model_name, diag in diagnostic_results.items():
            status = diag.get('overfitting_status', 'Unknown')
            severity = diag.get('overfitting_severity', 'Unknown')
            gaps = diag.get('performance_gaps', {})
            lines.append(f"Model: {model_name}")
            lines.append(f"  - Status:   {status} (Severity: {severity})")
            if 'auc' in gaps:
                lines.append(f"  - AUC Gap:  {gaps.get('auc')} (Train: {gaps.get('train_auc')}, Test: {gaps.get('test_auc')})")
            lines.append("-" * 59)
        return "\n".join(lines)
