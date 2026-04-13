import requests
import streamlit as st
import pandas as pd
from typing import Dict, List


# Regionen – Flights (global via OpenSky)
REGIONS = {
    "Welt":          {"lamin": -60, "lamax": 75, "lomin": -180, "lomax": 180},
    "Europa":        {"lamin": 35,  "lamax": 72, "lomin": -12,  "lomax": 45},
    "Nordamerika":   {"lamin": 15,  "lamax": 72, "lomin": -170, "lomax": -50},
    "Asien":         {"lamin": -10, "lamax": 55, "lomin": 60,   "lomax": 150},
    "Naher Osten":   {"lamin": 12,  "lamax": 42, "lomin": 25,   "lomax": 65},
    "Afrika":        {"lamin": -35, "lamax": 37, "lomin": -20,  "lomax": 55},
    "Südamerika":    {"lamin": -56, "lamax": 15, "lomin": -82,  "lomax": -34},
}


# Regionen – Vessels (Digitraffic = Ostsee/Nordeuropa)
VESSEL_REGIONS = {
    "Alle Gewässer":     {"lat": 60.5, "lon": 21, "zoom": 4.3},
    "Ostsee Zentral":    {"lat": 57.5, "lon": 18, "zoom": 5.5},
    "Finnischer Meerbusen": {"lat": 60.0, "lon": 26, "zoom": 6.5},
    "Bottnischer Meerbusen": {"lat": 63.0, "lon": 20, "zoom": 5.5},
    "Kattegat / Skagerrak": {"lat": 57.5, "lon": 11, "zoom": 6.5},
    "Rigaischer Meerbusen": {"lat": 57.8, "lon": 23.5, "zoom": 7},
    "Ostsee Süd (DE/PL)": {"lat": 55.5, "lon": 16, "zoom": 6},
}

# Globale Handelsrouten – statische Overlay-Daten für Weltkarte
GLOBAL_TRADE_ROUTES = [
    {
        "name": "Suez → Mittelmeer → Nordeuropa",
        "lats": [30.5, 35.0, 36.5, 43.5, 48.0, 51.5, 54.0, 58.0],
        "lons": [32.3, 25.0, 10.0,  0.0, -5.0,  1.5,  8.0, 18.0],
        "color": "#ff6600", "commodities": "Oil, LNG, Container",
    },
    {
        "name": "Persischer Golf → Hormuz → Suez",
        "lats": [26.5, 25.5, 23.0, 15.0, 12.6, 14.0, 22.0, 30.5],
        "lons": [52.0, 56.5, 59.0, 52.0, 43.3, 42.0, 38.0, 32.3],
        "color": "#ff3300", "commodities": "Crude Oil, LNG",
    },
    {
        "name": "Asien → Malacca → Suez",
        "lats": [22.3, 10.0, 2.5, -5.0, 12.6, 30.5],
        "lons": [114.0, 107.0, 101.0, 80.0, 43.3, 32.3],
        "color": "#ff9900", "commodities": "Container, Electronics",
    },
    {
        "name": "Transatlantik (EU ↔ US East Coast)",
        "lats": [51.0, 50.0, 48.0, 42.0, 40.7],
        "lons": [ 1.3, -8.0, -20.0, -55.0, -74.0],
        "color": "#3388ff", "commodities": "Container, Autos, Chemicals",
    },
    {
        "name": "Kap der Guten Hoffnung → Atlantik",
        "lats": [-34.4, -25.0, -10.0, 8.0, 35.0, 48.0, 51.5],
        "lons": [ 18.5,  10.0,  -5.0, -20.0, -10.0, -5.0, 1.3],
        "color": "#cc00ff", "commodities": "Oil (Suez bypass), Bulk",
    },
    {
        "name": "Panama → US / EU",
        "lats": [9.1, 20.0, 30.0, 40.7],
        "lons": [-79.7, -75.0, -70.0, -74.0],
        "color": "#33cc99", "commodities": "LNG, Grain, Container",
    },
    {
        "name": "Transpazifik (Asien → US West Coast)",
        "lats": [22.3, 30.0, 35.0, 33.7],
        "lons": [114.0, 150.0, -170.0, -118.3],
        "color": "#66ccff", "commodities": "Container, Electronics",
    },
    {
        "name": "Ostsee Grain Corridor (UKR/RUS → EU)",
        "lats": [41.1, 45.0, 54.5, 56.0, 57.5, 58.0],
        "lons": [29.0, 28.0, 14.0, 11.0, 11.5, 18.0],
        "color": "#ffcc00", "commodities": "Wheat, Barley, Fertilizer",
    },
]

