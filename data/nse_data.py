# data/nse_data.py
"""Data layer for Indian stock OHLCV using yfinance (fallback to nsepy).
Provides functions for current price, historical OHLCV data, and ticker autocomplete.
"""
import json
import os
from typing import List
import pandas as pd
import yfinance as yf

# Load a small symbol list for autocomplete fallback
_SYMBOLS_PATH = os.path.join(os.path.dirname(__file__), "symbols.json")
if os.path.exists(_SYMBOLS_PATH):
    with open(_SYMBOLS_PATH, "r", encoding="utf-8") as f:
        _ALL_SYMBOLS = json.load(f)  # dict mapping ticker -> name
else:
    _ALL_SYMBOLS = {}


def get_symbol_suggestions(query: str, limit: int = 10) -> List[str]:
    """Return a list of ticker suggestions that match query on either ticker or company name.
    Matching is case-insensitive.
    Suggestions are returned in format: "TICKER - Company Name".
    """
    if not query:
        return []
    query = query.upper()
    matches = []
    
    # First pass: search exact starts-with on ticker to prioritize direct ticker search
    for ticker, name in _ALL_SYMBOLS.items():
        if ticker.upper().startswith(query):
            matches.append(f"{ticker} - {name}")
            
    # Second pass: search starts-with or contains on company name or contains on ticker
    for ticker, name in _ALL_SYMBOLS.items():
        formatted = f"{ticker} - {name}"
        if formatted in matches:
            continue
        if query in name.upper() or query in ticker.upper():
            matches.append(formatted)
            
    return matches[:limit]


def get_current_price(ticker: str) -> float:
    """Fetch the latest market price for the given Indian ticker.
    Uses yfinance to retrieve the most recent close price.
    """
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.history(period="1d")
    if data.empty:
        raise ValueError(f"No price data found for ticker {ticker}")
    # Use the last close price (could be NaN for intraday, fallback to last available)
    price = data["Close"].iloc[-1]
    return float(price)


def get_historical_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Return OHLCV historical data for the ticker.
    `period` follows yfinance conventions (e.g., "1mo", "3mo", "6mo", "1y", "2y").
    The returned DataFrame has columns: Open, High, Low, Close, Volume, and a DatetimeIndex.
    """
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=period)
    if hist.empty:
        raise ValueError(f"No historical data for ticker {ticker} with period {period}")
    # Ensure proper column names
    hist = hist.rename(columns={"Open": "Open", "High": "High", "Low": "Low", "Close": "Close", "Volume": "Volume"})
    return hist[["Open", "High", "Low", "Close", "Volume"]]
