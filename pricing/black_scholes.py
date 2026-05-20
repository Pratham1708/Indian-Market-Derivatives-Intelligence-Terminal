"""
Black-Scholes Option Pricing Model
====================================

The Black-Scholes model is the foundation of modern option pricing theory.
It provides a closed-form solution for pricing European-style options.

Key Assumptions:
    1. The stock price follows a geometric Brownian motion (log-normal distribution).
    2. No dividends are paid during the option's life.
    3. Markets are frictionless (no transaction costs, no taxes).
    4. The risk-free interest rate is constant and known.
    5. Volatility is constant and known.

The Black-Scholes Formula
--------------------------
Call Price:  C = S·N(d₁)  −  K·e^(−rT)·N(d₂)
Put  Price:  P = K·e^(−rT)·N(−d₂) − S·N(−d₁)

Where:
    d₁ = [ln(S/K) + (r + σ²/2)·T]  /  (σ·√T)
    d₂ = d₁ − σ·√T

    S  = Current stock price
    K  = Strike price
    T  = Time to maturity (in years)
    r  = Risk-free interest rate (annualized)
    σ  = Volatility of the underlying asset (annualized)
    N(·) = Cumulative distribution function of the standard normal distribution
"""

import numpy as np
from scipy.stats import norm


# ---------------------------------------------------------------------------
# Helper: compute d₁ and d₂
# ---------------------------------------------------------------------------

def _d1_d2(S: float, K: float, T: float, r: float, sigma: float):
    """
    Calculate d₁ and d₂ parameters used in the Black-Scholes formula.

    Parameters
    ----------
    S     : Current stock price
    K     : Strike price
    T     : Time to maturity in years
    r     : Risk-free interest rate (e.g. 0.05 for 5 %)
    sigma : Annualized volatility  (e.g. 0.20 for 20 %)

    Returns
    -------
    (d1, d2) : tuple of floats
    """
    # Guard against division-by-zero when T or sigma are zero
    if T <= 0 or sigma <= 0:
        return 0.0, 0.0

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


# ---------------------------------------------------------------------------
# European Call price
# ---------------------------------------------------------------------------

def call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Price a European Call option using Black-Scholes.

    C = S·N(d₁) − K·e^(−rT)·N(d₂)

    Returns
    -------
    float : Theoretical call price
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return float(price)


# ---------------------------------------------------------------------------
# European Put price
# ---------------------------------------------------------------------------

def put_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Price a European Put option using Black-Scholes.

    P = K·e^(−rT)·N(−d₂) − S·N(−d₁)

    Returns
    -------
    float : Theoretical put price
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return float(price)


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

def price_option(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call",
) -> float:
    """
    Price a European option (call or put).

    Parameters
    ----------
    option_type : 'call' or 'put'

    Returns
    -------
    float : Theoretical option price
    """
    option_type = option_type.strip().lower()
    if option_type == "call":
        return call_price(S, K, T, r, sigma)
    elif option_type == "put":
        return put_price(S, K, T, r, sigma)
    else:
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")