# Cargo / Freight Airline Detection
# Callsign prefixes of major cargo/freight airlines
_CARGO_PREFIXES = (
    "FDX", "FXE",   # FedEx
    "UPS", "5X",     # UPS
    "BOX",           # AeroLogic (DHL)
    "BCS",           # European Air Transport (DHL)
    "DHK", "DHL",    # DHL Aviation
    "GTI",           # Atlas Air
    "CLX",           # Cargolux
    "CAO",           # Air China Cargo
    "CKK",           # China Cargo Airlines
    "KAL",           # Korean Air Cargo
    "NCA",           # Nippon Cargo Airlines
    "SQC",           # Singapore Airlines Cargo
    "QTR", "QR",     # Qatar Airways Cargo
    "ETD", "ETH",    # Etihad / Ethiopian Cargo
    "THA",           # Thai Cargo
    "GEC",           # Lufthansa Cargo
    "ABW", "ABD",    # AirBridgeCargo (Volga-Dnepr)
    "SLK",           # Silkway
    "TRK",           # Turkish Cargo
    "MAS",           # MASkargo
    "PAC",           # Polar Air Cargo
    "WOA",           # Western Global Airlines
    "KLJ",           # Kalitta Air
    "NPT",           # LATAM Cargo
    "ASA",           # Alaska Air Cargo
    "ICL",           # CAL Cargo Air Lines
    "SWR",           # Swiss WorldCargo (prefix overlap)
    "MPH",           # Martinair
)

# Major financial hub airports (IATA → coords for distance-based analysis)
FINANCIAL_HUBS = {
    "New York (JFK/EWR)":  (40.64, -73.78),
    "London (LHR)":        (51.47, -0.46),
    "Hong Kong (HKG)":     (22.31, 113.91),
    "Singapore (SIN)":     (1.35, 103.99),
    "Tokyo (NRT)":         (35.76, 140.39),
    "Frankfurt (FRA)":     (50.03, 8.57),
    "Zürich (ZRH)":        (47.46, 8.55),
    "Dubai (DXB)":         (25.25, 55.36),
    "Shanghai (PVG)":      (31.14, 121.81),
    "Chicago (ORD)":       (41.97, -87.91),
}


def _classify_flight(callsign: str, country: str) -> str:
    """Klassifiziert einen Flug: Cargo, Passenger, Private, Military, Unknown."""
    cs = callsign.upper().strip()
    if not cs:
        return "Unknown"
    for prefix in _CARGO_PREFIXES:
        if cs.startswith(prefix):
            return "Cargo/Freight"
    # Military patterns (common)
    mil_prefixes = ("RCH", "CNV", "RRR", "IAM", "MMF", "NAV", "AIO",
                    "DUKE", "REACH", "KING", "JAKE", "TEAL")
    for mp in mil_prefixes:
        if cs.startswith(mp):
            return "Military"
    # Private jets often have short registrations
    if len(cs) <= 4 and not cs[0].isdigit():
        return "Private/Bizjet"
    return "Passenger"


# Schiffskategorien (AIS Ship Type codes) – Trading-Fokus
_SHIP_CATEGORIES = {
    range(70, 80): "Cargo/Container",
    range(80, 90): "Tanker (Oil/LNG/Chem)",
    range(60, 70): "Passenger/Cruise",
    range(30, 36): "Fishing",
    range(36, 40): "Sailing/Pleasure",
    range(40, 50): "High Speed Craft",
    range(50, 60): "SAR/Military",
    range(20, 30): "Wing in Ground",
}

# Commodity-relevante Kategorien
COMMODITY_SHIP_TYPES = {"Cargo/Container", "Tanker (Oil/LNG/Chem)", "Fishing"}


