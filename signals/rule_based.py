# signals/rule_based.py
"""Rule‑based signal generation for Indian stock analysis.
The engine examines technical indicator values and produces a structured
signal dictionary with:
- ``signal``: one of "Strong Bullish", "Bullish", "Neutral", "Bearish",
  "Strong Bearish"
- ``confidence``: float [0,1]
- ``explanation``: human‑readable description of why the signal was generated.
- ``recommendation``: a ready‑to‑display markdown string for the UI.
"""

from typing import Dict, Any
import pandas as pd

# Thresholds (can be tweaked later)
RSI_OVERSOLD = 30
RSI_OVERBORED = 70
MACD_CROSS_THRESHOLD = 0
VOLUME_SPIKE_MULTIPLIER = 1.5  # volume compared to 20‑day SMA volume
ATR_VOLATILITY_THRESHOLD = 0.02  # relative to price


def _latest_row(df: pd.DataFrame) -> pd.Series:
    """Return the most recent row (last index) of the indicator DataFrame."""
    return df.iloc[-1]


def _volume_spike(df: pd.DataFrame) -> bool:
    """Detect a volume spike: current volume > multiplier * SMA20 volume.
    Returns ``True`` if a spike is present.
    """
    if "Volume" not in df.columns:
        return False
    vol_series = df["Volume"]
    sma20_vol = vol_series.rolling(20, min_periods=1).mean().iloc[-1]
    return vol_series.iloc[-1] > VOLUME_SPIKE_MULTIPLIER * sma20_vol


def _price_trend(df: pd.DataFrame) -> int:
    """Determine price trend based on SMA20 vs SMA50.
    Returns ``+1`` for bullish, ``-1`` for bearish, ``0`` for neutral.
    """
    if "SMA20" not in df.columns or "SMA50" not in df.columns:
        return 0
    sma20 = df["SMA20"].iloc[-1]
    sma50 = df["SMA50"].iloc[-1]
    if sma20 > sma50:
        return 1
    if sma20 < sma50:
        return -1
    return 0


def generate_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a signal dictionary from a DataFrame containing all indicators.

    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame returned by ``analytics.indicators.compute_all_indicators``.

    Returns
    -------
    dict
        ``{"signal": ..., "confidence": ..., "explanation": ..., "recommendation": ...}``
    """
    row = _latest_row(df)
    score = 0
    reasons = []

    # 1. RSI assessment
    rsi = row.get("RSI")
    if pd.notna(rsi):
        if rsi < RSI_OVERSOLD:
            score += 1
            reasons.append(f"RSI {rsi:.1f} indicates oversold conditions (bullish).")
        elif rsi > RSI_OVERBORED:
            score -= 1
            reasons.append(f"RSI {rsi:.1f} indicates overbought conditions (bearish).")
        else:
            reasons.append(f"RSI {rsi:.1f} is neutral.")

    # 2. MACD crossover
    macd = row.get("MACD")
    macd_sig = row.get("MACD_Signal")
    if pd.notna(macd) and pd.notna(macd_sig):
        diff = macd - macd_sig
        if diff > MACD_CROSS_THRESHOLD:
            score += 1
            reasons.append("MACD is above its signal line (bullish).")
        elif diff < -MACD_CROSS_THRESHOLD:
            score -= 1
            reasons.append("MACD is below its signal line (bearish).")
        else:
            reasons.append("MACD near signal line – neutral.")

    # 3. Trend via moving averages
    trend = _price_trend(df)
    if trend == 1:
        score += 1
        reasons.append("20‑day SMA above 50‑day SMA – uptrend.")
    elif trend == -1:
        score -= 1
        reasons.append("20‑day SMA below 50‑day SMA – downtrend.")
    else:
        reasons.append("SMA20 and SMA50 are close – sideways.")

    # 4. Volume spike
    if _volume_spike(df):
        score += 1
        reasons.append("Current volume exceeds 1.5× 20‑day average – strong interest.")

    # 5. ATR (volatility) – high ATR can indicate strong moves
    atr = row.get("ATR")
    close = row.get("Close")
    if pd.notna(atr) and pd.notna(close) and close != 0:
        rel_atr = atr / close
        if rel_atr > ATR_VOLATILITY_THRESHOLD:
            score += 1
            reasons.append(f"ATR {atr:.2f} ({rel_atr:.2%}) signals heightened volatility.")
        else:
            reasons.append(f"ATR {atr:.2f} ({rel_atr:.2%}) within normal range.")

    # Map score to signal categories
    if score >= 3:
        signal = "Strong Bullish"
        color = "green"
    elif score == 2:
        signal = "Bullish"
        color = "green"
    elif score == 1:
        signal = "Neutral"
        color = "yellow"
    elif score == 0:
        signal = "Neutral"
        color = "yellow"
    elif score == -1:
        signal = "Neutral"
        color = "yellow"
    elif score == -2:
        signal = "Bearish"
        color = "red"
    else:  # score <= -3
        signal = "Strong Bearish"
        color = "red"

    confidence = min(abs(score) / 5.0, 1.0)  # normalize to [0,1]
    explanation = " ".join(reasons)

    # Build markdown recommendation
    recommendation = f"**{signal}** (confidence {confidence:.0%}) – {explanation}"

    return {
        "signal": signal,
        "color": color,
        "confidence": confidence,
        "explanation": explanation,
        "recommendation": recommendation,
    }
