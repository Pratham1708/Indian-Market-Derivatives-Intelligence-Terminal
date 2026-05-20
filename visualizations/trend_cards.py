# visualizations/trend_cards.py
"""Helper to render a signal card in Streamlit.
The function ``render_signal_card`` expects a dictionary produced by
``signals.rule_based.generate_signals`` and creates a styled card with a
colored badge, confidence bar, and explanation.
"""

import streamlit as st


def _confidence_bar(confidence: float, color: str) -> str:
    """Return an HTML snippet for a horizontal confidence bar.
    ``confidence`` should be between 0 and 1.
    """
    width_percent = int(confidence * 100)
    bar_html = f"""
    <div style='background:#2C2F36;height:12px;border-radius:6px;position:relative;'>
        <div style='background:{color};width:{width_percent}%;height:100%;border-radius:6px;'></div>
    </div>
    """
    return bar_html


def render_signal_card(signal_info: dict) -> None:
    """Render a premium‑looking signal card.

    Parameters
    ----------
    signal_info: dict
        Must contain ``signal``, ``color``, ``confidence`` (0‑1), and ``explanation``.
    """
    signal = signal_info.get("signal", "Neutral")
    color_name = signal_info.get("color", "yellow")
    confidence = signal_info.get("confidence", 0.0)
    explanation = signal_info.get("explanation", "")

    # Map logical colour name to hex for the badge & bar
    colour_map = {
        "green": "#00E396",
        "red": "#FF4560",
        "yellow": "#FEB019",
    }
    badge_color = colour_map.get(color_name, "#FEB019")

    # Card container
    st.markdown(
        f"""
        <div style='background:#1A1D23;border:2px solid {badge_color};border-radius:12px;padding:16px;margin:12px 0;'>
            <h3 style='margin:0;color:{badge_color};'>{signal}</h3>
            <p style='margin:8px 0;color:#F0F2F6;'>{explanation}</p>
            <div>Confidence: {int(confidence*100)}%</div>
            {_confidence_bar(confidence, badge_color)}
        </div>
        """,
        unsafe_allow_html=True,
    )
