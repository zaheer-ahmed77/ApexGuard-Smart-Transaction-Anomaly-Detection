"""
Rule-based AML detection scenarios and adaptive threshold calculation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AdaptiveThresholdCalculator:
    """
    Calculates adaptive thresholds for AML monitoring based on segments and outlier statistics.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        adaptive_cfg = self.config.get('adaptive_thresholds', {})
        self.enabled = adaptive_cfg.get('enabled', True)
        self.n_segments = adaptive_cfg.get('n_segments', 5)
        self.outlier_method = adaptive_cfg.get('outlier_method', 'iqr')
        self.thresholds: Dict[str, float] = {}

    def calculate_thresholds(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculates adaptive amount thresholds from distribution."""
        if 'amount' not in df.columns or len(df) == 0:
            return {'large_amount': 200000.0, 'structuring_lower': 9000.0}

        amounts = df['amount'].dropna()
        if self.outlier_method == 'iqr':
            q25 = amounts.quantile(0.25)
            q75 = amounts.quantile(0.75)
            iqr = q75 - q25
            large_thresh = float(q75 + 3.0 * iqr)
        else:
            large_thresh = float(amounts.quantile(0.99))

        # Ensure realistic baseline limits
        large_thresh = max(large_thresh, 50000.0)
        self.thresholds = {
            'large_amount': large_thresh,
            'structuring_lower': 9000.0,
            'structuring_upper': 10000.0
        }
        return self.thresholds


class AMLRuleEngine:
    """
    Rule-based AML Detection Engine covering primary FATF and financial compliance scenarios:
    1. Large value transaction (Threshold reporting)
    2. Structuring / Smurfing (Transactions just below reporting threshold)
    3. Rapid movement / Complete balance depletion (Sudden empty account)
    4. Destination anomaly / High velocity to new accounts
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        rule_cfg = self.config.get('rule_engine', {})
        self.large_transaction_threshold = rule_cfg.get('large_transaction_threshold', 200000.0)
        self.structuring_threshold = rule_cfg.get('structuring_threshold', 9000.0)
        self.structuring_upper = 10000.0
        self.rapid_movement_threshold = rule_cfg.get('rapid_movement_threshold', 5)
        self.rapid_movement_window = rule_cfg.get('rapid_movement_window', 10)
        self.threshold_calculator = AdaptiveThresholdCalculator(self.config)

    def evaluate_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single transaction in real time against rule set.
        """
        amount = float(tx.get('amount', 0.0))
        tx_type = str(tx.get('type', '')).upper()
        old_orig = float(tx.get('oldbalanceOrg', 0.0))
        new_orig = float(tx.get('newbalanceOrig', 0.0))
        old_dest = float(tx.get('oldbalanceDest', 0.0))
        new_dest = float(tx.get('newbalanceDest', 0.0))

        flags = []
        rule_score = 0.0

        # Rule 1: Large value transaction
        if amount >= self.large_transaction_threshold:
            flags.append("LARGE_TRANSACTION_THRESHOLD")
            rule_score += 0.35

        # Rule 2: Structuring / Smurfing pattern ($9,000 - $10,000)
        if self.structuring_threshold <= amount < self.structuring_upper:
            flags.append("STRUCTURING_SMURFING_SUSPECT")
            rule_score += 0.30

        # Rule 3: Rapid balance drain (Cash-out or Transfer clearing account)
        if old_orig > 1000 and new_orig == 0 and tx_type in ['TRANSFER', 'CASH_OUT']:
            flags.append("RAPID_BALANCE_DRAINAGE")
            rule_score += 0.40

        # Rule 4: Ghost destination or destination discrepancy
        if tx_type in ['TRANSFER'] and old_dest == 0 and new_dest == 0 and amount > 5000:
            flags.append("DESTINATION_BALANCE_ANOMALY")
            rule_score += 0.25

        # Cap score to 1.0
        rule_score = min(rule_score, 1.0)
        is_suspicious = len(flags) > 0 or rule_score >= 0.40

        return {
            'is_suspicious': is_suspicious,
            'rule_score': round(rule_score, 4),
            'triggered_rules': flags,
            'rule_count': len(flags)
        }

    def run_all_scenarios(self, df: pd.DataFrame, high_risk_accounts: Optional[List[str]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Execute rule scenarios on a DataFrame of transactions.
        Returns:
            Tuple of (results_df, summary_df)
        """
        results_df = df.copy()

        # Rule 1: Large Transaction Flag
        results_df['rule_large_transaction'] = (results_df['amount'] >= self.large_transaction_threshold).astype(int)

        # Rule 2: Structuring (Smurfing)
        results_df['rule_structuring'] = (
            (results_df['amount'] >= self.structuring_threshold) & 
            (results_df['amount'] < self.structuring_upper)
        ).astype(int)

        # Rule 3: Rapid Balance Drain
        results_df['rule_rapid_drain'] = (
            (results_df['oldbalanceOrg'] > 1000) & 
            (results_df['newbalanceOrig'] == 0) & 
            (results_df['type'].isin(['TRANSFER', 'CASH_OUT']))
        ).astype(int)

        # Rule 4: High-Risk Accounts if provided
        if high_risk_accounts:
            risk_set = set(high_risk_accounts)
            results_df['rule_high_risk_entity'] = (
                results_df['nameOrig'].isin(risk_set) | results_df['nameDest'].isin(risk_set)
            ).astype(int)
        else:
            results_df['rule_high_risk_entity'] = 0

        # Calculate composite score & flags
        rule_cols = ['rule_large_transaction', 'rule_structuring', 'rule_rapid_drain', 'rule_high_risk_entity']
        results_df['rule_score'] = (
            results_df['rule_large_transaction'] * 0.35 +
            results_df['rule_structuring'] * 0.30 +
            results_df['rule_rapid_drain'] * 0.40 +
            results_df['rule_high_risk_entity'] * 0.35
        ).clip(0.0, 1.0)

        results_df['is_suspicious'] = (results_df[rule_cols].sum(axis=1) > 0).astype(int)

        # Build summary DataFrame
        total_count = max(len(results_df), 1)
        summary_rows = [
            {
                'scenario': 'Large Transaction Threshold',
                'flagged_count': int(results_df['rule_large_transaction'].sum()),
                'percentage': float(results_df['rule_large_transaction'].mean() * 100),
                'risk_level': 'High'
            },
            {
                'scenario': 'Structuring (Smurfing)',
                'flagged_count': int(results_df['rule_structuring'].sum()),
                'percentage': float(results_df['rule_structuring'].mean() * 100),
                'risk_level': 'Medium'
            },
            {
                'scenario': 'Rapid Balance Depletion',
                'flagged_count': int(results_df['rule_rapid_drain'].sum()),
                'percentage': float(results_df['rule_rapid_drain'].mean() * 100),
                'risk_level': 'Critical'
            },
            {
                'scenario': 'High Risk Entities',
                'flagged_count': int(results_df['rule_high_risk_entity'].sum()),
                'percentage': float(results_df['rule_high_risk_entity'].mean() * 100),
                'risk_level': 'High'
            },
            {
                'scenario': 'Overall Rule-Based Suspicious',
                'flagged_count': int(results_df['is_suspicious'].sum()),
                'percentage': float(results_df['is_suspicious'].mean() * 100),
                'risk_level': 'Combined'
            }
        ]
        summary_df = pd.DataFrame(summary_rows)

        return results_df, summary_df
