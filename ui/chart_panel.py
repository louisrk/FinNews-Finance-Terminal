import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data.stock_fetcher import fetch_history, SYMBOL_NAMES, SYMBOL_CATALOG
from data.technical import sma, ema, rsi, macd, bollinger_bands, vwap


# Intervall-Map je Zeitraum
_INTERVAL_MAP = {
    "1d":  ["1m", "2m", "5m", "15m", "30m", "1h"],
    "5d":  ["5m", "15m", "30m", "1h"],
    "1mo": ["30m", "1h", "1d"],
    "3mo": ["1d", "1wk"],
    "6mo": ["1d", "1wk"],
    "1y":  ["1d", "1wk", "1mo"],
    "2y":  ["1d", "1wk", "1mo"],
    "5y":  ["1wk", "1mo"],
    "max": ["1mo", "3mo"],
}

_PERIOD_LABELS = {
    "1d": "1D", "5d": "5D", "1mo": "1M", "3mo": "3M",
    "6mo": "6M", "1y": "1Y", "2y": "2Y", "5y": "5Y", "max": "MAX",
}


def _fmt(price: float, sym: str) -> str:
    if any(x in sym for x in ["=X"]):
        return f"{price:.4f}"
    if price < 1:
        return f"{price:.6f}"
    if price < 100:
        return f"{price:.2f}"
    return f"{price:,.2f}"


