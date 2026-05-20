# src/analytics/backtesting.py
"""Advanced Backtesting Engine for Phase 4.
Supports setup-based backtesting with regime-aware filtering
and institutional-grade performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List


def _identify_entries(df: pd.DataFrame, setup_type: str) -> List[int]:
    """Return list of integer positions where the setup fires."""
    positions = []
    if len(df) < 20:
        return positions

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        fired = False

        if setup_type == "Breakout":
            fired = row["Close"] > row["BB_Upper"]
        elif setup_type == "Pullback":
            fired = row["SMA20"] > row["SMA50"] and row["Close"] <= row["SMA20"] * 1.01
        elif setup_type == "Reversal":
            fired = prev["RSI"] < 30 and row["RSI"] >= 30
        elif setup_type == "Trend Continuation":
            fired = row["SMA20"] > row["SMA50"] and row["MACD"] > row["MACD_Signal"]

        if fired:
            positions.append(i)

    return positions


def backtest_setup(
    df: pd.DataFrame,
    setup_type: str,
    holding_period: int = 5,
    stop_loss_pct: float = 0.03,
    target_pct: float = 0.05,
) -> Dict[str, object]:
    """Run a backtest on a specific setup type.

    Parameters
    ----------
    df : DataFrame with OHLCV + indicators
    setup_type : 'Breakout', 'Pullback', 'Reversal', 'Trend Continuation'
    holding_period : number of bars to hold
    stop_loss_pct : stop loss as fraction (0.03 = 3%)
    target_pct : target as fraction (0.05 = 5%)

    Returns
    -------
    dict with CAGR, Sharpe, Sortino, max_drawdown, win_rate, expectancy,
    profit_factor, total_trades, and trade_log.
    """
    default = {
        "total_trades": 0, "win_rate": 0.0, "avg_return": 0.0,
        "cagr": 0.0, "sharpe": 0.0, "sortino": 0.0,
        "max_drawdown": 0.0, "expectancy": 0.0, "profit_factor": 0.0,
        "explanation": "Insufficient data or no trades found.",
        "trade_log": [],
    }

    if df.empty or len(df) < 30:
        return default

    entries = _identify_entries(df, setup_type)

    if not entries:
        default["explanation"] = f"No {setup_type} entries found in the data."
        return default

    trade_log = []
    returns = []

    for pos in entries:
        if pos + holding_period >= len(df):
            continue

        entry_price = df.iloc[pos]["Close"]
        exit_price = entry_price  # default

        # Simulate holding with SL/target
        for j in range(1, holding_period + 1):
            bar = df.iloc[pos + j]
            low = bar["Low"]
            high = bar["High"]
            close = bar["Close"]

            # Check stop loss (intrabar)
            if (low - entry_price) / entry_price <= -stop_loss_pct:
                exit_price = entry_price * (1 - stop_loss_pct)
                break
            # Check target
            if (high - entry_price) / entry_price >= target_pct:
                exit_price = entry_price * (1 + target_pct)
                break
            exit_price = close

        ret = (exit_price - entry_price) / entry_price
        returns.append(ret)
        trade_log.append({
            "entry_idx": pos,
            "entry_price": round(entry_price, 2),
            "exit_price": round(exit_price, 2),
            "return_pct": round(ret * 100, 2),
        })

    if not returns:
        default["explanation"] = "Trades found but none could complete within data range."
        return default

    returns_arr = np.array(returns)
    winners = returns_arr[returns_arr > 0]
    losers = returns_arr[returns_arr <= 0]

    total = len(returns_arr)
    win_rate = len(winners) / total
    avg_return = float(np.mean(returns_arr))
    avg_win = float(np.mean(winners)) if len(winners) > 0 else 0
    avg_loss = float(np.mean(losers)) if len(losers) > 0 else 0
    expectancy = avg_win * win_rate + avg_loss * (1 - win_rate)

    # Profit factor
    gross_profit = float(np.sum(winners)) if len(winners) > 0 else 0
    gross_loss = abs(float(np.sum(losers))) if len(losers) > 0 else 1e-9
    profit_factor = gross_profit / gross_loss

    # Equity curve for drawdown and Sharpe
    equity = np.cumprod(1 + returns_arr)
    peak = np.maximum.accumulate(equity)
    drawdowns = (equity - peak) / peak
    max_dd = float(np.min(drawdowns))

    # CAGR (approximate)
    n_years = total * 5 / 252  # assume 5-day holds
    if n_years > 0 and equity[-1] > 0:
        cagr = float((equity[-1]) ** (1 / n_years) - 1)
    else:
        cagr = 0.0

    # Sharpe / Sortino
    std = float(np.std(returns_arr))
    sharpe = float(np.mean(returns_arr) / std * np.sqrt(252 / 5)) if std > 0 else 0
    downside = returns_arr[returns_arr < 0]
    downside_std = float(np.std(downside)) if len(downside) > 0 else 1e-9
    sortino = float(np.mean(returns_arr) / downside_std * np.sqrt(252 / 5))

    explanation = (
        f"{setup_type} backtest: {total} trades, "
        f"{win_rate*100:.1f}% win rate, "
        f"{avg_return*100:.2f}% avg return, "
        f"Sharpe {sharpe:.2f}, Max DD {max_dd*100:.1f}%."
    )

    return {
        "total_trades": total,
        "win_rate": round(win_rate, 3),
        "avg_return": round(avg_return, 4),
        "cagr": round(cagr, 4),
        "sharpe": round(sharpe, 2),
        "sortino": round(sortino, 2),
        "max_drawdown": round(max_dd, 4),
        "expectancy": round(expectancy, 4),
        "profit_factor": round(profit_factor, 2),
        "explanation": explanation,
        "trade_log": trade_log[-20:],  # last 20 trades
    }
