# src/analytics/signal_reliability.py
"""Signal Reliability Engine for Phase 3.
Evaluates historical win rate, expectancy, and consistency of signal types
by scanning past occurrences in the indicator DataFrame.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def _identify_setup_occurrences(df: pd.DataFrame, setup_type: str) -> pd.Series:
    """Return a boolean Series marking rows where the setup_type fired."""
    mask = pd.Series(False, index=df.index)

    if len(df) < 20:
        return mask

    if setup_type == "Breakout":
        mask = df["Close"] > df["BB_Upper"]

    elif setup_type == "Pullback":
        mask = (df["SMA20"] > df["SMA50"]) & (df["Close"] <= df["SMA20"] * 1.01)

    elif setup_type == "Reversal":
        mask = (df["RSI"].shift(1) < 30) & (df["RSI"] >= 30)

    elif setup_type == "Trend Continuation":
        mask = (df["SMA20"] > df["SMA50"]) & (df["MACD"] > df["MACD_Signal"])

    # For Consolidation / Neutral / Unknown we cannot meaningfully backtest
    return mask.fillna(False)


def evaluate_signal_reliability(
    df: pd.DataFrame, signal_type: str
) -> Dict[str, object]:
    """Backtest a setup type on the historical indicator DataFrame.

    Parameters
    ----------
    df : DataFrame with OHLCV + indicators (SMA20, SMA50, RSI, MACD, …)
    signal_type : one of 'Breakout', 'Pullback', 'Reversal', 'Trend Continuation'

    Returns
    -------
    dict with win_rate, total_signals, avg_return_5d, expectancy, reliability_label, explanation
    """
    default = {
        "win_rate": None,
        "total_signals": 0,
        "avg_return_5d": 0.0,
        "expectancy": 0.0,
        "reliability_label": "Insufficient Data",
        "explanation": "Not enough data to evaluate reliability.",
    }

    if df.empty or len(df) < 30:
        return default

    occurrences = _identify_setup_occurrences(df, signal_type)
    indices = df.index[occurrences]

    if len(indices) == 0:
        default["explanation"] = f"No historical {signal_type} setups found in the data."
        return default

    # Calculate 5-day forward returns for each occurrence
    fwd_returns = []
    for idx in indices:
        pos = df.index.get_loc(idx)
        if pos + 5 < len(df):
            entry_price = df.iloc[pos]["Close"]
            exit_price = df.iloc[pos + 5]["Close"]
            ret = (exit_price - entry_price) / entry_price
            fwd_returns.append(ret)

    if len(fwd_returns) < 3:
        default["total_signals"] = len(fwd_returns)
        default["explanation"] = f"Only {len(fwd_returns)} {signal_type} occurrence(s) found — insufficient for reliability."
        return default

    returns = np.array(fwd_returns)
    winners = returns[returns > 0]
    losers = returns[returns <= 0]

    win_rate = len(winners) / len(returns)
    avg_return = float(np.mean(returns))
    avg_win = float(np.mean(winners)) if len(winners) > 0 else 0.0
    avg_loss = float(np.mean(losers)) if len(losers) > 0 else 0.0
    expectancy = avg_win * win_rate + avg_loss * (1 - win_rate)

    label = get_reliability_label(win_rate)

    wr_pct = round(win_rate * 100, 1)
    ret_pct = round(avg_return * 100, 2)
    explanation = (
        f"{signal_type} setups historically succeed {wr_pct}% "
        f"with {ret_pct}% avg 5-day return over {len(returns)} occurrences."
    )

    return {
        "win_rate": round(win_rate, 3),
        "total_signals": len(returns),
        "avg_return_5d": round(avg_return, 4),
        "expectancy": round(expectancy, 4),
        "reliability_label": label,
        "explanation": explanation,
    }


def get_reliability_label(win_rate: Optional[float]) -> str:
    """Human-readable reliability label."""
    if win_rate is None or (isinstance(win_rate, float) and np.isnan(win_rate)):
        return "Insufficient Data"
    if win_rate >= 0.65:
        return "High Reliability ✅"
    if win_rate >= 0.50:
        return "Moderate Reliability ⚠"
    return "Low Reliability ❌"
