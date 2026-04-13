import yfinance as yf
import streamlit as st
import pandas as pd
from typing import Dict


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
        tickers = yf.Tickers(" ".join(symbols))
        result = {}
        for name, sym in SECTOR_ETFS.items():
            try:
                info = tickers.tickers[sym].fast_info
                price = getattr(info, "last_price", None)
                prev = getattr(info, "previous_close", None)
                if price and prev:
                    result[name] = {
                        "symbol": sym,
                        "price": price,
                        "change_pct": (price - prev) / prev * 100,
                    }
            except Exception:
                continue
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
        tickers = yf.Tickers(" ".join(all_symbols))
        result = {}
        for category, symbols in MARKET_OVERVIEW.items():
            cat_data = {}
            for sym, name in symbols.items():
                try:
                    info = tickers.tickers[sym].fast_info
                    price = getattr(info, "last_price", None)
                    prev = getattr(info, "previous_close", None)
                    if price and prev:
                        change = price - prev
                        change_pct = (change / prev * 100) if prev else 0
                        cat_data[sym] = {
                            "name": name,
                            "price": price,
                            "change": change,
                            "change_pct": change_pct,
                        }
                except Exception:
                    continue
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
        tickers = yf.Tickers(" ".join(symbols))
        rows = []
        for sym in symbols:
            try:
                info = tickers.tickers[sym].fast_info
                price = getattr(info, "last_price", None)
                prev = getattr(info, "previous_close", None)
                mcap = getattr(info, "market_cap", None)
                if price and prev:
                    rows.append({
                        "symbol": sym,
                        "change_pct": (price - prev) / prev * 100,
                        "market_cap": mcap or 1e9,
                    })
            except Exception:
                continue
        return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()