def render_chart_panel() -> None:
    """Interaktiver Chart mit technischen Indikatoren."""

    # Controls
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1:
        def _sym_label(s: str) -> str:
            name = SYMBOL_NAMES.get(s, "")
            return f"{s}  ·  {name}" if name else s

        current = st.session_state.get("chart_symbol", "AAPL")
        try:
            idx = SYMBOL_CATALOG.index(current)
        except ValueError:
            idx = SYMBOL_CATALOG.index("AAPL")

        symbol = st.selectbox(
            "SYM", options=SYMBOL_CATALOG, index=idx,
            format_func=_sym_label,
            key="chart_sym_select", label_visibility="collapsed",
            placeholder="Symbol suchen …",
        )
        st.session_state.chart_symbol = symbol
    with c2:
        period = st.selectbox("Period", list(_PERIOD_LABELS.keys()),
                              index=4, format_func=lambda x: _PERIOD_LABELS[x],
                              label_visibility="collapsed")
    with c3:
        intervals = _INTERVAL_MAP.get(period, ["1d"])
        interval = st.selectbox("Interval", intervals, index=0,
                                label_visibility="collapsed")
    with c4:
        chart_type = st.selectbox("Type", ["Candle", "Line", "OHLC"],
                                  label_visibility="collapsed")

    # Indicator Toggles (inline)
    ind = st.session_state.get("indicators", {})
    with st.expander("INDICATORS", expanded=False):
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            st.caption("MOVING AVERAGES")
            ind["sma_20"]  = st.toggle("SMA 20",  value=ind.get("sma_20", True),  key="t_sma20")
            ind["sma_50"]  = st.toggle("SMA 50",  value=ind.get("sma_50", True),  key="t_sma50")
            ind["sma_200"] = st.toggle("SMA 200", value=ind.get("sma_200", False), key="t_sma200")
            ind["ema_12"]  = st.toggle("EMA 12",  value=ind.get("ema_12", False), key="t_ema12")
            ind["ema_26"]  = st.toggle("EMA 26",  value=ind.get("ema_26", False), key="t_ema26")
        with ic2:
            st.caption("OVERLAYS")
            ind["bollinger"] = st.toggle("Bollinger Bands", value=ind.get("bollinger", False), key="t_boll")
            ind["vwap"]      = st.toggle("VWAP",            value=ind.get("vwap", False),      key="t_vwap")
        with ic3:
            st.caption("OSCILLATORS & VOLUME")
            ind["rsi"]    = st.toggle("RSI (14)", value=ind.get("rsi", True),  key="t_rsi")
            ind["macd"]   = st.toggle("MACD",     value=ind.get("macd", False), key="t_macd")
            ind["volume"] = st.toggle("Volume",   value=ind.get("volume", True), key="t_vol")
    st.session_state.indicators = ind

    sym = st.session_state.chart_symbol
    if not sym:
        return

    # Daten laden
    df = fetch_history(sym, period, interval)
    if df.empty:
        st.warning(f"Keine Daten für **{sym}**.")
        return

    ind = st.session_state.get("indicators", {})

    # Sub-Plot-Struktur bestimmen
    rows, heights = [1], [0.55]
    if ind.get("volume"):
        rows.append(len(rows) + 1); heights.append(0.15)
    if ind.get("rsi"):
        rows.append(len(rows) + 1); heights.append(0.15)
    if ind.get("macd"):
        rows.append(len(rows) + 1); heights.append(0.15)

    total = sum(heights)
    heights = [h / total for h in heights]

    fig = make_subplots(
        rows=len(heights), cols=1, shared_xaxes=True,
        vertical_spacing=0.025, row_heights=heights,
    )

    # Hauptchart
    if chart_type == "Candle":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            increasing=dict(line=dict(color="#00cc00"), fillcolor="rgba(0,136,34,0.5)"),
            decreasing=dict(line=dict(color="#cc0000"), fillcolor="rgba(136,0,0,0.5)"),
            name="OHLC",
        ), row=1, col=1)
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"], mode="lines",
            line=dict(color="#ff6600", width=1.5), name="Close",
        ), row=1, col=1)
    else:
        fig.add_trace(go.Ohlc(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            increasing_line_color="#00cc00", decreasing_line_color="#cc0000",
            name="OHLC",
        ), row=1, col=1)

    # Overlays
    overlay_cfg = [
        ("sma_20",  "SMA 20",  lambda: sma(df["Close"], 20),  "#ffaa00", "solid"),
        ("sma_50",  "SMA 50",  lambda: sma(df["Close"], 50),  "#5999ff", "solid"),
        ("sma_200", "SMA 200", lambda: sma(df["Close"], 200), "#ff55ff", "solid"),
        ("ema_12",  "EMA 12",  lambda: ema(df["Close"], 12),  "#00cccc", "dash"),
        ("ema_26",  "EMA 26",  lambda: ema(df["Close"], 26),  "#cc00cc", "dash"),
    ]
    for key, label, fn, color, dash in overlay_cfg:
        if ind.get(key):
            fig.add_trace(go.Scatter(
                x=df.index, y=fn(), mode="lines",
                line=dict(color=color, width=1, dash=dash), name=label,
            ), row=1, col=1)

    if ind.get("bollinger"):
        bb_u, bb_m, bb_l = bollinger_bands(df["Close"])
        fig.add_trace(go.Scatter(x=df.index, y=bb_u, mode="lines",
                                 line=dict(color="#666", width=0.8), name="BB Upper",
                                 showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=bb_l, mode="lines",
                                 line=dict(color="#666", width=0.8), fill="tonexty",
                                 fillcolor="rgba(100,100,100,0.08)", name="Bollinger"),
                      row=1, col=1)

    if ind.get("vwap") and "Volume" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=vwap(df), mode="lines",
                                 line=dict(color="#ff00ff", width=1, dash="dot"),
                                 name="VWAP"), row=1, col=1)

    # Volume
    cur_row = 1
    if ind.get("volume") and "Volume" in df.columns:
        cur_row += 1
        colors = ["rgba(0,204,0,0.6)" if c >= o else "rgba(204,0,0,0.6)"
                  for c, o in zip(df["Close"], df["Open"])]
        fig.add_trace(go.Bar(x=df.index, y=df["Volume"], marker_color=colors,
                             name="Vol", showlegend=False), row=cur_row, col=1)

    # RSI
    if ind.get("rsi"):
        cur_row += 1
        rsi_vals = rsi(df["Close"])
        fig.add_trace(go.Scatter(x=df.index, y=rsi_vals, mode="lines",
                                 line=dict(color="#ffaa00", width=1), name="RSI 14"),
                      row=cur_row, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="#cc0000",
                      line_width=0.5, row=cur_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00cc00",
                      line_width=0.5, row=cur_row, col=1)

    # MACD
    if ind.get("macd"):
        cur_row += 1
        ml, sl, hist = macd(df["Close"])
        hc = ["#00cc00" if v >= 0 else "#cc0000" for v in hist]
        fig.add_trace(go.Bar(x=df.index, y=hist, marker_color=hc,
                             name="Hist", showlegend=False), row=cur_row, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ml, mode="lines",
                                 line=dict(color="#5999ff", width=1), name="MACD"),
                      row=cur_row, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=sl, mode="lines",
                                 line=dict(color="#ff6600", width=1), name="Signal"),
                      row=cur_row, col=1)

    # Layout
    name = SYMBOL_NAMES.get(sym, sym)
    last_p = df["Close"].iloc[-1]
    prev_p = df["Close"].iloc[-2] if len(df) > 1 else last_p
    chg = last_p - prev_p
    chg_pct = (chg / prev_p * 100) if prev_p else 0
    arrow = "+" if chg >= 0 else "-"

    fig.update_layout(
        title=dict(
            text=(f"<span style='color:#ff6600'>{name}</span>  "
                  f"<span style='color:#fff'>{_fmt(last_p, sym)}</span>  "
                  f"<span style='color:{'#00cc00' if chg>=0 else '#cc0000'}'>"
                  f"{arrow} {abs(chg):.2f} ({abs(chg_pct):.2f}%)</span>"),
            font=dict(size=15), x=0,
        ),
        height=680,
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#060606",
        font=dict(family="JetBrains Mono, Consolas, monospace",
                  color="#aaa", size=10),
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,.8)", bordercolor="#333",
                    font=dict(size=9), orientation="h",
                    yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=55, r=15, t=55, b=15),
    )
    fig.update_xaxes(gridcolor="#111", zeroline=False)
    fig.update_yaxes(gridcolor="#111", zeroline=False)

    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": True,
        "modeBarButtonsToAdd": [
            "drawline", "drawopenpath", "drawrect", "eraseshape",
        ],
    })

    # Preis-Infobar
    _render_price_bar(df, sym)


