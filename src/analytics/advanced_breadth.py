# src/analytics/advanced_breadth.py
"""Advanced Market Breadth Intelligence for Phase 3.
Computes breadth momentum, participation, leadership shifts, divergence,
and generates institutional-style market narrative feeds.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def compute_advanced_breadth(scan_results_df: pd.DataFrame) -> Dict[str, object]:
    """Compute advanced breadth metrics from scanner results.

    Parameters
    ----------
    scan_results_df : DataFrame with columns Stock, Sector, Signal, Confidence,
                      Setup Type, Trade Quality, Relative Strength, Opportunity Score

    Returns
    -------
    dict with breadth metrics, narrative, and alerts.
    """
    default = {
        "bullish_pct": 0.0,
        "bearish_pct": 0.0,
        "participation_rate": 0.0,
        "leadership_sectors": [],
        "lagging_sectors": [],
        "breadth_divergence": False,
        "sector_rotation": {},
        "market_narrative": "Insufficient data for breadth analysis.",
        "alerts": [],
    }

    if scan_results_df.empty or len(scan_results_df) < 3:
        return default

    total = len(scan_results_df)

    # Bullish / Bearish percentages
    bullish = len(scan_results_df[scan_results_df["Signal"].str.contains("Bullish", na=False)])
    bearish = len(scan_results_df[scan_results_df["Signal"].str.contains("Bearish", na=False)])
    bullish_pct = round(bullish / total * 100, 1)
    bearish_pct = round(bearish / total * 100, 1)

    # Participation rate: % of stocks with Trade Quality > 5.0
    participation = len(scan_results_df[scan_results_df["Trade Quality"] > 5.0])
    participation_rate = round(participation / total * 100, 1)

    # Sector analysis
    sector_stats = scan_results_df.groupby("Sector").agg(
        avg_tq=("Trade Quality", "mean"),
        avg_rs=("Relative Strength", "mean"),
        count=("Stock", "count"),
    ).sort_values("avg_tq", ascending=False)

    leadership_sectors = sector_stats.head(2).index.tolist() if len(sector_stats) >= 2 else sector_stats.index.tolist()
    lagging_sectors = sector_stats.tail(2).index.tolist() if len(sector_stats) >= 2 else []

    sector_rotation = sector_stats["avg_rs"].round(2).to_dict()

    # Breadth divergence: majority bearish but avg score high, or vice versa
    avg_score = scan_results_df["Opportunity Score"].mean() if "Opportunity Score" in scan_results_df.columns else 5.0
    breadth_divergence = (bearish_pct > 60 and avg_score > 5.0) or (bullish_pct > 60 and avg_score < 4.0)

    # Build alerts
    alerts = []
    if breadth_divergence:
        if bearish_pct > 60 and avg_score > 5.0:
            alerts.append("⚠ Index metrics strong while majority of stocks bearish — breadth divergence.")
        elif bullish_pct > 60 and avg_score < 4.0:
            alerts.append("⚠ Majority bullish signals but low opportunity scores — quality divergence.")

    if participation_rate < 30:
        alerts.append("⚠ Participation narrowing — fewer than 30% of stocks show quality setups.")
    elif participation_rate > 70:
        alerts.append("📈 Broad market participation — over 70% of stocks show quality setups.")

    if len(leadership_sectors) >= 1 and len(lagging_sectors) >= 1:
        if leadership_sectors[0] != lagging_sectors[-1]:
            alerts.append(f"⚡ Sector leadership: {leadership_sectors[0]} leading, {lagging_sectors[-1]} lagging.")

    # Market narrative
    narrative_parts = []
    narrative_parts.append(f"Market breadth: {bullish_pct}% bullish, {bearish_pct}% bearish.")
    narrative_parts.append(f"Quality participation at {participation_rate}%.")
    if leadership_sectors:
        narrative_parts.append(f"Strongest sector: {leadership_sectors[0]}.")
    if breadth_divergence:
        narrative_parts.append("Breadth divergence detected — exercise caution.")

    return {
        "bullish_pct": bullish_pct,
        "bearish_pct": bearish_pct,
        "participation_rate": participation_rate,
        "leadership_sectors": leadership_sectors,
        "lagging_sectors": lagging_sectors,
        "breadth_divergence": breadth_divergence,
        "sector_rotation": sector_rotation,
        "market_narrative": " ".join(narrative_parts),
        "alerts": alerts,
    }


def generate_breadth_feed(breadth_info: Dict) -> List[str]:
    """Generate a list of 2-4 short intelligence feed strings from breadth data."""
    feed = []

    leaders = breadth_info.get("leadership_sectors", [])
    laggers = breadth_info.get("lagging_sectors", [])
    participation = breadth_info.get("participation_rate", 0)
    bullish_pct = breadth_info.get("bullish_pct", 0)
    divergence = breadth_info.get("breadth_divergence", False)

    if leaders:
        feed.append(f"📈 Sector leadership concentrated in {leaders[0]}.")

    if laggers and leaders and laggers[-1] != leaders[0]:
        feed.append(f"⚡ Momentum leadership shifting — {laggers[-1]} underperforming.")

    if participation > 60:
        feed.append(f"📈 Broad participation active ({participation}% quality setups).")
    elif participation < 30:
        feed.append(f"⚠ Narrow market participation ({participation}% quality setups).")

    if divergence:
        feed.append("⚠ Breadth divergence detected — surface strength may be misleading.")

    if bullish_pct > 70:
        feed.append(f"📈 Strong bullish breadth ({bullish_pct}% of stocks bullish).")
    elif bullish_pct < 30:
        feed.append(f"⚠ Weak market breadth ({bullish_pct}% bullish).")

    # Cap at 4 items
    return feed[:4]
