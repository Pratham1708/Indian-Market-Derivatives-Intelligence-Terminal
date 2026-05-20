"""
Option Greeks Calculator
=========================

The "Greeks" measure the sensitivity of an option's price to changes in
the underlying parameters.  They are essential for risk management and
hedging.

Greek   | Measures sensitivity to …        | Formula (Call)
--------|----------------------------------|------------------------------------
Delta   | Underlying price (S)              | N(d₁)
Gamma   | Rate of change of Delta           | φ(d₁) / (S·σ·√T)
Vega    | Volatility (σ)                    | S·φ(d₁)·√T
Theta   | Time decay (T)                    | −[S·φ(d₁)·σ / (2√T)] − r·K·e^(−rT)·N(d₂)
Rho     | Risk-free rate (r)                | K·T·e^(−rT)·N(d₂)

Where φ(·) is the standard-normal probability density function (PDF).
"""

import numpy as np
from scipy.stats import norm


# ---------------------------------------------------------------------------
# Reusable d₁ / d₂ helper  (mirrors black_scholes._d1_d2)
# ---------------------------------------------------------------------------

def _d1_d2(S: float, K: float, T: float, r: float, sigma: float):
    """Calculate d₁ and d₂ for the Black-Scholes model."""
    if T <= 0 or sigma <= 0:
        return 0.0, 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


# ---------------------------------------------------------------------------
# Individual Greek functions
# ---------------------------------------------------------------------------

def delta(S: float, K: float, T: float, r: float, sigma: float,
          option_type: str = "call") -> float:
    """
    Delta (Δ)  –  Sensitivity of option price to a $1 change in the stock.

    Call Delta = N(d₁)          ∈ [0, 1]
    Put  Delta = N(d₁) − 1      ∈ [−1, 0]

    Interpretation:
        A delta of 0.6 means the option price moves ~$0.60
        for every $1 move in the underlying.
    """
    d1, _ = _d1_d2(S, K, T, r, sigma)
    if option_type.lower() == "call":
        return float(norm.cdf(d1))
    else:
        return float(norm.cdf(d1) - 1)


def gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Gamma (Γ)  –  Rate of change of Delta per $1 move in the stock.

    Γ = φ(d₁) / (S · σ · √T)

    Interpretation:
        High gamma means Delta is changing rapidly, making the
        option harder to hedge (often near-the-money, close to expiry).
    """
    d1, _ = _d1_d2(S, K, T, r, sigma)
    if T <= 0 or sigma <= 0:
        return 0.0
    return float(norm.pdf(d1) / (S * sigma * np.sqrt(T)))


def vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Vega (ν)  –  Sensitivity of option price to a 1 % change in volatility.

    ν = S · φ(d₁) · √T

    Note: Vega is the same for calls and puts.  The result is typically
    expressed per 1 percentage-point change (divide by 100).
    """
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return float(S * norm.pdf(d1) * np.sqrt(T) / 100)   # per 1 % vol change


def theta(S: float, K: float, T: float, r: float, sigma: float,
          option_type: str = "call") -> float:
    """
    Theta (Θ)  –  Time decay: how much the option loses per day.

    Call Θ = −[S·φ(d₁)·σ / (2√T)] − r·K·e^(−rT)·N(d₂)
    Put  Θ = −[S·φ(d₁)·σ / (2√T)] + r·K·e^(−rT)·N(−d₂)

    Result is annualized; divide by 365 for daily decay.
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    if T <= 0 or sigma <= 0:
        return 0.0

    common = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    if option_type.lower() == "call":
        th = common - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        th = common + r * K * np.exp(-r * T) * norm.cdf(-d2)
    return float(th / 365)   # daily theta


def rho(S: float, K: float, T: float, r: float, sigma: float,
        option_type: str = "call") -> float:
    """
    Rho (ρ)  –  Sensitivity to a 1 % change in the risk-free rate.

    Call ρ =  K·T·e^(−rT)·N(d₂)   / 100
    Put  ρ = −K·T·e^(−rT)·N(−d₂)  / 100
    """
    _, d2 = _d1_d2(S, K, T, r, sigma)
    if option_type.lower() == "call":
        return float(K * T * np.exp(-r * T) * norm.cdf(d2) / 100)
    else:
        return float(-K * T * np.exp(-r * T) * norm.cdf(-d2) / 100)


# ---------------------------------------------------------------------------
# Convenience: calculate all Greeks at once
# ---------------------------------------------------------------------------

def calculate_all_greeks(
    S: float, K: float, T: float, r: float, sigma: float,
    option_type: str = "call",
) -> dict:
    """
    Return a dictionary with all five Greeks for the given option.

    Returns
    -------
    dict with keys: 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho'
    """
    return {
        "Delta": delta(S, K, T, r, sigma, option_type),
        "Gamma": gamma(S, K, T, r, sigma),
        "Vega":  vega(S, K, T, r, sigma),
        "Theta": theta(S, K, T, r, sigma, option_type),
        "Rho":   rho(S, K, T, r, sigma, option_type),
    }
