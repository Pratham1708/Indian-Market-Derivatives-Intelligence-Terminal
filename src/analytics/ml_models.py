# src/analytics/ml_models.py
"""ML Intelligence Engine for Phase 3.
Implements Isolation Forest for anomaly detection on volume, volatility, and momentum.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame) -> dict:
    """
    Detect anomalies in momentum, volatility, and volume using Isolation Forest.
    Returns a dictionary with anomaly score and explanation.
    """
    if df.empty or len(df) < 50:
        return {"anomaly_score": 0.0, "anomaly_class": "Normal", "explanation": "Insufficient data for ML"}
        
    try:
        # Prepare features
        features = pd.DataFrame(index=df.index)
        
        # 1. Volume feature (Volume relative to 20-day moving average)
        vol_ma = df['Volume'].rolling(20).mean()
        features['vol_ratio'] = np.where(vol_ma > 0, df['Volume'] / vol_ma, 1.0)
        
        # 2. Volatility feature (ATR relative to close price)
        if 'ATR' in df.columns:
            features['atr_ratio'] = df['ATR'] / df['Close']
        else:
            features['atr_ratio'] = (df['High'] - df['Low']) / df['Close']
            
        # 3. Momentum feature (Rate of Change)
        features['roc'] = df['Close'].pct_change(periods=5)
        
        # Drop NaNs
        features = features.dropna()
        
        if len(features) < 20:
            return {"anomaly_score": 0.0, "anomaly_class": "Normal", "explanation": "Insufficient valid data"}
            
        # Train Isolation Forest
        clf = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        
        # Fit and predict
        preds = clf.fit_predict(features)
        scores = clf.decision_function(features)
        
        # Latest row analysis
        latest_pred = preds[-1]
        latest_score = scores[-1]
        latest_feat = features.iloc[-1]
        
        # Normalize score: decision_function is typically < 0 for anomalies
        # We invert it so higher score = more anomalous
        # Scikit-learn scores are generally in [-0.5, 0.5] range
        anomaly_score = max(0.0, min(100.0, float((-latest_score + 0.1) * 200))) 
        
        if latest_pred == -1:
            anomaly_class = "Anomaly Detected"
            reasons = []
            if latest_feat['vol_ratio'] > 2.0:
                reasons.append("unusual volume participation")
            if latest_feat['atr_ratio'] > features['atr_ratio'].mean() + 2 * features['atr_ratio'].std():
                reasons.append("abnormal volatility expansion")
            if abs(latest_feat['roc']) > features['roc'].abs().mean() + 2 * features['roc'].abs().std():
                reasons.append("momentum anomaly")
                
            if reasons:
                explanation = "⚠ " + " and ".join(reasons).capitalize() + " detected outside historical norms."
            else:
                explanation = "⚠ Statistically rare price action detected."
        else:
            anomaly_class = "Normal"
            explanation = "Behavior within historical norms."
            
        return {
            "anomaly_score": round(anomaly_score, 1),
            "anomaly_class": anomaly_class,
            "explanation": explanation
        }
    except Exception as e:
        return {"anomaly_score": 0.0, "anomaly_class": "Error", "explanation": f"ML Error: {e}"}
