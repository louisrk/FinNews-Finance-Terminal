"""
Die Daten kommen nicht von einer API, sondern sind manuell kuratiert – basierend auf den offiziellen Veröffentlichungsplänen der Zentralbanken und Statistikämter für 2026.
Kuratierter Makrokalender 2026 – alle marktrelevanten Ereignisse
(Fed, EZB, BoE, BoJ, CPI, NFP, PCE, BIP usw.)
"""

from datetime import date, timedelta
from typing import List, Dict

# ── Impact-Level ─────────────────────────────────────────────────────────────
CRITICAL = "CRITICAL"   # Fed / EZB Zinsentscheid
HIGH     = "HIGH"       # CPI, NFP, PCE, BIP
MEDIUM   = "MEDIUM"     # Protokolle, Flash PMI, etc.
LOW      = "LOW"

# ── Kategorien ───────────────────────────────────────────────────────────────
CB         = "Zentralbank"
INFLATION  = "Inflation"
EMPLOYMENT = "Arbeitsmarkt"
GROWTH     = "Wachstum / BIP"
TRADE      = "Handel"
SENTIMENT  = "Stimmung / PMI"


def _ev(d: str, time: str, event: str, impact: str,
        country: str, category: str, currency: str,
        notes: str = "") -> Dict:
    return {
        "date":     date.fromisoformat(d),
        "time":     time,
        "event":    event,
        "impact":   impact,
        "country":  country,
        "category": category,
        "currency": currency,
        "notes":    notes,
    }


