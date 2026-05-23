# src/analytics/ml_features.py
"""ML Feature Engineering Pipeline for Phase 5.
Extracts 25+ engineered features from indicator DataFrames for the ML Signal Engine.
Features span 7 groups: momentum, trend, volume, volatility, price action, persistence, cross-module.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


# ── Human-readable display names for each feature ──────────────────────────
FEATURE_DISPLAY_NAMES: Dict[str, str] = {
    # Momentum
    "rsi": "RSI Level",
    "rsi_slope_5": "RSI Momentum Direction",
    "macd_histogram": "MACD Momentum",
    "macd_hist_change": "MACD Trend Change",
    # Trend
    "sma20_sma50_ratio": "Trend Structure",
    "sma20_slope": "Trend Direction",
    "price_vs_sma20": "Price vs Short-Term Trend",
    "price_vs_sma50": "Price vs Long-Term Trend",
    # Volume
    "volume_ratio": "Volume Expansion",
    "volume_trend_5": "Volume Trend",
    "volume_expansion": "Volume Spike",
    # Volatility
    "atr_pct": "Volatility Level",
    "atr_percentile": "Volatility Regime",
    "bb_width": "Bollinger Band Width",
    "bb_position": "Price Position in Bands",
    # Price Action
    "roc_5": "5-Day Momentum",
    "roc_10": "10-Day Momentum",
    "roc_20": "20-Day Momentum",
    "candle_body_ratio": "Candle Strength",
    "upper_wick_ratio": "Selling Pressure",
    # Persistence
    "bullish_streak": "Momentum Persistence",
    "rsi_above_50_duration": "Momentum Duration",
    # Cross-module (optional)
    "trade_quality_score": "Trade Quality",
    "anomaly_score": "Anomaly Level",
}


def get_feature_names() -> List[str]:
    """Return ordered list of core feature names (excluding optional cross-module)."""
    return [
        # Momentum (4)
        "rsi", "rsi_slope_5", "macd_histogram", "macd_hist_change",
        # Trend (4)
        "sma20_sma50_ratio", "sma20_slope", "price_vs_sma20", "price_vs_sma50",
        # Volume (3)
        "volume_ratio", "volume_trend_5", "volume_expansion",
        # Volatility (4)
        "atr_pct", "atr_percentile", "bb_width", "bb_position",
        # Price Action (5)
        "roc_5", "roc_10", "roc_20", "candle_body_ratio", "upper_wick_ratio",
        # Persistence (2)
        "bullish_streak", "rsi_above_50_duration",
    ]


def _safe_div(a, b, default=0.0):
    """Division with zero/NaN safety."""
    if b is None or b == 0 or (isinstance(b, float) and np.isnan(b)):
        return default
    result = a / b
    return default if np.isnan(result) or np.isinf(result) else result


# ── Group 1: Momentum Features ────────────────────────────────────────────

def _momentum_features(df: pd.DataFrame) -> pd.DataFrame:
    """RSI, RSI slope, MACD histogram, MACD histogram change."""
    feats = pd.DataFrame(index=df.index)

    # RSI value (already computed)
    feats["rsi"] = df.get("RSI", pd.Series(50.0, index=df.index))

    # RSI 5-bar slope (rate of change)
    feats["rsi_slope_5"] = feats["rsi"].diff(5)

    # MACD histogram = MACD - MACD_Signal
    macd = df.get("MACD", pd.Series(0.0, index=df.index))
    macd_sig = df.get("MACD_Signal", pd.Series(0.0, index=df.index))
    feats["macd_histogram"] = macd - macd_sig

    # MACD histogram 3-bar change
    feats["macd_hist_change"] = feats["macd_histogram"].diff(3)

    return feats


# ── Group 2: Trend Features ───────────────────────────────────────────────

def _trend_features(df: pd.DataFrame) -> pd.DataFrame:
    """SMA structure, slopes, price distances."""
    feats = pd.DataFrame(index=df.index)

    sma20 = df.get("SMA20", pd.Series(dtype=float))
    sma50 = df.get("SMA50", pd.Series(dtype=float))
    close = df["Close"]

    # SMA20/SMA50 ratio
    feats["sma20_sma50_ratio"] = np.where(
        sma50 > 0, sma20 / sma50, 1.0
    )

    # SMA20 slope: % change over 5 bars
    feats["sma20_slope"] = sma20.pct_change(5) * 100

    # Price distance from SMA20 (%)
    feats["price_vs_sma20"] = np.where(
        sma20 > 0, (close - sma20) / sma20 * 100, 0.0
    )

    # Price distance from SMA50 (%)
    feats["price_vs_sma50"] = np.where(
        sma50 > 0, (close - sma50) / sma50 * 100, 0.0
    )

    return feats


# ── Group 3: Volume Features ──────────────────────────────────────────────

def _volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """Volume ratio, volume trend, volume expansion flag."""
    feats = pd.DataFrame(index=df.index)

    vol = df["Volume"].astype(float)
    vol_ma20 = vol.rolling(20, min_periods=1).mean()

    # Volume ratio (current / 20-day average)
    feats["volume_ratio"] = np.where(vol_ma20 > 0, vol / vol_ma20, 1.0)

    # Volume 5-bar trend (simple slope via pct_change)
    feats["volume_trend_5"] = vol.pct_change(5)

    # Volume expansion flag (1 if > 1.5x average)
    feats["volume_expansion"] = (feats["volume_ratio"] > 1.5).astype(float)

    return feats


# ── Group 4: Volatility Features ──────────────────────────────────────────

def _volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """ATR percentage, ATR percentile, BB width, BB position."""
    feats = pd.DataFrame(index=df.index)

    close = df["Close"]
    atr = df.get("ATR", pd.Series(0.0, index=df.index))
    bb_upper = df.get("BB_Upper", pd.Series(dtype=float))
    bb_lower = df.get("BB_Lower", pd.Series(dtype=float))

    # ATR as % of price
    feats["atr_pct"] = np.where(close > 0, atr / close * 100, 0.0)

    # ATR percentile rank over 20 bars
    feats["atr_percentile"] = atr.rolling(20, min_periods=5).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
    )

    # Bollinger Band width (% of price)
    bb_range = bb_upper - bb_lower
    feats["bb_width"] = np.where(close > 0, bb_range / close * 100, 0.0)

    # BB position: where price sits within bands (0 = lower, 1 = upper)
    feats["bb_position"] = np.where(
        bb_range > 0, (close - bb_lower) / bb_range, 0.5
    )

    return feats


# ── Group 5: Price Action Features ────────────────────────────────────────

def _price_action_features(df: pd.DataFrame) -> pd.DataFrame:
    """Rate of change, candle body ratio, wick ratios."""
    feats = pd.DataFrame(index=df.index)

    close = df["Close"]
    open_ = df["Open"]
    high = df["High"]
    low = df["Low"]

    # Rate of change at 5, 10, 20 bars
    feats["roc_5"] = close.pct_change(5) * 100
    feats["roc_10"] = close.pct_change(10) * 100
    feats["roc_20"] = close.pct_change(20) * 100

    # Candle body ratio: |Close - Open| / (High - Low)
    hl_range = high - low
    feats["candle_body_ratio"] = np.where(
        hl_range > 0, (close - open_).abs() / hl_range, 0.5
    )

    # Upper wick ratio: (High - max(Open, Close)) / (High - Low)
    body_top = pd.concat([close, open_], axis=1).max(axis=1)
    feats["upper_wick_ratio"] = np.where(
        hl_range > 0, (high - body_top) / hl_range, 0.0
    )

    return feats


# ── Group 6: Persistence Features ─────────────────────────────────────────

def _persistence_features(df: pd.DataFrame) -> pd.DataFrame:
    """Consecutive bullish bars, RSI above 50 duration."""
    feats = pd.DataFrame(index=df.index)

    # Consecutive bullish bars (Close > Open)
    bullish = (df["Close"] > df["Open"]).astype(int)
    streak = pd.Series(0, index=df.index)
    current_streak = 0
    for i in range(len(bullish)):
        if bullish.iloc[i] == 1:
            current_streak += 1
        else:
            current_streak = 0
        streak.iloc[i] = current_streak
    feats["bullish_streak"] = streak

    # RSI above 50 duration
    rsi = df.get("RSI", pd.Series(50.0, index=df.index))
    above_50 = (rsi > 50).astype(int)
    rsi_duration = pd.Series(0, index=df.index)
    current_dur = 0
    for i in range(len(above_50)):
        if above_50.iloc[i] == 1:
            current_dur += 1
        else:
            current_dur = 0
        rsi_duration.iloc[i] = current_dur
    feats["rsi_above_50_duration"] = rsi_duration

    return feats


# ── Group 7: Cross-Module Features (Optional) ─────────────────────────────

def _cross_module_features(extra_signals: Optional[dict]) -> Dict[str, float]:
    """Extract cross-module features from external analytics.
    Returns dict of scalar values (applied to the latest row only for prediction).
    """
    cross = {}
    if extra_signals is None:
        return cross

    cross["trade_quality_score"] = extra_signals.get("trade_quality", 5.0)
    cross["anomaly_score"] = extra_signals.get("anomaly_score", 0.0)

    return cross


# ── Main Feature Extraction ───────────────────────────────────────────────

def extract_ml_features(
    df: pd.DataFrame, extra_signals: Optional[dict] = None
) -> pd.DataFrame:
    """Extract all ML features from an indicator DataFrame.

    Parameters
    ----------
    df : DataFrame
        Must contain OHLCV columns + indicators from ``compute_all_indicators()``:
        SMA20, SMA50, EMA20, RSI, MACD, MACD_Signal, BB_Upper, BB_Lower, ATR, VWAP.
    extra_signals : dict, optional
        Optional cross-module signals: ``{"trade_quality": 7.2, "anomaly_score": 15.0, "regime": "Trending Bullish"}``.

    Returns
    -------
    pd.DataFrame
        DataFrame with 22-25 feature columns, same index as input.
        Early rows will have NaN (from rolling calculations) — forward/backward filled.
    """
    if df.empty or len(df) < 20:
        return pd.DataFrame()

    # Extract feature groups
    momentum = _momentum_features(df)
    trend = _trend_features(df)
    volume = _volume_features(df)
    volatility = _volatility_features(df)
    price_action = _price_action_features(df)
    persistence = _persistence_features(df)

    # Combine all groups
    features = pd.concat(
        [momentum, trend, volume, volatility, price_action, persistence],
        axis=1,
    )

    # Add cross-module features as constant columns (if provided)
    cross = _cross_module_features(extra_signals)
    for key, value in cross.items():
        features[key] = value

    # Handle NaN: forward fill → backward fill → zero fill
    features = features.ffill().bfill().fillna(0.0)

    # Replace inf values
    features = features.replace([np.inf, -np.inf], 0.0)

    return features


def get_feature_detail(feature_name: str, value: float, historical_mean: float = None) -> str:
    """Generate a human-readable detail string for a feature value.

    Parameters
    ----------
    feature_name : str
        Internal feature name (e.g., "rsi_slope_5").
    value : float
        Current feature value.
    historical_mean : float, optional
        Mean of the feature over training data, for comparison.

    Returns
    -------
    str
        Human-readable detail string.
    """
    display = FEATURE_DISPLAY_NAMES.get(feature_name, feature_name)

    detail_templates = {
        "rsi": lambda v: f"RSI at {v:.1f}" + (", in bullish territory" if v > 55 else ", in bearish territory" if v < 45 else ", neutral"),
        "rsi_slope_5": lambda v: f"RSI {'rising' if v > 0 else 'falling'} over last 5 bars ({v:+.1f})",
        "macd_histogram": lambda v: f"MACD histogram {'positive and expanding' if v > 0 else 'negative and contracting'}",
        "macd_hist_change": lambda v: f"MACD histogram {'accelerating upward' if v > 0 else 'decelerating'}",
        "sma20_sma50_ratio": lambda v: f"SMA20 {v:.3f}× {'above' if v > 1 else 'below'} SMA50",
        "sma20_slope": lambda v: f"SMA20 {'rising' if v > 0 else 'falling'} at {abs(v):.2f}% per 5 bars",
        "price_vs_sma20": lambda v: f"Price {abs(v):.1f}% {'above' if v > 0 else 'below'} SMA20",
        "price_vs_sma50": lambda v: f"Price {abs(v):.1f}% {'above' if v > 0 else 'below'} SMA50",
        "volume_ratio": lambda v: f"Volume {v:.1f}× {'above' if v > 1 else 'below'} 20-day average",
        "volume_trend_5": lambda v: f"Volume {'increasing' if v > 0 else 'decreasing'} over last 5 bars",
        "volume_expansion": lambda v: f"{'Significant volume spike detected' if v > 0.5 else 'Normal volume'}",
        "atr_pct": lambda v: f"ATR at {v:.1f}% of price — {'high' if v > 2.5 else 'moderate' if v > 1.5 else 'low'}",
        "atr_percentile": lambda v: f"Volatility in {v*100:.0f}th percentile",
        "bb_width": lambda v: f"Bands {'widening' if v > 5 else 'narrowing'} — {'high' if v > 5 else 'squeeze potential' if v < 2 else 'normal'} width",
        "bb_position": lambda v: f"Price in {'upper' if v > 0.6 else 'lower' if v < 0.4 else 'middle'} {v*100:.0f}% of Bollinger range",
        "roc_5": lambda v: f"{v:+.1f}% over 5 days",
        "roc_10": lambda v: f"{v:+.1f}% over 10 days",
        "roc_20": lambda v: f"{v:+.1f}% over 20 days",
        "candle_body_ratio": lambda v: f"{'Strong' if v > 0.6 else 'Weak'} {'candle body' if v > 0 else 'doji pattern'}",
        "upper_wick_ratio": lambda v: f"{'Minimal' if v < 0.2 else 'Significant'} upper wick — {'buyers dominant' if v < 0.2 else 'selling pressure'}",
        "bullish_streak": lambda v: f"{int(v)} consecutive bullish bars",
        "rsi_above_50_duration": lambda v: f"RSI above 50 for {int(v)} consecutive bars",
        "trade_quality_score": lambda v: f"Overall quality score: {v:.1f}/10",
        "anomaly_score": lambda v: f"{'Behavior within normal range' if v < 30 else 'Anomalous behavior detected (score: ' + f'{v:.0f})'}",
    }

    template = detail_templates.get(feature_name)
    if template:
        return template(value)
    return f"{display}: {value:.2f}"
