from typing import Set, List
KEYWORD_TICKER_MAP = {
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – US Tech & Large Cap
    # ─────────────────────────────────────────────────────────────────────────
    "apple": {"AAPL"},
    "iphone": {"AAPL"},
    "tim cook": {"AAPL"},
    "microsoft": {"MSFT"},
    "azure": {"MSFT"},
    "satya nadella": {"MSFT"},
    "windows": {"MSFT"},
    "google": {"GOOGL", "GOOG"},
    "alphabet": {"GOOGL", "GOOG"},
    "android": {"GOOGL", "GOOG"},
    "chromebook": {"GOOGL", "GOOG"},
    "amazon": {"AMZN"},
    "aws": {"AMZN"},
    "andy jassy": {"AMZN"},
    "meta": {"META"},
    "facebook": {"META"},
    "instagram": {"META"},
    "whatsapp": {"META"},
    "mark zuckerberg": {"META"},
    "tesla": {"TSLA"},
    "elon musk": {"TSLA"},
    "nvdia": {"NVDA"},
    "nvidia": {"NVDA"},
    "jensen huang": {"NVDA"},
    "cuda": {"NVDA"},
    "intel": {"INTC"},
    "amd": {"AMD"},
    "ibm": {"IBM"},
    "oracle": {"ORCL"},
    "salesforce": {"CRM"},
    "adobe": {"ADBE"},
    "netflix": {"NFLX"},
    "disney": {"DIS"},
    "warner bros": {"WBD"},
    "paramount": {"PARA"},
    "nokia": {"NOK"},
    "qualcomm": {"QCOM"},
    "broadcom": {"AVGO"},
    "cisco": {"CSCO"},
    "dell": {"DELL"},
    "hp": {"HPQ"},
    "ebay": {"EBAY"},
    "paypal": {"PYPL"},
    "square": {"SQ"},
    "block": {"SQ"},
    "uber": {"UBER"},
    "lyft": {"LYFT"},
    "airbnb": {"ABNB"},
    "zoom": {"ZM"},
    "slack": {"SLACK"},
    "crowdstrike": {"CRWD"},
    "crowdstrike holdings": {"CRWD"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – Finance & Banking
    # ─────────────────────────────────────────────────────────────────────────
    "jpmorgan": {"JPM"},
    "goldman sachs": {"GS"},
    "morgan stanley": {"MS"},
    "bank of america": {"BAC"},
    "bofa": {"BAC"},
    "wells fargo": {"WFC"},
    "citigroup": {"C"},
    "american express": {"AXP"},
    "berkshire": {"BRK.B"},
    "buffett": {"BRK.B"},
    "blackrock": {"BLK"},
    "vanguard": {"BLK"},
    "charles schwab": {"SCHW"},
    "e-trade": {"SCHW"},
    "robinhood": {"HOOD"},
    "coinbase": {"COIN"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – Healthcare
    # ─────────────────────────────────────────────────────────────────────────
    "pfizer": {"PFE"},
    "moderna": {"MRNA"},
    "johnson & johnson": {"JNJ"},
    "j&j": {"JNJ"},
    "merck": {"MRK"},
    "bristol-myers": {"BMY"},
    "eli lilly": {"LLY"},
    "novo nordisk": {"NVO"},
    "ozempic": {"NVO"},
    "roche": {"RHHBY"},
    "novartis": {"NVS"},
    "astrazeneca": {"AZN"},
    "glaxosmithkline": {"GSK"},
    "regeneron": {"REGN"},
    "vertex": {"VRTX"},
    "incyte": {"INCY"},
    "amgen": {"AMGN"},
    "gilead": {"GILD"},
    "biogen": {"BIIB"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – Energy
    # ─────────────────────────────────────────────────────────────────────────
    "exxonmobil": {"XOM"},
    "exxon": {"XOM"},
    "chevron": {"CVX"},
    "shell": {"SHEL"},
    "bp": {"BP"},
    "total energies": {"TTE"},
    "conocophillips": {"COP"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – Automotive
    # ─────────────────────────────────────────────────────────────────────────
    "ford": {"F"},
    "general motors": {"GM"},
    "toyota": {"TM"},
    "volkswagen": {"VWAGY"},
    "bmw": {"BMWYY"},
    "mercedes": {"DDAIF"},
    "porsche": {"POAHY"},
    "rivian": {"RIVN"},
    "lucid": {"LCID"},
    "nio": {"NIO"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # EQUITIES – Consumer & Retail
    # ─────────────────────────────────────────────────────────────────────────
    "walmart": {"WMT"},
    "target": {"TGT"},
    "costco": {"COST"},
    "nike": {"NKE"},
    "adidas": {"ADDYY"},
    "puma": {"PUMPY"},
    "starbucks": {"SBUX"},
    "chipotle": {"CMG"},
    "mcdonalds": {"MCD"},
    "mcdonald's": {"MCD"},
    "dominino's": {"DPZ"},
    "pizza hut": {"YUM"},
    "kfc": {"YUM"},
    "yum brands": {"YUM"},
    "general mills": {"GIS"},
    "kroger": {"KR"},
    "whole foods": {"WFM"},
    "gap": {"GPS"},
    "lululemon": {"LULU"},
    "lvmh": {"LVMHF"},
    "ferrari": {"RACE"},
    "gucci": {"EOAN"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # INDEXES & ETFs
    # ─────────────────────────────────────────────────────────────────────────
    "s&p 500": {"SPY"},
    "sp500": {"SPY"},
    "sp 500": {"SPY"},
    "nasdaq": {"QQQ"},
    "nasdaq-100": {"QQQ"},
    "dow jones": {"DIA"},
    "ftse": {"EWU"},
    "dax": {"EWG"},
    "cac": {"EWQ"},
    "nikkei": {"EWJ"},
    "hang seng": {"EWH"},
    "sse": {"EWH"},
    "composite": {"EWH"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMMODITIES – Oil & Gas
    # ─────────────────────────────────────────────────────────────────────────
    "wti": {"CL=F"},
    "brent": {"BZ=F"},
    "crude oil": {"CL=F"},
    "oil barrel": {"CL=F"},
    "opec": {"CL=F"},
    "petroleum": {"CL=F"},
    "gasoline": {"RB=F"},
    "natural gas": {"NG=F"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMMODITIES – Precious Metals
    # ─────────────────────────────────────────────────────────────────────────
    "gold": {"GC=F"},
    "silver": {"SI=F"},
    "platinum": {"PL=F"},
    "palladium": {"PA=F"},
    "copper": {"HG=F"},
    "uranium": {"UUU=F"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMMODITIES – Agriculture
    # ─────────────────────────────────────────────────────────────────────────
    "wheat": {"ZWZ"},
    "corn": {"ZCZ"},
    "soybeans": {"ZSZ"},
    "cocoa": {"CCZ"},
    "coffee": {"KCZ"},
    "sugar": {"SBZ"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # CRYPTO
    # ─────────────────────────────────────────────────────────────────────────
    "bitcoin": {"BTC-USD"},
    "btc": {"BTC-USD"},
    "ethereum": {"ETH-USD"},
    "eth": {"ETH-USD"},
    "cardano": {"ADA-USD"},
    "ada": {"ADA-USD"},
    "solana": {"SOL-USD"},
    "sol": {"SOL-USD"},
    "ripple": {"XRP-USD"},
    "xrp": {"XRP-USD"},
    "dogecoin": {"DOGE-USD"},
    "doge": {"DOGE-USD"},
    "litecoin": {"LTC-USD"},
    "ltc": {"LTC-USD"},
    "monero": {"XMR-USD"},
    "polkadot": {"DOT-USD"},
    "chainlink": {"LINK-USD"},
    "uniswap": {"UNI-USD"},
    "aave": {"AAVE-USD"},
    "compound": {"COMP-USD"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # FOREX – Major Pairs
    # ─────────────────────────────────────────────────────────────────────────
    "eurusd": {"EURUSD=X"},
    "eur/usd": {"EURUSD=X"},
    "gbpusd": {"GBPUSD=X"},
    "gbp/usd": {"GBPUSD=X"},
    "usdjpy": {"USDJPY=X"},
    "usd/jpy": {"USDJPY=X"},
    "audusd": {"AUDUSD=X"},
    "aud/usd": {"AUDUSD=X"},
    "usdcad": {"USDCAD=X"},
    "usd/cad": {"USDCAD=X"},
    "usdchf": {"USDCHF=X"},
    "usd/chf": {"USDCHF=X"},
    "nzdusd": {"NZDUSD=X"},
    "nzd/usd": {"NZDUSD=X"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # BONDS & Fixed Income
    # ─────────────────────────────────────────────────────────────────────────
    "treasury": {"TNX"},
    "treasurie": {"TNX"},
    "fed": {"TNX"},
    "interest rate": {"TNX"},
    "rates": {"TNX"},
    "yield": {"TNX"},
    "10-year": {"TNX"},
    "bonds": {"TNX", "BND"},
    "tlt": {"TLT"},
    "ief": {"IEF"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # VOLATILITY & VIX
    # ─────────────────────────────────────────────────────────────────────────
    "vix": {"^VIX"},
    "volatility": {"^VIX"},
    "fear index": {"^VIX"},
    "vvix": {"^VVIX"},
    
    # ─────────────────────────────────────────────────────────────────────────
    # Economic Themes / Keywords (mehrere Ticker relevant)
    # ─────────────────────────────────────────────────────────────────────────
    "iran": {"CL=F", "^VIX"},
    "israel": {"CL=F", "^VIX"},
    "conflict": {"CL=F", "^VIX"},
    "war": {"CL=F", "^VIX"},
    "russia": {"CL=F", "^VIX"},
    "ukraine": {"CL=F", "^VIX"},
    "sanctions": {"CL=F"},
    "brexit": {"GBPUSD=X"},
    "recession": {"^VIX", "TLT"},
    "inflation": {"TNX", "EURUSD=X"},
    "deflation": {"TNX"},
    "powell": {"TNX", "^VIX"},
    "lagarde": {"EURUSD=X"},
    "cnbc": {"SPY"},  # Often covers market indices
    "earnings": {"SPY", "QQQ"},
    "earnings season": {"SPY", "QQQ"},
    "earnings miss": {"^VIX"},
    "earnings beat": {"SPY"},
    "guidance": {"SPY", "QQQ"},
    "dividend": {"SPY"},
    "ipo": {"RBLX", "SNOW"},
    "merger": {"^VIX"},
    "acquisition": {"^VIX"},
    "bankruptcy": {"^VIX"},
    "default": {"TNX"},
}

def detect_assets(text: str) -> Set[str]:
    if not text:
        return set()
    
    text_lower = text.lower()
    detected_tickers: Set[str] = set()
    for keyword, tickers in KEYWORD_TICKER_MAP.items():
        if keyword in text_lower:
            detected_tickers.update(tickers)
    if len(detected_tickers) > 3:
        return set(list(detected_tickers)[:3])
    return detected_tickers


def tradingview_url_for_ticker(ticker: str) -> str:
    """Erstellt einen TradingView-Link für ein yfinance-Ticker-Symbol."""
    if ticker.endswith("=X"):
        # Beispiel EURUSD=X -> EURUSD
        symbol = ticker.replace("=X", "")
    else:
        symbol = ticker

    # ETF/Index-Kürzel konvertieren, falls nötig (z.B. ^VIX aktuell nicht direkt von TradingView unterstützt)
    special = {
        "^VIX": "CBOE:VIX",
        "^TNX": "CBOE:TNX",
        "GC=F": "COMEX:GC1!",
        "CL=F": "NYMEX:CL1!",
        "BZ=F": "ICEBRENT:1!",
        "SI=F": "COMEX:SI1!",
        "NZDUSD=X": "FX:NZDUSD",
        "EURUSD=X": "FX:EURUSD",
        "GBPUSD=X": "FX:GBPUSD",
        "USDJPY=X": "FX:USDJPY",
    }

    if ticker in special:
        return f"https://www.tradingview.com/symbols/{special[ticker]}/"

    # Standard -> US-Aktien: NASDAQ/NYSE
    # Wenn es ein US-Aktien-Ticker ist (A-Z, optional .), in der Regel NASDAQ
    if symbol.isalnum() or "." in symbol:
        return f"https://www.tradingview.com/symbols/{symbol.upper()}/"

    return f"https://www.tradingview.com/markets/"  # Fallback


def format_ticker_buttons(tickers: Set[str]) -> str:
    """
    Formatiert Ticker als Links für die Anzeige.
    
    Args:
        tickers: Set von Ticker-Symbolen
        
    Returns:
        HTML-String mit Link-Buttons
    """
    if not tickers:
        return ""

    buttons_html = '<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">'
    for ticker in sorted(tickers):
        tv_url = tradingview_url_for_ticker(ticker)
        yf_url = f'https://finance.yahoo.com/quote/{ticker.replace("=X", "")}'

        buttons_html += (
            f'<a href="{tv_url}" target="_blank" '
            f'style="background:#1e2d4a;color:#60a5fa;padding:4px 10px;border-radius:4px;font-size:11px;font-weight:600;border:1px solid #3b82f6;text-decoration:none;">'
            f' {ticker}</a>'
        )
        buttons_html += (
            f'<a href="{yf_url}" target="_blank" '
            f'style="background:#0d1225;color:#a5f3fc;padding:4px 10px;border-radius:4px;font-size:11px;font-weight:500;border:1px solid #06b6d4;text-decoration:none;">'
            f' YF</a>'
        )
    buttons_html += '</div>'

    return buttons_html
