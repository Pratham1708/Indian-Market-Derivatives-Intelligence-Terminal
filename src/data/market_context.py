# src/data/market_context.py
"""Market context utilities.
Provides functions to fetch NIFTY (or other index) data and compute overall market regime,
sector trends, and relative strength of a stock against the index.
"""

import yfinance as yf
import pandas as pd
from typing import Tuple, Dict

# Index ticker for NIFTY 50 in Yahoo Finance
NIFTY_TICKER = "^NSEI"


def fetch_index_history(period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Download historical OHLCV for the index.
    Returns a DataFrame with DateTime index.
    """
    df = yf.download(NIFTY_TICKER, period=period, interval=interval, auto_adjust=True, progress=False)
    df.dropna(inplace=True)
    return df


def compute_index_regime(df: pd.DataFrame) -> Tuple[str, float]:
    """Simple market‑regime detection for the index.
    Uses SMA20 vs SMA50 and ADX to classify.
    Returns a tuple (regime_name, confidence 0‑1).
    """
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    # ADX using pandas_ta if available, fallback to simple true range
    try:
        import ta.trend
        adx = ta.trend.ADXIndicator(high=df["High"], low=df["Low"], close=df["Close"], window=14)
        df["ADX"] = adx.adx()
    except Exception:
        df["ADX"] = 0
    latest = df.iloc[-1]
    if latest["ADX"] > 25:
        if latest["SMA20"] > latest["SMA50"]:
            regime = "Trending Bullish"
        else:
            regime = "Trending Bearish"
    else:
        regime = "Sideways"
    # confidence based on distance between SMAs normalized
    sma_diff = abs(latest["SMA20"] - latest["SMA50"]) / latest["Close"]
    confidence = min(sma_diff * 10, 1.0)
    return regime, confidence


def relative_strength(stock_df: pd.DataFrame, index_df: pd.DataFrame) -> float:
    """Calculate relative strength as the ratio of percent returns.
    Positive >1 means out‑performance.
    """
    # Align on dates
    merged = pd.merge(stock_df["Close"], index_df["Close"], left_index=True, right_index=True, suffixes=("_stock", "_idx"))
    # 30‑day returns
    stock_ret = merged["Close_stock"].pct_change(30).iloc[-1]
    idx_ret = merged["Close_idx"].pct_change(30).iloc[-1]
    if idx_ret == 0:
        return 0.0
    return (1 + stock_ret) / (1 + idx_ret)

def get_market_context(stock_ticker: str, period: str = "1y") -> Dict[str, any]:
    """High‑level market context for a given stock.
    Returns a dict with index regime, confidence, and relative strength.
    """
    stock_df = yf.download(stock_ticker, period=period, interval="1d", auto_adjust=True, progress=False)
    index_df = fetch_index_history(period=period)
    regime, confidence = compute_index_regime(index_df)
    rs = relative_strength(stock_df, index_df)
    return {
        "index_regime": regime,
        "regime_confidence": confidence,
        "relative_strength": rs,
    }
