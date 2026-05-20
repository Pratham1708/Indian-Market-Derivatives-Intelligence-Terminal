# src/analytics/probability_engine.py
"""Probabilistic Setup Engine for Phase 3.
Estimates setup success probability using historical hit rate + factor adjustments.
Provides expected-move forecasting based on ATR.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def _historical_hit_rate(df: pd.DataFrame, setup_type: str) -> float:
    """Scan historical data for setup occurrences and compute hit rate (5-day forward return > 0)."""
    if len(df) < 30:
        return 0.50  # prior / fallback

    mask = pd.Series(False, index=df.index)

    if setup_type == "Breakout":
        mask = df["Close"] > df["BB_Upper"]
    elif setup_type == "Pullback":
        mask = (df["SMA20"] > df["SMA50"]) & (df["Close"] <= df["SMA20"] * 1.01)
    elif setup_type == "Reversal":
        mask = (df["RSI"].shift(1) < 30) & (df["RSI"] >= 30)
    elif setup_type == "Trend Continuation":
        mask = (df["SMA20"] > df["SMA50"]) & (df["MACD"] > df["MACD_Signal"])

    mask = mask.fillna(False)
    indices = df.index[mask]

    if len(indices) < 3:
        return 0.50  # not enough data, use neutral prior

    wins = 0
    total = 0
    for idx in indices:
        pos = df.index.get_loc(idx)
        if pos + 5 < len(df):
            entry = df.iloc[pos]["Close"]
            exit_ = df.iloc[pos + 5]["Close"]
            total += 1
            if exit_ > entry:
                wins += 1

    return wins / total if total >= 3 else 0.50


def estimate_setup_probability(
    df: pd.DataFrame, setup_type: str
) -> Dict[str, object]:
    """Estimate the probability of setup success using historical + factor adjustments.

    Returns dict with probability, confidence_band, factors, explanation.
    """
    default = {
        "probability": 0.50,
        "confidence_band": (0.40, 0.60),
        "factors": {},
        "probability_label": "Moderate Probability ⚠",
        "explanation": "Insufficient data for probability estimation.",
    }

    if df.empty or len(df) < 30:
        return default

    latest = df.iloc[-1]

    # Base: historical hit rate
    base = _historical_hit_rate(df, setup_type)

    # Factor adjustments
    factors = {}

    # Momentum factor
    rsi = latest.get("RSI", 50)
    if 40 <= rsi <= 70:
        factors["momentum"] = 0.05
    else:
        factors["momentum"] = -0.05

    # Volume factor
    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    if pd.notna(avg_vol) and avg_vol > 0 and latest.get("Volume", 0) > avg_vol:
        factors["volume_confirmation"] = 0.05
    else:
        factors["volume_confirmation"] = -0.02

    # Trend alignment factor
    sma20 = latest.get("SMA20", 0)
    sma50 = latest.get("SMA50", 0)
    if setup_type in ("Breakout", "Trend Continuation", "Pullback"):
        if sma20 > sma50:
            factors["trend_alignment"] = 0.05
        else:
            factors["trend_alignment"] = -0.05
    else:
        factors["trend_alignment"] = 0.0

    # Volatility factor
    atr = latest.get("ATR", 0)
    close = latest.get("Close", 1)
    atr_ratio = atr / close if close else 0
    if atr_ratio < 0.025:
        factors["volatility_quality"] = 0.03
    else:
        factors["volatility_quality"] = -0.03

    # Final probability
    adjustment = sum(factors.values())
    prob = np.clip(base + adjustment, 0.10, 0.95)
    band = (round(max(0.05, prob - 0.10), 2), round(min(0.99, prob + 0.10), 2))

    label = get_probability_label(prob)

    # Explanation
    factor_parts = []
    if factors.get("volume_confirmation", 0) > 0:
        factor_parts.append("strong volume")
    if factors.get("momentum", 0) > 0:
        factor_parts.append("favorable momentum")
    if factors.get("trend_alignment", 0) > 0:
        factor_parts.append("trend alignment")
    if factors.get("volatility_quality", 0) > 0:
        factor_parts.append("controlled volatility")

    prob_pct = round(prob * 100, 1)
    if factor_parts:
        explanation = f"{setup_type} probability estimated at {prob_pct}% supported by {', '.join(factor_parts)}."
    else:
        explanation = f"{setup_type} probability estimated at {prob_pct}% based on historical analysis."

    return {
        "probability": round(prob, 3),
        "confidence_band": band,
        "factors": factors,
        "probability_label": label,
        "explanation": explanation,
    }


def get_probability_label(prob: float) -> str:
    """Human-readable probability label."""
    if prob >= 0.70:
        return "High Probability ✅"
    if prob >= 0.50:
        return "Moderate Probability ⚠"
    return "Low Probability ❌"


def compute_expected_move(df: pd.DataFrame, days: int = 5) -> Dict[str, object]:
    """Estimate expected price range over N days using ATR and recent volatility.

    Returns dict with expected_move_pct, upper_target, lower_target, explanation.
    """
    default = {
        "expected_move_pct": 0.0,
        "upper_target": 0.0,
        "lower_target": 0.0,
        "explanation": "Insufficient data for move estimation.",
    }

    if df.empty or len(df) < 20:
        return default

    latest = df.iloc[-1]
    close = latest.get("Close", 0)
    atr = latest.get("ATR", 0)

    if close == 0 or atr == 0:
        return default

    # Expected move ≈ ATR * sqrt(days) scaled
    expected_move = atr * np.sqrt(days)
    move_pct = (expected_move / close) * 100

    upper = round(close + expected_move, 2)
    lower = round(close - expected_move, 2)

    return {
        "expected_move_pct": round(move_pct, 2),
        "upper_target": upper,
        "lower_target": lower,
        "explanation": (
            f"Expected {days}-day move: ±{round(move_pct, 1)}% "
            f"(₹{lower:,.0f} – ₹{upper:,.0f}) based on ATR volatility."
        ),
    }
