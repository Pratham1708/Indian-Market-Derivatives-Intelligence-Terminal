# analytics/indicators.py
"""Technical indicator calculations for Indian stock OHLCV data.
All functions operate on a pandas DataFrame with columns: Open, High, Low, Close, Volume.
The main helper `compute_all_indicators` returns the original DataFrame with additional
columns for each indicator used throughout the dashboard.
"""

import pandas as pd
import numpy as np


def _sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window, min_periods=1).mean()


def _ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential Moving Average.
    `span` corresponds to the conventional EMA period.
    """
    return series.ewm(span=span, adjust=False).mean()


def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index.
    Returns a Series aligned with the input; early values are NaN until `period` is met.
    """
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    # Use Wilder's smoothing
    roll_up = up.ewm(alpha=1 / period, adjust=False).mean()
    roll_down = down.ewm(alpha=1 / period, adjust=False).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """MACD indicator.
    Returns a DataFrame with columns ``MACD`` and ``MACD_Signal``.
    """
    ema_fast = _ema(series, fast)
    ema_slow = _ema(series, slow)
    macd_line = ema_fast - ema_slow
    macd_signal = _ema(macd_line, signal)
    return pd.DataFrame({"MACD": macd_line, "MACD_Signal": macd_signal})


def _bollinger(series: pd.Series, window: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
    """Bollinger Bands (upper, lower) based on a simple moving average."""
    sma = _sma(series, window)
    std = series.rolling(window, min_periods=1).std()
    upper = sma + std_dev * std
    lower = sma - std_dev * std
    return pd.DataFrame({"BB_Upper": upper, "BB_Lower": lower})


def _atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range.
    ``df`` must contain ``High``, ``Low`` and ``Close`` columns.
    """
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.ewm(alpha=1/period, adjust=False).mean()
    return atr


def _vwap(df: pd.DataFrame) -> pd.Series:
    """Volume Weighted Average Price.
    Cumulative (price * volume) / cumulative volume.
    """
    price_vol = (df['Close'] * df['Volume']).cumsum()
    vol_cum = df['Volume'].cumsum()
    return price_vol / vol_cum


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the full set of technical indicators used by the dashboard.

    Parameters
    ----------
    df: pandas.DataFrame
        OHLCV dataframe with a DateTime index.

    Returns
    -------
    pandas.DataFrame
        The original dataframe extended with indicator columns:
        ``SMA20``, ``SMA50``, ``EMA20``, ``RSI``, ``MACD``, ``MACD_Signal``,
        ``BB_Upper``, ``BB_Lower``, ``ATR``, ``VWAP``.
    """
    indicators = df.copy()
    # Simple and exponential moving averages
    indicators['SMA20'] = _sma(indicators['Close'], 20)
    indicators['SMA50'] = _sma(indicators['Close'], 50)
    indicators['EMA20'] = _ema(indicators['Close'], 20)

    # RSI
    indicators['RSI'] = _rsi(indicators['Close'], period=14)

    # MACD
    macd_df = _macd(indicators['Close'])
    indicators['MACD'] = macd_df['MACD']
    indicators['MACD_Signal'] = macd_df['MACD_Signal']

    # Bollinger Bands
    bb_df = _bollinger(indicators['Close'])
    indicators['BB_Upper'] = bb_df['BB_Upper']
    indicators['BB_Lower'] = bb_df['BB_Lower']

    # ATR
    indicators['ATR'] = _atr(indicators)

    # VWAP
    indicators['VWAP'] = _vwap(indicators)

    return indicators