def _render_price_bar(df: pd.DataFrame, sym: str) -> None:
    if df.empty or len(df) < 2:
        return
    last = df.iloc[-1]
    c = st.columns(8)

    def _vol_fmt(v):
        if v >= 1e9: return f"{v/1e9:.2f}B"
        if v >= 1e6: return f"{v/1e6:.1f}M"
        if v >= 1e3: return f"{v/1e3:.0f}K"
        return f"{v:,.0f}"

    with c[0]: st.metric("Open",  _fmt(last["Open"],  sym))
    with c[1]: st.metric("High",  _fmt(last["High"],  sym))
    with c[2]: st.metric("Low",   _fmt(last["Low"],   sym))
    with c[3]: st.metric("Close", _fmt(last["Close"], sym))
    with c[4]:
        if "Volume" in df.columns:
            st.metric("Volume", _vol_fmt(last.get("Volume", 0)))
    with c[5]:
        h52 = df["High"].tail(252).max() if len(df) >= 252 else df["High"].max()
        st.metric("52w Hi", _fmt(h52, sym))
    with c[6]:
        l52 = df["Low"].tail(252).min() if len(df) >= 252 else df["Low"].min()
        st.metric("52w Lo", _fmt(l52, sym))
    with c[7]:
        if "Volume" in df.columns:
            avg = df["Volume"].tail(20).mean()
            st.metric("AvgVol 20", _vol_fmt(avg))