# ── Alle Ereignisse 2026 ─────────────────────────────────────────────────────
EVENTS: List[Dict] = [

    # ════════════════════════════════════════════════════════════════════════
    # FOMC – Federal Open Market Committee
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-28", "20:00 ET", "FOMC Zinsentscheid", CRITICAL, "US", CB, "USD",
        "Pressekonferenz 20:30 ET"),
    _ev("2026-02-18", "20:00 ET", "FOMC Protokoll – Januar-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-03-18", "20:00 ET", "FOMC Zinsentscheid + SEP / Dot Plot", CRITICAL, "US", CB, "USD",
        "Vierteljährliche Wirtschaftsprojektionen · Pressekonferenz 20:30 ET"),
    _ev("2026-04-08", "20:00 ET", "FOMC Protokoll – März-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-04-29", "20:00 ET", "FOMC Zinsentscheid", CRITICAL, "US", CB, "USD",
        "Pressekonferenz 20:30 ET"),
    _ev("2026-05-20", "20:00 ET", "FOMC Protokoll – April-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-06-10", "20:00 ET", "FOMC Zinsentscheid + SEP / Dot Plot", CRITICAL, "US", CB, "USD",
        "Vierteljährliche Wirtschaftsprojektionen · Pressekonferenz 20:30 ET"),
    _ev("2026-07-08", "20:00 ET", "FOMC Protokoll – Juni-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-07-29", "20:00 ET", "FOMC Zinsentscheid", CRITICAL, "US", CB, "USD",
        "Pressekonferenz 20:30 ET"),
    _ev("2026-08-19", "20:00 ET", "FOMC Protokoll – Juli-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-09-16", "20:00 ET", "FOMC Zinsentscheid + SEP / Dot Plot", CRITICAL, "US", CB, "USD",
        "Vierteljährliche Wirtschaftsprojektionen · Pressekonferenz 20:30 ET"),
    _ev("2026-10-07", "20:00 ET", "FOMC Protokoll – September-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-10-28", "20:00 ET", "FOMC Zinsentscheid", CRITICAL, "US", CB, "USD",
        "Pressekonferenz 20:30 ET"),
    _ev("2026-11-18", "20:00 ET", "FOMC Protokoll – Oktober-Sitzung", MEDIUM, "US", CB, "USD"),
    _ev("2026-12-09", "20:00 ET", "FOMC Zinsentscheid + SEP / Dot Plot", CRITICAL, "US", CB, "USD",
        "Vierteljährliche Wirtschaftsprojektionen · Pressekonferenz 20:30 ET"),

    # ════════════════════════════════════════════════════════════════════════
    # EZB – Europäische Zentralbank
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-22", "14:15 ET", "EZB Zinsentscheid", CRITICAL, "EU", CB, "EUR",
        "Pressekonferenz 14:45 ET"),
    _ev("2026-03-05", "14:15 ET", "EZB Zinsentscheid + Projektionen", CRITICAL, "EU", CB, "EUR",
        "Staff Projections (Inflation & Wachstum) · Pressekonferenz 14:45 ET"),
    _ev("2026-04-16", "14:15 ET", "EZB Zinsentscheid", CRITICAL, "EU", CB, "EUR",
        "Pressekonferenz 14:45 ET"),
    _ev("2026-06-04", "14:15 ET", "EZB Zinsentscheid + Projektionen", CRITICAL, "EU", CB, "EUR",
        "Staff Projections · Pressekonferenz 14:45 ET"),
    _ev("2026-07-23", "14:15 ET", "EZB Zinsentscheid", CRITICAL, "EU", CB, "EUR",
        "Pressekonferenz 14:45 ET"),
    _ev("2026-09-10", "14:15 ET", "EZB Zinsentscheid + Projektionen", CRITICAL, "EU", CB, "EUR",
        "Staff Projections · Pressekonferenz 14:45 ET"),
    _ev("2026-10-29", "14:15 ET", "EZB Zinsentscheid", CRITICAL, "EU", CB, "EUR",
        "Pressekonferenz 14:45 ET"),
    _ev("2026-12-17", "14:15 ET", "EZB Zinsentscheid + Projektionen", CRITICAL, "EU", CB, "EUR",
        "Staff Projections · Pressekonferenz 14:45 ET"),

    # ════════════════════════════════════════════════════════════════════════
    # Bank of England
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-02-06", "13:00 ET", "BoE Zinsentscheid + Monetary Policy Report", HIGH, "GB", CB, "GBP"),
    _ev("2026-03-19", "13:00 ET", "BoE Zinsentscheid", HIGH, "GB", CB, "GBP"),
    _ev("2026-05-07", "13:00 ET", "BoE Zinsentscheid + Monetary Policy Report", HIGH, "GB", CB, "GBP"),
    _ev("2026-06-18", "13:00 ET", "BoE Zinsentscheid", HIGH, "GB", CB, "GBP"),
    _ev("2026-08-06", "13:00 ET", "BoE Zinsentscheid + Monetary Policy Report", HIGH, "GB", CB, "GBP"),
    _ev("2026-09-17", "13:00 ET", "BoE Zinsentscheid", HIGH, "GB", CB, "GBP"),
    _ev("2026-11-05", "13:00 ET", "BoE Zinsentscheid + Monetary Policy Report", HIGH, "GB", CB, "GBP"),
    _ev("2026-12-17", "13:00 ET", "BoE Zinsentscheid", HIGH, "GB", CB, "GBP"),

    # ════════════════════════════════════════════════════════════════════════
    # Bank of Japan
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-24", "TBD JST", "BoJ Zinsentscheid", HIGH, "JP", CB, "JPY"),
    _ev("2026-03-19", "TBD JST", "BoJ Zinsentscheid + Outlook Report", HIGH, "JP", CB, "JPY"),
    _ev("2026-05-01", "TBD JST", "BoJ Zinsentscheid + Outlook Report", HIGH, "JP", CB, "JPY"),
    _ev("2026-06-17", "TBD JST", "BoJ Zinsentscheid", HIGH, "JP", CB, "JPY"),
    _ev("2026-07-31", "TBD JST", "BoJ Zinsentscheid + Outlook Report", HIGH, "JP", CB, "JPY"),
    _ev("2026-09-23", "TBD JST", "BoJ Zinsentscheid", HIGH, "JP", CB, "JPY"),
    _ev("2026-10-29", "TBD JST", "BoJ Zinsentscheid + Outlook Report", HIGH, "JP", CB, "JPY"),
    _ev("2026-12-18", "TBD JST", "BoJ Zinsentscheid + Outlook Report", HIGH, "JP", CB, "JPY"),

    # ════════════════════════════════════════════════════════════════════════
    # US CPI – Verbraucherpreise
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-14", "08:30 ET", "US CPI – Dezember 2025", HIGH, "US", INFLATION, "USD"),
    _ev("2026-02-11", "08:30 ET", "US CPI – Januar 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-03-11", "08:30 ET", "US CPI – Februar 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-04-14", "08:30 ET", "US CPI – März 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-05-13", "08:30 ET", "US CPI – April 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-06-11", "08:30 ET", "US CPI – Mai 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-07-14", "08:30 ET", "US CPI – Juni 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-08-12", "08:30 ET", "US CPI – Juli 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-09-11", "08:30 ET", "US CPI – August 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-10-13", "08:30 ET", "US CPI – September 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-11-12", "08:30 ET", "US CPI – Oktober 2026", HIGH, "US", INFLATION, "USD"),
    _ev("2026-12-11", "08:30 ET", "US CPI – November 2026", HIGH, "US", INFLATION, "USD"),

    # ════════════════════════════════════════════════════════════════════════
    # US PCE – Fed-bevorzugtes Inflationsmaß
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-30", "08:30 ET", "US PCE Inflation – Dezember 2025", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-02-27", "08:30 ET", "US PCE Inflation – Januar 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-03-27", "08:30 ET", "US PCE Inflation – Februar 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-04-30", "08:30 ET", "US PCE Inflation – März 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-05-29", "08:30 ET", "US PCE Inflation – April 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-06-26", "08:30 ET", "US PCE Inflation – Mai 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-07-31", "08:30 ET", "US PCE Inflation – Juni 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-08-28", "08:30 ET", "US PCE Inflation – Juli 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-09-25", "08:30 ET", "US PCE Inflation – August 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-10-30", "08:30 ET", "US PCE Inflation – September 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-11-25", "08:30 ET", "US PCE Inflation – Oktober 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),
    _ev("2026-12-23", "08:30 ET", "US PCE Inflation – November 2026", HIGH, "US", INFLATION, "USD",
        "Fed-bevorzugtes Inflationsmaß"),

    # ════════════════════════════════════════════════════════════════════════
    # US Non-Farm Payrolls (NFP) – Arbeitsmarktbericht
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-09", "08:30 ET", "US Non-Farm Payrolls – Dezember 2025", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-02-06", "08:30 ET", "US Non-Farm Payrolls – Januar 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-03-06", "08:30 ET", "US Non-Farm Payrolls – Februar 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-04-03", "08:30 ET", "US Non-Farm Payrolls – März 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-05-01", "08:30 ET", "US Non-Farm Payrolls – April 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-06-05", "08:30 ET", "US Non-Farm Payrolls – Mai 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-07-02", "08:30 ET", "US Non-Farm Payrolls – Juni 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-08-07", "08:30 ET", "US Non-Farm Payrolls – Juli 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-09-04", "08:30 ET", "US Non-Farm Payrolls – August 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-10-02", "08:30 ET", "US Non-Farm Payrolls – September 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-11-06", "08:30 ET", "US Non-Farm Payrolls – Oktober 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),
    _ev("2026-12-04", "08:30 ET", "US Non-Farm Payrolls – November 2026", HIGH, "US", EMPLOYMENT, "USD",
        "Arbeitslosenquote + Lohnwachstum"),

    # ════════════════════════════════════════════════════════════════════════
    # US BIP – Bruttoinlandsprodukt
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-29", "08:30 ET", "US BIP Erstschätzung Q4 2025", HIGH, "US", GROWTH, "USD"),
    _ev("2026-02-26", "08:30 ET", "US BIP 2. Schätzung Q4 2025", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-03-26", "08:30 ET", "US BIP 3. Schätzung Q4 2025", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-04-30", "08:30 ET", "US BIP Erstschätzung Q1 2026", HIGH, "US", GROWTH, "USD"),
    _ev("2026-05-28", "08:30 ET", "US BIP 2. Schätzung Q1 2026", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-06-25", "08:30 ET", "US BIP 3. Schätzung Q1 2026", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-07-30", "08:30 ET", "US BIP Erstschätzung Q2 2026", HIGH, "US", GROWTH, "USD"),
    _ev("2026-08-27", "08:30 ET", "US BIP 2. Schätzung Q2 2026", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-09-24", "08:30 ET", "US BIP 3. Schätzung Q2 2026", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-10-29", "08:30 ET", "US BIP Erstschätzung Q3 2026", HIGH, "US", GROWTH, "USD"),
    _ev("2026-11-24", "08:30 ET", "US BIP 2. Schätzung Q3 2026", MEDIUM, "US", GROWTH, "USD"),
    _ev("2026-12-22", "08:30 ET", "US BIP 3. Schätzung Q3 2026", MEDIUM, "US", GROWTH, "USD"),

    # ════════════════════════════════════════════════════════════════════════
    # Eurozone VPI (HVPI Flash)
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-07", "05:00 ET", "Eurozone HVPI Flash – Dezember 2025", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-02-04", "05:00 ET", "Eurozone HVPI Flash – Januar 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-03-04", "05:00 ET", "Eurozone HVPI Flash – Februar 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-04-01", "05:00 ET", "Eurozone HVPI Flash – März 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-04-30", "05:00 ET", "Eurozone HVPI Flash – April 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-05-29", "05:00 ET", "Eurozone HVPI Flash – Mai 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-07-01", "05:00 ET", "Eurozone HVPI Flash – Juni 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-07-31", "05:00 ET", "Eurozone HVPI Flash – Juli 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-09-01", "05:00 ET", "Eurozone HVPI Flash – August 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-09-30", "05:00 ET", "Eurozone HVPI Flash – September 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-10-30", "05:00 ET", "Eurozone HVPI Flash – Oktober 2026", MEDIUM, "EU", INFLATION, "EUR"),
    _ev("2026-11-30", "05:00 ET", "Eurozone HVPI Flash – November 2026", MEDIUM, "EU", INFLATION, "EUR"),

    # ════════════════════════════════════════════════════════════════════════
    # Eurozone BIP
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-01-30", "05:00 ET", "Eurozone BIP Erstschätzung Q4 2025", MEDIUM, "EU", GROWTH, "EUR"),
    _ev("2026-04-30", "05:00 ET", "Eurozone BIP Erstschätzung Q1 2026", MEDIUM, "EU", GROWTH, "EUR"),
    _ev("2026-07-30", "05:00 ET", "Eurozone BIP Erstschätzung Q2 2026", MEDIUM, "EU", GROWTH, "EUR"),
    _ev("2026-10-30", "05:00 ET", "Eurozone BIP Erstschätzung Q3 2026", MEDIUM, "EU", GROWTH, "EUR"),

    # ════════════════════════════════════════════════════════════════════════
    # US ISM Manufacturing / Services PMI
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-05-01", "10:00 ET", "US ISM Manufacturing PMI – April 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-06-01", "10:00 ET", "US ISM Manufacturing PMI – Mai 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-07-01", "10:00 ET", "US ISM Manufacturing PMI – Juni 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-08-03", "10:00 ET", "US ISM Manufacturing PMI – Juli 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-09-01", "10:00 ET", "US ISM Manufacturing PMI – August 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-10-01", "10:00 ET", "US ISM Manufacturing PMI – September 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-11-02", "10:00 ET", "US ISM Manufacturing PMI – Oktober 2026", MEDIUM, "US", SENTIMENT, "USD"),
    _ev("2026-12-01", "10:00 ET", "US ISM Manufacturing PMI – November 2026", MEDIUM, "US", SENTIMENT, "USD"),

    # ════════════════════════════════════════════════════════════════════════
    # Sonderereignisse
    # ════════════════════════════════════════════════════════════════════════
    _ev("2026-08-27", "TBD", "Jackson Hole Symposium – Tag 1", HIGH, "US", CB, "USD",
        "Fed-Vorsitzender Powell Rede erwartet – globale Geldpolitiksignale"),
    _ev("2026-08-28", "TBD", "Jackson Hole Symposium – Tag 2", MEDIUM, "US", CB, "USD"),
    _ev("2026-08-29", "TBD", "Jackson Hole Symposium – Tag 3", MEDIUM, "US", CB, "USD"),

    # US Staatsschulden-Schuldenobergrenze / Treasury-Auktionen (wenn bekannt)
    _ev("2026-05-06", "13:00 ET", "US Treasury – 3-Jahres-Note Auktion", LOW, "US", TRADE, "USD"),
    _ev("2026-05-07", "13:00 ET", "US Treasury – 10-Jahres-Note Auktion", MEDIUM, "US", TRADE, "USD",
        "Wichtig für Zinsniveau & Anleihemarkt"),
    _ev("2026-05-08", "13:00 ET", "US Treasury – 30-Jahres-Bond Auktion", MEDIUM, "US", TRADE, "USD",
        "Wichtig für Zinsniveau & Anleihemarkt"),
]


