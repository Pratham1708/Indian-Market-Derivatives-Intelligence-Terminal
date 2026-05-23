# src/visualizations/executive_summary_v2.py
"""Redesigned Executive Summary for Phase 5.
Renders a glassmorphism-styled decision-support intelligence layout
with signal badge, confidence bars, narrative insight, and secondary metrics.
Replaces the old 3×4 st.metric() grid.
"""

import streamlit as st
from typing import Dict, Optional


# ── CSS Design System ────────────────────────────────────────────────────

EXEC_SUMMARY_CSS = """
<style>
/* Signal badge — large left card */
.signal-badge {
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(10px);
}
.signal-badge .signal-label {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
.signal-badge .signal-price {
    font-size: 1.3rem;
    font-weight: 600;
    opacity: 0.9;
}
.signal-badge .signal-method {
    font-size: 0.75rem;
    opacity: 0.6;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Key metrics panel — right side */
.metrics-panel {
    background: rgba(26,29,35,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    min-height: 180px;
    backdrop-filter: blur(10px);
}
.metrics-panel .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.metrics-panel .metric-row:last-child {
    border-bottom: none;
}
.metrics-panel .metric-label {
    color: #9ca3af;
    font-size: 0.9rem;
}
.metrics-panel .metric-value {
    font-weight: 600;
    font-size: 0.95rem;
}

/* Confidence bar */
.conf-bar-container {
    background: #2C2F36;
    height: 10px;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 4px;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 5px;
    transition: width 0.8s ease-in-out;
}

/* Insight card — narrative block */
.insight-card {
    background: rgba(26,29,35,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 12px;
    backdrop-filter: blur(10px);
}
.insight-card .insight-title {
    font-size: 0.85rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}
.insight-card .insight-text {
    font-size: 1rem;
    line-height: 1.6;
    color: #e5e7eb;
}
.insight-card .use-case {
    margin-top: 12px;
    font-size: 0.9rem;
    color: #00D4FF;
}
.insight-card .warning {
    margin-top: 8px;
    font-size: 0.9rem;
    color: #FEB019;
}

/* Secondary metrics row */
.metric-pill {
    background: #1A1D23;
    border: 1px solid #2d3139;
    border-radius: 10px;
    padding: 14px 12px;
    text-align: center;
}
.metric-pill .pill-label {
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.metric-pill .pill-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F0F2F6;
}
</style>
"""


# ── Color Mapping ────────────────────────────────────────────────────────

def _get_signal_colors(signal: str) -> dict:
    """Return color scheme for a given signal."""
    schemes = {
        "Strong Bullish": {
            "bg": "linear-gradient(135deg, rgba(0,227,150,0.18) 0%, rgba(0,212,255,0.08) 100%)",
            "border": "#00E396",
            "text": "#00E396",
            "bar": "linear-gradient(90deg, #00E396, #00D4FF)",
            "emoji": "🟢",
        },
        "Bullish Continuation": {
            "bg": "linear-gradient(135deg, rgba(0,212,255,0.18) 0%, rgba(0,227,150,0.08) 100%)",
            "border": "#00D4FF",
            "text": "#00D4FF",
            "bar": "linear-gradient(90deg, #00D4FF, #00E396)",
            "emoji": "🔵",
        },
        "Weak Bullish": {
            "bg": "linear-gradient(135deg, rgba(168,230,207,0.18) 0%, rgba(254,176,25,0.08) 100%)",
            "border": "#A8E6CF",
            "text": "#A8E6CF",
            "bar": "linear-gradient(90deg, #A8E6CF, #FEB019)",
            "emoji": "🟡",
        },
        "Neutral / Consolidation": {
            "bg": "linear-gradient(135deg, rgba(254,176,25,0.15) 0%, rgba(200,200,200,0.05) 100%)",
            "border": "#FEB019",
            "text": "#FEB019",
            "bar": "linear-gradient(90deg, #FEB019, #FFD700)",
            "emoji": "🟡",
        },
        "Weak Bearish": {
            "bg": "linear-gradient(135deg, rgba(255,179,186,0.18) 0%, rgba(254,176,25,0.08) 100%)",
            "border": "#FFB3BA",
            "text": "#FFB3BA",
            "bar": "linear-gradient(90deg, #FFB3BA, #FF6B6B)",
            "emoji": "🟠",
        },
        "Bearish Breakdown": {
            "bg": "linear-gradient(135deg, rgba(255,107,107,0.18) 0%, rgba(255,69,96,0.08) 100%)",
            "border": "#FF6B6B",
            "text": "#FF6B6B",
            "bar": "linear-gradient(90deg, #FF6B6B, #FF4560)",
            "emoji": "🔴",
        },
        "Strong Bearish": {
            "bg": "linear-gradient(135deg, rgba(255,69,96,0.18) 0%, rgba(255,50,50,0.08) 100%)",
            "border": "#FF4560",
            "text": "#FF4560",
            "bar": "linear-gradient(90deg, #FF4560, #FF2020)",
            "emoji": "🔴",
        },
        "High Volatility / Uncertain": {
            "bg": "linear-gradient(135deg, rgba(155,89,182,0.18) 0%, rgba(254,176,25,0.08) 100%)",
            "border": "#9B59B6",
            "text": "#9B59B6",
            "bar": "linear-gradient(90deg, #9B59B6, #FEB019)",
            "emoji": "⚠",
        },
    }
    return schemes.get(signal, schemes["Neutral / Consolidation"])


