import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.geo_tracker import (
    fetch_flights, fetch_vessels, REGIONS,
    CHOKEPOINTS, COMMODITY_SHIP_TYPES, FINANCIAL_HUBS,
    count_vessels_near_chokepoint, VESSEL_REGIONS, GLOBAL_TRADE_ROUTES,
)


# Hilfsfunktionen
_MAP_LAYOUT = dict(
    paper_bgcolor="#000", plot_bgcolor="#000",
    font=dict(family="JetBrains Mono, monospace", color="#ccc", size=10),
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0.85)", font=dict(size=9),
                bordercolor="#333", borderwidth=1),
)

_CAT_COLORS = {
    "Cargo/Freight": "#ff6600",
    "Passenger":     "#3388ff",
    "Private/Bizjet": "#ffcc00",
    "Military":      "#cc0000",
    "Unknown":       "#444",
}

_SHIP_COLORS = {
    "Tanker (Oil/LNG/Chem)": "#ff3300",
    "Cargo/Container":       "#ff9900",
    "Fishing":               "#33cc99",
    "Passenger/Cruise":      "#3388ff",
    "High Speed Craft":      "#cc00ff",
    "SAR/Military":          "#cc0000",
    "Sailing/Pleasure":      "#66ccff",
    "Other":                 "#777",
    "Unknown":               "#888",
}


def _bb_header(text: str) -> None:
    st.markdown(f'<div class="bb-section-header">{text}</div>',
                unsafe_allow_html=True)


def _kpi_box(label: str, value: str, delta: str = "", color: str = "#ff6600") -> str:
    return (
        f'<div style="background:#060606;border:1px solid #222;padding:8px 12px;'
        f'text-align:center">'
        f'<div style="font-size:9px;color:#666;text-transform:uppercase;'
        f'letter-spacing:.12em">{label}</div>'
        f'<div style="font-size:18px;font-weight:700;color:{color}">{value}</div>'
        f'<div style="font-size:9px;color:#888">{delta}</div></div>'
    )


