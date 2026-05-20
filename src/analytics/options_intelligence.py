# src/analytics/options_intelligence.py
"""Options Intelligence Engine for Phase 4.
Integrates Black-Scholes pricing, Greeks, implied volatility,
IV percentile, and realized-vs-implied volatility analysis
into the trader intelligence workflow.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
from scipy.stats import norm
from scipy.optimize import brentq


# ── Black-Scholes Core ────────────────────────────────────────────────────

def _d1_d2(S: float, K: float, T: float, r: float, sigma: float):
    if T <= 0 or sigma <= 0:
        return 0.0, 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_price(S, K, T, r, sigma, option_type="call"):
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    if option_type == "call":
        return float(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    return float(K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))


def calculate_greeks(S, K, T, r, sigma, option_type="call") -> Dict[str, float]:
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T)) if T > 0 and sigma > 0 else 0
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100 if T > 0 else 0
    if T > 0 and sigma > 0:
        common = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        if option_type == "call":
            theta = (common - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        else:
            theta = (common + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    else:
        theta = 0
    if option_type == "call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    return {
        "Delta": round(float(delta), 4),
        "Gamma": round(float(gamma), 6),
        "Vega": round(float(vega), 4),
        "Theta": round(float(theta), 4),
        "Rho": round(float(rho), 4),
    }


# ── Implied Volatility ───────────────────────────────────────────────────

def implied_volatility(
    market_price: float, S: float, K: float, T: float, r: float,
    option_type: str = "call"
) -> float:
    """Calculate IV using Brent's method. Returns annualized IV."""
    if T <= 0 or market_price <= 0:
        return 0.0
    try:
        def objective(sigma):
            return bs_price(S, K, T, r, sigma, option_type) - market_price
        iv = brentq(objective, 0.001, 5.0, xtol=1e-6)
        return round(float(iv), 4)
    except Exception:
        return 0.0


# ── Realized vs Implied Volatility ────────────────────────────────────────

def realized_volatility(df: pd.DataFrame, window: int = 20) -> float:
    """Annualized realized volatility from log returns."""
    if df.empty or len(df) < window:
        return 0.0
    log_ret = np.log(df["Close"] / df["Close"].shift(1)).dropna()
    rv = float(log_ret.tail(window).std() * np.sqrt(252))
    return round(rv, 4)


def iv_percentile(current_iv: float, historical_ivs: list) -> float:
    """IV percentile: % of historical IV values below current IV."""
    if not historical_ivs or current_iv <= 0:
        return 0.0
    below = sum(1 for iv in historical_ivs if iv < current_iv)
    return round(below / len(historical_ivs) * 100, 1)


# ── Integrated Options Intelligence ──────────────────────────────────────

def compute_options_intelligence(
    df: pd.DataFrame,
    strike: Optional[float] = None,
    r: float = 0.065,
    T: float = 30 / 365,
) -> Dict[str, object]:
    """Compute options intelligence for a stock using its OHLCV data.
    
    If no strike is provided, uses ATM (current close price).
    Uses realized volatility as a proxy for IV when market option prices
    are not available.
    """
    if df.empty or len(df) < 30:
        return {
            "iv_estimate": 0.0, "rv_20d": 0.0, "iv_percentile": 0.0,
            "iv_regime": "Unknown", "call_price": 0.0, "put_price": 0.0,
            "greeks_call": {}, "greeks_put": {},
            "explanation": "Insufficient data for options intelligence.",
        }

    close = float(df.iloc[-1]["Close"])
    K = strike if strike else round(close / 50) * 50  # Round to nearest 50
    
    # Realized Volatility
    rv = realized_volatility(df, window=20)
    
    # Estimate IV as RV (proxy when no options market data)
    iv_est = rv
    
    # IV percentile from rolling RV history
    rv_series = []
    for i in range(20, len(df)):
        log_ret = np.log(df["Close"].iloc[i-19:i+1] / df["Close"].iloc[i-19:i+1].shift(1)).dropna()
        if len(log_ret) > 0:
            rv_series.append(float(log_ret.std() * np.sqrt(252)))
    
    iv_pct = iv_percentile(iv_est, rv_series)
    
    # IV Regime
    if iv_pct >= 80:
        iv_regime = "High IV (Elevated Premiums)"
    elif iv_pct >= 50:
        iv_regime = "Moderate IV"
    elif iv_pct >= 20:
        iv_regime = "Low IV"
    else:
        iv_regime = "Very Low IV (Compressed)"
    
    # Price options
    cp = bs_price(close, K, T, r, iv_est, "call")
    pp = bs_price(close, K, T, r, iv_est, "put")
    
    # Greeks
    greeks_c = calculate_greeks(close, K, T, r, iv_est, "call")
    greeks_p = calculate_greeks(close, K, T, r, iv_est, "put")
    
    # Explanation
    parts = [f"IV estimate: {iv_est*100:.1f}% (from 20-day realized vol)."]
    parts.append(f"IV percentile: {iv_pct:.0f}%.")
    if iv_pct >= 80:
        parts.append("Elevated premiums — option selling may be attractive.")
    elif iv_pct <= 20:
        parts.append("Compressed volatility — option buying is relatively cheap.")
    
    return {
        "spot": close,
        "strike": K,
        "iv_estimate": iv_est,
        "rv_20d": rv,
        "iv_percentile": iv_pct,
        "iv_regime": iv_regime,
        "call_price": round(cp, 2),
        "put_price": round(pp, 2),
        "greeks_call": greeks_c,
        "greeks_put": greeks_p,
        "explanation": " ".join(parts),
    }
