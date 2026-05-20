"""
Visualization Module – Charts for the Dashboard
=================================================
All chart functions return Plotly Figure objects so Streamlit can render
them with st.plotly_chart().
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ── Color palette ──────────────────────────────────────────────────────────
COLORS = {
    "bg":       "#0E1117",
    "card":     "#1A1D23",
    "accent":   "#00D4FF",
    "green":    "#00E396",
    "red":      "#FF4560",
    "yellow":   "#FEB019",
    "purple":   "#9B59B6",
    "grid":     "#2C2F36",
    "text":     "#F0F2F6",        # ← brighter base text
}

# ── Font presets ───────────────────────────────────────────────────────────
_FONT_FAMILY = "Inter, sans-serif"
_TITLE_FONT  = dict(family=_FONT_FAMILY, size=18, color="#FFFFFF")
_AXIS_TITLE  = dict(family=_FONT_FAMILY, size=14, color="#D0D4E0")
_TICK_FONT   = dict(family=_FONT_FAMILY, size=12, color="#C0C4D0")
_LEGEND_FONT = dict(family=_FONT_FAMILY, size=13, color="#E0E2E8")

_LAYOUT_DEFAULTS = dict(
    template="plotly_dark",
    paper_bgcolor=COLORS["bg"],
    plot_bgcolor=COLORS["bg"],
    font=dict(family=_FONT_FAMILY, size=13, color=COLORS["text"]),
    margin=dict(l=50, r=30, t=60, b=50),
    legend=dict(font=_LEGEND_FONT, bgcolor="rgba(0,0,0,0)"),
)


def _apply_layout(fig, title=""):
    """Apply consistent dark-theme styling with high-visibility fonts."""
    fig.update_layout(
        title=dict(text=title, font=_TITLE_FONT, x=0.01),
        **_LAYOUT_DEFAULTS,
    )
    fig.update_xaxes(
        gridcolor=COLORS["grid"],
        zeroline=False,
        title_font=_AXIS_TITLE,
        tickfont=_TICK_FONT,
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        zeroline=False,
        title_font=_AXIS_TITLE,
        tickfont=_TICK_FONT,
    )
    return fig


# ───────────────────────────────────────────────────────────────────────────
# A. Stock Price Chart with Moving Averages
# ───────────────────────────────────────────────────────────────────────────

def stock_price_chart(hist: pd.DataFrame, ticker: str = "") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist["Close"], name="Close",
        line=dict(color=COLORS["accent"], width=2),
    ))
    for window, color in [(20, COLORS["yellow"]), (50, COLORS["purple"])]:
        if len(hist) >= window:
            ma = hist["Close"].rolling(window).mean()
            fig.add_trace(go.Scatter(
                x=hist.index, y=ma, name=f"MA-{window}",
                line=dict(color=color, width=1.5, dash="dot"),
            ))
    return _apply_layout(fig, f"{ticker} Stock Price")


# ───────────────────────────────────────────────────────────────────────────
# B. Option Payoff Diagram
# ───────────────────────────────────────────────────────────────────────────

def payoff_chart(K: float, premium_call: float, premium_put: float,
                 S_range=None) -> go.Figure:
    if S_range is None:
        S_range = np.linspace(K * 0.7, K * 1.3, 200)

    call_payoff = np.maximum(S_range - K, 0) - premium_call
    put_payoff  = np.maximum(K - S_range, 0) - premium_put

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=call_payoff, name="Call Payoff",
                             line=dict(color=COLORS["green"], width=2.5)))
    fig.add_trace(go.Scatter(x=S_range, y=put_payoff, name="Put Payoff",
                             line=dict(color=COLORS["red"], width=2.5)))
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["text"], opacity=0.3)
    fig.update_xaxes(title_text="Stock Price at Expiry")
    fig.update_yaxes(title_text="Profit / Loss ($)")
    return _apply_layout(fig, "Option Payoff Diagram")


# ───────────────────────────────────────────────────────────────────────────
# C. Volatility Smile
# ───────────────────────────────────────────────────────────────────────────

def volatility_smile(df: pd.DataFrame) -> go.Figure:
    valid = df.dropna(subset=["strike", "iv"])
    valid = valid[valid["iv"] > 0].sort_values("strike")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=valid["strike"], y=valid["iv"] * 100,
        mode="lines+markers", name="Implied Vol",
        line=dict(color=COLORS["accent"], width=2),
        marker=dict(size=6),
    ))
    fig.update_xaxes(title_text="Strike Price ($)")
    fig.update_yaxes(title_text="Implied Volatility (%)")
    return _apply_layout(fig, "Volatility Smile")


# ───────────────────────────────────────────────────────────────────────────
# D. Mispricing Heatmap
# ───────────────────────────────────────────────────────────────────────────

def mispricing_heatmap(df: pd.DataFrame) -> go.Figure:
    valid = df.dropna(subset=["strike", "mispricing"]).sort_values("strike")
    colors = [COLORS["green"] if v < 0 else COLORS["red"]
              for v in valid["mispricing"]]
    fig = go.Figure(go.Bar(
        x=valid["strike"], y=valid["mispricing"],
        marker_color=colors, name="Mispricing",
        text=[f"${v:+.2f}" for v in valid["mispricing"]],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["text"]),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["text"], opacity=0.3)
    fig.update_xaxes(title_text="Strike Price ($)")
    fig.update_yaxes(title_text="Mispricing ($)")
    return _apply_layout(fig, "Mispricing by Strike  (Green = Under, Red = Over)")


# ───────────────────────────────────────────────────────────────────────────
# E. Greeks Bar Chart
# ───────────────────────────────────────────────────────────────────────────

def greeks_bar_chart(greeks: dict) -> go.Figure:
    names = list(greeks.keys())
    vals  = list(greeks.values())
    bar_colors = [COLORS["accent"], COLORS["green"], COLORS["purple"],
                  COLORS["red"], COLORS["yellow"]]
    fig = go.Figure(go.Bar(
        x=names, y=vals,
        marker_color=bar_colors[:len(names)],
        text=[f"{v:+.4f}" for v in vals],
        textposition="outside",
        textfont=dict(size=13, color="#FFFFFF", family=_FONT_FAMILY),
    ))
    fig.update_xaxes(tickfont=dict(size=14, color="#FFFFFF"))
    fig.update_yaxes(title_text="Value")
    return _apply_layout(fig, "Option Greeks")


# ───────────────────────────────────────────────────────────────────────────
# F. Anomaly Scatter
# ───────────────────────────────────────────────────────────────────────────

def anomaly_scatter(df: pd.DataFrame) -> go.Figure:
    if "anomaly_label" not in df.columns:
        return go.Figure()

    df = df.dropna(subset=["strike", "anomaly_score"])
    normal  = df[df["anomaly_label"] == 1]
    anomaly = df[df["anomaly_label"] == -1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=normal["strike"], y=normal["anomaly_score"],
        mode="markers", name="Normal",
        marker=dict(color=COLORS["green"], size=8, opacity=0.7),
    ))
    fig.add_trace(go.Scatter(
        x=anomaly["strike"], y=anomaly["anomaly_score"],
        mode="markers", name="Anomaly",
        marker=dict(color=COLORS["red"], size=12, symbol="x", opacity=0.9),
    ))
    fig.update_xaxes(title_text="Strike Price ($)")
    fig.update_yaxes(title_text="Anomaly Score")
    return _apply_layout(fig, "ML Anomaly Detection Results")
