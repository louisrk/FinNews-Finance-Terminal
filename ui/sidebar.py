import streamlit as st
from data.stock_fetcher import DEFAULT_SYMBOLS


def render_sidebar() -> None:
    with st.sidebar:
        # Header
        st.markdown(
            '<div style="font-family:JetBrains Mono,monospace;font-size:22px;'
            'font-weight:700;color:#ff6600;letter-spacing:.2em">FINNEWS</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:9px;color:#555;letter-spacing:.12em;'
            'text-transform:uppercase;margin-bottom:12px">'
            'Real-Time Finance Terminal</div>',
            unsafe_allow_html=True,
        )
        st.divider()

        # Watchlist
        st.markdown("**⌨ WATCHLIST**")
        c1, c2 = st.columns(2)
        if c1.button("US Focus", use_container_width=True):
            st.session_state.watchlist = (
                DEFAULT_SYMBOLS["Indexes"][:4]
                + DEFAULT_SYMBOLS["Equities"][:5]
                + DEFAULT_SYMBOLS["Crypto"][:2]
            )
            st.rerun()
        if c2.button("Crypto", use_container_width=True):
            st.session_state.watchlist = (
                DEFAULT_SYMBOLS["Crypto"]
                + DEFAULT_SYMBOLS["Indexes"][:3]
            )
            st.rerun()
        if c1.button("FX & Comm", use_container_width=True):
            st.session_state.watchlist = (
                DEFAULT_SYMBOLS["Forex"]
                + DEFAULT_SYMBOLS["Commodities"]
            )
            st.rerun()
        if c2.button("Alle", use_container_width=True):
            all_s = []
            for s in DEFAULT_SYMBOLS.values():
                all_s.extend(s)
            st.session_state.watchlist = list(dict.fromkeys(all_s))
            st.rerun()

        with st.expander("Manuell bearbeiten"):
            raw = st.text_area(
                "Symbole (eines pro Zeile)",
                value="\n".join(st.session_state.watchlist),
                height=120,
            )
            if st.button("Übernehmen", use_container_width=True):
                st.session_state.watchlist = [
                    s.strip().upper() for s in raw.splitlines() if s.strip()
                ]
                st.rerun()

        st.divider()

        # Chart Symbol
        st.markdown("**CHART**")
        sym = st.text_input(
            "Symbol",
            value=st.session_state.get("chart_symbol", "AAPL"),
            label_visibility="collapsed",
            placeholder="Symbol …",
        )
        st.session_state.chart_symbol = sym.strip().upper()

        st.divider()

        # Technische Indikatoren
        st.markdown("**INDICATORS**")
        ind = st.session_state.get("indicators", {
            "sma_20": True, "sma_50": True, "sma_200": False,
            "ema_12": False, "ema_26": False,
            "bollinger": False, "volume": True,
            "rsi": True, "macd": False, "vwap": False,
        })

        with st.expander("Moving Averages", expanded=True):
            ind["sma_20"]  = st.toggle("SMA 20",  value=ind.get("sma_20",  True),  key="t_sma20")
            ind["sma_50"]  = st.toggle("SMA 50",  value=ind.get("sma_50",  True),  key="t_sma50")
            ind["sma_200"] = st.toggle("SMA 200", value=ind.get("sma_200", False), key="t_sma200")
            ind["ema_12"]  = st.toggle("EMA 12",  value=ind.get("ema_12",  False), key="t_ema12")
            ind["ema_26"]  = st.toggle("EMA 26",  value=ind.get("ema_26",  False), key="t_ema26")

        with st.expander("Overlays"):
            ind["bollinger"] = st.toggle("Bollinger Bands", value=ind.get("bollinger", False), key="t_boll")
            ind["vwap"]      = st.toggle("VWAP",            value=ind.get("vwap",      False), key="t_vwap")

        with st.expander("Oszillatoren & Volumen"):
            ind["rsi"]    = st.toggle("RSI (14)", value=ind.get("rsi",    True),  key="t_rsi")
            ind["macd"]   = st.toggle("MACD",     value=ind.get("macd",   False), key="t_macd")
            ind["volume"] = st.toggle("Volume",   value=ind.get("volume", True),  key="t_vol")

        st.session_state.indicators = ind

        st.divider()

        # Info
        st.markdown(
            '<div style="font-size:10px;color:#444;line-height:1.7;'
            'font-family:JetBrains Mono,monospace">'
            '<span style="color:#ff6600">Quellen</span><br>'
            'Reuters · FT · CoinDesk · FXStreet<br>'
            'Kitco · CNBC · Seeking Alpha<br><br>'
            '<span style="color:#ff6600">Kurse</span><br>'
            'Yahoo Finance (yfinance) – ~15 Min verzögert<br><br>'
            '<span style="color:#ff6600">Hinweis</span><br>'
            'Kein Handelssignal. Nur zu Informationszwecken.'
            '</div>',
            unsafe_allow_html=True,
        )
