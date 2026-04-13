import streamlit as st
import streamlit.components.v1 as components
from typing import Dict


def _fmt_price(price: float, sym: str) -> str:
    if any(x in sym for x in ["=X", "USDJPY"]):
        return f"{price:.4f}"
    if price < 1:
        return f"{price:.6f}"
    if price < 100:
        return f"{price:.2f}"
    return f"{price:,.2f}"


def render_ticker_bar(quotes: Dict[str, Dict]) -> None:
    if not quotes:
        st.markdown(
            '<div style="background:#000;border-bottom:1px solid #333;padding:6px 12px;'
            'color:#666;font-size:11px;font-family:monospace">Lade Kurse …</div>',
            unsafe_allow_html=True,
        )
        return

    items_html = ""
    for sym, q in quotes.items():
        price = _fmt_price(q["price"], sym)
        pct   = q["change_pct"]
        arrow = "+" if pct >= 0 else "-"
        clr   = "#00cc00" if pct >= 0 else "#cc0000"
        name  = q["name"]

        items_html += (
            f'<span class="ti">'
            f'<span style="color:#ff6600;font-weight:700">{name}</span> '
            f'<span style="color:#fff">{price}</span> '
            f'<span style="color:{clr}">{arrow}{abs(pct):.2f}%</span>'
            f'</span>'
            f'<span style="color:#333">│</span>'
        )

    full = items_html * 2

    components.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
        body {{ margin:0; padding:0; background:#000; }}
        .tw {{
            overflow:hidden; background:#000;
            border-bottom:1px solid #ff660066; padding:5px 0;
        }}
        .tt {{
            display:flex; gap:28px; white-space:nowrap; width:max-content;
            animation:scroll 50s linear infinite;
        }}
        .tt:hover {{ animation-play-state:paused; }}
        @keyframes scroll {{
            0%   {{ transform:translateX(0); }}
            100% {{ transform:translateX(-50%); }}
        }}
        .ti {{
            display:inline-flex; align-items:center; gap:6px;
            font-family:'JetBrains Mono',monospace; font-size:12px;
        }}
    </style>
    <div class="tw"><div class="tt">{full}</div></div>
    """, height=38)
