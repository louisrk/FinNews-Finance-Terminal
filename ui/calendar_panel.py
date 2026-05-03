import streamlit as st
from datetime import date, timedelta
from itertools import groupby
from typing import List, Dict

from data.economic_calendar import (
    get_events, get_today_events, get_week_events, get_next_critical,
    CB, INFLATION, EMPLOYMENT, GROWTH, SENTIMENT, TRADE,
    CRITICAL, HIGH, MEDIUM, LOW,
)

# ── Konstanten ────────────────────────────────────────────────────────────────
_IMPACT_COLOR = {
    CRITICAL: "#ff2200",
    HIGH:     "#ff6600",
    MEDIUM:   "#ffaa00",
    LOW:      "#555555",
}
_IMPACT_DOT = {
    CRITICAL: "●●●",
    HIGH:     "●●○",
    MEDIUM:   "●○○",
    LOW:      "○○○",
}
_IMPACT_LABEL = {
    CRITICAL: "KRITISCH",
    HIGH:     "HOCH",
    MEDIUM:   "MITTEL",
    LOW:      "GERING",
}
_FLAG = {
    "US": "🇺🇸", "EU": "🇪🇺", "GB": "🇬🇧",
    "JP": "🇯🇵", "DE": "🇩🇪", "CN": "🇨🇳",
}
_WEEKDAY_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
_MONTH_DE = [
    "", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
    "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",
]


def _bb_header(text: str) -> None:
    st.markdown(
        f'<div class="bb-section-header">{text}</div>',
        unsafe_allow_html=True,
    )


def _date_label(d: date) -> str:
    return f"{_WEEKDAY_DE[d.weekday()]} {d.day:02d}.{d.month:02d}."


def _event_card(ev: Dict, compact: bool = False) -> str:
    today     = date.today()
    is_today  = ev["date"] == today
    is_past   = ev["date"] < today
    impact    = ev["impact"]
    color     = _IMPACT_COLOR.get(impact, "#555")
    #flag      = _FLAG.get(ev["country"], "")

    bg         = "#0d0500" if is_today else "#050505"
    border_l   = color
    border_box = color if is_today else "#1a1a1a"
    opacity    = "0.38" if is_past and not is_today else "1"

    today_badge = (
        '<span style="background:#ff2200;color:#fff;font-size:7px;font-weight:700;'
        'padding:1px 5px;letter-spacing:.12em;margin-left:7px;vertical-align:middle">'
        'HEUTE</span>'
    ) if is_today else ""

    past_badge = (
        '<span style="color:#333;font-size:8px;margin-left:6px">✓ veröffentlicht</span>'
    ) if is_past and not is_today else ""

    notes_html = (
        f'<div style="font-size:9px;color:#555;margin-top:3px;'
        f'border-top:1px solid #111;padding-top:3px">{ev["notes"]}</div>'
    ) if ev.get("notes") else ""

    dot_html = (
        f'<span style="color:{color};font-size:10px;letter-spacing:-1px">'
        f'{_IMPACT_DOT.get(impact, "○○○")}</span>'
    )

    return (
        f'<div style="display:flex;align-items:flex-start;padding:7px 10px;'
        f'background:{bg};border:1px solid {border_box};'
        f'border-left:3px solid {border_l};margin-bottom:4px;'
        f'opacity:{opacity};font-family:JetBrains Mono,monospace;">'
        # Datum-Spalte
        f'<div style="min-width:52px;text-align:right;margin-right:10px;'
        f'padding-top:1px">'
        f'<div style="font-size:10px;color:#ccc;font-weight:600">'
        f'{_date_label(ev["date"])}</div>'
        f'<div style="font-size:9px;color:#444;margin-top:1px">{ev["time"]}</div>'
        f'</div>'
        # Impact-Spalte
        f'<div style="min-width:38px;text-align:center;margin-right:10px;'
        f'padding-top:2px">'
        f'{dot_html}'
        f'<div style="font-size:7px;color:{color};letter-spacing:.06em;'
        f'margin-top:2px">{_IMPACT_LABEL.get(impact, "")}</div>'
        f'</div>'
        # Inhalt-Spalte
        f'<div style="flex:1;min-width:0">'
        f'<div style="font-size:11px;color:#ddd;line-height:1.3;'
        f'font-weight:500;">{flag} {ev["event"]}{today_badge}{past_badge}</div>'
        f'<div style="font-size:9px;color:#555;margin-top:2px">'
        f'{ev["currency"]} · {ev["category"]}</div>'
        f'{notes_html}'
        f'</div>'
        f'</div>'
    )