# ── Öffentliche API ───────────────────────────────────────────────────────────

_IMPACT_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def get_events(days_back: int = 7, days_ahead: int = 90) -> List[Dict]:
    """Alle Ereignisse im Fenster [heute-days_back … heute+days_ahead]."""
    today = date.today()
    start = today - timedelta(days=days_back)
    end   = today + timedelta(days=days_ahead)
    return sorted(
        [e for e in EVENTS if start <= e["date"] <= end],
        key=lambda x: (x["date"], _IMPACT_ORDER.get(x["impact"], 9)),
    )


def get_today_events() -> List[Dict]:
    today = date.today()
    return sorted(
        [e for e in EVENTS if e["date"] == today],
        key=lambda x: _IMPACT_ORDER.get(x["impact"], 9),
    )


def get_week_events() -> List[Dict]:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())   # Montag
    week_end   = week_start + timedelta(days=6)            # Sonntag
    return sorted(
        [e for e in EVENTS if week_start <= e["date"] <= week_end],
        key=lambda x: (x["date"], _IMPACT_ORDER.get(x["impact"], 9)),
    )


def get_next_critical() -> List[Dict]:
    """Nächste 3 CRITICAL-Ereignisse ab heute."""
    today = date.today()
    critical = [e for e in EVENTS if e["date"] >= today and e["impact"] == CRITICAL]
    critical.sort(key=lambda x: x["date"])
    return critical[:3]
