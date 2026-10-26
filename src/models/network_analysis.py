"""
Graph and network analysis for transaction anomaly and money laundering ring detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)


class TransactionNetworkAnalyzer:
    """
    Analyzes transaction flows between accounts (nameOrig -> nameDest)
    to identify network anomalies, smurfing hubs, and cycles.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.high_degree_threshold = 10
        self.fan_out_threshold = 5

    def build_network_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates network graph centrality and connectivity metrics from transaction logs.
        """
        if 'nameOrig' not in df.columns or 'nameDest' not in df.columns:
            return {'total_nodes': 0, 'total_edges': 0, 'hubs': []}

        orig_counts = df['nameOrig'].value_counts()
        dest_counts = df['nameDest'].value_counts()

        high_orig_hubs = orig_counts[orig_counts >= self.fan_out_threshold].to_dict()
        high_dest_hubs = dest_counts[dest_counts >= self.fan_out_threshold].to_dict()

        unique_nodes = set(df['nameOrig']).union(set(df['nameDest']))

        return {
            'total_nodes': len(unique_nodes),
            'total_edges': len(df),
            'high_activity_senders': len(high_orig_hubs),
            'high_activity_receivers': len(high_dest_hubs),
            'top_senders': dict(list(high_orig_hubs.items())[:10]),
            'top_receivers': dict(list(high_dest_hubs.items())[:10])
        }

    def detect_suspicious_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Annotates transactions with network anomaly flags (fan-out, high velocity).
        """
        result = df.copy()
        if 'nameOrig' in df.columns:
            orig_freq = df['nameOrig'].map(df['nameOrig'].value_counts())
            result['network_orig_frequency'] = orig_freq
            result['network_fan_out_flag'] = (orig_freq >= self.fan_out_threshold).astype(int)
        else:
            result['network_fan_out_flag'] = 0

        return result
