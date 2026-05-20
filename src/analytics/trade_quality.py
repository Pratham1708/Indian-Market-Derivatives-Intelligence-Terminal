# src/analytics/trade_quality.py
"""Trade quality scoring utilities.
Provides a composite score for a trade based on multiple quantitative
components (trend, momentum, volume, volatility, etc.).
"""

from typing import Dict
import numpy as np


def score_trend_strength(sma_diff: float) -> float:
    """Score trend strength from SMA difference.
    Positive diff => bullish trend. Normalized to 0‑10.
    """
    # simple linear mapping, cap at 10
    score = np.clip(sma_diff * 10, -10, 10)
    return max(score, 0) / 10 * 10  # ensure 0‑10 range


def score_momentum(rsi: float) -> float:
    """Score momentum from RSI (0‑100)."""
    if rsi >= 70:
        return 8.0
    if rsi <= 30:
        return 2.0
    # linear between 30 and 70
    return 2.0 + (rsi - 30) * (6.0 / 40.0)


def score_volume(volume: float, avg_volume: float) -> float:
    """Score volume confirmation.
    Relative volume > 1.5 = 9, >1.0 = 7, else 4.
    """
    rel = volume / avg_volume if avg_volume else 0
    if rel >= 1.5:
        return 9.0
    if rel >= 1.0:
        return 7.0
    return 4.0


def score_volatility(atr: float, price: float) -> float:
    """Score volatility quality.
    Lower ATR % of price gets higher score.
    """
    perc = (atr / price) * 100 if price else 0
    if perc < 1:
        return 9.0
    if perc < 2:
        return 7.0
    return 5.0


def compute_trade_quality_score(
    sma_diff: float,
    rsi: float,
    volume: float,
    avg_volume: float,
    atr: float,
    price: float,
) -> Dict[str, float]:
    """Return component scores and an overall weighted score.
    Weighting can be tuned; currently equal weighting.
    """
    trend = score_trend_strength(sma_diff)
    momentum = score_momentum(rsi)
    vol_conf = score_volume(volume, avg_volume)
    vol_quality = score_volatility(atr, price)
    # simple average for overall quality
    overall = np.mean([trend, momentum, vol_conf, vol_quality])
    return {
        "trend_strength": round(trend, 1),
        "momentum": round(momentum, 1),
        "volume_confirmation": round(vol_conf, 1),
        "volatility_quality": round(vol_quality, 1),
        "overall_quality": round(overall, 2),
    }

# Example usage (called from UI)
# scores = compute_trade_quality_score(sma_diff=0.02, rsi=55, volume=1.2e6,
#                                     avg_volume=1.0e6, atr=12, price=2450)
