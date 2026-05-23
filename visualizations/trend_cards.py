# visualizations/trend_cards.py
"""Helper to render a signal card in Streamlit.
The function ``render_signal_card`` expects a dictionary produced by
``ml_signal_engine.ml_generate_signal`` or ``signals.rule_based.generate_signals``
and creates a styled card with a colored badge, confidence bar, and explanation.
Updated for Phase 5: supports 7-class signal taxonomy.
"""

import streamlit as st


def _confidence_bar(confidence: float, color: str) -> str:
    """Return an HTML snippet for a horizontal confidence bar.
    ``confidence`` should be between 0 and 1.
    """
    width_percent = int(confidence * 100)
    bar_html = f"""
    <div style='background:#2C2F36;height:12px;border-radius:6px;position:relative;'>
        <div style='background:{color};width:{width_percent}%;height:100%;border-radius:6px;
                     transition:width 0.6s ease-in-out;'></div>
    </div>
    """
    return bar_html


def render_signal_card(signal_info: dict) -> None:
    """Render a premium‑looking signal card.

    Parameters
    ----------
    signal_info: dict
        Must contain ``signal``, ``color`` (or ``color_hex``),
        ``confidence`` (0‑1), and ``explanation``.
        Optionally: ``model_agreement``, ``method``, ``probabilities``.
    """
    signal = signal_info.get("signal", "Neutral / Consolidation")
    confidence = signal_info.get("confidence", 0.0)
    explanation = signal_info.get("explanation", "")
    method = signal_info.get("method", "")

    # Get color — prefer color_hex, fallback to color name mapping
    badge_color = signal_info.get("color_hex")
    if not badge_color:
        color_name = signal_info.get("color", "yellow")
        colour_map = {
            "green": "#00E396",
            "cyan": "#00D4FF",
            "light_green": "#A8E6CF",
            "yellow": "#FEB019",
            "light_red": "#FFB3BA",
            "red": "#FF4560",
            "purple": "#9B59B6",
        }
        badge_color = colour_map.get(color_name, "#FEB019")

    # Method label
    method_label = ""
    if method == "ml_ensemble":
        method_label = "<span style='font-size:0.7rem;opacity:0.5;'>ML Ensemble</span>"
    elif method == "rule_based_fallback":
        method_label = "<span style='font-size:0.7rem;opacity:0.5;'>Rule-Based</span>"

    # Model agreement
    agreement_html = ""
    agreement = signal_info.get("model_agreement", 0)
    if agreement > 0:
        agree_pct = int(agreement * 100)
        agreement_html = f"""
        <div style='margin-top:8px;'>
            <span style='font-size:0.8rem;color:#9ca3af;'>Model Agreement: {agree_pct}%</span>
            <div style='background:#2C2F36;height:6px;border-radius:3px;margin-top:3px;'>
                <div style='background:{"#00E396" if agree_pct > 70 else "#FEB019"};
                            width:{agree_pct}%;height:100%;border-radius:3px;'></div>
            </div>
        </div>
        """

    # Probability breakdown
    probs_html = ""
    probs = signal_info.get("probabilities", {})
    if probs:
        bull_p = probs.get("bullish", 0) * 100
        neut_p = probs.get("neutral", 0) * 100
        bear_p = probs.get("bearish", 0) * 100
        probs_html = f"""
        <div style='margin-top:10px;display:flex;gap:12px;font-size:0.8rem;'>
            <span style='color:#00E396;'>▲ {bull_p:.0f}%</span>
            <span style='color:#FEB019;'>● {neut_p:.0f}%</span>
            <span style='color:#FF4560;'>▼ {bear_p:.0f}%</span>
        </div>
        """

    # Card container
    st.markdown(
        f"""
        <div style='background:#1A1D23;border:2px solid {badge_color};border-radius:12px;
                     padding:18px;margin:12px 0;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <h3 style='margin:0;color:{badge_color};'>{signal}</h3>
                {method_label}
            </div>
            <p style='margin:8px 0;color:#F0F2F6;font-size:0.9rem;'>{explanation}</p>
            <div>Confidence: {int(confidence * 100)}%</div>
            {_confidence_bar(confidence, badge_color)}
            {probs_html}
            {agreement_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

