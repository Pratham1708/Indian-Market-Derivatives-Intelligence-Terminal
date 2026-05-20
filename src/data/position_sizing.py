# src/data/position_sizing.py
"""Position sizing utilities.
Provides a simple volatility‑adjusted position size calculator used by the
core trader‑decision workflow.
"""

from typing import Optional
import numpy as np


def calculate_position_size(
    capital: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
    atr: Optional[float] = None,
    use_atr: bool = True,
) -> int:
    """Return the number of shares/contracts to trade.

    Parameters
    ----------
    capital: Total account equity (₹).
    risk_percent: Fraction of capital to risk per trade (e.g. 0.01 for 1%).
    entry_price: Desired entry price.
    stop_price: Stop‑loss price.
    atr: Average True Range (optional). If provided and ``use_atr`` is True
         the stop distance is taken as ``max(|entry‑stop|, atr)`` to give a
         volatility‑adjusted stop.
    use_atr: Whether to consider ATR when computing stop distance.

    Returns
    -------
    int: Rounded quantity (shares) that respects the risk budget.
    """
    # absolute stop distance
    stop_distance = abs(entry_price - stop_price)
    if use_atr and atr is not None:
        stop_distance = max(stop_distance, atr)
    # risk amount per trade
    risk_amount = capital * risk_percent
    # quantity = risk_amount / stop_distance
    qty = risk_amount / stop_distance
    # round down to whole shares
    return int(np.floor(qty))

# Example usage (will be called from UI)
# qty = calculate_position_size(capital=100_000, risk_percent=0.01,
#                               entry_price=2450, stop_price=2410, atr=12)
