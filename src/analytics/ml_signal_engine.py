# src/analytics/ml_signal_engine.py
"""ML Signal Engine for Phase 5.
Replaces the rule-based signal system with an ensemble ML classifier
(RandomForest + GradientBoosting) that produces 7-class signals with
confidence scores and explainable contributing factors.

Falls back to rule-based engine when insufficient data is available.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.analytics.ml_features import (
    extract_ml_features,
    get_feature_names,
    FEATURE_DISPLAY_NAMES,
    get_feature_detail,
)

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────────

LABEL_MAP = {0: "bearish", 1: "neutral", 2: "bullish"}
LABEL_MAP_INV = {"bearish": 0, "neutral": 1, "bullish": 2}

# 7-class signal taxonomy with color mapping
SIGNAL_COLORS = {
    "Strong Bullish": ("#00E396", "green"),
    "Bullish Continuation": ("#00D4FF", "cyan"),
    "Weak Bullish": ("#A8E6CF", "light_green"),
    "Neutral / Consolidation": ("#FEB019", "yellow"),
    "Weak Bearish": ("#FFB3BA", "light_red"),
    "Bearish Breakdown": ("#FF6B6B", "red"),
    "Strong Bearish": ("#FF4560", "red"),
    "High Volatility / Uncertain": ("#9B59B6", "purple"),
}

MIN_TRAINING_ROWS = 100
MIN_VALIDATION_ACCURACY = 0.35


# ── Label Generation ─────────────────────────────────────────────────────

def _generate_labels(
    df: pd.DataFrame,
    horizon: int = 5,
    bull_threshold: float = 0.015,
    bear_threshold: float = -0.015,
) -> pd.Series:
    """Generate classification labels from forward returns.

    Parameters
    ----------
    df : DataFrame
        Must contain a ``Close`` column.
    horizon : int
        Number of bars to look ahead for return calculation.
    bull_threshold : float
        Minimum return for bullish label (default: +1.5%).
    bear_threshold : float
        Maximum return for bearish label (default: -1.5%).

    Returns
    -------
    pd.Series
        Integer labels: 2=Bullish, 1=Neutral, 0=Bearish.
        Last ``horizon`` rows will be NaN.
    """
    future_close = df["Close"].shift(-horizon)
    forward_return = (future_close - df["Close"]) / df["Close"]

    labels = pd.Series(1, index=df.index, dtype=float)  # default neutral
    labels[forward_return > bull_threshold] = 2  # bullish
    labels[forward_return < bear_threshold] = 0  # bearish
    labels[forward_return.isna()] = np.nan  # can't label last N rows

    return labels


# ── ML Signal Engine Class ───────────────────────────────────────────────

class MLSignalEngine:
    """Ensemble ML signal classifier using RandomForest + GradientBoosting.

    Trains on historical indicator data to predict directional bias
    and produces 7-class signal taxonomy with confidence and explanations.
    """

    def __init__(self):
        self.rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        self.gb = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=5,
            min_samples_leaf=10,
            learning_rate=0.1,
            random_state=42,
        )
        self.is_trained = False
        self.feature_names: List[str] = []
        self.training_metrics: Dict[str, Any] = {}
        self._feature_means: Optional[pd.Series] = None

    def train(
        self,
        features: pd.DataFrame,
        labels: pd.Series,
        validation_split: int = 30,
    ) -> Dict[str, Any]:
        """Train both models on historical features and labels.

        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix from ``extract_ml_features()``.
        labels : pd.Series
            Classification labels from ``_generate_labels()``.
        validation_split : int
            Number of rows to hold out for validation (from the end).

        Returns
        -------
        dict
            Training metrics: train_accuracy, val_accuracy, samples_used, class_distribution.
        """
        # Drop rows where labels are NaN
        valid_mask = labels.notna()
        X = features[valid_mask]
        y = labels[valid_mask].astype(int)

        if len(X) < MIN_TRAINING_ROWS:
            raise ValueError(
                f"Insufficient training data: {len(X)} rows (minimum: {MIN_TRAINING_ROWS})"
            )

        self.feature_names = list(X.columns)
        self._feature_means = X.mean()

        # Split: train vs validation
        val_size = min(validation_split, len(X) // 5)
        X_train = X.iloc[:-val_size]
        y_train = y.iloc[:-val_size]
        X_val = X.iloc[-val_size:]
        y_val = y.iloc[-val_size:]

        # Train models
        self.rf.fit(X_train, y_train)
        self.gb.fit(X_train, y_train)

        # Compute metrics
        train_acc_rf = self.rf.score(X_train, y_train)
        train_acc_gb = self.gb.score(X_train, y_train)
        val_acc_rf = self.rf.score(X_val, y_val) if len(X_val) > 0 else 0
        val_acc_gb = self.gb.score(X_val, y_val) if len(X_val) > 0 else 0

        self.training_metrics = {
            "train_accuracy": round((train_acc_rf + train_acc_gb) / 2, 3),
            "validation_accuracy": round((val_acc_rf + val_acc_gb) / 2, 3),
            "samples_used": len(X_train),
            "validation_samples": len(X_val),
            "class_distribution": {
                LABEL_MAP[int(c)]: int((y_train == c).sum())
                for c in sorted(y_train.unique())
            },
        }

        self.is_trained = True
        logger.info(
            f"ML Signal Engine trained: {self.training_metrics}"
        )

        return self.training_metrics

    def predict(
        self,
        features: pd.DataFrame,
        regime: str = "Unknown",
        anomaly_detected: bool = False,
        trend_aligned: bool = True,
    ) -> Dict[str, Any]:
        """Predict signal for the latest row using soft-vote ensemble.

        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix — prediction uses the **last row**.
        regime : str
            Current market regime from ``detect_regime()``.
        anomaly_detected : bool
            Whether an anomaly was detected by IsolationForest.
        trend_aligned : bool
            Whether the SMA20 > SMA50 trend structure supports the signal.

        Returns
        -------
        dict
            Complete signal dictionary with 7-class taxonomy.
        """
        if not self.is_trained:
            raise RuntimeError("MLSignalEngine has not been trained yet.")

        # Get latest row features
        latest = features.iloc[[-1]][self.feature_names]

        # Get class probabilities from both models
        rf_probs = self.rf.predict_proba(latest)[0]
        gb_probs = self.gb.predict_proba(latest)[0]

        # Ensure both models have all 3 classes
        rf_prob_dict = self._probs_to_dict(self.rf.classes_, rf_probs)
        gb_prob_dict = self._probs_to_dict(self.gb.classes_, gb_probs)

        # Soft-vote: average probabilities
        avg_probs = {
            "bearish": (rf_prob_dict["bearish"] + gb_prob_dict["bearish"]) / 2,
            "neutral": (rf_prob_dict["neutral"] + gb_prob_dict["neutral"]) / 2,
            "bullish": (rf_prob_dict["bullish"] + gb_prob_dict["bullish"]) / 2,
        }

        # Model agreement (how similar are the two model's predictions)
        agreement = 1.0 - sum(
            abs(rf_prob_dict[c] - gb_prob_dict[c]) for c in avg_probs
        ) / 2.0

        # Classify into 7-class taxonomy
        signal = self._classify_signal(
            avg_probs, regime, anomaly_detected, trend_aligned
        )

        # Determine simplified signal class
        signal_class = self._get_signal_class(signal)

        # Get confidence (max probability)
        confidence = max(avg_probs.values())

        # Get color
        color_hex, color_name = SIGNAL_COLORS.get(
            signal, ("#FEB019", "yellow")
        )

        # Explain the signal
        contributing_factors = self._explain_signal(features.iloc[-1])

        # Build explanation text
        explanation = self._build_explanation(
            signal, confidence, contributing_factors
        )

        # Build recommendation text
        recommendation = (
            f"**{signal}** (confidence {confidence:.0%}) — {explanation}"
        )

        return {
            "signal": signal,
            "signal_class": signal_class,
            "confidence": round(confidence, 3),
            "probabilities": {
                k: round(v, 3) for k, v in avg_probs.items()
            },
            "color": color_name,
            "color_hex": color_hex,
            "contributing_factors": contributing_factors,
            "explanation": explanation,
            "recommendation": recommendation,
            "model_agreement": round(agreement, 3),
            "training_metrics": self.training_metrics,
            "horizon": 5,
            "method": "ml_ensemble",
        }

    def _probs_to_dict(self, classes: np.ndarray, probs: np.ndarray) -> Dict[str, float]:
        """Convert class array + probability array to labelled dict."""
        result = {"bearish": 0.0, "neutral": 0.0, "bullish": 0.0}
        for cls, prob in zip(classes, probs):
            label = LABEL_MAP.get(int(cls), "neutral")
            result[label] = float(prob)
        return result

    @staticmethod
    def _classify_signal(
        probs: Dict[str, float],
        regime: str,
        anomaly_detected: bool,
        trend_aligned: bool,
    ) -> str:
        """Map averaged probabilities to 7-class signal taxonomy.

        Decision order (first match wins):
        1. High Volatility / Uncertain — if anomaly AND high vol regime
        2. Strong Bullish — bullish prob >= 0.70
        3. Bullish Continuation — bullish 0.55–0.70 AND trend aligned
        4. Weak Bullish — bullish 0.55–0.70 AND trend NOT aligned
        5. Strong Bearish — bearish prob >= 0.70
        6. Bearish Breakdown — bearish 0.55–0.70 AND trend aligned (bearish)
        7. Weak Bearish — bearish 0.55–0.70 AND trend NOT aligned
        8. Neutral / Consolidation — fallback
        """
        bull_p = probs.get("bullish", 0)
        bear_p = probs.get("bearish", 0)

        # 1. Uncertainty check
        if anomaly_detected and "High Volatility" in regime:
            return "High Volatility / Uncertain"

        # 2-4. Bullish signals
        if bull_p >= 0.70:
            return "Strong Bullish"
        if bull_p >= 0.55:
            return "Bullish Continuation" if trend_aligned else "Weak Bullish"

        # 5-7. Bearish signals
        if bear_p >= 0.70:
            return "Strong Bearish"
        if bear_p >= 0.55:
            return "Bearish Breakdown" if not trend_aligned else "Weak Bearish"

        # 8. Neutral fallback
        return "Neutral / Consolidation"

    @staticmethod
    def _get_signal_class(signal: str) -> str:
        """Map 7-class signal to simplified class."""
        if "Bullish" in signal:
            return "bullish"
        if "Bearish" in signal:
            return "bearish"
        if "Uncertain" in signal or "Volatility" in signal:
            return "uncertain"
        return "neutral"

    def _explain_signal(self, features_row: pd.Series) -> List[Dict[str, Any]]:
        """Generate contributing factors from feature importances.

        Returns top 5 features with their impact direction and detail.
        """
        if not self.is_trained or not self.feature_names:
            return []

        # Average feature importances from both models
        rf_imp = dict(zip(self.feature_names, self.rf.feature_importances_))
        gb_imp = dict(zip(self.feature_names, self.gb.feature_importances_))

        avg_importance = {
            name: (rf_imp.get(name, 0) + gb_imp.get(name, 0)) / 2
            for name in self.feature_names
        }

        # Sort by importance (descending)
        top_features = sorted(
            avg_importance.items(), key=lambda x: x[1], reverse=True
        )[:5]

        factors = []
        for feat_name, importance in top_features:
            value = features_row.get(feat_name, 0)
            mean_val = (
                self._feature_means[feat_name]
                if self._feature_means is not None and feat_name in self._feature_means
                else 0
            )

            # Determine impact direction
            # Positive features (higher = more bullish)
            bullish_features = {
                "rsi", "rsi_slope_5", "macd_histogram", "macd_hist_change",
                "sma20_sma50_ratio", "sma20_slope", "price_vs_sma20",
                "price_vs_sma50", "volume_ratio", "volume_expansion",
                "roc_5", "roc_10", "roc_20", "bullish_streak",
                "rsi_above_50_duration", "bb_position", "trade_quality_score",
            }

            if feat_name in bullish_features:
                impact = "positive" if value > mean_val else "negative"
            else:
                # Volatility/wick features: lower is generally better for bullish
                impact = "negative" if value > mean_val else "positive"

            detail = get_feature_detail(feat_name, value, mean_val)
            display_name = FEATURE_DISPLAY_NAMES.get(feat_name, feat_name)

            factors.append({
                "factor": display_name,
                "feature_name": feat_name,
                "impact": impact,
                "importance": round(importance, 4),
                "detail": detail,
            })

        return factors

    def _build_explanation(
        self,
        signal: str,
        confidence: float,
        factors: List[Dict[str, Any]],
    ) -> str:
        """Build human-readable explanation from signal and factors."""
        if not factors:
            return f"{signal} signal detected with {confidence:.0%} confidence."

        pos_factors = [f["factor"] for f in factors if f["impact"] == "positive"][:3]
        neg_factors = [f["factor"] for f in factors if f["impact"] == "negative"][:2]

        parts = []
        if pos_factors:
            parts.append(
                signal.split("/")[0].strip()
                + " supported by "
                + ", ".join(pos_factors).lower()
            )
        if neg_factors:
            parts.append("tempered by " + ", ".join(neg_factors).lower())

        if parts:
            return ". ".join(parts) + "."
        return f"{signal} signal detected with {confidence:.0%} confidence."


# ── Cached Training Wrapper ──────────────────────────────────────────────

# Module-level cache for trained engines (keyed by ticker+period)
_engine_cache: Dict[str, MLSignalEngine] = {}


def _get_or_train_engine(
    df: pd.DataFrame, ticker: str, period: str, extra_signals: dict = None
) -> Tuple[MLSignalEngine, pd.DataFrame]:
    """Get a cached engine or train a new one.

    Returns (engine, features_df).
    """
    cache_key = f"{ticker}_{period}"

    if cache_key in _engine_cache:
        engine = _engine_cache[cache_key]
        features = extract_ml_features(df, extra_signals)
        return engine, features

    # Train new engine
    engine = MLSignalEngine()
    features = extract_ml_features(df, extra_signals)
    labels = _generate_labels(df, horizon=5)

    engine.train(features, labels)

    # Cache it
    _engine_cache[cache_key] = engine

    return engine, features


# ── Main Entry Point ─────────────────────────────────────────────────────

def ml_generate_signal(
    df: pd.DataFrame,
    extra_signals: dict = None,
    ticker: str = "STOCK",
    period: str = "6mo",
) -> Dict[str, Any]:
    """Main entry point for ML signal generation.

    Uses the ML ensemble engine if sufficient data is available,
    otherwise falls back to the rule-based engine.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with OHLCV + indicators from ``compute_all_indicators()``.
    extra_signals : dict, optional
        Cross-module signals: ``{"trade_quality": 7.2, "anomaly_score": 15.0,
        "regime": "Trending Bullish"}``.
    ticker : str
        Ticker symbol (used for caching).
    period : str
        Data period (used for caching).

    Returns
    -------
    dict
        Signal dictionary with 7-class taxonomy, confidence, explanation.
        Contains ``"method": "ml_ensemble"`` or ``"method": "rule_based_fallback"``.
    """
    # Check minimum data requirement
    if df.empty or len(df) < MIN_TRAINING_ROWS:
        logger.info(
            f"Insufficient data for ML ({len(df)} rows). "
            f"Falling back to rule-based engine."
        )
        return _rule_based_fallback(df)

    try:
        engine, features = _get_or_train_engine(df, ticker, period, extra_signals)

        # Check validation accuracy
        val_acc = engine.training_metrics.get("validation_accuracy", 0)
        if val_acc < MIN_VALIDATION_ACCURACY:
            logger.warning(
                f"ML validation accuracy too low ({val_acc:.3f}). "
                f"Falling back to rule-based engine."
            )
            return _rule_based_fallback(df)

        # Determine regime and trend alignment from extra_signals
        regime = (extra_signals or {}).get("regime", "Unknown")
        anomaly_detected = (
            (extra_signals or {}).get("anomaly_score", 0) > 50
            or (extra_signals or {}).get("anomaly_class") == "Anomaly Detected"
        )

        # Trend alignment: SMA20 > SMA50
        latest = df.iloc[-1]
        sma20 = latest.get("SMA20", 0)
        sma50 = latest.get("SMA50", 0)
        trend_aligned = sma20 > sma50 if (pd.notna(sma20) and pd.notna(sma50)) else True

        # Predict
        signal_dict = engine.predict(
            features,
            regime=regime,
            anomaly_detected=anomaly_detected,
            trend_aligned=trend_aligned,
        )

        return signal_dict

    except Exception as e:
        logger.error(f"ML Signal Engine failed: {e}. Falling back to rule-based.")
        return _rule_based_fallback(df)


def _rule_based_fallback(df: pd.DataFrame) -> Dict[str, Any]:
    """Wrap rule-based signal output to match ML engine output format."""
    try:
        from signals.rule_based import generate_signals

        if df.empty:
            return _empty_signal()

        rb_result = generate_signals(df)

        # Map rule-based signal to 7-class taxonomy
        signal = rb_result.get("signal", "Neutral")
        signal_map = {
            "Strong Bullish": "Strong Bullish",
            "Bullish": "Weak Bullish",
            "Neutral": "Neutral / Consolidation",
            "Bearish": "Weak Bearish",
            "Strong Bearish": "Bearish Breakdown",
        }
        mapped_signal = signal_map.get(signal, "Neutral / Consolidation")

        # Determine signal class
        if "Bullish" in mapped_signal:
            signal_class = "bullish"
        elif "Bearish" in mapped_signal:
            signal_class = "bearish"
        else:
            signal_class = "neutral"

        confidence = rb_result.get("confidence", 0.0)
        color_hex, color_name = SIGNAL_COLORS.get(
            mapped_signal, ("#FEB019", "yellow")
        )

        return {
            "signal": mapped_signal,
            "signal_class": signal_class,
            "confidence": confidence,
            "probabilities": {
                "bullish": confidence if signal_class == "bullish" else 0.0,
                "neutral": confidence if signal_class == "neutral" else (1 - confidence),
                "bearish": confidence if signal_class == "bearish" else 0.0,
            },
            "color": color_name,
            "color_hex": color_hex,
            "contributing_factors": [],
            "explanation": rb_result.get("explanation", ""),
            "recommendation": rb_result.get("recommendation", ""),
            "model_agreement": 0.0,
            "training_metrics": {},
            "horizon": 5,
            "method": "rule_based_fallback",
        }
    except Exception as e:
        logger.error(f"Rule-based fallback also failed: {e}")
        return _empty_signal()


def _empty_signal() -> Dict[str, Any]:
    """Return an empty/default signal dict."""
    return {
        "signal": "Neutral / Consolidation",
        "signal_class": "neutral",
        "confidence": 0.0,
        "probabilities": {"bullish": 0.33, "neutral": 0.34, "bearish": 0.33},
        "color": "yellow",
        "color_hex": "#FEB019",
        "contributing_factors": [],
        "explanation": "Insufficient data for signal generation.",
        "recommendation": "**Neutral** — Insufficient data.",
        "model_agreement": 0.0,
        "training_metrics": {},
        "horizon": 5,
        "method": "insufficient_data",
    }
