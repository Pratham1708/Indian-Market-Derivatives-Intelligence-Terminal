# src/analytics/regime_detection.py
"""Regime Transition Detection Engine for Phase 3.
Detects current market regime, identifies transitions, and generates alerts.
"""

import pandas as pd
import numpy as np
from typing import Dict


def detect_regime_at_row(row: pd.Series) -> str:
    """Classify regime for a single row of indicator data."""
    close = row.get("Close", 0)
    sma20 = row.get("SMA20", 0)
    sma50 = row.get("SMA50", 0)
    macd = row.get("MACD", 0)
    macd_sig = row.get("MACD_Signal", 0)
    atr = row.get("ATR", 0)

    atr_ratio = atr / close if close else 0

    if atr_ratio > 0.03:
        return "High Volatility Expansion"
    if atr_ratio < 0.012:
        return "Consolidation"
    if sma20 > sma50 and macd > macd_sig:
        return "Trending Bullish"
    if sma20 < sma50 and macd < macd_sig:
        return "Trending Bearish"
    return "Sideways"


def detect_regime(df: pd.DataFrame) -> Dict[str, object]:
    """Detect current regime, previous regime, and whether a transition occurred.

    Parameters
    ----------
    df : DataFrame with OHLCV + indicators

    Returns
    -------
    dict with current_regime, previous_regime, transition_detected,
    transition_description, regime_duration, explanation
    """
    default = {
        "current_regime": "Unknown",
        "previous_regime": "Unknown",
        "transition_detected": False,
        "transition_description": "",
        "regime_duration": 0,
        "explanation": "Insufficient data for regime detection.",
    }

    if df.empty or len(df) < 20:
        return default

    latest = df.iloc[-1]
    current_regime = detect_regime_at_row(latest)

    # Previous regime: look back 10 bars
    lookback = min(10, len(df) - 1)
    prev_row = df.iloc[-(lookback + 1)]
    previous_regime = detect_regime_at_row(prev_row)

    transition = current_regime != previous_regime

    # Regime duration: count consecutive bars matching current regime (up to 50)
    duration = 0
    for i in range(1, min(len(df), 51)):
        row = df.iloc[-i]
        if detect_regime_at_row(row) == current_regime:
            duration += 1
        else:
            break

    # Transition description
    if transition:
        desc = f"{previous_regime} → {current_regime}"
    else:
        desc = f"Stable {current_regime} (for {duration} bars)"

    # Explanation
    atr_ratio = latest.get("ATR", 0) / latest.get("Close", 1) if latest.get("Close", 1) else 0
    rsi = latest.get("RSI", 50)

    parts = [f"Current regime: {current_regime}."]
    if transition:
        parts.append(f"Transition detected from {previous_regime}.")
    if atr_ratio > 0.025:
        parts.append("Elevated volatility observed.")
    if rsi > 70:
        parts.append("Overbought momentum may signal exhaustion.")
    elif rsi < 30:
        parts.append("Oversold conditions may signal reversal potential.")

    return {
        "current_regime": current_regime,
        "previous_regime": previous_regime,
        "transition_detected": transition,
        "transition_description": desc,
        "regime_duration": duration,
        "explanation": " ".join(parts),
    }


def get_regime_alert(regime_info: Dict) -> str:
    """Return a user-friendly alert string from regime detection results."""
    current = regime_info.get("current_regime", "Unknown")
    transition = regime_info.get("transition_detected", False)
    prev = regime_info.get("previous_regime", "Unknown")
    duration = regime_info.get("regime_duration", 0)

    if transition:
        if current == "High Volatility Expansion":
            return "⚠ Volatility expansion beginning."
        if current == "Consolidation" and prev.startswith("Trending"):
            return "⚠ Trend exhaustion — entering consolidation."
        if current == "Trending Bullish" and prev == "Consolidation":
            return "📈 Breakout from consolidation — bullish trend emerging."
        if current == "Trending Bearish":
            return "⚠ Momentum regime weakening — bearish transition."
        return f"⚠ Regime shift: {prev} → {current}."
    else:
        if current == "Trending Bullish" and duration > 20:
            return "✅ Stable bullish trend continuing."
        if current == "Trending Bearish" and duration > 20:
            return "⚠ Extended bearish trend — caution advised."
        if current == "High Volatility Expansion":
            return "⚠ High volatility regime active."
        if current == "Consolidation":
            return "ℹ Market consolidating — watch for breakout."
        return f"ℹ {current} regime (duration: {duration} bars)."
