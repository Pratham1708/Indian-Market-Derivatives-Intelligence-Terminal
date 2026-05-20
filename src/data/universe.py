# src/data/universe.py
"""Universe Engine for Phase 2.
Provides functions to get symbols for NIFTY 50, NIFTY 100, and sectors.
Includes robust fallbacks.
"""

from typing import List, Dict
import pandas as pd
import yfinance as yf

# Hardcoded NIFTY 50 fallback list (reliable and fast)
NIFTY_50_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "HCLTECH.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "JSWSTEEL.NS",
    "TATASTEEL.NS", "NTPC.NS", "POWERGRID.NS", "M&M.NS", "LTIM.NS",
    "ADANIENT.NS", "ADANIPORTS.NS", "ONGC.NS", "COALINDIA.NS", "ITC.NS",
    "GRASIM.NS", "HINDALCO.NS", "TATAMOTORS.NS", "INDUSINDBK.NS", "SBILIFE.NS",
    "DRREDDY.NS", "CIPLA.NS", "WIPRO.NS", "HDFCLIFE.NS", "NESTLEIND.NS",
    "TECHM.NS", "BAJAJFINSV.NS", "HINDUNILVR.NS", "BRITANNIA.NS", "EICHERMOT.NS",
    "HEROMOTOCO.NS", "APOLLOHOSP.NS", "BAJAJ-AUTO.NS", "DIVISLAB.NS", "BPCL.NS"
]

# Basic Sector Mapping for NIFTY 50
SECTOR_MAPPING = {
    "Financial Services": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "INDUSINDBK.NS", "SBILIFE.NS", "HDFCLIFE.NS"],
    "Information Technology": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"],
    "Oil & Gas": ["RELIANCE.NS", "ONGC.NS", "BPCL.NS"],
    "FMCG": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
    "Automobile": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS"],
    "Healthcare": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "APOLLOHOSP.NS", "DIVISLAB.NS"],
    "Metals & Mining": ["JSWSTEEL.NS", "TATASTEEL.NS", "HINDALCO.NS", "COALINDIA.NS"],
    "Construction": ["LT.NS"],
    "Consumer Durables": ["ASIANPAINT.NS", "TITAN.NS"],
    "Cement": ["ULTRACEMCO.NS", "GRASIM.NS"],
    "Power": ["NTPC.NS", "POWERGRID.NS"],
    "Diversified": ["ADANIENT.NS"],
    "Services": ["ADANIPORTS.NS"]
}

def get_nifty50_symbols() -> List[str]:
    """Return the list of NIFTY 50 stock tickers."""
    # In a full implementation, this could fetch from NSE CSV.
    # For now, return the reliable hardcoded list.
    return NIFTY_50_STOCKS

def get_nifty100_symbols() -> List[str]:
    """Return the list of NIFTY 100 stock tickers (mocked for now)."""
    # Fallback: return NIFTY 50 + some other liquid stocks to simulate 100
    additional_stocks = [
        "DMART.NS", "PIDILITIND.NS", "SIEMENS.NS", "GODREJCP.NS", "DABUR.NS",
        "DLF.NS", "VBL.NS", "BEL.NS", "HAVELLS.NS", "SRF.NS",
        "GAIL.NS", "IOC.NS", "AMBUJACEM.NS", "ACC.NS", "ICICIPRULI.NS"
    ]
    return list(set(NIFTY_50_STOCKS + additional_stocks))

def get_sector_symbols(sector_name: str) -> List[str]:
    """Return the list of stock tickers for a given sector."""
    return SECTOR_MAPPING.get(sector_name, [])

def get_all_sectors() -> List[str]:
    """Return a list of all sector names."""
    return list(SECTOR_MAPPING.keys())

def get_stock_sector(ticker: str) -> str:
    """Return the sector name for a given ticker."""
    for sector, tickers in SECTOR_MAPPING.items():
        if ticker in tickers:
            return sector
    return "Unknown"
