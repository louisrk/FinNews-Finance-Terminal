import feedparser
import streamlit as st
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List

# Kategorien
CATEGORIES = ["Alle", "Bonds", "Commodities", "Crypto", "Equities", "Forex", "Indexes", "Macro"]

# RSS Feed-Quellen pro Kategorie
FEEDS: Dict[str, List[Dict]] = {

    "Macro": [
        {"name": "Reuters Business",    "url": "https://feeds.reuters.com/reuters/businessNews"},
        {"name": "FT Markets",          "url": "https://www.ft.com/markets?format=rss"},
        {"name": "WSJ Economy",         "url": "https://feeds.content.dowjones.io/public/rss/mw_economy"},
        {"name": "MarketWatch Economy", "url": "https://feeds.content.dowjones.io/public/rss/mw_realestate"},
        {"name": "Investing.com Macro", "url": "https://www.investing.com/rss/news_14.rss"},
        {"name": "ECB News",            "url": "https://www.ecb.europa.eu/rss/press.html"},
    ],

    "Equities": [
        {"name": "Reuters Stocks",      "url": "https://feeds.reuters.com/reuters/companyNews"},
        {"name": "Seeking Alpha",       "url": "https://seekingalpha.com/feed.xml"},
        {"name": "MarketWatch Stocks",  "url": "https://feeds.content.dowjones.io/public/rss/mw_topstories"},
        {"name": "Investing.com Stocks","url": "https://www.investing.com/rss/news_25.rss"},
        {"name": "Yahoo Finance",       "url": "https://finance.yahoo.com/news/rssindex"},
    ],

    "Crypto": [
        {"name": "CoinDesk",            "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
        {"name": "CoinTelegraph",       "url": "https://cointelegraph.com/rss"},
        {"name": "The Block",           "url": "https://www.theblock.co/rss.xml"},
        {"name": "Bitcoin Magazine",    "url": "https://bitcoinmagazine.com/.rss/full/"},
        {"name": "Decrypt",             "url": "https://decrypt.co/feed"},
    ],

    "Forex": [
        {"name": "FXStreet",            "url": "https://www.fxstreet.com/rss/news"},
        {"name": "DailyFX",             "url": "https://www.dailyfx.com/feeds/all"},
        {"name": "Investing.com Forex", "url": "https://www.investing.com/rss/news_1.rss"},
        {"name": "ForexLive",           "url": "https://www.forexlive.com/feed/news"},
    ],

    "Commodities": [
        {"name": "Reuters Commodities", "url": "https://feeds.reuters.com/reuters/commoditiesNews"},
        {"name": "Kitco Gold",          "url": "https://www.kitco.com/rss/rss-feeds-for-kitconews.xml"},
        {"name": "Oil Price",           "url": "https://oilprice.com/rss/main"},
        {"name": "Investing.com Comm.", "url": "https://www.investing.com/rss/news_8.rss"},
    ],

    "Bonds": [
        {"name": "Reuters Bonds",       "url": "https://feeds.reuters.com/reuters/governmentDebtNews"},
        {"name": "Investing.com Bonds", "url": "https://www.investing.com/rss/news_95.rss"},
        {"name": "MarketWatch Bonds",   "url": "https://feeds.content.dowjones.io/public/rss/mw_bonds"},
        {"name": "WSJ Bonds",           "url": "https://feeds.content.dowjones.io/public/rss/mw_govdebt"},
    ],

    "Indexes": [
        {"name": "Reuters Markets",     "url": "https://feeds.reuters.com/reuters/marketsNews"},
        {"name": "MarketWatch Markets", "url": "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"},
        {"name": "Investing.com Index", "url": "https://www.investing.com/rss/news_11.rss"},
        {"name": "CNBC Markets",        "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"},
    ],
}

# Hilfsfunktion: Zeitstempel parsen
def _parse_time(entry) -> datetime:
    for attr in ("published", "updated"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return parsedate_to_datetime(val).astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                pass
    return datetime.utcnow()

# Einzelnen Feed laden
def _fetch_feed(source: Dict, max_items: int = 15) -> List[Dict]:
    try:
        feed = feedparser.parse(source["url"])
        items = []
        for entry in feed.entries[:max_items]:
            title   = entry.get("title", "").strip()
            link    = entry.get("link",  "")
            summary = entry.get("summary", entry.get("description", ""))
            
            import re
            summary = re.sub(r"<[^>]+>", "", summary)[:280].strip()

            if title:
                items.append({
                    "title":   title,
                    "link":    link,
                    "summary": summary,
                    "source":  source["name"],
                    "time":    _parse_time(entry),
                })
        return items
    except Exception:
        return []

# Alle Feeds laden (gecacht) 
@st.cache_data(ttl=120, show_spinner=False)   # 2 Minuten Cache
def fetch_all_news() -> Dict[str, List[Dict]]:
    """Lädt alle RSS-Feeds und gibt sie nach Kategorie sortiert zurück."""
    result: Dict[str, List[Dict]] = {cat: [] for cat in CATEGORIES if cat != "Alle"}

    for category, sources in FEEDS.items():
        all_items = []
        for source in sources:
            all_items.extend(_fetch_feed(source))
        # Nach Zeit sortieren – neueste zuerst
        all_items.sort(key=lambda x: x["time"], reverse=True)
        result[category] = all_items

    return result