def _ship_type_label(code) -> str:
    if code is None:
        return "Unknown"
    try:
        code = int(code)
    except (ValueError, TypeError):
        return "Unknown"
    for r, label in _SHIP_CATEGORIES.items():
        if code in r:
            return label
    return "Other"


# Maritime Chokepoints – für Commodity-Trading
CHOKEPOINTS = {
    "Strait of Hormuz": {
        "lat": 26.56, "lon": 56.25,
        "radius_deg": 1.5,
        "relevance": "~20% der Welt-Ölproduktion, Crude Oil / LNG",
        "commodities": ["CL=F", "BZ=F", "NG=F"],
        "desc": "Iran–Oman. Engpass für Öl aus dem Persischen Golf.",
    },
    "Suez Canal": {
        "lat": 30.45, "lon": 32.35,
        "radius_deg": 1.0,
        "relevance": "~12% Welthandel, ~30% Container-Schifffahrt",
        "commodities": ["CL=F", "NG=F"],
        "desc": "Ägypten. Verbindet Mittelmeer und Rotes Meer.",
    },
    "Strait of Malacca": {
        "lat": 2.5, "lon": 101.0,
        "radius_deg": 2.0,
        "relevance": "~25% Welthandel, Öl nach China/Japan/Korea",
        "commodities": ["CL=F", "BZ=F"],
        "desc": "Malaysia–Indonesien. Kritisch für asiatische Energieimporte.",
    },
    "Panama Canal": {
        "lat": 9.1, "lon": -79.7,
        "radius_deg": 0.8,
        "relevance": "~5% Welthandel, US LNG nach Asien",
        "commodities": ["NG=F", "ZW=F"],
        "desc": "Panama. Engpass für transozeanischen Handel.",
    },
    "Bab el-Mandeb": {
        "lat": 12.6, "lon": 43.3,
        "radius_deg": 1.2,
        "relevance": "~10% Welthandel, Zugang zum Suezkanal",
        "commodities": ["CL=F", "BZ=F"],
        "desc": "Jemen–Dschibuti. Houthi-Angriffe seit 2023 relevant.",
    },
    "Turkish Straits": {
        "lat": 41.1, "lon": 29.05,
        "radius_deg": 0.5,
        "relevance": "Getreide, russ. Öl, Schwarzmeer-Exporte",
        "commodities": ["ZW=F", "CL=F"],
        "desc": "Bosporus + Dardanellen. Getreide-Korridor Ukraine.",
    },
    "English Channel": {
        "lat": 50.9, "lon": 1.3,
        "radius_deg": 1.0,
        "relevance": "Europäischer Haupthandelsweg, Container",
        "commodities": [],
        "desc": "UK–Frankreich. Einer der meistbefahrenen Seewege.",
    },
    "Cape of Good Hope": {
        "lat": -34.35, "lon": 18.5,
        "radius_deg": 2.0,
        "relevance": "Suez-Alternative, Umleitung bei Blockaden",
        "commodities": ["CL=F", "BZ=F"],
        "desc": "Südafrika. Ausweichroute wenn Suez/Bab el-Mandeb unsicher.",
    },
}


# OpenSky Feld-Index
_OS = {
    "icao24": 0, "callsign": 1, "origin_country": 2,
    "longitude": 5, "latitude": 6, "baro_altitude": 7,
    "on_ground": 8, "velocity": 9, "true_track": 10,
    "vertical_rate": 11, "geo_altitude": 13,
}


