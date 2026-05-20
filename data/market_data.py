"""
Market Data Fetcher
====================

Uses the **yfinance** library to pull real-time (delayed) data from
Yahoo Finance, including:

    • Current stock price & info
    • Historical OHLCV data
    • Option chain (calls & puts) for every available expiry

All functions return clean Pandas DataFrames / Python dicts so the rest
of the project never has to worry about the Yahoo Finance API directly.

Rate-Limit Handling
-------------------
Yahoo Finance aggressively rate-limits requests from cloud IPs (e.g.
Streamlit Cloud).  This module mitigates that with:

    1. Reusing a single ``yf.Ticker`` object wherever possible.
    2. Preferring the lightweight ``fast_info`` endpoint over ``info``.
    3. Automatic retry with exponential back-off on HTTP 429 errors.
"""

import datetime
import time
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------

def _retry(func, *args, max_retries=3, base_delay=2.0, **kwargs):
    """
    Call *func* with retry + exponential backoff on rate-limit errors.

    Parameters
    ----------
    max_retries : int   – number of retry attempts (default 3)
    base_delay  : float – initial wait in seconds; doubles each retry

    Raises
    ------
    The original exception if all retries are exhausted.
    """
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            last_exc = exc
            msg = str(exc).lower()
            is_rate_limit = (
                "429" in msg
                or "too many requests" in msg
                or "rate limit" in msg
            )
            if is_rate_limit and attempt < max_retries:
                wait = base_delay * (2 ** attempt)
                time.sleep(wait)
            else:
                raise
    raise last_exc  # pragma: no cover


# ---------------------------------------------------------------------------
# Stock-level helpers
# ---------------------------------------------------------------------------

def get_stock_info(ticker: str) -> dict:
    """
    Fetch basic information about a stock (name, sector, price, etc.).

    Returns
    -------
    dict with keys like 'shortName', 'sector', 'currentPrice', …
    """
    stock = yf.Ticker(ticker)
    info = _retry(lambda: stock.info)
    return info


def get_current_price(ticker: str) -> float:
    """Return the latest available price for *ticker*.

    Uses ``fast_info`` first (lightweight), then falls back to
    ``info``, and finally to the last historical close.
    """
    stock = yf.Ticker(ticker)

    # ── Attempt 1: fast_info (no full page scrape) ────────────────────
    try:
        fi = stock.fast_info
        price = getattr(fi, "last_price", None)
        if price and price > 0:
            return float(price)
    except Exception:
        pass

    # ── Attempt 2: full info dict ─────────────────────────────────────
    try:
        info = _retry(lambda: stock.info)
        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )
        if price:
            return float(price)
    except Exception:
        pass

    # ── Attempt 3: last historical close ──────────────────────────────
    hist = _retry(lambda: stock.history(period="5d"))
    if not hist.empty:
        return float(hist["Close"].iloc[-1])

    raise ValueError(f"Could not retrieve price for {ticker}")


def get_historical_data(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download historical OHLCV data.

    Parameters
    ----------
    period   : '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'
    interval : '1d', '1wk', '1mo'

    Returns
    -------
    DataFrame with columns: Open, High, Low, Close, Volume
    """
    stock = yf.Ticker(ticker)
    hist = _retry(lambda: stock.history(period=period, interval=interval))
    return hist


# ---------------------------------------------------------------------------
# Option-chain helpers
# ---------------------------------------------------------------------------

def get_expiry_dates(ticker: str) -> list:
    """Return all available option expiry dates for *ticker*."""
    stock = yf.Ticker(ticker)
    return list(_retry(lambda: stock.options))   # tuple → list


def get_option_chain(ticker: str, expiry_date: str) -> dict:
    """
    Fetch the option chain for a specific expiry.

    Returns
    -------
    dict with keys 'calls' and 'puts', each a DataFrame.
    """
    stock = yf.Ticker(ticker)
    chain = _retry(lambda: stock.option_chain(expiry_date))
    return {"calls": chain.calls, "puts": chain.puts}


# ---------------------------------------------------------------------------
# Implied-volatility helper
# ---------------------------------------------------------------------------

def _bs_price(S, K, T, r, sigma, option_type="call"):
    """Tiny Black-Scholes pricer (avoids circular import)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def implied_volatility(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    option_type: str = "call",
) -> float:
    """
    Back-solve for the implied volatility that makes the Black-Scholes
    price equal the observed *market_price*.

    Uses Brent's root-finding method on the interval σ ∈ [0.001, 5.0].

    Returns
    -------
    float : implied volatility (annualized), or NaN if it cannot converge.
    """
    if T <= 0 or market_price <= 0:
        return np.nan

    def objective(sigma):
        return _bs_price(S, K, T, r, sigma, option_type) - market_price

    try:
        iv = brentq(objective, 0.001, 5.0, maxiter=200)
        return float(iv)
    except (ValueError, RuntimeError):
        return np.nan


def get_enriched_option_chain(
    ticker: str,
    expiry_date: str,
    risk_free_rate: float = 0.05,
) -> dict:
    """
    Fetch the option chain and enrich it with:
        • time to maturity (T)
        • implied volatility (computed via our own solver when the
          exchange-supplied value is missing)

    This function reuses a single ``yf.Ticker`` object to minimise
    the number of HTTP calls and reduce rate-limit risk.

    Returns
    -------
    dict  {'calls': DataFrame, 'puts': DataFrame}
    """
    # ── Single Ticker instance for all calls ──────────────────────────
    stock = yf.Ticker(ticker)

    chain_raw = _retry(lambda: stock.option_chain(expiry_date))
    chain = {"calls": chain_raw.calls, "puts": chain_raw.puts}

    # Get price from the same Ticker object to avoid extra HTTP call
    try:
        fi = stock.fast_info
        S = getattr(fi, "last_price", None)
        if not S or S <= 0:
            raise AttributeError
    except Exception:
        S = get_current_price(ticker)

    # Time to maturity in years
    expiry_dt = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
    today = datetime.datetime.now()
    T = max((expiry_dt - today).days / 365.0, 1 / 365)  # at least 1 day

    for opt_type, key in [("call", "calls"), ("put", "puts")]:
        df = chain[key].copy()
        df["T"] = T
        df["stockPrice"] = S

        # Compute our own IV where the exchange value is missing / zero
        ivs = []
        for _, row in df.iterrows():
            market = row.get("lastPrice", np.nan)
            strike = row.get("strike", np.nan)
            if pd.isna(market) or market <= 0 or pd.isna(strike):
                ivs.append(np.nan)
            else:
                ivs.append(
                    implied_volatility(market, S, strike, T, risk_free_rate, opt_type)
                )
        df["computedIV"] = ivs

        # Use exchange IV when available, fall back to our own
        if "impliedVolatility" in df.columns:
            df["iv"] = df["impliedVolatility"].where(
                df["impliedVolatility"] > 0, df["computedIV"]
            )
        else:
            df["iv"] = df["computedIV"]

        chain[key] = df

    return chain