# ── Risk Level Color ─────────────────────────────────────────────────────

def _risk_color(level: str) -> str:
    """Return color hex for risk level."""
    return {"Low": "#00E396", "Moderate": "#FEB019", "High": "#FF4560"}.get(
        level, "#FEB019"
    )


# ── Main Renderer ────────────────────────────────────────────────────────

def render_executive_summary_v2(
    ticker: str,
    price: float,
    signal_info: dict,
    regime_result: dict,
    prob_result: dict,
    options_intel: dict,
    deriv_sentiment: dict,
    anomaly_result: dict,
    reliability: dict,
    move_result: dict,
    ai_recommendation: dict,
    trade_quality: dict = None,
) -> None:
    """Render the redesigned executive summary in Streamlit.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    price : float
        Current stock price.
    signal_info : dict
        Output from ``ml_signal_engine.ml_generate_signal()``.
    regime_result : dict
        Output from ``regime_detection.detect_regime()``.
    prob_result : dict
        Output from ``probability_engine.estimate_setup_probability()``.
    options_intel : dict
        Output from ``options_intelligence.compute_options_intelligence()``.
    deriv_sentiment : dict
        Output from ``derivatives_sentiment.compute_derivatives_sentiment()``.
    anomaly_result : dict
        Output from ``ml_models.detect_anomalies()``.
    reliability : dict
        Output from ``signal_reliability.evaluate_signal_reliability()``.
    move_result : dict
        Output from ``probability_engine.compute_expected_move()``.
    ai_recommendation : dict
        Output from ``llm_recommendation_engine.get_recommendation()``.
    trade_quality : dict, optional
        Output from ``trade_quality.compute_trade_quality_score()``.
    """
    # Inject CSS
    st.markdown(EXEC_SUMMARY_CSS, unsafe_allow_html=True)

    # Extract values
    signal = signal_info.get("signal", "Neutral / Consolidation")
    confidence = signal_info.get("confidence", 0.0)
    method = signal_info.get("method", "unknown")
    colors = _get_signal_colors(signal)

    regime = regime_result.get("current_regime", "Unknown")
    risk_level = ai_recommendation.get("risk_level", "Moderate")
    momentum = ai_recommendation.get("momentum_label", "Moderate")
    volatility = regime_result.get("current_regime", "Unknown")
    if "High Volatility" in volatility:
        vol_label = "High / Expanding"
    elif "Consolidation" in volatility:
        vol_label = "Low / Compressed"
    else:
        vol_label = "Stable"

    # ── Title + Accent Bar ───────────────────────────────────────────
    st.markdown(
        f"""
        <div style='margin-bottom:4px;'>
            <h3 style='margin:0;color:#F0F2F6;'>📋 AI Market Intelligence Summary — {ticker}</h3>
        </div>
        <div class='accent-bar'></div>
        """,
        unsafe_allow_html=True,
    )

    # ── Row 1: Signal Badge (left) + Key Metrics (right) ────────────
    col_badge, col_metrics = st.columns([1, 2])

    with col_badge:
        method_label = "ML Ensemble" if method == "ml_ensemble" else "Rule-Based"
        st.markdown(
            f"""
            <div class='signal-badge' style='
                background: {colors["bg"]};
                border: 2px solid {colors["border"]};
            '>
                <div class='signal-label' style='color:{colors["text"]};'>
                    {colors["emoji"]} {signal}
                </div>
                <div class='signal-price' style='color:{colors["text"]};'>
                    ₹{price:,.2f}
                </div>
                <div class='signal-method'>
                    {method_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_metrics:
        conf_pct = int(confidence * 100)
        risk_clr = _risk_color(risk_level)

        st.markdown(
            f"""
            <div class='metrics-panel'>
                <div class='metric-row'>
                    <span class='metric-label'>📊 Bias</span>
                    <span class='metric-value' style='color:{colors["text"]};'>{signal}</span>
                </div>
                <div class='metric-row'>
                    <span class='metric-label'>🎯 Confidence</span>
                    <span class='metric-value'>{conf_pct}%</span>
                </div>
                <div class='metric-row' style='border-bottom:none;padding-bottom:2px;'>
                    <span></span><span></span>
                </div>
                <div class='conf-bar-container'>
                    <div class='conf-bar-fill' style='
                        width:{conf_pct}%;
                        background:{colors["bar"]};
                    '></div>
                </div>
                <div class='metric-row' style='margin-top:8px;'>
                    <span class='metric-label'>⚡ Momentum</span>
                    <span class='metric-value'>{momentum}</span>
                </div>
                <div class='metric-row'>
                    <span class='metric-label'>🌡 Volatility</span>
                    <span class='metric-value'>{vol_label}</span>
                </div>
                <div class='metric-row'>
                    <span class='metric-label'>⚠ Risk Level</span>
                    <span class='metric-value' style='color:{risk_clr};'>{risk_level}</span>
                </div>
                <div class='metric-row'>
                    <span class='metric-label'>📈 Regime</span>
                    <span class='metric-value'>{regime}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Row 2: AI Insight / Narrative Card ───────────────────────────
    key_insight = ai_recommendation.get("key_insight", "")
    best_use_case = ai_recommendation.get("best_use_case", "")
    warning = ai_recommendation.get("warning", "")

    st.markdown(
        f"""
        <div class='insight-card'>
            <div class='insight-title'>💡 Key Insight</div>
            <div class='insight-text'>{key_insight}</div>
            <div class='use-case'>📌 Best Use Case: {best_use_case}</div>
            <div class='warning'>⚠ {warning}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Row 3: Secondary Metrics (5 pills) ──────────────────────────
    wr = reliability.get("win_rate")
    wr_str = f"{wr * 100:.1f}%" if wr is not None else "N/A"
    prob_str = f"{prob_result.get('probability', 0) * 100:.0f}%"
    iv_regime = options_intel.get("iv_regime", "N/A")
    deriv_str = deriv_sentiment.get("sentiment", "N/A")
    move_str = f"±{move_result.get('expected_move_pct', 0):.1f}%"

    p1, p2, p3, p4, p5 = st.columns(5)

    pills = [
        (p1, "Win Rate", wr_str),
        (p2, "Probability", prob_str),
        (p3, "IV Regime", iv_regime),
        (p4, "Derivatives", deriv_str),
        (p5, "Exp. Move", move_str),
    ]

    for col, label, value in pills:
        with col:
            st.markdown(
                f"""
                <div class='metric-pill'>
                    <div class='pill-label'>{label}</div>
                    <div class='pill-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Contributing Factors (collapsible) ───────────────────────────
    factors = signal_info.get("contributing_factors", [])
    if factors:
        with st.expander("🔍 Signal Contributing Factors", expanded=False):
            for f in factors:
                impact_emoji = "🟢" if f["impact"] == "positive" else "🔴"
                imp_pct = f"{f.get('importance', 0) * 100:.1f}%"
                st.markdown(
                    f"{impact_emoji} **{f['factor']}** ({imp_pct} importance) — {f.get('detail', '')}"
                )

    st.markdown("---")