# Flugzeuge – OpenSky Network
@st.cache_data(ttl=60, show_spinner=False)
def fetch_flights(region: str = "Europa", max_items: int = 3000) -> pd.DataFrame:
    """Live Flugdaten via OpenSky – mit Trading-Klassifizierung."""
    bbox = REGIONS.get(region, REGIONS["Europa"])
    try:
        params = {}
        if region != "Welt":
            params = {
                "lamin": bbox["lamin"], "lamax": bbox["lamax"],
                "lomin": bbox["lomin"], "lomax": bbox["lomax"],
            }
        r = requests.get(
            "https://opensky-network.org/api/states/all",
            params=params, timeout=15,
        )
        r.raise_for_status()
        states = r.json().get("states", [])
    except Exception:
        return pd.DataFrame()

    rows = []
    for s in states[:max_items]:
        lat = s[_OS["latitude"]]
        lon = s[_OS["longitude"]]
        if lat is None or lon is None:
            continue
        alt = s[_OS["baro_altitude"]] or s[_OS["geo_altitude"]] or 0
        vel = s[_OS["velocity"]]
        cs = (s[_OS["callsign"]] or "").strip()
        country = s[_OS["origin_country"]]
        rows.append({
            "icao24":    s[_OS["icao24"]],
            "callsign":  cs,
            "country":   country,
            "lat":       lat,
            "lon":       lon,
            "altitude":  alt,
            "velocity":  round(vel * 3.6, 1) if vel else 0,
            "track":     s[_OS["true_track"]] or 0,
            "on_ground": s[_OS["on_ground"]],
            "v_rate":    s[_OS["vertical_rate"]] or 0,
            "category":  _classify_flight(cs, country),
        })
    return pd.DataFrame(rows)


# Schiffe – Digitraffic AIS
@st.cache_data(ttl=60, show_spinner=False)
def _fetch_vessel_metadata() -> Dict[int, int]:
    """Holt Schiffstyp-Codes via /vessels Endpoint. Returns {mmsi: shipType}."""
    try:
        r = requests.get(
            "https://meri.digitraffic.fi/api/ais/v1/vessels",
            headers={
                "Accept": "application/json",
                "Digitraffic-User": "finnews-terminal",
            },
            timeout=20,
        )
        r.raise_for_status()
        vessels = r.json()
    except Exception:
        return {}
    if not isinstance(vessels, list):
        return {}
    return {v["mmsi"]: v.get("shipType") for v in vessels if "mmsi" in v}


@st.cache_data(ttl=60, show_spinner=False)
def fetch_vessels(max_items: int = 5000) -> pd.DataFrame:
    """Live AIS-Schiffsdaten mit Trading-Klassifizierung.

    Joined locations (Koordinaten) + vessels (Schiffstyp-Metadaten).
    """
    _headers = {
        "Accept": "application/json",
        "Digitraffic-User": "finnews-terminal",
    }
    try:
        r = requests.get(
            "https://meri.digitraffic.fi/api/ais/v1/locations",
            headers=_headers, timeout=15,
        )
        r.raise_for_status()
        features = r.json().get("features", [])
    except Exception:
        return pd.DataFrame()

    # Vessel metadata (shipType) from separate endpoint
    meta = _fetch_vessel_metadata()

    rows = []
    for f in features[:max_items]:
        props = f.get("properties", {})
        geo = f.get("geometry", {})
        coords = geo.get("coordinates", [None, None])
        if coords[0] is None or coords[1] is None:
            continue
        mmsi = props.get("mmsi", 0)
        ship_type_code = meta.get(mmsi)
        stype = _ship_type_label(ship_type_code)
        sog = round(props.get("sog", 0) or 0, 1)
        rows.append({
            "mmsi":       mmsi,
            "lat":        coords[1],
            "lon":        coords[0],
            "sog":        sog,
            "cog":        props.get("cog", 0) or 0,
            "heading":    props.get("heading") or 0,
            "nav_status": props.get("navStat", -1),
            "ship_type":  stype,
            "commodity_relevant": stype in COMMODITY_SHIP_TYPES,
        })
    return pd.DataFrame(rows)


def count_vessels_near_chokepoint(df: pd.DataFrame, lat: float, lon: float,
                                  radius: float) -> Dict:
    """Zählt Schiffe in einem Chokepoint-Radius. Gibt Breakdown nach Typ zurück."""
    if df.empty:
        return {"total": 0, "tanker": 0, "cargo": 0, "other": 0}
    nearby = df[
        (df["lat"].between(lat - radius, lat + radius)) &
        (df["lon"].between(lon - radius, lon + radius))
    ]
    return {
        "total":  len(nearby),
        "tanker": len(nearby[nearby["ship_type"].str.contains("Tanker", na=False)]),
        "cargo":  len(nearby[nearby["ship_type"].str.contains("Cargo", na=False)]),
        "other":  len(nearby) - len(nearby[nearby["ship_type"].str.contains("Tanker|Cargo", na=False)]),
    }

