# src/analytics/derivatives_sentiment.py
"""Derivatives Sentiment Engine for Phase 4.
Simulates OI-based sentiment analysis (PCR, buildup classification,
max pain) using OHLCV + volume data as proxies when live option
chain data is unavailable.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def estimate_pcr(df: pd.DataFrame) -> float:
    """Estimate Put-Call Ratio proxy from price action.
    
    Uses the ratio of bearish-volume days to bullish-volume days
    as a sentiment proxy when actual OI data is unavailable.
    """
    if df.empty or len(df) < 20:
        return 1.0

    recent = df.tail(20).copy()
    recent["change"] = recent["Close"].pct_change()
    bearish_vol = recent.loc[recent["change"] < 0, "Volume"].sum()
    bullish_vol = recent.loc[recent["change"] > 0, "Volume"].sum()

    if bullish_vol == 0:
        return 2.0  # extreme bearish
    return round(float(bearish_vol / bullish_vol), 2)


def classify_oi_buildup(df: pd.DataFrame) -> Dict[str, str]:
    """Classify Open Interest buildup type from price + volume behavior.
    
    Returns classification and explanation.
    """
    if df.empty or len(df) < 10:
        return {"buildup": "Unknown", "explanation": "Insufficient data."}

    recent = df.tail(10)
    price_change = (recent["Close"].iloc[-1] - recent["Close"].iloc[0]) / recent["Close"].iloc[0]
    vol_trend = recent["Volume"].iloc[-5:].mean() / max(recent["Volume"].iloc[:5].mean(), 1)

    if price_change > 0.02 and vol_trend > 1.1:
        return {
            "buildup": "Long Buildup",
            "explanation": "Rising price with rising volume — fresh buying detected.",
        }
    elif price_change < -0.02 and vol_trend > 1.1:
        return {
            "buildup": "Short Buildup",
            "explanation": "Falling price with rising volume — fresh shorting detected.",
        }
    elif price_change > 0.01 and vol_trend < 0.9:
        return {
            "buildup": "Short Covering",
            "explanation": "Rising price with declining volume — shorts exiting positions.",
        }
    elif price_change < -0.01 and vol_trend < 0.9:
        return {
            "buildup": "Long Unwinding",
            "explanation": "Falling price with declining volume — longs exiting positions.",
        }
    return {
        "buildup": "Neutral",
        "explanation": "No strong directional buildup detected.",
    }


def estimate_max_pain(spot: float) -> Dict[str, float]:
    """Estimate max pain zone as nearest round strike level.
    
    In the absence of live OI data, max pain is approximated as
    the nearest round number strike (to nearest 50 for large-cap stocks).
    """
    rounded = round(spot / 50) * 50
    return {
        "max_pain_estimate": rounded,
        "distance_pct": round(abs(spot - rounded) / spot * 100, 2),
    }


def compute_derivatives_sentiment(df: pd.DataFrame) -> Dict[str, object]:
    """Full derivatives sentiment analysis for a stock.
    
    Returns PCR proxy, OI buildup classification, max pain estimate,
    overall sentiment, and explanation.
    """
    if df.empty or len(df) < 20:
        return {
            "pcr": 1.0,
            "buildup": "Unknown",
            "max_pain": 0.0,
            "sentiment": "Neutral",
            "explanation": "Insufficient data for derivatives sentiment.",
        }

    pcr = estimate_pcr(df)
    buildup_info = classify_oi_buildup(df)
    spot = float(df.iloc[-1]["Close"])
    max_pain_info = estimate_max_pain(spot)

    # Overall sentiment
    bullish_signals = 0
    bearish_signals = 0

    if pcr < 0.7:
        bullish_signals += 1
    elif pcr > 1.3:
        bearish_signals += 1

    if buildup_info["buildup"] in ("Long Buildup", "Short Covering"):
        bullish_signals += 1
    elif buildup_info["buildup"] in ("Short Buildup", "Long Unwinding"):
        bearish_signals += 1

    if bullish_signals > bearish_signals:
        sentiment = "Bullish Positioning"
    elif bearish_signals > bullish_signals:
        sentiment = "Bearish Positioning"
    else:
        sentiment = "Neutral Positioning"

    # Explanation
    parts = [f"PCR proxy: {pcr} —"]
    if pcr < 0.7:
        parts.append("bullish sentiment (more call-side activity).")
    elif pcr > 1.3:
        parts.append("bearish sentiment (more put-side activity).")
    else:
        parts.append("neutral sentiment.")
    parts.append(f"OI Buildup: {buildup_info['buildup']}.")
    parts.append(f"Max pain estimate: ₹{max_pain_info['max_pain_estimate']:,.0f}.")

    return {
        "pcr": pcr,
        "buildup": buildup_info["buildup"],
        "buildup_explanation": buildup_info["explanation"],
        "max_pain": max_pain_info["max_pain_estimate"],
        "max_pain_distance_pct": max_pain_info["distance_pct"],
        "sentiment": sentiment,
        "explanation": " ".join(parts),
    }
