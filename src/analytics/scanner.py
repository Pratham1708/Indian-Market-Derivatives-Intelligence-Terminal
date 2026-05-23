# src/analytics/scanner.py
"""Market Scanner Engine for Phase 2.
Scans a list of tickers, calculates signals and trade quality,
and returns a ranked list of opportunities using multi-factor prioritization.
Includes detailed logging and error handling to prevent silent failures.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import sys
import os
import traceback

# Add project root to path to import from root folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.nse_data import get_historical_data
from analytics.indicators import compute_all_indicators
from signals.rule_based import generate_signals
from src.analytics.trade_quality import compute_trade_quality_score
from src.analytics.ml_signal_engine import ml_generate_signal
from src.data.universe import get_nifty50_symbols, get_stock_sector
from src.data.market_context import fetch_index_history, relative_strength
from src.analytics.ml_models import detect_anomalies
from src.analytics.regime_detection import detect_regime, get_regime_alert

DEFAULT_TICKERS = get_nifty50_symbols()

def classify_setup(df: pd.DataFrame) -> str:
    """Classify the setup type based on indicators.
    Simple heuristic for Phase 2.
    """
    if df.empty or len(df) < 20:
        return "Unknown"
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Breakout
    if latest["Close"] > latest["BB_Upper"]:
        return "Breakout"
    
    # Pullback
    if latest["SMA20"] > latest["SMA50"] and latest["Close"] <= latest["SMA20"] * 1.01:
        return "Pullback"
    
    # Reversal
    if prev["RSI"] < 30 and latest["RSI"] >= 30:
        return "Reversal"
    
    # Trend Continuation
    if latest["SMA20"] > latest["SMA50"] and latest["MACD"] > latest["MACD_Signal"]:
        return "Trend Continuation"
    
    # Consolidation
    atr_rel = latest["ATR"] / latest["Close"] if latest["Close"] else 0
    if atr_rel < 0.01:
        return "Consolidation"
        
    return "Neutral"

def scan_market(tickers: List[str] = DEFAULT_TICKERS, period: str = "6mo") -> Tuple[pd.DataFrame, List[str], Dict[str, str]]:
    """Scan a list of tickers and return a ranked DataFrame of opportunities,
    along with debug logs and a dict of failed tickers.
    """
    results = []
    logs = []
    failed_tickers = {}
    
    logs.append(f"[INFO] Starting market scan for {len(tickers)} tickers with period={period}")
    
    # 1. Fetch NIFTY data once for relative strength
    logs.append("[INFO] Fetching NIFTY index data for benchmark...")
    try:
        index_df = fetch_index_history(period=period)
        logs.append(f"[INFO] NIFTY data fetched successfully ({len(index_df)} rows)")
    except Exception as e:
        logs.append(f"[ERROR] Failed to fetch NIFTY data: {e}")
        index_df = pd.DataFrame()
        
    for ticker in tickers:
        logs.append(f"[INFO] --- Scanning {ticker} ---")
        try:
            # Fetch data
            logs.append(f"[INFO] Fetching data for {ticker}...")
            df = get_historical_data(ticker, period=period)
            
            if df.empty:
                logs.append(f"[WARNING] {ticker} returned empty DataFrame")
                failed_tickers[ticker] = "Empty data returned"
                continue
                
            logs.append(f"[INFO] {ticker} fetched successfully ({len(df)} rows)")
            
            # Validate columns
            required_cols = ["Open", "High", "Low", "Close", "Volume"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                logs.append(f"[WARNING] {ticker} missing columns: {missing_cols}")
                failed_tickers[ticker] = f"Missing columns: {missing_cols}"
                continue
            
            # Compute indicators
            logs.append(f"[INFO] Computing indicators for {ticker}...")
            df_ind = compute_all_indicators(df)
            logs.append(f"[INFO] Indicators computed successfully")
            
            # Generate signals (ML engine with rule-based fallback)
            logs.append(f"[INFO] Generating ML signals for {ticker}...")
            sig_dict = ml_generate_signal(
                df_ind,
                extra_signals={
                    "regime": regime_info.get("current_regime", "Unknown") if 'regime_info' in dir() else "Unknown",
                },
                ticker=ticker,
                period=period,
            )
            logs.append(f"[INFO] Signal: {sig_dict['signal']} (Confidence: {sig_dict['confidence']}, Method: {sig_dict.get('method', 'unknown')})")
            
            # Compute trade quality
            latest = df_ind.iloc[-1]
            
            # Check for NaN in critical values
            critical_fields = ["SMA20", "SMA50", "RSI", "MACD", "ATR", "Close"]
            nans = [field for field in critical_fields if pd.isna(latest.get(field))]
            if nans:
                logs.append(f"[WARNING] {ticker} has NaN in critical fields for latest row: {nans}")
                # We can still proceed if we have fallback or if it's just one field,
                # but let's log it.
                
            sma_diff = (latest["SMA20"] - latest["SMA50"]) / latest["SMA50"] if pd.notna(latest.get("SMA50")) and latest["SMA50"] != 0 else 0
            avg_vol = df_ind["Volume"].rolling(20).mean().iloc[-1]
            
            tq_dict = compute_trade_quality_score(
                sma_diff=sma_diff,
                rsi=latest.get("RSI", 50), # fallback to 50 if NaN
                volume=latest.get("Volume", 0),
                avg_volume=avg_vol if pd.notna(avg_vol) else 1,
                atr=latest.get("ATR", 0),
                price=latest.get("Close", 1)
            )
            
            # Calculate Relative Strength
            rs = 1.0
            if not index_df.empty:
                try:
                    rs = relative_strength(df, index_df)
                    logs.append(f"[INFO] Relative Strength: {rs:.2f}")
                except Exception as e:
                    logs.append(f"[WARNING] Relative strength calculation failed for {ticker}: {e}")
                    rs = 1.0 # fallback
            
            # Classify setup
            setup_type = classify_setup(df_ind)
            logs.append(f"[INFO] Setup Type: {setup_type}")
            
            # Phase 3: Anomaly Detection
            try:
                anomaly_info = detect_anomalies(df_ind)
                logs.append(f"[INFO] Anomaly: {anomaly_info['anomaly_class']} (score: {anomaly_info['anomaly_score']})")
            except Exception as e:
                logs.append(f"[WARNING] Anomaly detection failed for {ticker}: {e}")
                anomaly_info = {"anomaly_score": 0.0, "anomaly_class": "N/A", "explanation": ""}
            
            # Phase 3: Regime Detection
            try:
                regime_info = detect_regime(df_ind)
                logs.append(f"[INFO] Regime: {regime_info['current_regime']}")
            except Exception as e:
                logs.append(f"[WARNING] Regime detection failed for {ticker}: {e}")
                regime_info = {"current_regime": "Unknown", "transition_detected": False}
            
            results.append({
                "Stock": ticker,
                "Sector": get_stock_sector(ticker),
                "Signal": sig_dict["signal"],
                "Signal_Class": sig_dict.get("signal_class", "neutral"),
                "Confidence": sig_dict["confidence"],
                "ML_Confidence": sig_dict["confidence"],
                "Setup Type": setup_type,
                "Trade Quality": tq_dict["overall_quality"],
                "Relative Strength": round(rs, 2),
                "Anomaly Score": anomaly_info["anomaly_score"],
                "Anomaly": anomaly_info["anomaly_class"],
                "Regime": regime_info["current_regime"],
                "Method": sig_dict.get("method", "unknown"),
            })
            
        except Exception as e:
            logs.append(f"[ERROR] Unexpected error scanning {ticker}: {e}")
            logs.append(f"[DEBUG] Traceback: {traceback.format_exc()}")
            failed_tickers[ticker] = str(e)
            continue
            
    # Create DataFrame
    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        logs.append("[WARNING] All scans failed or returned no results")
        return results_df, logs, failed_tickers
        
    # 2. Calculate Sector Strength
    logs.append("[INFO] Calculating sector strength...")
    sector_strength = results_df.groupby("Sector")["Trade Quality"].mean().to_dict()
    
    # 3. Calculate Final Opportunity Score and Conviction
    logs.append("[INFO] Calculating final opportunity scores and conviction...")
    def compute_final_score(row):
        tq = row["Trade Quality"] / 10.0
        ml_conf = row.get("ML_Confidence", row["Confidence"])
        rs = min(row["Relative Strength"] / 2.0, 1.0)
        sec_str = sector_strength.get(row["Sector"], 5.0) / 10.0
        anomaly_adj = 0.95 if row["Anomaly"] == "Anomaly Detected" else 1.0
        
        # ML confidence is now the primary scoring factor
        score = (ml_conf * 0.30) + (tq * 0.25) + (rs * 0.15) + (sec_str * 0.20) + (0.5 * 0.10)
        score *= anomaly_adj
        return round(score * 10, 1)
        
    results_df["Opportunity Score"] = results_df.apply(compute_final_score, axis=1)
    
    def get_conviction(score):
        if score >= 8.0: return "Elite Setup ⭐⭐⭐⭐"
        if score >= 6.5: return "High Conviction ⭐⭐⭐"
        if score >= 5.0: return "Moderate ⭐⭐"
        return "Weak ⭐"
        
    results_df["Conviction"] = results_df["Opportunity Score"].apply(get_conviction)
    
    # 4. Generate Explanation
    def generate_explanation(row):
        reasons = []
        if row["Opportunity Score"] >= 6.5:
            reasons.append("Ranked highly due to strong overall setup")
            if row["Relative Strength"] > 1.1:
                reasons.append("outperformance vs NIFTY")
            if sector_strength.get(row["Sector"], 0) > 6.5:
                reasons.append("strong sector participation")
        else:
            reasons.append("Lower ranking due to weaker metrics")
            if row["Relative Strength"] < 1.0:
                reasons.append("underperformance vs NIFTY")
        return ", ".join(reasons) + "."
        
    results_df["Explanation"] = results_df.apply(generate_explanation, axis=1)
    
    # Rank by Opportunity Score
    results_df = results_df.sort_values(by="Opportunity Score", ascending=False)
    
    logs.append(f"[INFO] Scan complete. Successfully processed {len(results_df)} stocks.")
        
    return results_df, logs, failed_tickers

def calculate_breadth(results_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate market breadth metrics from scanner results."""
    if results_df.empty:
        return {}
        
    total = len(results_df)
    # Use Signal_Class for cleaner classification if available
    if "Signal_Class" in results_df.columns:
        bullish = len(results_df[results_df["Signal_Class"] == "bullish"])
        bearish = len(results_df[results_df["Signal_Class"] == "bearish"])
    else:
        bullish = len(results_df[results_df["Signal"].str.contains("Bullish")])
        bearish = len(results_df[results_df["Signal"].str.contains("Bearish")])
    neutral = total - bullish - bearish
    
    return {
        "Total Stocks": total,
        "Bullish Count": bullish,
        "Bearish Count": bearish,
        "Neutral Count": neutral,
        "Bullish %": round(bullish / total * 100, 1) if total else 0,
        "Bearish %": round(bearish / total * 100, 1) if total else 0,
        "Advancing vs Declining": f"{bullish} / {bearish}"
    }
