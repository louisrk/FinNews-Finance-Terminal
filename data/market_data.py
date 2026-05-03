import yfinance as yf
import streamlit as st
import pandas as pd
from typing import Dict


def _close_df(data: pd.DataFrame, symbols: list) -> pd.DataFrame:
    """Extrahiert Close-Preise aus yf.download()-Ergebnis (single oder multi ticker)."""
    if data.empty:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        # Multi-Ticker: Columns sind (Feld, Ticker)
        level0 = data.columns.get_level_values(0)
        col = "Close" if "Close" in level0 else ("Adj Close" if "Adj Close" in level0 else None)
        if col is None:
            return pd.DataFrame()
        return data[col]
    else:
        # Single Ticker: einfache Spalten
        col = "Close" if "Close" in data.columns else ("Adj Close" if "Adj Close" in data.columns else None)
        if col is None:
            return pd.DataFrame()
        return data[[col]].rename(columns={col: symbols[0]})


# S&P 500 Sektor-ETFs
SECTOR_ETFS = {
    "Technology": "XLK",
    "Financials": "XLF",
    "Healthcare": "XLV",
    "Cons. Discr.": "XLY",
    "Communication": "XLC",
    "Industrials": "XLI",
    "Cons. Staples": "XLP",
    "Energy": "XLE",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Materials": "XLB",
}

# Marktübersicht: Symbole nach Kategorie 
MARKET_OVERVIEW = {
    "US Indices": {
        "^GSPC": "S&P 500",
        "^NDX": "Nasdaq 100",
        "^DJI": "Dow Jones",
        "^RUT": "Russell 2000",
        "^VIX": "VIX",
    },
    "Europe / Asia": {
        "^STOXX50E": "EuroStoxx 50",
        "^FTSE": "FTSE 100",
        "^GDAXI": "DAX 40",
        "^N225": "Nikkei 225",
        "^HSI": "Hang Seng",
    },
    "Crypto": {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "SOL-USD": "Solana",
        "XRP-USD": "XRP",
        "BNB-USD": "BNB",
    },
    "Forex": {
        "EURUSD=X": "EUR/USD",
        "GBPUSD=X": "GBP/USD",
        "USDJPY=X": "USD/JPY",
        "USDCHF=X": "USD/CHF",
        "DX-Y.NYB": "DXY Index",
    },
    "Commodities": {
        "GC=F": "Gold",
        "SI=F": "Silver",
        "CL=F": "WTI Crude",
        "NG=F": "Natural Gas",
        "HG=F": "Copper",
    },
    "Bonds / Rates": {
        "^TNX": "US 10Y Yield",
        "^TYX": "US 30Y Yield",
        "^FVX": "US 5Y Yield",
        "^IRX": "US 3M Yield",
    },
}


@st.cache_data(ttl=60, show_spinner=False)
def fetch_sector_performance() -> Dict[str, Dict]:
    """Sektorperformance via ETFs."""
    symbols = list(SECTOR_ETFS.values())
    try:
        data = yf.download(symbols, period="5d", interval="1d",
                           progress=False, auto_adjust=True)
        close = _close_df(data, symbols)
        if close.empty:
            return {}
        result = {}
        for name, sym in SECTOR_ETFS.items():
            if sym not in close.columns:
                continue
            series = close[sym].dropna()
            if len(series) < 2:
                continue
            price = float(series.iloc[-1])
            prev  = float(series.iloc[-2])
            result[name] = {
                "symbol": sym,
                "price": price,
                "change_pct": (price - prev) / prev * 100,
            }
        return result
    except Exception:
        return {}


@st.cache_data(ttl=60, show_spinner=False)
def fetch_market_overview() -> Dict[str, Dict]:
    """Alle Marktübersichtsdaten abrufen."""
    all_symbols = []
    for cat_syms in MARKET_OVERVIEW.values():
        all_symbols.extend(cat_syms.keys())

    try:
        data = yf.download(all_symbols, period="5d", interval="1d",
                           progress=False, auto_adjust=True)
        close = _close_df(data, all_symbols)
        if close.empty:
            return {}
        result = {}
        for category, symbols in MARKET_OVERVIEW.items():
            cat_data = {}
            for sym, name in symbols.items():
                if sym not in close.columns:
                    continue
                series = close[sym].dropna()
                if len(series) < 2:
                    continue
                price = float(series.iloc[-1])
                prev  = float(series.iloc[-2])
                change = price - prev
                change_pct = (change / prev * 100) if prev else 0
                cat_data[sym] = {
                    "name": name,
                    "price": price,
                    "change": change,
                    "change_pct": change_pct,
                }
            result[category] = cat_data
        return result
    except Exception:
        return {}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_heatmap_data() -> pd.DataFrame:
    """Heatmap-Daten: Top-Aktien nach Marktkapitalisierung."""
    symbols = [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK-B",
        "JPM", "V", "UNH", "MA", "HD", "PG", "JNJ", "XOM", "COST", "ABBV",
        "BAC", "CRM", "AVGO", "AMD", "WMT", "PFE", "KO", "PEP", "MRK",
        "NFLX", "LLY", "TMO", "ADBE", "ORCL", "CSCO", "ACN", "INTC",
    ]
    try:
        data = yf.download(symbols, period="5d", interval="1d",
                           progress=False, auto_adjust=True)
        close = _close_df(data, symbols)
        if close.empty:
            return pd.DataFrame()
        rows = []
        for sym in symbols:
            if sym not in close.columns:
                continue
            series = close[sym].dropna()
            if len(series) < 2:
                continue
            price = float(series.iloc[-1])
            prev  = float(series.iloc[-2])
            rows.append({
                "symbol": sym,
                "change_pct": (price - prev) / prev * 100,
                "market_cap": 1e9,
            })
        return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()