def _next_critical_bar(events: List[Dict]) -> None:
    """Kompakter Hinweis auf die nächsten CRITICAL-Events ganz oben."""
    if not events:
        return
    today = date.today()
    parts = []
    for ev in events:
        delta = (ev["date"] - today).days
        if delta == 0:
            when = "HEUTE"
        elif delta == 1:
            when = "MORGEN"
        else:
            when = f"in {delta}d"
        flag = _FLAG.get(ev["country"], "")
        parts.append(
            f'<span style="margin-right:24px">'
            f'<span style="color:#ff2200;font-weight:700">{flag} {ev["event"]}</span>'
            f'<span style="color:#555"> · {_date_label(ev["date"])} · '
            f'<span style="color:#ffaa00">{when}</span></span></span>'
        )
    st.markdown(
        f'<div style="background:#0d0000;border:1px solid #330000;'
        f'border-left:3px solid #ff2200;padding:7px 12px;margin-bottom:10px;'
        f'font-family:JetBrains Mono,monospace;font-size:10px;overflow-x:auto;'
        f'white-space:nowrap">'
        f'<span style="color:#ff2200;font-weight:700;letter-spacing:.12em;'
        f'margin-right:16px">▲ NÄCHSTE ZINSENTSCHEIDE</span>'
        + "".join(parts)
        + "</div>",
        unsafe_allow_html=True,
    )


def _empty_box(msg: str) -> None:
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:10px;'
        f'color:#333;padding:12px;border:1px dashed #1a1a1a;text-align:center;'
        f'margin-bottom:10px">{msg}</div>',
        unsafe_allow_html=True,
    )