# FLIGHT RADAR – Trading Focus
def _render_flight_radar() -> None:
    _bb_header("AIR TRAFFIC MONITOR  ·  OPENSKY NETWORK  ·  LIVE")

    st.markdown(
        '<div style="font-size:10px;color:#666;margin-bottom:8px">'
        'Cargo/Freight-Volumen = Proxy für globale Handelsaktivität. '
        'Private Jets zu Finanzhubs = mögliche M&A / Deal-Signale.</div>',
        unsafe_allow_html=True,
    )

    # Controls
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        region = st.selectbox("Region", list(REGIONS.keys()), index=1,
                              key="flight_region", label_visibility="collapsed")
    with c2:
        view_mode = st.selectbox("Ansicht",
                                 ["Alle (nach Typ)", "Nur Cargo/Freight",
                                  "Nur Private/Bizjets", "Nur Military"],
                                 key="flight_view", label_visibility="collapsed")
    with c3:
        max_items = st.select_slider("Max",
                                     options=[1000, 2000, 3000, 5000],
                                     value=3000, key="flight_max",
                                     label_visibility="collapsed")

    df = fetch_flights(region, max_items)
    if df.empty:
        st.warning("Keine Flugdaten. OpenSky API ggf. überlastet.")
        return

    airborne = df[~df["on_ground"]].copy()
    if airborne.empty:
        st.info("Keine Flüge in der Luft.")
        return

    # KPI Row
    total    = len(airborne)
    cargo    = len(airborne[airborne["category"] == "Cargo/Freight"])
    private  = len(airborne[airborne["category"] == "Private/Bizjet"])
    military = len(airborne[airborne["category"] == "Military"])
    pax      = len(airborne[airborne["category"] == "Passenger"])
    cargo_pct = (cargo / total * 100) if total else 0

    kpi_html = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px">'
    kpi_html += _kpi_box("TOTAL IN AIR", f"{total:,}", f"{region}")
    kpi_html += _kpi_box("CARGO/FREIGHT", f"{cargo:,}", f"{cargo_pct:.1f}% of total", "#ff6600")
    kpi_html += _kpi_box("PASSENGER", f"{pax:,}", "", "#3388ff")
    kpi_html += _kpi_box("PRIVATE/BIZJET", f"{private:,}", "M&A Signal", "#ffcc00")
    kpi_html += _kpi_box("MILITARY", f"{military:,}", "Geopolitik", "#cc0000")
    kpi_html += _kpi_box("COUNTRIES", f"{airborne['country'].nunique()}", "", "#00cc00")
    kpi_html += '</div>'
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Filter
    view_df = airborne
    if view_mode == "Nur Cargo/Freight":
        view_df = airborne[airborne["category"] == "Cargo/Freight"]
    elif view_mode == "Nur Private/Bizjets":
        view_df = airborne[airborne["category"] == "Private/Bizjet"]
    elif view_mode == "Nur Military":
        view_df = airborne[airborne["category"] == "Military"]

    if view_df.empty:
        st.info(f"Keine Flüge für Filter: {view_mode}")
        return

    # Karte 
    bbox = REGIONS[region]
    center_lat = (bbox["lamin"] + bbox["lamax"]) / 2
    center_lon = (bbox["lomin"] + bbox["lomax"]) / 2
    zoom = 2.5 if region == "Welt" else 3.8 if region in ("Nordamerika", "Asien") else 4.2

    fig = px.scatter_mapbox(
        view_df, lat="lat", lon="lon", color="category",
        hover_name="callsign",
        hover_data={"country": True, "altitude": True, "velocity": True,
                    "category": True, "lat": False, "lon": False},
        color_discrete_map=_CAT_COLORS,
        zoom=zoom, center=dict(lat=center_lat, lon=center_lon),
        mapbox_style="carto-darkmatter",
    )

    # Financial Hub Marker
    for name, (lat, lon) in FINANCIAL_HUBS.items():
        if (bbox["lamin"] <= lat <= bbox["lamax"] and
                bbox["lomin"] <= lon <= bbox["lomax"]) or region == "Welt":
            fig.add_trace(go.Scattermapbox(
                lat=[lat], lon=[lon], mode="markers+text",
                marker=dict(size=10, color="#ffcc00", symbol="star"),
                text=[name], textposition="top right",
                textfont=dict(size=8, color="#ffcc00"),
                name="Financial Hub", showlegend=False,
                hoverinfo="text",
            ))

    fig.update_traces(marker=dict(size=4, opacity=0.85),
                      selector=dict(type="scattermapbox"))
    fig.update_layout(height=550, **_MAP_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    # Cargo Breakdown
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("📦 CARGO / FREIGHT BREAKDOWN", expanded=True):
            cargo_df = airborne[airborne["category"] == "Cargo/Freight"]
            if not cargo_df.empty:
                top_c = cargo_df["country"].value_counts().head(10).reset_index()
                top_c.columns = ["Origin", "Flights"]
                html = '<table class="wl-table"><thead><tr><th>ORIGIN</th><th>FLIGHTS</th><th>SHARE</th></tr></thead><tbody>'
                ct = top_c["Flights"].sum()
                for _, r in top_c.iterrows():
                    pct = r["Flights"] / ct * 100
                    html += (
                        f'<tr><td style="color:#ff6600">{r["Origin"]}</td>'
                        f'<td style="color:#fff">{r["Flights"]}</td>'
                        f'<td style="color:#888">{pct:.1f}%</td></tr>'
                    )
                html += '</tbody></table>'
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.caption("Keine Cargo-Flüge in dieser Region.")

    with col2:
        with st.expander("PRIVATE JETS > FINANCIAL HUBS", expanded=True):
            pj = airborne[airborne["category"] == "Private/Bizjet"]
            if not pj.empty:
                top_p = pj["country"].value_counts().head(10).reset_index()
                top_p.columns = ["Origin", "Jets"]
                html = '<table class="wl-table"><thead><tr><th>ORIGIN</th><th>JETS</th><th>SIGNAL</th></tr></thead><tbody>'
                for _, r in top_p.iterrows():
                    sig = "HIGH" if r["Jets"] > 5 else "Normal"
                    clr = "#ffcc00" if r["Jets"] > 5 else "#888"
                    html += (
                        f'<tr><td style="color:#ffcc00">{r["Origin"]}</td>'
                        f'<td style="color:#fff">{r["Jets"]}</td>'
                        f'<td style="color:{clr}">{sig}</td></tr>'
                    )
                html += '</tbody></table>'
                st.markdown(html, unsafe_allow_html=True)
                st.markdown(
                    '<div style="font-size:9px;color:#555;margin-top:4px">'
                    'Ungewöhnlich viele Private Jets zu Finanzzentren können '
                    'auf bevorstehende M&A-Deals hindeuten.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("Keine Private Jets erkannt.")

# VESSEL RADAR – Commodity & Trade Flow

def _render_global_routes_map() -> None:
    """Weltkarte mit den wichtigsten Handelsrouten + Chokepoint-Markern."""
    _bb_header("GLOBAL TRADE ROUTES  ·  MAJOR SHIPPING LANES & CHOKEPOINTS")

    st.markdown(
        '<div style="font-size:10px;color:#666;margin-bottom:8px">'
        'Kritische Seewege für den Welthandel. Unterbrechungen dieser Routen '
        'haben direkte Auswirkungen auf Commodity-Preise (Öl, LNG, Getreide, Container-Frachtraten).</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure()

    # Trade route lines
    for route in GLOBAL_TRADE_ROUTES:
        fig.add_trace(go.Scattermapbox(
            lat=route["lats"], lon=route["lons"],
            mode="lines",
            line=dict(width=2.5, color=route["color"]),
            name=route["name"],
            hovertext=f'{route["name"]}<br>Commodities: {route["commodities"]}',
            hoverinfo="text",
        ))

    # Chokepoint markers
    for name, cp in CHOKEPOINTS.items():
        commodities_str = ", ".join(cp["commodities"]) if cp["commodities"] else "–"
        fig.add_trace(go.Scattermapbox(
            lat=[cp["lat"]], lon=[cp["lon"]],
            mode="markers+text",
            marker=dict(size=12, color="#cc0000", symbol="circle"),
            text=[name.split("(")[0].strip()[:20]],
            textposition="top right",
            textfont=dict(size=8, color="#ff6600"),
            name=name,
            showlegend=False,
            hovertext=f'<b>{name}</b><br>{cp["desc"]}<br>Relevanz: {cp["relevance"]}<br>Commodities: {commodities_str}',
            hoverinfo="text",
        ))

    fig.update_layout(
        height=500,
        mapbox=dict(style="carto-darkmatter", zoom=1.5,
                    center=dict(lat=25, lon=30)),
        paper_bgcolor="#000", plot_bgcolor="#000",
        font=dict(family="JetBrains Mono, monospace", color="#ccc", size=10),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(bgcolor="rgba(0,0,0,0.85)", font=dict(size=8, color="#ccc"),
                    bordercolor="#333", borderwidth=1, x=0.01, y=0.99,
                    orientation="v"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Chokepoint risk table
    _bb_header("CHOKEPOINT RISK DASHBOARD")
    cols = st.columns(4)
    for i, (name, cp) in enumerate(CHOKEPOINTS.items()):
        with cols[i % 4]:
            commodities_str = " ".join(cp["commodities"]) if cp["commodities"] else "–"
            html = (
                f'<div style="background:#060606;border:1px solid #222;'
                f'padding:10px;margin-bottom:8px">'
                f'<div style="font-size:10px;font-weight:700;color:#ff6600;'
                f'letter-spacing:.1em">{name}</div>'
                f'<div style="font-size:9px;color:#666;margin:3px 0">{cp["desc"]}</div>'
                f'<div style="font-size:9px;color:#888;margin-top:4px">'
                f'Relevanz: {cp["relevance"]}</div>'
                f'<div style="font-size:8px;color:#555;margin-top:4px;'
                f'border-top:1px solid #222;padding-top:4px">'
                f'Commodities: <span style="color:#ff6600">{commodities_str}</span></div>'
                f'</div>'
            )
            st.markdown(html, unsafe_allow_html=True)


def _render_vessel_radar() -> None:
    _bb_header("VESSEL TRACKER  ·  LIVE AIS  ·  OSTSEE / NORDEUROPA")

    st.markdown(
        '<div style="font-size:10px;color:#666;margin-bottom:8px">'
        'Live AIS-Daten via Digitraffic (Finnland). Abdeckung: <b>Ostsee, '
        'Bottnischer & Finnischer Meerbusen, Kattegat/Skagerrak</b>. '
        'Tanker + Cargo-Dichte = Proxy für nordeuropäische Handelsaktivität, '
        'Ostsee-Getreideexporte und Nordsee-Ölverkehr.</div>',
        unsafe_allow_html=True,
    )

    # Controls
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        region_key = st.selectbox("Region", list(VESSEL_REGIONS.keys()),
                                  index=0, key="vessel_region",
                                  label_visibility="collapsed")
    with c2:
        vessel_view = st.selectbox("Ansicht",
                                   ["Alle (nach Typ)", "Nur Tanker (Oil/LNG)",
                                    "Nur Cargo/Container", "Nur Commodity-relevant"],
                                   key="vessel_view", label_visibility="collapsed")
    with c3:
        max_v = st.select_slider("Max",
                                 options=[2000, 5000, 8000, 12000, 18000],
                                 value=8000, key="vessel_max",
                                 label_visibility="collapsed")

    df = fetch_vessels(max_v)
    if df.empty:
        st.warning("Keine Schiffsdaten.")
        return

    # KPI Row 
    total     = len(df)
    tankers   = len(df[df["ship_type"].str.contains("Tanker", na=False)])
    cargo     = len(df[df["ship_type"].str.contains("Cargo", na=False)])
    moving    = len(df[df["sog"] > 0.5])
    commodity = len(df[df["commodity_relevant"]])
    com_pct   = (commodity / total * 100) if total else 0

    kpi_html = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px">'
    kpi_html += _kpi_box("TOTAL VESSELS", f"{total:,}", "AIS tracked")
    kpi_html += _kpi_box("TANKERS", f"{tankers:,}", "Oil / LNG / Chem", "#ff3300")
    kpi_html += _kpi_box("CARGO", f"{cargo:,}", "Container / Bulk", "#ff9900")
    kpi_html += _kpi_box("IN MOTION", f"{moving:,}", f"{moving/total*100:.0f}%", "#00cc00")
    kpi_html += _kpi_box("AT ANCHOR", f"{total - moving:,}", "Possible congestion", "#ffcc00")
    kpi_html += _kpi_box("COMMODITY REL.", f"{commodity:,}", f"{com_pct:.0f}% of fleet", "#ff6600")
    kpi_html += '</div>'
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Filter 
    view_df = df
    if vessel_view == "Nur Tanker (Oil/LNG)":
        view_df = df[df["ship_type"].str.contains("Tanker", na=False)]
    elif vessel_view == "Nur Cargo/Container":
        view_df = df[df["ship_type"].str.contains("Cargo", na=False)]
    elif vessel_view == "Nur Commodity-relevant":
        view_df = df[df["commodity_relevant"]]

    if view_df.empty:
        st.info(f"Keine Schiffe für: {vessel_view}")
        return

    #  Karte zentriert auf gewählte Region
    rv = VESSEL_REGIONS[region_key]

    fig = px.scatter_mapbox(
        view_df, lat="lat", lon="lon", color="ship_type",
        hover_name="mmsi",
        hover_data={"ship_type": True, "sog": True, "cog": True,
                    "lat": False, "lon": False},
        color_discrete_map=_SHIP_COLORS,
        zoom=rv["zoom"], center=dict(lat=rv["lat"], lon=rv["lon"]),
        mapbox_style="carto-darkmatter",
    )

    fig.update_traces(marker=dict(size=4, opacity=0.8))
    fig.update_layout(height=550, **_MAP_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    # Ostsee Chokepoint/Region Analysis 
    _bb_header("OSTSEE HANDELSANALYSE  ·  REGIONALE DICHTE")

    # Baltic-specific points of interest
    baltic_pois = {
        "Kiel Canal":    {"lat": 54.3, "lon": 9.9, "radius": 0.5,
                          "desc": "Meistbefahrener Kanal der Welt – Ostsee↔Nordsee"},
        "Öresund":       {"lat": 55.8, "lon": 12.7, "radius": 0.5,
                          "desc": "DK↔SE – Zugang Ostsee, Öl/Getreide-Transit"},
        "Gotland Basin": {"lat": 57.5, "lon": 19.5, "radius": 1.5,
                          "desc": "Zentralostsee – Hauptschifffahrtsweg"},
        "Helsinki/Tallinn": {"lat": 59.8, "lon": 25.0, "radius": 0.8,
                             "desc": "Finnischer MB – Fähren, Container, RU-Öl"},
        "St. Petersburg": {"lat": 60.0, "lon": 28.5, "radius": 0.8,
                           "desc": "RU-Export – Öl, Fertilizer, Metalle"},
        "Bothnian Bay":  {"lat": 64.5, "lon": 22.5, "radius": 1.5,
                          "desc": "Papier, Erz, Stahl (SE/FI Industrie)"},
    }

    cols = st.columns(3)
    for i, (name, poi) in enumerate(baltic_pois.items()):
        counts = count_vessels_near_chokepoint(
            df, poi["lat"], poi["lon"], poi["radius"],
        )
        with cols[i % 3]:
            if counts["tanker"] > 10:
                level, lclr = "HIGH", "#cc0000"
            elif counts["tanker"] > 3:
                level, lclr = "MEDIUM", "#ffcc00"
            else:
                level, lclr = "LOW", "#00cc00"

            html = (
                f'<div style="background:#060606;border:1px solid #222;'
                f'padding:10px;margin-bottom:8px">'
                f'<div style="font-size:10px;font-weight:700;color:#ff6600;'
                f'letter-spacing:.1em">{name}</div>'
                f'<div style="font-size:9px;color:#666;margin:3px 0">{poi["desc"]}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:6px">'
                f'<div style="font-size:9px;color:#888">Vessels</div>'
                f'<div style="font-size:12px;color:#fff;font-weight:600">{counts["total"]}</div>'
                f'<div style="font-size:9px;color:#888">Tankers</div>'
                f'<div style="font-size:12px;color:#ff3300;font-weight:600">{counts["tanker"]}</div>'
                f'<div style="font-size:9px;color:#888">Cargo</div>'
                f'<div style="font-size:12px;color:#ff9900;font-weight:600">{counts["cargo"]}</div>'
                f'<div style="font-size:9px;color:#888">Density</div>'
                f'<div style="font-size:10px;color:{lclr};font-weight:700">{level}</div>'
                f'</div></div>'
            )
            st.markdown(html, unsafe_allow_html=True)

    # Commodity Vessel Mix 
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("TANKER / CARGO BREAKDOWN", expanded=True):
            commodity_df = df[df["commodity_relevant"]]
            if not commodity_df.empty:
                types = commodity_df["ship_type"].value_counts().reset_index()
                types.columns = ["Type", "Count"]
                colors = [_SHIP_COLORS.get(t, "#555") for t in types["Type"]]
                fig2 = go.Figure(go.Bar(
                    y=types["Type"], x=types["Count"], orientation="h",
                    marker_color=colors,
                    text=[f"{c:,}" for c in types["Count"]],
                    textposition="outside",
                    textfont=dict(color="#ccc", size=10),
                ))
                fig2.update_layout(
                    height=200, template="plotly_dark",
                    paper_bgcolor="#000", plot_bgcolor="#060606",
                    font=dict(family="JetBrains Mono", color="#ccc", size=10),
                    xaxis=dict(gridcolor="#111", title=""),
                    yaxis=dict(title=""),
                    margin=dict(l=130, r=50, t=5, b=15),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)

    with col2:
        with st.expander("VESSEL SPEED DISTRIBUTION", expanded=True):
            moving_df = df[df["sog"] > 0.1]
            if not moving_df.empty:
                fig3 = go.Figure(go.Histogram(
                    x=moving_df["sog"], nbinsx=40,
                    marker_color="#ff6600",
                ))
                fig3.add_vline(x=moving_df["sog"].median(),
                               line_dash="dash", line_color="#ffcc00",
                               annotation_text=f"Median: {moving_df['sog'].median():.1f} kn",
                               annotation_font=dict(color="#ffcc00", size=10))
                fig3.update_layout(
                    height=200, template="plotly_dark",
                    paper_bgcolor="#000", plot_bgcolor="#060606",
                    font=dict(family="JetBrains Mono", color="#ccc", size=10),
                    xaxis=dict(title="SOG (knots)", gridcolor="#111"),
                    yaxis=dict(title="Count", gridcolor="#111"),
                    margin=dict(l=50, r=15, t=5, b=35),
                    showlegend=False,
                )
                st.plotly_chart(fig3, use_container_width=True)



# Haupt-Render
def render_geo_panel() -> None:
    """Geopolitical Radar mit Trading-relevanten Subtabs."""
    sub_routes, sub_vessel, sub_flight = st.tabs([
        "GLOBAL TRADE ROUTES",
        "VESSEL LIVE · OSTSEE/NORDIC",
        "FLIGHT · TRADE ACTIVITY",
    ])

    with sub_routes:
        _render_global_routes_map()

    with sub_vessel:
        _render_vessel_radar()

    with sub_flight:
        _render_flight_radar()
