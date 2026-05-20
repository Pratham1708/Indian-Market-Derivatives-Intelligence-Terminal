# src/visualizations/executive_summary.py
"""Executive summary panel.
Generates a concise markdown block that summarises the most important
information for a given ticker: trend, momentum, volume, risk, regime,
relative strength, trade quality and market state.
"""

from typing import Dict


def render_executive_summary(
    ticker: str,
    signal: str,
    confidence: float,
    trend_strength: str,
    momentum: str,
    volume_confirmation: str,
    risk_level: str,
    trade_quality: float,
    market_regime: str,
    relative_strength: float,
    market_state: str,
) -> str:
    """Return a markdown string for the executive summary.
    Parameters are already formatted strings (e.g. "Strong", "Improving").
    """
    summary = f"""
---
## {ticker} — Executive Summary

🟢 **Market Bias:** {signal} (Confidence {confidence:.0%})
📈 **Trend Strength:** {trend_strength}
⚡ **Momentum:** {momentum}
📊 **Volume Confirmation:** {volume_confirmation}
🧠 **Trade Quality:** {trade_quality:.1f}/10
⚠ **Risk Level:** {risk_level}

**Regime:** {market_regime}
**Market State:** {market_state}
**Relative Strength vs NIFTY:** {relative_strength:.2f}

**Suggested Workflow**
* {"Watch breakout" if signal.lower().startswith("bull") else "Monitor pullback"} near current price.
* {"Strong sector relative strength" if relative_strength > 1 else "Sector neutral"}.
* {"Elevated" if risk_level.lower() == "high" else "Moderate"} volatility – adjust position size accordingly.
---
"""
    return summary.strip()

# Example usage (called from UI)
# md = render_executive_summary(
#     ticker="RELIANCE.NS",
#     signal="Bullish",
#     confidence=0.88,
#     trend_strength="Strong",
#     momentum="Improving",
#     volume_confirmation="High",
#     risk_level="Moderate",
#     trade_quality=8.3,
#     market_regime="Trending Bullish",
#     relative_strength=1.12,
#     market_state="Accumulation",
# )
# st.markdown(md)
