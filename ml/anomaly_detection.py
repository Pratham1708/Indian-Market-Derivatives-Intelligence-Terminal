"""
ML-Based Anomaly Detection for Option Mispricing
==================================================
Uses Isolation Forest from scikit-learn to flag unusual option contracts.

Features used:
    1. Implied Volatility (iv)
    2. Volume
    3. Open Interest (openInterest)
    4. Mispricing = Market Price - Theoretical Price
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_anomalies(
    df: pd.DataFrame,
    feature_cols: list = None,
    contamination: float = 0.10,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Run Isolation Forest on an option-chain DataFrame.

    Parameters
    ----------
    df              : DataFrame with the feature columns.
    feature_cols    : Columns to use as features.
    contamination   : Expected proportion of anomalies (0 < c < 0.5).
    random_state    : Seed for reproducibility.

    Returns
    -------
    DataFrame with 'anomaly_label' (1=normal, -1=anomaly) and
    'anomaly_score' columns added.
    """
    if feature_cols is None:
        feature_cols = ["iv", "volume", "openInterest", "mispricing"]

    df = df.copy()

    available = [c for c in feature_cols if c in df.columns]
    if len(available) < 2:
        df["anomaly_label"] = 1
        df["anomaly_score"] = 0.0
        return df

    X = df[available].copy().fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
    )
    df["anomaly_label"] = model.fit_predict(X_scaled)
    df["anomaly_score"] = model.decision_function(X_scaled)

    return df


def get_anomaly_summary(df: pd.DataFrame) -> dict:
    """Quick summary of anomaly detection results."""
    if "anomaly_label" not in df.columns:
        return {"total": len(df), "anomalies": 0, "pct": 0.0, "avg_score": 0.0}

    n = len(df)
    anomalies = int((df["anomaly_label"] == -1).sum())
    return {
        "total": n,
        "anomalies": anomalies,
        "pct": round(100 * anomalies / n, 1) if n else 0.0,
        "avg_score": round(float(df["anomaly_score"].mean()), 4),
    }
