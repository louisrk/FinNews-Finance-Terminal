import streamlit as st
from datetime import datetime
from typing import Dict, List
from data.news_fetcher import CATEGORIES
from data.asset_detector import detect_assets, format_ticker_buttons


def _time_ago(dt: datetime) -> str:
    diff = datetime.utcnow() - dt
    s = int(diff.total_seconds())
    if s < 60:   return f"{s}s ago"
    if s < 3600: return f"{s // 60}m ago"
    if s < 86400: return f"{s // 3600}h ago"
    return dt.strftime("%d.%m.%y")


def _is_new(dt: datetime, minutes: int = 30) -> bool:
    return (datetime.utcnow() - dt).total_seconds() < minutes * 60


def _render_card(item: Dict) -> None:
    badge = '<span class="badge-new">NEW</span>' if _is_new(item["time"]) else ""
    summary = (
        f'<div class="news-summary">{item["summary"]}</div>'
        if item.get("summary") else ""
    )

    text = (item.get("title", "") + " " + item.get("summary", "")).strip()
    tickers = detect_assets(text)
    ticker_html = format_ticker_buttons(tickers)

    st.markdown(
        f'<div class="news-card">'
        f'<div class="news-source">{item["source"]} {badge}</div>'
        f'<div class="news-title">'
        f'<a href="{item["link"]}" target="_blank">{item["title"]}</a></div>'
        f'<div class="news-meta"><span>{_time_ago(item["time"])}</span></div>'
        f'{summary}</div>',
        unsafe_allow_html=True,
    )
    if ticker_html:
        st.markdown(ticker_html, unsafe_allow_html=True)


def render_news_panel(news_data: Dict[str, List[Dict]]) -> None:
    if not news_data:
        st.info("Nachrichten werden geladen …")
        return

    all_items = []
    for cat_items in news_data.values():
        all_items.extend(cat_items)
    all_items.sort(key=lambda x: x["time"], reverse=True)

    tabs = st.tabs(CATEGORIES)

    with tabs[0]:
        col1, col2 = st.columns(2)
        half = len(all_items[:50]) // 2
        with col1:
            st.markdown('<div class="bb-section-header">LATEST · ALL</div>',
                        unsafe_allow_html=True)
            for item in all_items[:half]:
                _render_card(item)
        with col2:
            st.markdown('<div class="bb-section-header">&nbsp;</div>',
                        unsafe_allow_html=True)
            for item in all_items[half:50]:
                _render_card(item)

    for i, cat in enumerate(CATEGORIES[1:], start=1):
        with tabs[i]:
            items = news_data.get(cat, [])
            if not items:
                st.warning(f"Keine Nachrichten für **{cat}**.")
                continue
            col1, col2 = st.columns(2)
            mid = (len(items) + 1) // 2
            with col1:
                st.markdown(
                    f'<div class="bb-section-header">{cat.upper()} · '
                    f'{len(items)} ITEMS</div>',
                    unsafe_allow_html=True,
                )
                for item in items[:mid]:
                    _render_card(item)
            with col2:
                st.markdown('<div class="bb-section-header">&nbsp;</div>',
                            unsafe_allow_html=True)
                for item in items[mid:]:
                    _render_card(item)
