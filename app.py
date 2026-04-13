import streamlit as st
from datetime import datetime, timezone

from data.news_fetcher import fetch_all_news, CATEGORIES
from data.stock_fetcher import fetch_quotes, SYMBOL_NAMES, DEFAULT_SYMBOLS
from ui.ticker_bar import render_ticker_bar
from ui.news_panel import render_news_panel
from ui.chart_panel import render_chart_panel
from ui.market_overview import render_market_overview
from ui.geo_panel import render_geo_panel

# Page Config
st.set_page_config(
    page_title="FinNews Terminal",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Bloomberg Terminal CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

/* ── Global ─────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000 !important;
    color: #ccc;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
}
[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stHeader"] { background: #000 !important; }
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
.block-container { padding-top: .4rem !important; padding-bottom: 0 !important; }

/* ── Hide Streamlit chrome ──────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ──────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#000; }
::-webkit-scrollbar-thumb { background:#333; border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:#555; }

/* ── Bloomberg Section Headers ──────────────────────────────────────────── */
.bb-section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 700;
    letter-spacing: .18em; text-transform: uppercase;
    color: #ff6600; padding: 5px 0;
    border-bottom: 1px solid #333; margin-bottom: 8px;
}

/* ── Market Grid ────────────────────────────────────────────────────────── */
.market-grid { display:grid; grid-template-columns:1fr; gap:3px; }
.market-cell {
    display:flex; justify-content:space-between; align-items:center;
    padding:5px 8px; background:#060606; border:1px solid #111;
    font-family:'JetBrains Mono',monospace; font-size:11px;
    transition: border-color .15s;
}
.market-cell:hover { border-color:#ff6600; background:#0a0a0a; }
.market-cell-name { color:#ffaa00; font-weight:600; min-width:90px; }
.market-cell-price { color:#fff; font-weight:500; margin:0 10px; }

/* ── Tabs ───────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background:#000; border-bottom:2px solid #333; gap:0;
}
.stTabs [data-baseweb="tab"] {
    background:transparent; color:#555;
    font-family:'JetBrains Mono',monospace;
    font-size:11px; font-weight:700;
    letter-spacing:.12em; text-transform:uppercase;
    padding:9px 18px; border:none; border-radius:0;
}
.stTabs [aria-selected="true"] {
    background:#111 !important; color:#ff6600 !important;
    border-bottom:2px solid #ff6600 !important;
}

/* ── News Cards ─────────────────────────────────────────────────────────── */
.news-card {
    background:#050505; border:1px solid #161616;
    border-left:3px solid #222; border-radius:0;
    padding:9px 11px; margin-bottom:5px;
    font-family:'JetBrains Mono',monospace;
    transition: border-color .15s;
}
.news-card:hover { border-left-color:#ff6600; background:#0a0a0a; }
.news-source {
    font-size:9px; font-weight:700; letter-spacing:.15em;
    text-transform:uppercase; color:#ff6600; margin-bottom:2px;
}
.news-title { font-size:12px; font-weight:500; color:#ddd; line-height:1.3; margin-bottom:3px; }
.news-title a { color:inherit; text-decoration:none; }
.news-title a:hover { color:#ffaa00; }
.news-meta { font-size:9px; color:#444; display:flex; gap:8px; }
.news-summary {
    font-size:10px; color:#666; line-height:1.4; margin-top:3px;
    border-top:1px solid #161616; padding-top:3px;
}
.badge-new {
    background:#ff6600; color:#000;
    font-size:8px; font-weight:700; letter-spacing:.1em;
    padding:1px 4px; border-radius:1px; text-transform:uppercase;
}

/* ── Watchlist Table ────────────────────────────────────────────────────── */
.wl-table {
    width:100%; border-collapse:collapse;
    font-family:'JetBrains Mono',monospace; font-size:11px;
}
.wl-table th {
    background:#060606; color:#ff6600;
    font-size:9px; font-weight:700; letter-spacing:.15em;
    text-transform:uppercase; padding:7px 10px; text-align:left;
    border-bottom:2px solid #ff6600;
}
.wl-table td {
    padding:5px 10px; border-bottom:1px solid #111; color:#bbb;
}
.wl-table tr:hover { background:#0a0a0a; }

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button {
    background:#111 !important; color:#ff6600 !important;
    border:1px solid #ff6600 !important; border-radius:0 !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:10px !important; font-weight:600 !important;
    letter-spacing:.1em; text-transform:uppercase;
}
.stButton > button:hover {
    background:#ff6600 !important; color:#000 !important;
}

/* ── Inputs ─────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background:#060606 !important; color:#ff6600 !important;
    border:1px solid #333 !important; border-radius:0 !important;
    font-family:'JetBrains Mono',monospace !important; font-size:12px !important;
}
.stSelectbox > div > div {
    background:#060606 !important; border:1px solid #333 !important;
    border-radius:0 !important;
}

/* ── Metrics ────────────────────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family:'JetBrains Mono',monospace !important;
    color:#fff !important; font-size:13px !important;
}
[data-testid="stMetricLabel"] {
    font-family:'JetBrains Mono',monospace !important;
    color:#555 !important; font-size:9px !important;
    text-transform:uppercase; letter-spacing:.1em;
}

/* ── Expander ───────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background:#060606 !important; color:#ffaa00 !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important;
}

/* ── Checkbox ───────────────────────────────────────────────────────────── */
.stCheckbox label {
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important; color:#bbb !important;
}

/* ── Divider ────────────────────────────────────────────────────────────── */
hr { border-color:#222 !important; }

/* ── Status Bar ─────────────────────────────────────────────────────────── */
.status-bar {
    background:#000; border-top:1px solid #222;
    padding:3px 10px; font-family:'JetBrains Mono',monospace;
    font-size:9px; color:#444; display:flex;
    justify-content:space-between; align-items:center;
}
.status-dot {
    display:inline-block; width:5px; height:5px;
    border-radius:50%; background:#00cc00; margin-right:5px;
    animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

/* ── Hide Streamlit "Bearbeiten" / Edit buttons on widgets ──────────────── */
[data-testid="stBaseButton-elementToolbar"],
button[kind="elementToolbar"],
.element-toolbar,
[data-testid="stElementToolbar"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

# Session State
_DEFAULTS = {
    "news_data": {},
    "quotes_data": {},
    "watchlist": [
        "SPY", "QQQ", "BTC-USD", "ETH-USD", "GC=F", "CL=F",
        "EURUSD=X", "^VIX", "^TNX", "AAPL", "MSFT", "NVDA",
    ],
    "chart_symbol": "AAPL",
    "indicators": {
        "sma_20": True, "sma_50": True, "sma_200": False,
        "ema_12": False, "ema_26": False,
        "bollinger": False, "volume": True,
        "rsi": True, "macd": False, "vwap": False,
    },
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Data Loading
st.session_state.news_data   = fetch_all_news()
st.session_state.quotes_data = fetch_quotes(st.session_state.watchlist)

# Ticker Bar
render_ticker_bar(st.session_state.quotes_data)

# Header
h1, h2, h3 = st.columns([4, 3, 1])
with h1:
    st.markdown(
        '<span style="font-family:JetBrains Mono,monospace;font-size:22px;'
        'font-weight:700;color:#ff6600;letter-spacing:.18em">FINNEWS TERMINAL</span>',
        unsafe_allow_html=True,
    )
with h2:
    now = datetime.now(timezone.utc).strftime("%d %b %Y  %H:%M UTC")
    st.markdown(
        f'<div style="padding-top:6px;font-size:10px;color:#444;'
        f'font-family:JetBrains Mono,monospace;letter-spacing:.08em">'
        f'<span class="status-dot"></span> LIVE  ·  {now}  ·  '
        f'News 2min  ·  Kurse 30s</div>',
        unsafe_allow_html=True,
    )
with h3:
    if st.button("REFRESH", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Main Tabs
tab_markets, tab_chart, tab_news, tab_geo, tab_wl = st.tabs([
    "MARKETS", "CHART", "NEWS", "GEO RADAR", "WATCHLIST",
])

# Markets 
with tab_markets:
    render_market_overview()

# Chart 
with tab_chart:
    render_chart_panel()

# News
with tab_news:
    render_news_panel(st.session_state.news_data)

# Geo Radar
with tab_geo:
    render_geo_panel()

# Watchlist
with tab_wl:
    # Preset-Buttons + Manual Edit
    wl1, wl2, wl3, wl4, wl5 = st.columns([1, 1, 1, 1, 2])
    if wl1.button("US Focus", use_container_width=True):
        st.session_state.watchlist = (
            DEFAULT_SYMBOLS["Indexes"][:4]
            + DEFAULT_SYMBOLS["Equities"][:5]
            + DEFAULT_SYMBOLS["Crypto"][:2]
        )
        st.rerun()
    if wl2.button("Crypto", use_container_width=True):
        st.session_state.watchlist = (
            DEFAULT_SYMBOLS["Crypto"]
            + DEFAULT_SYMBOLS["Indexes"][:3]
        )
        st.rerun()
    if wl3.button("FX & Comm", use_container_width=True):
        st.session_state.watchlist = (
            DEFAULT_SYMBOLS["Forex"]
            + DEFAULT_SYMBOLS["Commodities"]
        )
        st.rerun()
    if wl4.button("Alle", use_container_width=True):
        all_s = []
        for s in DEFAULT_SYMBOLS.values():
            all_s.extend(s)
        st.session_state.watchlist = list(dict.fromkeys(all_s))
        st.rerun()
    with wl5:
        with st.popover("Manuell", use_container_width=True):
            raw = st.text_area(
                "symbols_edit",
                value="\n".join(st.session_state.watchlist),
                height=200,
                label_visibility="collapsed",
            )
            if st.button("APPLY", use_container_width=True, key="btn_apply_wl"):
                st.session_state.watchlist = [
                    s.strip().upper() for s in raw.splitlines() if s.strip()
                ]
                st.rerun()

    # Watchlist Table
    _quotes = st.session_state.quotes_data
    if not _quotes:
        st.info("Lade Watchlist …")
    else:
        def _wl_fmt(p, s):
            if "=X" in s: return f"{p:.4f}"
            if p < 1:     return f"{p:.6f}"
            if p < 100:   return f"{p:.2f}"
            return f"{p:,.2f}"

        html = ('<table class="wl-table"><thead><tr>'
                '<th>SYMBOL</th><th>NAME</th><th>PRICE</th>'
                '<th>CHG</th><th>CHG %</th>'
                '</tr></thead><tbody>')
        for sym, q in _quotes.items():
            c = "#00cc00" if q["change_pct"] >= 0 else "#cc0000"
            a = "+" if q["change_pct"] >= 0 else "-"
            html += (
                f'<tr>'
                f'<td style="color:#ff6600;font-weight:600">{sym}</td>'
                f'<td>{q["name"]}</td>'
                f'<td style="color:#fff">{_wl_fmt(q["price"], sym)}</td>'
                f'<td style="color:{c}">{q["change"]:+.2f}</td>'
                f'<td style="color:{c}">{a} {abs(q["change_pct"]):.2f}%</td>'
                f'</tr>'
            )
        html += '</tbody></table>'
        st.markdown(html, unsafe_allow_html=True)

# Status Bar
st.markdown(
    f'<div class="status-bar">'
    f'<span><span class="status-dot"></span>Connected  ·  '
    f'{len(st.session_state.watchlist)} symbols  ·  '
    f'{sum(len(v) for v in st.session_state.news_data.values())} news items</span>'
    f'<span>FinNews Terminal v2.0  ·  Daten: Yahoo Finance + RSS</span>'
    f'</div>',
    unsafe_allow_html=True,
)
