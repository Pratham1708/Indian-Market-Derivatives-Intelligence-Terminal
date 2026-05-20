# src/analytics/portfolio_intelligence.py
"""Portfolio Intelligence & Risk Engine for Phase 4.
Tracks positions, computes portfolio-level risk metrics,
generates concentration warnings, and estimates VaR.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def compute_portfolio_metrics(
    positions: List[Dict],
    sector_map: Optional[Dict[str, str]] = None,
) -> Dict[str, object]:
    """Compute portfolio-level intelligence from a list of positions.

    Parameters
    ----------
    positions : list of dicts, each with keys:
        - ticker: str
        - quantity: int
        - avg_price: float
        - current_price: float
        - sector: str (optional, can be derived from sector_map)
    sector_map : optional dict mapping ticker -> sector name

    Returns
    -------
    dict with total_value, total_pnl, sector_exposure, concentration_warnings,
    portfolio_volatility_estimate, var_95, and explanation.
    """
    if not positions:
        return {
            "total_value": 0, "total_pnl": 0, "pnl_pct": 0,
            "sector_exposure": {}, "concentration_warnings": [],
            "portfolio_volatility": 0, "var_95": 0,
            "explanation": "No positions to analyze.",
        }

    total_value = 0
    total_cost = 0
    sector_values = {}
    position_details = []

    for pos in positions:
        ticker = pos.get("ticker", "UNKNOWN")
        qty = pos.get("quantity", 0)
        avg_px = pos.get("avg_price", 0)
        cur_px = pos.get("current_price", avg_px)
        sector = pos.get("sector", "")
        if not sector and sector_map:
            sector = sector_map.get(ticker, "Unknown")

        value = qty * cur_px
        cost = qty * avg_px
        pnl = value - cost

        total_value += value
        total_cost += cost

        sector_values[sector] = sector_values.get(sector, 0) + value
        position_details.append({
            "ticker": ticker, "value": value, "pnl": pnl, "sector": sector
        })

    total_pnl = total_value - total_cost
    pnl_pct = (total_pnl / total_cost * 100) if total_cost else 0

    # Sector exposure as percentages
    sector_exposure = {}
    for sec, val in sector_values.items():
        sector_exposure[sec] = round(val / total_value * 100, 1) if total_value else 0

    # Concentration warnings
    warnings = []
    for sec, pct in sector_exposure.items():
        if pct > 40:
            warnings.append(f"⚠ Portfolio heavily concentrated in {sec} ({pct}%).")
    
    # Single stock concentration
    for pd_item in position_details:
        stock_pct = (pd_item["value"] / total_value * 100) if total_value else 0
        if stock_pct > 25:
            warnings.append(f"⚠ {pd_item['ticker']} is {stock_pct:.1f}% of portfolio — high single-stock risk.")

    # Approximate portfolio volatility (simplified: assume 20% avg stock vol, diversification benefit)
    n_positions = len(positions)
    avg_vol = 0.20  # 20% annualized assumption
    diversification = 1 / np.sqrt(max(n_positions, 1))
    portfolio_vol = avg_vol * diversification

    # VaR 95% (parametric, normal assumption)
    var_95 = total_value * portfolio_vol * 1.645 / np.sqrt(252)

    explanation = (
        f"Portfolio: ₹{total_value:,.0f} across {n_positions} positions. "
        f"P&L: ₹{total_pnl:,.0f} ({pnl_pct:+.1f}%). "
        f"Estimated daily VaR (95%): ₹{var_95:,.0f}."
    )

    return {
        "total_value": round(total_value, 2),
        "total_pnl": round(total_pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "n_positions": n_positions,
        "sector_exposure": sector_exposure,
        "concentration_warnings": warnings,
        "portfolio_volatility": round(portfolio_vol, 4),
        "var_95": round(var_95, 2),
        "position_details": position_details,
        "explanation": explanation,
    }


def generate_portfolio_alerts(metrics: Dict) -> List[str]:
    """Generate portfolio-level intelligence alerts."""
    alerts = list(metrics.get("concentration_warnings", []))

    vol = metrics.get("portfolio_volatility", 0)
    if vol > 0.15:
        alerts.append("⚠ High portfolio volatility estimated.")

    pnl_pct = metrics.get("pnl_pct", 0)
    if pnl_pct < -5:
        alerts.append(f"⚠ Portfolio drawdown: {pnl_pct:.1f}%.")

    return alerts
