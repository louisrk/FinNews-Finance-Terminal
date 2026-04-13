import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
from data.market_data import (
    fetch_market_overview,
    fetch_sector_performance,
    fetch_heatmap_data,
)


def _fmt(price: float, sym: str) -> str:
    if "=X" in sym:
        return f"{price:.4f}"
    if "^" in sym and price < 10:
        return f"{price:.3f}"
    if price < 1:
        return f"{price:.6f}"
    if price < 100:
        return f"{price:.2f}"
    return f"{price:,.2f}"


# Kategorie-Grid 
def _render_grid(title: str, data: Dict) -> None:
    if not data:
        return
    st.markdown(f'<div class="bb-section-header">{title}</div>', unsafe_allow_html=True)
    html = '<div class="market-grid">'
    for sym, info in data.items():
        p = _fmt(info["price"], sym)
        pct = info["change_pct"]
        clr = "#00cc00" if pct >= 0 else "#cc0000"
        arrow = "+" if pct >= 0 else "-"
        html += (
            f'<div class="market-cell">'
            f'<span class="market-cell-name">{info["name"]}</span>'
            f'<span class="market-cell-price">{p}</span>'
            f'<span style="color:{clr};font-size:11px;font-weight:600">{arrow} {abs(pct):.2f}%</span>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# Sektor-Balken
def _render_sector_chart(data: Dict) -> None:
    if not data:
        return
    st.markdown('<div class="bb-section-header">S&P 500 SECTOR PERFORMANCE</div>',
                unsafe_allow_html=True)
    names = list(data.keys())
    vals  = [data[n]["change_pct"] for n in names]
    colors = ["#00cc00" if v >= 0 else "#cc0000" for v in vals]

    fig = go.Figure(go.Bar(
        y=names, x=vals, orientation="h", marker_color=colors,
        text=[f"{v:+.2f}%" for v in vals], textposition="outside",
        textfont=dict(color="#ccc", size=10),
    ))
    fig.update_layout(
        height=380, template="plotly_dark",
        paper_bgcolor="#000", plot_bgcolor="#060606",
        font=dict(family="JetBrains Mono, monospace", color="#ccc", size=10),
        xaxis=dict(gridcolor="#111", zeroline=True, zerolinecolor="#333", title=""),
        yaxis=dict(gridcolor="#111", title=""),
        margin=dict(l=110, r=50, t=5, b=15), showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# Heatmap (Treemap)
def _render_heatmap(df) -> None:
    if df is None or df.empty:
        return
    st.markdown('<div class="bb-section-header">S&P 500 HEATMAP</div>',
                unsafe_allow_html=True)

    fig = px.treemap(
        df, path=["symbol"], values="market_cap",
        color="change_pct",
        color_continuous_scale=["#cc0000", "#330000", "#000", "#003300", "#00cc00"],
        color_continuous_midpoint=0, custom_data=["change_pct"],
    )
    fig.update_traces(
        textinfo="label+text",
        texttemplate="%{label}<br>%{customdata[0]:.2f}%",
        textfont=dict(size=11, family="JetBrains Mono"),
    )
    fig.update_layout(
        height=480, template="plotly_dark",
        paper_bgcolor="#000", plot_bgcolor="#060606",
        font=dict(family="JetBrains Mono, monospace", color="#ccc"),
        margin=dict(l=5, r=5, t=5, b=5),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(title="Chg%",
                                tickfont=dict(color="#888"),
                                title_font=dict(color="#888")),
    )
    st.plotly_chart(fig, use_container_width=True)


# Hauptfunktion
def render_market_overview() -> None:
    overview  = fetch_market_overview()
    sectors   = fetch_sector_performance()
    heatmap   = fetch_heatmap_data()

    if not overview:
        st.info("Lade Marktdaten …")
        return

    # Obere Reihe
    c1, c2, c3 = st.columns(3)
    with c1: _render_grid("US INDICES",     overview.get("US Indices", {}))
    with c2: _render_grid("EUROPE / ASIA",  overview.get("Europe / Asia", {}))
    with c3: _render_grid("CRYPTO",         overview.get("Crypto", {}))

    # Untere Reihe
    c1, c2, c3 = st.columns(3)
    with c1: _render_grid("FOREX",          overview.get("Forex", {}))
    with c2: _render_grid("COMMODITIES",    overview.get("Commodities", {}))
    with c3: _render_grid("BONDS / RATES",  overview.get("Bonds / Rates", {}))

    st.markdown("---")

    # Sektor + Heatmap
    c1, c2 = st.columns(2)
    with c1: _render_sector_chart(sectors)
    with c2: _render_heatmap(heatmap)
