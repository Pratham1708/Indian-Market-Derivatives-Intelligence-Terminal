# app.py
"""Indian Market & Derivatives Intelligence Terminal (Streamlit)

Institutional AI-Assisted Market Intelligence & Probabilistic Decision Support System.
Integrates OHLCV analytics, technical indicators, ML intelligence, options analytics,
derivatives sentiment, backtesting, and portfolio intelligence.

Phase 5: ML Signal Engine, AI Recommendation Narrator, Executive Summary V2.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ── Local modules ────────────────────────────────────────────────────────
from data.nse_data import (
    get_current_price,
    get_historical_data,
    get_symbol_suggestions,
)
from analytics.indicators import compute_all_indicators
from signals.rule_based import generate_signals
from visualizations.candlestick import plot_candlestick
from visualizations.trend_cards import render_signal_card

# Phase 2
from src.analytics.scanner import scan_market, calculate_breadth, classify_setup
from src.data.universe import get_all_sectors
from src.analytics.trade_quality import compute_trade_quality_score

# Phase 3
from src.analytics.ml_models import detect_anomalies
from src.analytics.regime_detection import detect_regime, get_regime_alert
from src.analytics.signal_reliability import evaluate_signal_reliability
from src.analytics.probability_engine import estimate_setup_probability, compute_expected_move
from src.analytics.advanced_breadth import compute_advanced_breadth, generate_breadth_feed

# Phase 4
from src.analytics.options_intelligence import compute_options_intelligence
from src.analytics.derivatives_sentiment import compute_derivatives_sentiment
from src.analytics.backtesting import backtest_setup

# Phase 5
from src.analytics.ml_signal_engine import ml_generate_signal
from src.analytics.llm_recommendation_engine import (
    build_intelligence_context,
    get_recommendation,
)
from src.visualizations.executive_summary_v2 import render_executive_summary_v2

# ── Page configuration & CSS ──────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Market & Derivatives Intelligence Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*='css'] {font-family: 'Inter', sans-serif;}
body {background-color: #0E1117; color: #F0F2F6;}
.accent-bar {height:4px;background:linear-gradient(90deg,#00D4FF,#9B59B6,#FF4560);border-radius:2px;margin-bottom:1.2rem;}
.badge {font-size:1.2rem;padding:4px 8px;border-radius:4px;}
.badge.green {background:#00E396;color:#000;}
.badge.red {background:#FF4560;color:#000;}
.badge.yellow {background:#FEB019;color:#000;}
.intel-card {background:#1a1d23;border:1px solid #2d3139;border-radius:8px;padding:1rem;margin-bottom:0.8rem;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar – Mode & Search ──────────────────────────────
st.sidebar.title("🎮 Dashboard Mode")
mode = st.sidebar.radio("Select Mode", ["Single Stock Analysis", "Market Scanner"])
st.sidebar.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

ticker = ""
hist_period = "1y"

if mode == "Single Stock Analysis":
    prefix = st.sidebar.text_input("Search Ticker/Company (e.g. RELIANCE, TCS, HDFC)", value="RELIANCE.NS", help="Start typing ticker or company name to see suggestions.")
    suggestions = []
    if len(prefix.strip()) >= 2:
        suggestions = get_symbol_suggestions(prefix.strip())
        if suggestions:
            selected_suggestion = st.sidebar.selectbox("Select matching stock", suggestions, index=0)
            ticker = selected_suggestion.split(" - ")[0].strip()
        else:
            ticker = prefix.upper().strip()
    else:
        ticker = prefix.upper().strip()
    hist_period = st.sidebar.selectbox("Historical Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)

    # Phase 5: AI Narrator settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Narrator")
    ai_provider = st.sidebar.selectbox(
        "LLM Provider",
        ["None (Template)", "Gemini", "OpenAI", "Claude"],
        index=0,
        help="Select an LLM provider for AI-powered narratives. 'None' uses high-quality templates (free, no API key)."
    )
    ai_api_key = ""
    sidebar_status = None
    if ai_provider != "None (Template)":
        ai_api_key = st.sidebar.text_input(
            f"{ai_provider} API Key",
            type="password",
            help=f"Enter your {ai_provider} API key, or set it in a .env file."
        )
        sidebar_status = st.sidebar.empty()

else:
    hist_period = st.sidebar.selectbox("Scan Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    ai_provider = "None (Template)"
    ai_api_key = ""
    sidebar_status = None

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit & Python")

# ── Main Header ──────────────────────────────────────────────────────────────
st.title("📈 Indian Market & Derivatives Intelligence Terminal")
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

# ── Data guard ────────────────────────────────────────────────────────────
if mode == "Single Stock Analysis":
    if not ticker:
        st.info("Please enter a ticker symbol in the sidebar to begin.")
        st.stop()

# ══════════════════════════════════════════════════════════════════════════
# SINGLE STOCK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════

def run_single_stock_analysis(ticker, hist_period):
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_data(ticker, period):
        price = get_current_price(ticker)
        hist = get_historical_data(ticker, period=period)
        return price, hist

    try:
        with st.spinner(f"Fetching data for **{ticker}** …"):
            current_price, hist_df = fetch_data(ticker, hist_period)
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        st.stop()

    indicators_df = compute_all_indicators(hist_df)
    setup = classify_setup(indicators_df)
    latest = indicators_df.iloc[-1]

    # ── Compute all intelligence ─────────────────────────────────────────
    anomaly_result = detect_anomalies(indicators_df)
    regime_result = detect_regime(indicators_df)
    regime_alert = get_regime_alert(regime_result)
    reliability = evaluate_signal_reliability(indicators_df, setup)
    prob_result = estimate_setup_probability(indicators_df, setup)
    move_result = compute_expected_move(indicators_df)
    options_intel = compute_options_intelligence(indicators_df)
    deriv_sentiment = compute_derivatives_sentiment(hist_df)

    # Trade Quality (fixed: was displaying SMA20 value)
    sma_diff = (latest.get("SMA20", 0) - latest.get("SMA50", 0)) / latest.get("SMA50", 1) if latest.get("SMA50", 0) > 0 else 0
    tq_dict = compute_trade_quality_score(
        sma_diff=sma_diff,
        rsi=latest.get("RSI", 50),
        volume=latest.get("Volume", 0),
        avg_volume=indicators_df["Volume"].rolling(20).mean().iloc[-1] if "Volume" in indicators_df.columns else 1,
        atr=latest.get("ATR", 0),
        price=current_price,
    )

    # Phase 5: ML Signal Engine (replaces rule-based)
    signal_info = ml_generate_signal(
        indicators_df,
        extra_signals={
            "regime": regime_result.get("current_regime", "Unknown"),
            "anomaly_score": anomaly_result.get("anomaly_score", 0),
            "anomaly_class": anomaly_result.get("anomaly_class", "Normal"),
            "trade_quality": tq_dict.get("overall_quality", 5.0),
        },
        ticker=ticker,
        period=hist_period,
    )

    # Phase 5: AI Recommendation Narrator
    intel_context = build_intelligence_context(
        ticker=ticker,
        price=current_price,
        signal_info=signal_info,
        regime_result=regime_result,
        prob_result=prob_result,
        options_intel=options_intel,
        deriv_sentiment=deriv_sentiment,
        anomaly_result=anomaly_result,
        reliability=reliability,
        move_result=move_result,
    )
    ai_recommendation = get_recommendation(
        context=intel_context,
        provider=ai_provider,
        api_key=ai_api_key,
    )

    # Update sidebar LLM connection status dynamically
    if sidebar_status:
        mode_val = ai_recommendation.get("mode", "Template")
        if mode_val == "LLM":
            sidebar_status.success(f"🤖 Connected to {ai_provider}!")
        elif "Fallback (Error:" in mode_val:
            err_msg = mode_val.replace("Template Fallback (Error: ", "").replace(")", "")
            sidebar_status.error(f"❌ {ai_provider} API Failed: {err_msg[:60]}...")
        elif "Fallback" in mode_val:
            sidebar_status.warning(f"⚠️ {mode_val}")
        else:
            sidebar_status.info("ℹ️ Running local templates (Free)")

    # ── Executive Summary V2 (Phase 5 redesign) ─────────────────────────
    render_executive_summary_v2(
        ticker=ticker,
        price=current_price,
        signal_info=signal_info,
        regime_result=regime_result,
        prob_result=prob_result,
        options_intel=options_intel,
        deriv_sentiment=deriv_sentiment,
        anomaly_result=anomaly_result,
        reliability=reliability,
        move_result=move_result,
        ai_recommendation=ai_recommendation,
        trade_quality=tq_dict,
    )

    # ── Price Action & Indicators ────────────────────────────────────────
    st.subheader("📊 Price Action & Indicators")
    fig = plot_candlestick(indicators_df, ticker)
    st.plotly_chart(fig, use_container_width=True)

    # ── Technical Indicators ─────────────────────────────────────────────
    st.subheader("📈 Technical Indicators")
    indicator_vals = {
        "SMA20": f"{latest['SMA20']:.2f}", "SMA50": f"{latest['SMA50']:.2f}",
        "EMA20": f"{latest['EMA20']:.2f}", "RSI": f"{latest['RSI']:.1f}",
        "MACD": f"{latest['MACD']:.2f}", "MACD_Signal": f"{latest['MACD_Signal']:.2f}",
        "BB Upper": f"{latest['BB_Upper']:.2f}", "BB Lower": f"{latest['BB_Lower']:.2f}",
        "ATR": f"{latest['ATR']:.2f}", "VWAP": f"{latest['VWAP']:.2f}",
    }
    st.table(indicator_vals)

    # ── Signal & Recommendation ──────────────────────────────────────────
    col_sig, col_rec = st.columns(2)
    with col_sig:
        st.subheader("⚡ ML Signal Engine")
        render_signal_card(signal_info)
    with col_rec:
        st.subheader("💡 AI Recommendation")
        
        # Show mode / status indicator
        mode_val = ai_recommendation.get("mode", "Template")
        if mode_val == "LLM":
            st.caption(f"🟢 **Live {ai_provider} AI Narrator Active**")
        elif "Fallback" in mode_val:
            st.caption(f"🟠 **{mode_val}** (using local template)")
        else:
            st.caption("ℹ️ **Local Template Narrator Active** (No API Key)")

        narrative = ai_recommendation.get("full_narrative", "")
        if narrative:
            st.markdown(narrative)
        else:
            st.markdown(signal_info.get("recommendation", "No recommendation available."))

    st.markdown("---")

    # ── AI Intelligence Panel ────────────────────────────────────────────
    st.subheader("🤖 AI Market Intelligence")

    ai1, ai2, ai3 = st.columns(3)

    with ai1:
        st.markdown("#### 🔬 Anomaly Detection")
        if anomaly_result["anomaly_class"] == "Anomaly Detected":
            st.error(f"**{anomaly_result['anomaly_class']}** — Score: {anomaly_result['anomaly_score']}")
        else:
            st.success(f"**{anomaly_result['anomaly_class']}** — Score: {anomaly_result['anomaly_score']}")
        st.caption(anomaly_result["explanation"])

    with ai2:
        st.markdown("#### 🌡️ Regime Detection")
        if regime_result["transition_detected"]:
            st.warning(f"**Transition:** {regime_result['transition_description']}")
        else:
            st.info(f"**{regime_result['current_regime']}** ({regime_result['regime_duration']} bars)")
        st.caption(regime_alert)

    with ai3:
        st.markdown("#### 📊 Signal Reliability")
        wr = reliability.get("win_rate")
        st.metric("Win Rate", f"{wr*100:.1f}%" if wr is not None else "N/A")
        st.caption(reliability.get("explanation", ""))

    # Probability row
    pr1, pr2, pr3 = st.columns(3)
    with pr1:
        st.markdown("#### 🎯 Setup Probability")
        st.metric("Success Probability", f"{prob_result['probability']*100:.1f}%")
        band = prob_result["confidence_band"]
        st.caption(f"Band: {band[0]*100:.0f}%–{band[1]*100:.0f}% | {prob_result['explanation']}")
    with pr2:
        st.markdown("#### 📐 Expected Move (5-Day)")
        st.metric("Move Range", f"±{move_result['expected_move_pct']}%")
        st.caption(move_result["explanation"])
    with pr3:
        st.markdown("#### 🎖️ Trade Quality")
        st.metric("Overall Score", f"{tq_dict['overall_quality']:.1f}/10")
        st.caption(
            f"Trend: {tq_dict['trend_strength']:.0f} | "
            f"Momentum: {tq_dict['momentum']:.0f} | "
            f"Volume: {tq_dict['volume_confirmation']:.0f} | "
            f"Volatility: {tq_dict['volatility_quality']:.0f}"
        )

    st.markdown("---")

    # ── Options Intelligence ─────────────────────────────────────────────
    st.subheader("📌 Options & Derivatives Intelligence")

    opt1, opt2, opt3 = st.columns(3)
    with opt1:
        st.markdown("#### 📈 IV Analysis")
        st.metric("IV Estimate", f"{options_intel['iv_estimate']*100:.1f}%")
        st.metric("IV Percentile", f"{options_intel['iv_percentile']:.0f}%")
        st.caption(f"RV (20d): {options_intel['rv_20d']*100:.1f}% | {options_intel['iv_regime']}")

    with opt2:
        st.markdown("#### 💰 Option Pricing (ATM)")
        st.metric("Call Price", f"₹{options_intel['call_price']:.2f}")
        st.metric("Put Price", f"₹{options_intel['put_price']:.2f}")
        st.caption(f"Strike: ₹{options_intel['strike']:,.0f} | Spot: ₹{options_intel['spot']:,.2f}")

    with opt3:
        st.markdown("#### 🇬🇷 Greeks (Call)")
        greeks = options_intel.get("greeks_call", {})
        for g, v in greeks.items():
            st.text(f"{g}: {v}")

    # Derivatives Sentiment
    ds1, ds2 = st.columns(2)
    with ds1:
        st.markdown("#### 📊 Derivatives Sentiment")
        st.metric("Sentiment", deriv_sentiment["sentiment"])
        st.metric("PCR Proxy", deriv_sentiment["pcr"])
        st.caption(deriv_sentiment["explanation"])
    with ds2:
        st.markdown("#### 🎯 Max Pain & Buildup")
        st.metric("Max Pain Estimate", f"₹{deriv_sentiment['max_pain']:,.0f}")
        st.metric("OI Buildup", deriv_sentiment["buildup"])
        st.caption(deriv_sentiment["buildup_explanation"])

    st.markdown("---")

    # ── Backtesting ──────────────────────────────────────────────────────
    st.subheader("🧪 Strategy Backtest")
    with st.expander("Run Backtest for Current Setup", expanded=False):
        bt_col1, bt_col2, bt_col3 = st.columns(3)
        holding = bt_col1.number_input("Holding Period (bars)", 3, 20, 5)
        sl = bt_col2.number_input("Stop Loss %", 1.0, 10.0, 3.0, step=0.5) / 100
        tgt = bt_col3.number_input("Target %", 1.0, 20.0, 5.0, step=0.5) / 100

        bt = backtest_setup(indicators_df, setup, holding_period=holding, stop_loss_pct=sl, target_pct=tgt)

        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total Trades", bt["total_trades"])
        b2.metric("Win Rate", f"{bt['win_rate']*100:.1f}%")
        b3.metric("Sharpe Ratio", bt["sharpe"])
        b4.metric("Max Drawdown", f"{bt['max_drawdown']*100:.1f}%")

        b5, b6, b7, b8 = st.columns(4)
        b5.metric("Avg Return", f"{bt['avg_return']*100:.2f}%")
        b6.metric("Expectancy", f"{bt['expectancy']*100:.2f}%")
        b7.metric("Profit Factor", bt["profit_factor"])
        b8.metric("Sortino", bt["sortino"])

        st.caption(bt["explanation"])

    st.markdown("---")

    # ── Raw Data ─────────────────────────────────────────────────────────
    st.subheader("📂 Raw OHLCV Data")
    st.dataframe(hist_df.tail(20))

# ══════════════════════════════════════════════════════════════════════════
# MARKET SCANNER
# ══════════════════════════════════════════════════════════════════════════

if mode == "Single Stock Analysis":
    run_single_stock_analysis(ticker, hist_period)

elif mode == "Market Scanner":
    st.subheader("🔍 Market Scanner")

    debug_mode = st.sidebar.checkbox("Scanner Debug Mode", value=False)

    with st.spinner("Scanning market…"):
        scan_results, scan_logs, scan_failed = scan_market(period=hist_period)

    if debug_mode:
        st.markdown("### 🛠️ Scanner Debug Panel")
        c1, c2 = st.columns(2)
        c1.metric("Successful Scans", len(scan_results))
        c2.metric("Failed Scans", len(scan_failed))
        with st.expander("Show Debug Logs"):
            for log in scan_logs:
                if "[ERROR]" in log:
                    st.error(log)
                elif "[WARNING]" in log:
                    st.warning(log)
                else:
                    st.text(log)
        with st.expander("Show Failed Tickers"):
            st.json(scan_failed)
        st.markdown("---")

    if not scan_results.empty:
        # Market Intelligence Feed
        adv_breadth = compute_advanced_breadth(scan_results)
        feed_items = generate_breadth_feed(adv_breadth)

        if feed_items:
            st.markdown("### 📡 Market Intelligence Feed")
            for item in feed_items:
                st.markdown(f"> {item}")
            st.markdown("---")

        # Breadth metrics
        breadth = calculate_breadth(scan_results)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Advancing / Declining", breadth.get("Advancing vs Declining"))
        col2.metric("Bullish %", f"{breadth.get('Bullish %')}%")
        col3.metric("Bearish %", f"{breadth.get('Bearish %')}%")
        col4.metric("Neutral", breadth.get("Neutral Count", 0))
        col5.metric("Participation", f"{adv_breadth.get('participation_rate', 0)}%")

        st.markdown("---")

        # Top Opportunities
        st.markdown("### 🏆 Top Opportunities")
        top_3 = scan_results.head(3)
        cols = st.columns(3)
        for i, (idx, row) in enumerate(top_3.iterrows()):
            if i < 3:
                with cols[i]:
                    method_badge = "🤖 ML" if row.get("Method") == "ml_ensemble" else "📏 RB"
                    st.markdown(f"""
                    ### {row['Stock']}
                    **Score:** {row['Opportunity Score']}  
                    *{row['Conviction']}*  
                    **Signal:** {row['Signal']} {method_badge}  
                    **Setup:** {row['Setup Type']}  
                    **Regime:** {row.get('Regime', 'N/A')}  
                    **Anomaly:** {row.get('Anomaly', 'N/A')}
                    """)
        st.markdown("---")

        # Filters
        st.markdown("### 🛠️ Filters")
        c1, c2, c3, c4 = st.columns(4)
        all_sectors = ["All"] + get_all_sectors()
        selected_sector = c1.selectbox("Filter by Sector", all_sectors)
        all_setups = ["All"] + list(scan_results["Setup Type"].unique())
        selected_setup = c2.selectbox("Filter by Setup Type", all_setups)
        all_regimes = ["All"] + list(scan_results["Regime"].unique()) if "Regime" in scan_results.columns else ["All"]
        selected_regime = c3.selectbox("Filter by Regime", all_regimes)
        # New: filter by signal class
        signal_classes = ["All"] + list(scan_results["Signal_Class"].unique()) if "Signal_Class" in scan_results.columns else ["All"]
        selected_signal_class = c4.selectbox("Filter by Signal Class", signal_classes)

        filtered_df = scan_results.copy()
        if selected_sector != "All":
            filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
        if selected_setup != "All":
            filtered_df = filtered_df[filtered_df["Setup Type"] == selected_setup]
        if selected_regime != "All" and "Regime" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Regime"] == selected_regime]
        if selected_signal_class != "All" and "Signal_Class" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Signal_Class"] == selected_signal_class]

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["All Opportunities", "Bullish Setups", "Bearish Setups", "Anomalies"])
        with tab1:
            st.dataframe(filtered_df, use_container_width=True)
        with tab2:
            if "Signal_Class" in filtered_df.columns:
                st.dataframe(filtered_df[filtered_df["Signal_Class"] == "bullish"], use_container_width=True)
            else:
                st.dataframe(filtered_df[filtered_df["Signal"].str.contains("Bullish", na=False)], use_container_width=True)
        with tab3:
            if "Signal_Class" in filtered_df.columns:
                st.dataframe(filtered_df[filtered_df["Signal_Class"] == "bearish"], use_container_width=True)
            else:
                st.dataframe(filtered_df[filtered_df["Signal"].str.contains("Bearish", na=False)], use_container_width=True)
        with tab4:
            if "Anomaly" in filtered_df.columns:
                anomaly_df = filtered_df[filtered_df["Anomaly"] == "Anomaly Detected"]
                if not anomaly_df.empty:
                    st.dataframe(anomaly_df, use_container_width=True)
                else:
                    st.info("No anomalies detected in current scan.")
            else:
                st.info("Anomaly data not available.")
    else:
        st.warning("No scan results available.")
        if not debug_mode:
            st.info("Enable 'Scanner Debug Mode' in the sidebar to see detailed logs.")

# End of app.py