def render_calendar_panel() -> None:
    today = date.today()

    # ── Nächste Zinsentscheide – Pinned Bar ───────────────────────────────────
    _next_critical_bar(get_next_critical())

    # ── Filter-Leiste ─────────────────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns([2, 2, 2, 1])
    with fc1:
        cat_options = ["Alle Kategorien", CB, INFLATION, EMPLOYMENT, GROWTH, SENTIMENT, TRADE]
        cat_filter = st.selectbox("Kategorie", cat_options,
                                  key="cal_cat", label_visibility="collapsed")
    with fc2:
        imp_options = ["Alle Impact-Level", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
        imp_filter = st.selectbox("Impact", imp_options,
                                  key="cal_impact", label_visibility="collapsed")
    with fc3:
        cur_options = ["Alle Währungen", "USD", "EUR", "GBP", "JPY"]
        cur_filter = st.selectbox("Währung", cur_options,
                                  key="cal_cur", label_visibility="collapsed")
    with fc4:
        horizon = st.select_slider(
            "Horizont", options=[30, 60, 90, 180], value=90,
            key="cal_horizon", label_visibility="collapsed",
            format_func=lambda x: f"{x}d",
        )

    def _apply_filters(events: List[Dict]) -> List[Dict]:
        out = events
        if cat_filter != "Alle Kategorien":
            out = [e for e in out if e["category"] == cat_filter]
        if imp_filter != "Alle Impact-Level":
            out = [e for e in out if e["impact"] == imp_filter]
        if cur_filter != "Alle Währungen":
            out = [e for e in out if e["currency"] == cur_filter]
        return out

    # ── HEUTE ─────────────────────────────────────────────────────────────────
    month_str = _MONTH_DE[today.month]
    day_str   = _WEEKDAY_DE[today.weekday()]
    _bb_header(
        f"HEUTE · {day_str} {today.day:02d}. {month_str} {today.year}"
    )

    today_filtered = _apply_filters(get_today_events())
    if today_filtered:
        st.markdown(
            "".join(_event_card(ev) for ev in today_filtered),
            unsafe_allow_html=True,
        )
    else:
        _empty_box("Heute keine marktrelevanten Ereignisse für die gewählten Filter.")

    st.markdown('<hr style="border-color:#111;margin:14px 0">', unsafe_allow_html=True)

    # ── DIESE WOCHE ───────────────────────────────────────────────────────────
    week_start = today - timedelta(days=today.weekday())
    week_end   = week_start + timedelta(days=4)   # Freitag
    _bb_header(
        f"DIESE WOCHE · {week_start.day:02d}.{week_start.month:02d}. "
        f"– {week_end.day:02d}.{week_end.month:02d}.{week_end.year}"
    )

    week_filtered = _apply_filters(get_week_events())
    if week_filtered:
        # Zeilen die nicht "heute" sind, in zwei Spalten aufteilen
        non_today = [e for e in week_filtered if e["date"] != today]
        if non_today:
            mid = (len(non_today) + 1) // 2
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    "".join(_event_card(ev) for ev in non_today[:mid]),
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    "".join(_event_card(ev) for ev in non_today[mid:]),
                    unsafe_allow_html=True,
                )
        else:
            _empty_box("Außer den heutigen Ereignissen nichts Weiteres diese Woche.")
    else:
        _empty_box("Keine Ereignisse diese Woche für die gewählten Filter.")

    st.markdown('<hr style="border-color:#111;margin:14px 0">', unsafe_allow_html=True)

    # ── NÄCHSTE N TAGE ────────────────────────────────────────────────────────
    _bb_header(f"MAKROKALENDER · NÄCHSTE {horizon} TAGE")

    all_events = _apply_filters(get_events(days_back=0, days_ahead=horizon))
    # Vergangene Ereignisse der letzten Woche (für Kontext)
    past_ctx   = _apply_filters(get_events(days_back=7, days_ahead=0))

    if not all_events and not past_ctx:
        _empty_box("Keine Ereignisse für die gewählten Filter gefunden.")
        return

    # Letzte Woche (Kontext, eingeklappt)
    if past_ctx:
        with st.expander(f"◀  Letzte 7 Tage ({len(past_ctx)} Ereignisse)", expanded=False):
            st.markdown(
                "".join(_event_card(ev) for ev in past_ctx),
                unsafe_allow_html=True,
            )

    # Zukünftig: tageweise gruppiert
    for ev_date, day_iter in groupby(all_events, key=lambda x: x["date"]):
        day_list = list(day_iter)
        is_today_group = (ev_date == today)

        # Tages-Trennlinie (außer für "heute" – schon oben gezeigt)
        if not is_today_group:
            day_lbl   = _date_label(ev_date)
            delta_d   = (ev_date - today).days
            delta_str = (
                "morgen" if delta_d == 1
                else f"in {delta_d} Tagen"
            )
            has_critical = any(e["impact"] == CRITICAL for e in day_list)
            label_color  = "#ff2200" if has_critical else "#ff6600"
            st.markdown(
                f'<div style="font-family:JetBrains Mono,monospace;'
                f'font-size:9px;color:{label_color};letter-spacing:.14em;'
                f'text-transform:uppercase;padding:6px 0 3px 2px;'
                f'border-bottom:1px solid #1a1a1a;margin-top:6px">'
                f'{day_lbl} · {delta_str}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            "".join(_event_card(ev) for ev in day_list),
            unsafe_allow_html=True,
        )
