# FinNews Terminal

> **Work in Progress** – Dieses Projekt befindet sich in aktiver Entwicklung. Features, UI und Architektur können sich jederzeit ändern. Geplant sind u.a. ML/AI-gestützte Erweiterungen (siehe Roadmap).

Finanzterminal mit Fokus auf **Echtzeit-Nachrichtenanalyse** und **geopolitisches Monitoring**. Gebaut mit Streamlit, Plotly und Python.

---

## Kernfunktionen

### Nachrichten & Geopolitik

- **Multi-Source News Aggregator** – 25+ RSS-Quellen (Reuters, FT, CoinDesk, FXStreet, Kitco, CNBC, Seeking Alpha u.v.m.), 7 Kategorien (Bonds, Commodities, Crypto, Equities, Forex, Indexes, Macro), 2-Minuten-Refresh, automatische NEW-Badges
- **Automatische Ticker-Erkennung** – Erkennt relevante Aktien/Assets in Nachrichtentext und verlinkt sie direkt zum Chart
- **GEO RADAR – Global Trade Routes** – Weltkarte mit den wichtigsten Handelsrouten und Chokepoint-Monitoring (Suezkanal, Strasse von Hormuz, Malakka etc.) inkl. Risiko-Dashboard und Commodity-Relevanz
- **GEO RADAR – Vessel Tracker** – Live AIS-Daten (Digitraffic) für Ostsee/Nordeuropa: Tanker/Cargo-Klassifikation, Dichteanalyse pro Region, Commodity-Relevanz-Score
- **GEO RADAR – Flight Monitor** – OpenSky Network Live-Daten: Cargo/Freight-Volumen als Proxy für Handelsaktivität, Private-Jet-Tracking zu Finanzhubs (M&A-Signal), Militärflug-Erkennung

### Marktdaten & Charting

- **1.100+ Symbole** – Aktien (S&P 500, DAX, FTSE, CAC 40, SMI ...), 137 Kryptowährungen, 56 Forex-Paare, 42 Rohstoff-Futures, 120 ETFs, 59 globale Indizes – durchsuchbar mit Autovervollständigung
- **Technische Analyse** – Interaktiver Candlestick/Line/OHLC-Chart mit 9 Indikatoren (SMA, EMA, RSI, MACD, Bollinger Bands, VWAP, ATR, Stochastic, OBV)
- **Marktübersicht** – Sektor-Performance (S&P 500 Sektoren), Treemap-Heatmap, Kursraster nach Kategorie
- **Makrokalender** – Kuratierter Wirtschaftskalender 2026 mit allen marktrelevanten Ereignissen (Fed/FOMC, EZB, BoE, BoJ, CPI, NFP, PCE, BIP u.v.m.), Impact-Stufen (KRITISCH / HOCH / MITTEL / GERING), Länder-Flags und Tages-/Vergangen-Badges
- **Scrollender Ticker** – Bloomberg-Style Live-Kursleiste mit 30s-Refresh
- **Watchlist** – Konfigurierbares Portfolio mit Preset-Filtern (US Focus, Crypto, FX & Commodities) und manueller Bearbeitung

---

## Geplant: ML / AI Roadmap

> Die folgenden Features sind in Planung und stellen den eigentlichen Schwerpunkt des Projekts dar.

- **Sentiment-Analyse** – NLP-basierte Echtzeit-Bewertung von Nachrichtenartikeln (Bullish/Bearish/Neutral) mit aggregiertem Sentiment-Score pro Asset
- **Anomalie-Erkennung** – ML-gestützte Erkennung ungewöhnlicher Kurs-/Volumenbewegungen und Vessel-/Flugmuster als Frühwarnsystem
- **News-Clustering & Topic Detection** – Automatische Gruppierung verwandter Nachrichten und Erkennung aufkommender Themen
- **Predictive Signals** – Zeitreihenprognose auf Basis historischer Daten und Nachrichtensentiment
- **Geopolitisches Risikoscoring** – ML-Modell zur Bewertung geopolitischer Risiken und deren Auswirkung auf Commodity-Preise und Handelsrouten
- **Smart Alerts** – Automatische Benachrichtigungen bei signifikanten Sentiment-Shifts, Anomalien oder Risikoveränderungen

---

## Projektstruktur

```
finnews/
├── app.py                    ← Hauptdatei, Layout, Tabs, CSS
├── requirements.txt
├── data/
│   ├── news_fetcher.py       ← RSS-Feeds, 25+ Quellen, 7 Kategorien
│   ├── stock_fetcher.py      ← yfinance Kurse, 1.100+ Symbole
│   ├── asset_detector.py     ← Keyword-zu-Ticker Erkennung in News
│   ├── market_data.py        ← Sektor-ETFs, Marktübersicht
│   ├── technical.py          ← 9 technische Indikatoren
│   ├── economic_calendar.py  ← Kuratierter Makrokalender 2026
│   └── geo_tracker.py        ← Flug- & Schiffsdaten, Chokepoints, Handelsrouten
└── ui/
    ├── ticker_bar.py         ← Scrollender Bloomberg-Ticker
    ├── news_panel.py         ← Nachrichten-Panels mit Ticker-Links
    ├── chart_panel.py        ← Interaktiver Chart + Indikatoren
    ├── market_overview.py    ← Sektor-Charts, Heatmap
    ├── calendar_panel.py     ← Makrokalender-Ansicht
    └── geo_panel.py          ← GEO RADAR (Routen, Vessel, Flight)
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Hinweis:** Erfordert **yfinance ≥ 1.3.0**. Ältere Versionen können keine Kursdaten mehr von Yahoo Finance abrufen (Cookie/Crumb-Authentifizierung). Bei Streamlit Community Cloud wird `yfinance>=1.3.0` in `requirements.txt` automatisch installiert.

## Datenquellen

| Typ | Quelle | Kosten |
|---|---|---|
| Nachrichten | Öffentliche RSS-Feeds | Kostenlos |
| Kurse | Yahoo Finance (yfinance ≥ 1.3.0) | Kostenlos, ~15 Min verzögert |
| Makrokalender | Manuell kuratiert (offizielle Zentralbank-/Statistikamt-Termine 2026) | Kostenlos |
| Flugdaten | OpenSky Network API | Kostenlos, kein Key nötig |
| Schiffsdaten | Digitraffic AIS (Finnland) | Kostenlos, kein Key nötig |

---

## Changelog

### Mai 2026
- **Bugfix:** Länder-Flags im Makrokalender wurden nicht angezeigt (auskommentierte Variable)
- **Bugfix:** Yahoo Finance Kursdaten schlugen auf allen Umgebungen fehl (`JSONDecodeError: Expecting value`)  
  → Vollständige Migration von `fast_info` / `yf.Tickers()` auf `yf.download()` + Upgrade auf yfinance 1.3.0 (nutzt `curl_cffi` für korrekte Cookie-Authentifizierung)
- **Bugfix:** `ValueError: The truth value of a Series is ambiguous` in `chart_panel.py`  
  → `fetch_history()` normalisiert jetzt MultiIndex-Spalten von yfinance 1.x auf flache Spaltennamen

---

**Status:** In aktiver Entwicklung · Kein produktives System · Keine Anlageberatung
