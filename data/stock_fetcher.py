import yfinance as yf
import streamlit as st
import pandas as pd
from typing import Dict, List


def _close_df(data: pd.DataFrame, symbols: list) -> pd.DataFrame:
    """Extrahiert Close-Preise aus yf.download()-Ergebnis (single oder multi ticker)."""
    if data.empty:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        level0 = data.columns.get_level_values(0)
        col = "Close" if "Close" in level0 else ("Adj Close" if "Adj Close" in level0 else None)
        if col is None:
            return pd.DataFrame()
        return data[col]
    else:
        col = "Close" if "Close" in data.columns else ("Adj Close" if "Adj Close" in data.columns else None)
        if col is None:
            return pd.DataFrame()
        return data[[col]].rename(columns={col: symbols[0]})

# Voreingestellte Symbole pro Kategorie
DEFAULT_SYMBOLS = {
    "Indexes":     ["^GSPC", "^NDX", "^DJI", "^STOXX50E", "^FTSE", "^N225", "^VIX"],
    "Equities":    ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"],
    "Crypto":      ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "BNB-USD"],
    "Forex":       ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", "AUDUSD=X"],
    "Commodities": ["GC=F", "SI=F", "CL=F", "NG=F", "HG=F", "ZW=F"],
    "Bonds":       ["^TNX", "^TYX", "^FVX", "^IRX"],
}

# Lesbare Namen 
# Lesbare Namen
SYMBOL_NAMES = {
    # INDEXES
    "^GSPC": "S&P 500", "^NDX": "Nasdaq 100", "^DJI": "Dow Jones",
    "^IXIC": "Nasdaq Composite", "^RUT": "Russell 2000",
    "^VIX": "VIX Volatility", "^OEX": "S&P 100",
    "^MID": "S&P MidCap 400", "^SP600": "S&P SmallCap 600",
    "^NYA": "NYSE Composite", "^XAX": "AMEX Composite",
    "^W5000": "Wilshire 5000", "^SOX": "PHLX Semiconductor",
    "^DJT": "Dow Transport", "^DJU": "Dow Utilities",
    # Europe
    "^GDAXI": "DAX 40", "^MDAXI": "MDAX", "^SDAXI": "SDAX",
    "^TECDAX": "TecDAX",
    "^STOXX50E": "Euro Stoxx 50", "^STOXX": "Stoxx Europe 600",
    "^FTSE": "FTSE 100", "^FTMC": "FTSE 250",
    "^FCHI": "CAC 40", "^IBEX": "IBEX 35",
    "^AEX": "AEX Amsterdam", "^SSMI": "SMI Swiss",
    "^BFX": "BEL 20", "^ATX": "ATX Vienna",
    "^OMXS30": "OMX Stockholm 30", "^OMXC25": "OMX Copenhagen 25",
    "^OMXH25": "OMX Helsinki 25", "^OBX": "OBX Oslo",
    "^ISEQ": "ISEQ Dublin", "^PSI20": "PSI 20 Lisbon",
    "^BVLG": "BEL All-Share",
    # Asia-Pacific
    "^N225": "Nikkei 225", "^HSI": "Hang Seng",
    "000001.SS": "Shanghai Composite", "399001.SZ": "Shenzhen Component",
    "^KS11": "KOSPI", "^KQ11": "KOSDAQ",
    "^TWII": "TAIEX", "^STI": "Straits Times",
    "^AXJO": "ASX 200", "^AORD": "All Ordinaries",
    "^BSESN": "BSE Sensex", "^NSEI": "Nifty 50",
    "^JKSE": "Jakarta Composite", "^SET.BK": "SET Thailand",
    "^KLSE": "KLCI Malaysia", "^NZ50": "NZX 50",
    # Americas
    "^GSPTSE": "TSX Composite", "^BVSP": "Bovespa Brazil",
    "^MXX": "IPC Mexico", "^MERV": "MERVAL Argentina",
    "^IPSA": "IPSA Chile",
    # Bonds / Rates
    "^TNX": "10Y US Treasury", "^TYX": "30Y US Treasury",
    "^FVX": "5Y US Treasury", "^IRX": "3M US T-Bill",

    # EQUITIES – US (S&P 500 vollständig + zusätzliche)
    # Technology
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA",
    "GOOGL": "Alphabet A", "GOOG": "Alphabet C", "META": "Meta Platforms",
    "AVGO": "Broadcom", "ORCL": "Oracle", "CSCO": "Cisco",
    "ADBE": "Adobe", "CRM": "Salesforce", "ACN": "Accenture",
    "IBM": "IBM", "INTC": "Intel", "AMD": "AMD",
    "TXN": "Texas Instruments", "QCOM": "Qualcomm", "AMAT": "Applied Materials",
    "NOW": "ServiceNow", "INTU": "Intuit", "MU": "Micron",
    "LRCX": "Lam Research", "KLAC": "KLA Corp", "SNPS": "Synopsys",
    "CDNS": "Cadence Design", "MRVL": "Marvell Technology",
    "ADSK": "Autodesk", "ANSS": "ANSYS", "FTNT": "Fortinet",
    "PANW": "Palo Alto Networks", "CRWD": "CrowdStrike",
    "ZS": "Zscaler", "NET": "Cloudflare", "DDOG": "Datadog",
    "MDB": "MongoDB", "SNOW": "Snowflake", "PLTR": "Palantir",
    "TEAM": "Atlassian", "WDAY": "Workday", "HUBS": "HubSpot",
    "VEEV": "Veeva Systems", "SPLK": "Splunk", "OKTA": "Okta",
    "TWLO": "Twilio", "ZM": "Zoom Video", "DOCU": "DocuSign",
    "BILL": "Bill.com", "PCTY": "Paylocity", "PAYC": "Paycom",
    "FFIV": "F5 Networks", "JNPR": "Juniper Networks",
    "AKAM": "Akamai", "EPAM": "EPAM Systems", "GDDY": "GoDaddy",
    "GEN": "Gen Digital", "HPE": "HP Enterprise", "HPQ": "HP Inc",
    "DELL": "Dell Technologies", "WDC": "Western Digital",
    "STX": "Seagate", "NTAP": "NetApp", "KEYS": "Keysight",
    "TER": "Teradyne", "ON": "ON Semiconductor",
    "NXPI": "NXP Semiconductors", "MCHP": "Microchip Technology",
    "SWKS": "Skyworks", "QRVO": "Qorvo", "ADI": "Analog Devices",
    "MPWR": "Monolithic Power", "ENPH": "Enphase Energy",
    "SEDG": "SolarEdge", "SMCI": "Super Micro Computer",
    "ARM": "ARM Holdings", "ASML": "ASML",
    "WOLF": "Wolfspeed", "CRUS": "Cirrus Logic",
    "MTSI": "MACOM Technology", "ONTO": "Onto Innovation",
    "RMBS": "Rambus", "SYNA": "Synaptics",
    "PSTG": "Pure Storage", "ESTC": "Elastic",
    "CFLT": "Confluent", "S": "SentinelOne",
    "MNDY": "Monday.com", "GTLB": "GitLab",
    "PATH": "UiPath", "AI": "C3.ai", "BBAI": "BigBear.ai",
    "IONQ": "IonQ", "RGTI": "Rigetti Computing",
    "APP": "AppLovin", "U": "Unity Software",
    "RBLX": "Roblox", "TTWO": "Take-Two Interactive",
    "EA": "Electronic Arts", "ATVI": "Activision Blizzard",
    # Consumer / E-Commerce / Internet
    "AMZN": "Amazon", "TSLA": "Tesla", "NFLX": "Netflix",
    "BKNG": "Booking Holdings", "UBER": "Uber", "LYFT": "Lyft",
    "ABNB": "Airbnb", "DASH": "DoorDash", "GRAB": "Grab Holdings",
    "SE": "Sea Limited", "MELI": "MercadoLibre", "JD": "JD.com",
    "PDD": "PDD Holdings", "BABA": "Alibaba", "BIDU": "Baidu",
    "NTES": "NetEase", "TCOM": "Trip.com", "WMT": "Walmart",
    "COST": "Costco", "TGT": "Target", "HD": "Home Depot",
    "LOW": "Lowe's", "DG": "Dollar General", "DLTR": "Dollar Tree",
    "ROST": "Ross Stores", "TJX": "TJX Companies",
    "BBY": "Best Buy", "EBAY": "eBay", "ETSY": "Etsy",
    "W": "Wayfair", "CHWY": "Chewy", "SHOP": "Shopify",
    "SQ": "Block Inc", "PYPL": "PayPal", "COIN": "Coinbase",
    "HOOD": "Robinhood", "SOFI": "SoFi Technologies",
    "AFRM": "Affirm", "UPST": "Upstart",
    "SPOT": "Spotify", "SNAP": "Snap Inc", "PINS": "Pinterest",
    "MTCH": "Match Group", "ROKU": "Roku", "TTD": "The Trade Desk",
    "MGNI": "Magnite", "DV": "DoubleVerify", "IAS": "Integral Ad Science",
    "NKE": "Nike", "LULU": "Lululemon", "UAA": "Under Armour",
    "DECK": "Deckers Outdoor", "CROX": "Crocs", "ONON": "On Holding",
    "BIRK": "Birkenstock", "SKX": "Skechers",
    "DIS": "Walt Disney", "CMCSA": "Comcast", "NWSA": "News Corp A",
    "PARA": "Paramount Global", "WBD": "Warner Bros Discovery",
    "FOXA": "Fox Corp A", "LYV": "Live Nation",
    "SBUX": "Starbucks", "MCD": "McDonald's", "CMG": "Chipotle",
    "YUM": "Yum! Brands", "DPZ": "Domino's", "QSR": "Restaurant Brands",
    "WING": "Wingstop", "SHAK": "Shake Shack", "CAVA": "Cava Group",
    "KO": "Coca-Cola", "PEP": "PepsiCo", "MNST": "Monster Beverage",
    "CELH": "Celsius Holdings", "KDP": "Keurig Dr Pepper",
    "STZ": "Constellation Brands", "SAM": "Boston Beer",
    "BUD": "Anheuser-Busch InBev", "DEO": "Diageo", "TAP": "Molson Coors",
    "PG": "Procter & Gamble", "CL": "Colgate-Palmolive",
    "KMB": "Kimberly-Clark", "CHD": "Church & Dwight",
    "EL": "Estee Lauder", "COTY": "Coty",
    "MO": "Altria", "PM": "Philip Morris", "BTI": "British American Tobacco",
    "HSY": "Hershey", "MDLZ": "Mondelez", "GIS": "General Mills",
    "K": "Kellanova", "CPB": "Campbell Soup", "SJM": "JM Smucker",
    "HRL": "Hormel Foods", "TSN": "Tyson Foods", "CAG": "Conagra",
    "KHC": "Kraft Heinz", "ADM": "Archer-Daniels-Midland",
    "BG": "Bunge", "INGR": "Ingredion",
    # Financials
    "JPM": "JPMorgan Chase", "BAC": "Bank of America",
    "WFC": "Wells Fargo", "C": "Citigroup", "GS": "Goldman Sachs",
    "MS": "Morgan Stanley", "SCHW": "Charles Schwab",
    "BLK": "BlackRock", "BX": "Blackstone", "KKR": "KKR & Co",
    "APO": "Apollo Global", "ARES": "Ares Management",
    "BRK-B": "Berkshire Hathaway B", "V": "Visa", "MA": "Mastercard",
    "AXP": "American Express", "DFS": "Discover Financial",
    "COF": "Capital One", "SYF": "Synchrony Financial",
    "USB": "US Bancorp", "PNC": "PNC Financial",
    "TFC": "Truist Financial", "FITB": "Fifth Third Bancorp",
    "HBAN": "Huntington Bancshares", "KEY": "KeyCorp",
    "RF": "Regions Financial", "CFG": "Citizens Financial",
    "MTB": "M&T Bank", "ZION": "Zions Bancorp",
    "SIVB": "SVB Financial", "FRC": "First Republic",
    "ALLY": "Ally Financial", "NYCB": "New York Community Bancorp",
    "WAL": "Western Alliance", "PACW": "PacWest Bancorp",
    "FHN": "First Horizon",
    "ICE": "Intercontinental Exchange", "CME": "CME Group",
    "NDAQ": "Nasdaq Inc", "CBOE": "Cboe Global Markets",
    "SPGI": "S&P Global", "MCO": "Moody's", "MSCI": "MSCI Inc",
    "FIS": "Fidelity National", "FISV": "Fiserv", "GPN": "Global Payments",
    "AJG": "Arthur J Gallagher", "MMC": "Marsh McLennan",
    "AON": "Aon", "WTW": "Willis Towers Watson",
    "AIG": "AIG", "MET": "MetLife", "PRU": "Prudential Financial",
    "AFL": "Aflac", "TRV": "Travelers", "CB": "Chubb",
    "ALL": "Allstate", "PGR": "Progressive",
    "HIG": "Hartford Financial", "CINF": "Cincinnati Financial",
    "RJF": "Raymond James", "LPLA": "LPL Financial",
    "IBKR": "Interactive Brokers", "MKTX": "MarketAxess",
    "VIRT": "Virtu Financial",
    # Healthcare / Biotech / Pharma
    "UNH": "UnitedHealth", "JNJ": "Johnson & Johnson",
    "LLY": "Eli Lilly", "ABBV": "AbbVie", "MRK": "Merck",
    "PFE": "Pfizer", "TMO": "Thermo Fisher", "ABT": "Abbott Labs",
    "DHR": "Danaher", "BMY": "Bristol-Myers Squibb",
    "AMGN": "Amgen", "GILD": "Gilead Sciences",
    "REGN": "Regeneron", "VRTX": "Vertex Pharma",
    "ISRG": "Intuitive Surgical", "SYK": "Stryker",
    "BSX": "Boston Scientific", "MDT": "Medtronic",
    "EW": "Edwards Lifesciences", "ZBH": "Zimmer Biomet",
    "BDX": "Becton Dickinson", "BAX": "Baxter",
    "HOLX": "Hologic", "IDXX": "IDEXX Labs",
    "IQV": "IQVIA", "A": "Agilent Technologies",
    "WAT": "Waters Corp", "MTD": "Mettler-Toledo",
    "DXCM": "DexCom", "PODD": "Insulet", "ALGN": "Align Technology",
    "TECH": "Bio-Techne", "MRNA": "Moderna",
    "BNTX": "BioNTech", "AZN": "AstraZeneca (US)",
    "NVO": "Novo Nordisk (US)", "GSK": "GSK plc",
    "SNY": "Sanofi (US)", "NVS": "Novartis (US)",
    "HCA": "HCA Healthcare", "ELV": "Elevance Health",
    "CI": "Cigna", "CNC": "Centene", "HUM": "Humana",
    "MOH": "Molina Healthcare", "CVS": "CVS Health",
    "WBA": "Walgreens Boots", "MCK": "McKesson",
    "CAH": "Cardinal Health", "ABC": "AmerisourceBergen",
    "BIIB": "Biogen", "ALNY": "Alnylam", "BMRN": "BioMarin",
    "EXAS": "Exact Sciences", "ILMN": "Illumina",
    "SGEN": "Seagen", "INCY": "Incyte", "ARGS": "Argus",
    "HZNP": "Horizon Therapeutics", "JAZZ": "Jazz Pharma",
    "NBIX": "Neurocrine Bio", "PCVX": "Vaxcyte",
    "UTHR": "United Therapeutics", "RARE": "Ultragenyx",
    "IONS": "Ionis Pharma", "SRPT": "Sarepta Therapeutics",
    "LEGN": "Legend Biotech", "CRSP": "CRISPR Therapeutics",
    "BEAM": "Beam Therapeutics", "NTLA": "Intellia Therapeutics",
    "EDIT": "Editas Medicine",
    # Industrials
    "GE": "GE Aerospace", "HON": "Honeywell", "RTX": "RTX Corp",
    "BA": "Boeing", "LMT": "Lockheed Martin", "GD": "General Dynamics",
    "NOC": "Northrop Grumman", "LHX": "L3Harris",
    "HII": "Huntington Ingalls", "TDG": "TransDigm",
    "HWM": "Howmet Aerospace",
    "CAT": "Caterpillar", "DE": "Deere & Co",
    "EMR": "Emerson Electric", "ROK": "Rockwell Automation",
    "ETN": "Eaton Corp", "PH": "Parker Hannifin",
    "ITW": "Illinois Tool Works", "MMM": "3M",
    "SWK": "Stanley Black & Decker", "IR": "Ingersoll Rand",
    "DOV": "Dover Corp", "AME": "AMETEK",
    "UNP": "Union Pacific", "CSX": "CSX Corp",
    "NSC": "Norfolk Southern", "CNI": "Canadian National Railway",
    "CP": "Canadian Pacific Kansas City",
    "UPS": "UPS", "FDX": "FedEx",
    "DAL": "Delta Air Lines", "UAL": "United Airlines",
    "AAL": "American Airlines", "LUV": "Southwest Airlines",
    "ALK": "Alaska Air", "JBLU": "JetBlue",
    "SAVE": "Spirit Airlines", "HA": "Hawaiian Airlines",
    "JBHT": "J.B. Hunt", "LSTR": "Landstar", "ODFL": "Old Dominion",
    "XPO": "XPO Inc", "SAIA": "Saia Inc",
    "GWW": "Grainger", "FAST": "Fastenal", "AOS": "A.O. Smith",
    "JCI": "Johnson Controls", "CARR": "Carrier Global",
    "TT": "Trane Technologies", "LII": "Lennox International",
    "SNA": "Snap-on", "GNRC": "Generac",
    "WM": "Waste Management", "RSG": "Republic Services",
    "VRSK": "Verisk Analytics",
    # Energy
    "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips",
    "EOG": "EOG Resources", "SLB": "Schlumberger",
    "MPC": "Marathon Petroleum", "VLO": "Valero Energy",
    "PSX": "Phillips 66", "PXD": "Pioneer Natural Resources",
    "OXY": "Occidental Petroleum", "DVN": "Devon Energy",
    "FANG": "Diamondback Energy", "HAL": "Halliburton",
    "BKR": "Baker Hughes", "OKE": "ONEOK",
    "WMB": "Williams Companies", "KMI": "Kinder Morgan",
    "ET": "Energy Transfer", "EPD": "Enterprise Products",
    "MPLX": "MPLX LP", "TRGP": "Targa Resources",
    "CTRA": "Coterra Energy", "EQT": "EQT Corp",
    "AR": "Antero Resources", "RRC": "Range Resources",
    "SWN": "Southwestern Energy", "CHK": "Chesapeake Energy",
    "APA": "APA Corp", "MRO": "Marathon Oil",
    "HES": "Hess Corp", "DINO": "HF Sinclair",
    # Real Estate / REITs
    "AMT": "American Tower", "PLD": "Prologis",
    "CCI": "Crown Castle", "EQIX": "Equinix",
    "DLR": "Digital Realty", "PSA": "Public Storage",
    "O": "Realty Income", "WELL": "Welltower",
    "SPG": "Simon Property", "VICI": "VICI Properties",
    "AVB": "AvalonBay", "EQR": "Equity Residential",
    "VTR": "Ventas", "ARE": "Alexandria Real Estate",
    "MAA": "Mid-America Apartment", "UDR": "UDR Inc",
    "ESS": "Essex Property", "INVH": "Invitation Homes",
    # Utilities
    "NEE": "NextEra Energy", "SO": "Southern Co",
    "DUK": "Duke Energy", "D": "Dominion Energy",
    "AEP": "American Electric Power", "EXC": "Exelon",
    "SRE": "Sempra", "XEL": "Xcel Energy",
    "ED": "Consolidated Edison", "WEC": "WEC Energy",
    "ES": "Eversource", "AES": "AES Corp",
    "AWK": "American Water Works", "CEG": "Constellation Energy",
    "VST": "Vistra Corp", "NRG": "NRG Energy",
    # Telecom / Media
    "T": "AT&T", "VZ": "Verizon", "TMUS": "T-Mobile US",
    "CHTR": "Charter Communications", "LBRDA": "Liberty Broadband A",
    # Autos
    "F": "Ford Motor", "GM": "General Motors",
    "RIVN": "Rivian", "LCID": "Lucid Motors",
    "LI": "Li Auto", "NIO": "NIO Inc", "XPEV": "XPeng",
    "TM": "Toyota (US)", "HMC": "Honda (US)",
    "STLA": "Stellantis", "RACE": "Ferrari",
    "APTV": "Aptiv", "BWA": "BorgWarner", "ALV.TO": "Autoliv",
    # Materials
    "LIN": "Linde", "APD": "Air Products", "SHW": "Sherwin-Williams",
    "ECL": "Ecolab", "DD": "DuPont", "DOW": "Dow Inc",
    "NEM": "Newmont Mining", "FCX": "Freeport-McMoRan",
    "NUE": "Nucor", "STLD": "Steel Dynamics",
    "CLF": "Cleveland-Cliffs", "X": "United States Steel",
    "AA": "Alcoa", "GOLD": "Barrick Gold", "AEM": "Agnico Eagle",
    "WPM": "Wheaton Precious Metals", "FNV": "Franco-Nevada",
    "RGLD": "Royal Gold", "KGC": "Kinross Gold",
    "PAAS": "Pan American Silver", "AG": "First Majestic Silver",
    "CDE": "Coeur Mining", "HL": "Hecla Mining",
    "TECK": "Teck Resources", "RIO": "Rio Tinto (US)",
    "BHP": "BHP Group (US)", "VALE": "Vale SA (US)",
    "SCCO": "Southern Copper", "MP": "MP Materials",
    "LAC": "Lithium Americas", "ALB": "Albemarle",
    "SQM": "Sociedad Quimica Minera", "LTHM": "Livent",
    "IPI": "Intrepid Potash", "MOS": "Mosaic",
    "NTR": "Nutrien", "CF": "CF Industries",
    "UAN": "CVR Partners", "CTVA": "Corteva Agriscience",
    "FMC": "FMC Corp",
    # Misc / Other S&P & popular
    "ADP": "ADP", "PAYX": "Paychex",
    "CPRT": "Copart", "ORLY": "O'Reilly Automotive",
    "AZO": "AutoZone", "AAP": "Advance Auto Parts",
    "KMX": "CarMax", "CVNA": "Carvana",
    "MAR": "Marriott", "HLT": "Hilton", "H": "Hyatt",
    "RCL": "Royal Caribbean", "CCL": "Carnival Corp",
    "NCLH": "Norwegian Cruise Line", "EXPE": "Expedia",
    "TRIP": "TripAdvisor",
    "CLX": "Clorox", "SPB": "Spectrum Brands",
    "CTAS": "Cintas", "RHI": "Robert Half",
    "IT": "Gartner", "LDOS": "Leidos", "BAH": "Booz Allen Hamilton",
    "SAIC": "SAIC", "PSN": "Parsons",
    "TRMB": "Trimble", "BR": "Broadridge",
    "FLT": "Fleetcor", "WEX": "WEX Inc",

    # EQUITIES – EUROPE
    # Germany (XETRA)
    "SAP": "SAP SE", "SIE.DE": "Siemens", "ALV.DE": "Allianz",
    "DTE.DE": "Deutsche Telekom", "BAS.DE": "BASF",
    "BMW.DE": "BMW", "MBG.DE": "Mercedes-Benz", "VOW3.DE": "Volkswagen",
    "ADS.DE": "Adidas", "MUV2.DE": "Munich Re",
    "DBK.DE": "Deutsche Bank", "IFX.DE": "Infineon",
    "SHL.DE": "Siemens Healthineers", "HEN3.DE": "Henkel",
    "FRE.DE": "Fresenius", "RWE.DE": "RWE",
    "EON.DE": "E.ON", "1COV.DE": "Covestro",
    "MTX.DE": "MTU Aero Engines", "ZAL.DE": "Zalando",
    "HFG.DE": "HelloFresh", "DHER.DE": "Delivery Hero",
    "P911.DE": "Porsche AG", "PAH3.DE": "Porsche SE",
    "PUM.DE": "Puma", "BEI.DE": "Beiersdorf",
    "AIR.DE": "Airbus (DE)", "RHM.DE": "Rheinmetall",
    "HNR1.DE": "Hannover Re", "CON.DE": "Continental",
    "SRT3.DE": "Sartorius", "MRK.DE": "Merck KGaA",
    "BAYN.DE": "Bayer", "FME.DE": "Fresenius Medical Care",
    "SY1.DE": "Symrise", "HEI.DE": "HeidelbergCement",
    "VNA.DE": "Vonovia",
    # Switzerland
    "NESN.SW": "Nestle", "NOVN.SW": "Novartis", "ROG.SW": "Roche",
    "ABBN.SW": "ABB", "SREN.SW": "Swiss Re",
    "UBSG.SW": "UBS", "CSGN.SW": "Credit Suisse",
    "ZURN.SW": "Zurich Insurance", "GIVN.SW": "Givaudan",
    "SGSN.SW": "SGS", "GEBN.SW": "Geberit",
    "LONN.SW": "Lonza", "SIKA.SW": "Sika",
    "SCMN.SW": "Swisscom", "LOGN.SW": "Logitech",
    "ALC.SW": "Alcon", "SLHN.SW": "Swiss Life",
    # France
    "MC.PA": "LVMH", "OR.PA": "L'Oreal", "TTE.PA": "TotalEnergies",
    "SAN.PA": "Sanofi", "AIR.PA": "Airbus",
    "BN.PA": "Danone", "KER.PA": "Kering",
    "RI.PA": "Pernod Ricard", "SU.PA": "Schneider Electric",
    "AI.PA": "Air Liquide", "CS.PA": "AXA",
    "BNP.PA": "BNP Paribas", "GLE.PA": "Societe Generale",
    "CA.PA": "Carrefour", "VIV.PA": "Vivendi",
    "ORA.PA": "Orange", "DG.PA": "Vinci",
    "SGO.PA": "Saint-Gobain", "CAP.PA": "Capgemini",
    "DSY.PA": "Dassault Systemes", "HO.PA": "Thales",
    "RMS.PA": "Hermes",
    # UK
    "SHEL.L": "Shell", "AZN.L": "AstraZeneca",
    "HSBA.L": "HSBC", "ULVR.L": "Unilever", "BP.L": "BP",
    "GSK.L": "GSK", "RIO.L": "Rio Tinto", "GLEN.L": "Glencore",
    "AAL.L": "Anglo American", "BHP.L": "BHP Group (UK)",
    "LLOY.L": "Lloyds Banking", "BARC.L": "Barclays",
    "NWG.L": "NatWest", "STAN.L": "Standard Chartered",
    "LSEG.L": "London Stock Exchange", "DGE.L": "Diageo",
    "RKT.L": "Reckitt Benckiser", "REL.L": "RELX",
    "CPG.L": "Compass Group", "BA.L": "BAE Systems",
    "RR.L": "Rolls-Royce", "VOD.L": "Vodafone",
    "BT-A.L": "BT Group", "NG.L": "National Grid",
    "SSE.L": "SSE plc", "CNA.L": "Centrica",
    "ABF.L": "Associated British Foods", "TSCO.L": "Tesco",
    "SBRY.L": "Sainsbury's",
    # Nordics
    "NOVO-B.CO": "Novo Nordisk", "MAERSK-B.CO": "Maersk",
    "CARL-B.CO": "Carlsberg", "VWS.CO": "Vestas Wind",
    "ORSTED.CO": "Orsted",
    "ERIC-B.ST": "Ericsson", "VOLV-B.ST": "Volvo",
    "ATCO-A.ST": "Atlas Copco", "SEB-A.ST": "SEB",
    "SAND.ST": "Sandvik", "ABB.ST": "ABB (SE)",
    "HM-B.ST": "H&M", "INVE-B.ST": "Investor AB",
    "NOKIA.HE": "Nokia", "UPM.HE": "UPM-Kymmene",
    "STERV.HE": "Stora Enso",
    "NHY.OL": "Norsk Hydro", "EQNR.OL": "Equinor",
    "TEL.OL": "Telenor", "MOWI.OL": "Mowi",
    "YAR.OL": "Yara International",
    # Italy / Spain / Netherlands
    "ENI.MI": "Eni", "ISP.MI": "Intesa Sanpaolo",
    "UCG.MI": "UniCredit", "ENEL.MI": "Enel",
    "STLAM.MI": "Stellantis (MI)", "RACE.MI": "Ferrari (MI)",
    "G.MI": "Generali",
    "ITX.MC": "Inditex", "SAN.MC": "Banco Santander",
    "BBVA.MC": "BBVA", "IBE.MC": "Iberdrola",
    "TEF.MC": "Telefonica", "REP.MC": "Repsol",
    "ASML.AS": "ASML (NL)", "INGA.AS": "ING Group",
    "PHIA.AS": "Philips", "AD.AS": "Ahold Delhaize",
    "UNA.AS": "Unilever (NL)", "HEIA.AS": "Heineken",
    "WKL.AS": "Wolters Kluwer", "DSM.AS": "DSM-Firmenich",
    # Japan (US-listed ADRs)
    "TM": "Toyota", "HMC": "Honda", "SONY": "Sony",
    "MUFG": "Mitsubishi UFJ", "SMFG": "Sumitomo Mitsui",
    "NMR": "Nomura", "MFG": "Mizuho Financial",

    # CRYPTO (100+)
    # Top 20
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "BNB-USD": "BNB",
    "XRP-USD": "Ripple XRP", "SOL-USD": "Solana",
    "ADA-USD": "Cardano", "DOGE-USD": "Dogecoin",
    "TRX-USD": "TRON", "AVAX-USD": "Avalanche",
    "DOT-USD": "Polkadot", "LINK-USD": "Chainlink",
    "MATIC-USD": "Polygon", "TON11419-USD": "Toncoin",
    "SHIB-USD": "Shiba Inu", "DAI-USD": "Dai",
    "LTC-USD": "Litecoin", "BCH-USD": "Bitcoin Cash",
    "ATOM-USD": "Cosmos", "UNI7083-USD": "Uniswap",
    "XLM-USD": "Stellar",
    # DeFi
    "AAVE-USD": "Aave", "MKR-USD": "Maker",
    "CRV-USD": "Curve DAO", "COMP-USD": "Compound",
    "SNX-USD": "Synthetix", "LDO-USD": "Lido DAO",
    "SUSHI-USD": "SushiSwap", "1INCH-USD": "1inch",
    "BAL-USD": "Balancer", "YFI-USD": "Yearn Finance",
    "CAKE-USD": "PancakeSwap", "JOE-USD": "Trader Joe",
    "DYDX-USD": "dYdX", "RPL-USD": "Rocket Pool",
    "FXS-USD": "Frax Share", "PENDLE-USD": "Pendle",
    "GMX-USD": "GMX", "RBN-USD": "Ribbon Finance",
    # Layer 1
    "NEAR-USD": "NEAR Protocol", "APT-USD": "Aptos",
    "SUI20947-USD": "Sui", "SEI-USD": "Sei",
    "ICP-USD": "Internet Computer", "FIL-USD": "Filecoin",
    "HBAR-USD": "Hedera", "ALGO-USD": "Algorand",
    "VET-USD": "VeChain", "EOS-USD": "EOS",
    "FTM-USD": "Fantom", "EGLD-USD": "MultiversX",
    "FLOW-USD": "Flow", "KAVA-USD": "Kava",
    "MINA-USD": "Mina Protocol", "KDA-USD": "Kadena",
    "ONE-USD": "Harmony", "CELO-USD": "Celo",
    "ZIL-USD": "Zilliqa", "ICX-USD": "ICON",
    "ROSE-USD": "Oasis Network", "KAS-USD": "Kaspa",
    "CFX-USD": "Conflux", "INJ-USD": "Injective",
    "TIA-USD": "Celestia", "STX-USD": "Stacks",
    # Layer 2 / Scaling
    "ARB11841-USD": "Arbitrum", "OP-USD": "Optimism",
    "IMX-USD": "Immutable X", "METIS-USD": "Metis",
    "BOBA-USD": "Boba Network", "CELR-USD": "Celer Network",
    "SKL-USD": "SKALE", "LRC-USD": "Loopring",
    "ZKJ-USD": "Polyhedra", "MANTA-USD": "Manta Network",
    # Gaming / Metaverse
    "AXS-USD": "Axie Infinity", "SAND-USD": "The Sandbox",
    "MANA-USD": "Decentraland", "GALA-USD": "Gala Games",
    "ENJ-USD": "Enjin Coin", "ILV-USD": "Illuvium",
    "SUPER-USD": "SuperVerse", "PRIME-USD": "Echelon Prime",
    "RONIN-USD": "Ronin", "WEMIX-USD": "WEMIX",
    "MAGIC-USD": "MAGIC", "YGG-USD": "Yield Guild Games",
    "PIXEL-USD": "Pixels",
    # Privacy
    "XMR-USD": "Monero", "ZEC-USD": "Zcash",
    "SCRT-USD": "Secret", "DASH-USD": "Dash",
    "DCR-USD": "Decred", "FIRO-USD": "Firo",
    # Storage / Compute
    "AR-USD": "Arweave", "RNDR-USD": "Render",
    "THETA-USD": "Theta", "TFUEL-USD": "Theta Fuel",
    "AKT-USD": "Akash Network", "FET-USD": "Fetch.ai",
    "AGIX-USD": "SingularityNET", "OCEAN-USD": "Ocean Protocol",
    "GRT-USD": "The Graph", "STORJ-USD": "Storj",
    "SC-USD": "Siacoin",
    # Infrastructure / Oracle
    "QNT-USD": "Quant", "BAND-USD": "Band Protocol",
    "API3-USD": "API3", "TRB-USD": "Tellor",
    "PYTH-USD": "Pyth Network", "JUP-USD": "Jupiter",
    "W-USD": "Wormhole",
    # Meme / Social
    "PEPE-USD": "Pepe", "FLOKI-USD": "Floki",
    "WIF-USD": "dogwifhat", "BONK-USD": "Bonk",
    "MEME-USD": "Memecoin", "PEOPLE-USD": "ConstitutionDAO",
    "LUNC-USD": "Terra Classic", "LUNA-USD": "Terra 2.0",
    "ELON-USD": "Dogelon Mars", "BABYDOGE-USD": "Baby Doge Coin",
    # Exchange Tokens
    "CRO-USD": "Cronos", "OKB-USD": "OKB",
    "LEO-USD": "UNUS SED LEO", "HT-USD": "Huobi Token",
    "GT-USD": "Gate Token", "MX-USD": "MX Token",
    # Stablecoins
    "USDT-USD": "Tether", "USDC-USD": "USD Coin",
    "BUSD-USD": "Binance USD", "TUSD-USD": "TrueUSD",
    "FRAX-USD": "Frax", "LUSD-USD": "Liquity USD",
    # Cross-chain / Interop
    "DOT-USD": "Polkadot", "RUNE-USD": "THORChain",
    "ZRX-USD": "0x Protocol", "REN-USD": "Ren",
    "WBTC-USD": "Wrapped Bitcoin",

    # COMMODITIES (Futures)
    # Precious Metals
    "GC=F": "Gold", "SI=F": "Silver",
    "PL=F": "Platinum", "PA=F": "Palladium",
    "MGC=F": "Micro Gold", "SIL=F": "Micro Silver",
    # Energy
    "CL=F": "WTI Crude Oil", "BZ=F": "Brent Crude",
    "NG=F": "Natural Gas", "HO=F": "Heating Oil",
    "RB=F": "RBOB Gasoline", "MCL=F": "Micro WTI Crude",
    "QG=F": "E-mini Natural Gas",
    "TTF=F": "Dutch TTF Gas",
    # Base / Industrial Metals
    "HG=F": "Copper", "ALI=F": "Aluminum",
    "QC=F": "E-mini Copper",
    "NICKEL=F": "Nickel LME", "TIN=F": "Tin LME",
    "ZINC=F": "Zinc LME", "LEAD=F": "Lead LME",
    # Grains
    "ZW=F": "Wheat", "ZC=F": "Corn", "ZS=F": "Soybeans",
    "ZM=F": "Soybean Meal", "ZL=F": "Soybean Oil",
    "ZO=F": "Oats", "ZR=F": "Rough Rice",
    "KE=F": "KC HRW Wheat", "MWE=F": "Minneapolis Wheat",
    # Softs
    "KC=F": "Coffee", "SB=F": "Sugar", "CC=F": "Cocoa",
    "CT=F": "Cotton", "OJ=F": "Orange Juice",
    "RC=F": "Robusta Coffee",
    # Livestock
    "LE=F": "Live Cattle", "GF=F": "Feeder Cattle",
    "HE=F": "Lean Hogs",
    # Lumber / Dairy
    "LBS=F": "Lumber",
    "DC=F": "Class III Milk", "CSC=F": "Cheese",
    # Commodity ETFs & Mining Stocks
    "DBA": "Invesco DB Agriculture", "DBC": "Invesco DB Commodity",
    "GSG": "iShares S&P GSCI", "PDBC": "Invesco Optimum Yield",
    "CORN": "Teucrium Corn", "WEAT": "Teucrium Wheat",
    "SOYB": "Teucrium Soybean", "CANE": "Teucrium Sugar",
    "NIB": "iPath Cocoa", "JO": "iPath Coffee",
    "UNG": "United States Natural Gas", "UGA": "United States Gasoline",
    "PALL": "abrdn Palladium", "PPLT": "abrdn Platinum",
    "COPX": "Global X Copper Miners", "LIT": "Global X Lithium",
    "URA": "Global X Uranium",
    "REMX": "VanEck Rare Earth", "PICK": "iShares MSCI Metals & Mining",
    "XME": "SPDR S&P Metals & Mining", "SIL": "Global X Silver Miners",
    "GDX": "VanEck Gold Miners", "GDXJ": "VanEck Junior Gold Miners",
    "SILJ": "ETFMG Prime Junior Silver",

    # FOREX
    # Majors
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD",
    "USDJPY=X": "USD/JPY", "USDCHF=X": "USD/CHF",
    "AUDUSD=X": "AUD/USD", "NZDUSD=X": "NZD/USD",
    "USDCAD=X": "USD/CAD",
    # Crosses
    "EURGBP=X": "EUR/GBP", "EURJPY=X": "EUR/JPY",
    "GBPJPY=X": "GBP/JPY", "AUDJPY=X": "AUD/JPY",
    "EURCHF=X": "EUR/CHF", "EURAUD=X": "EUR/AUD",
    "GBPCHF=X": "GBP/CHF", "GBPAUD=X": "GBP/AUD",
    "CADJPY=X": "CAD/JPY", "NZDJPY=X": "NZD/JPY",
    "CHFJPY=X": "CHF/JPY", "AUDNZD=X": "AUD/NZD",
    "AUDCAD=X": "AUD/CAD", "GBPCAD=X": "GBP/CAD",
    "EURCAD=X": "EUR/CAD", "EURNZD=X": "EUR/NZD",
    "GBPNZD=X": "GBP/NZD",
    # Emerging
    "USDMXN=X": "USD/MXN", "USDZAR=X": "USD/ZAR",
    "USDTRY=X": "USD/TRY", "USDSEK=X": "USD/SEK",
    "USDNOK=X": "USD/NOK", "USDSGD=X": "USD/SGD",
    "USDHKD=X": "USD/HKD", "USDCNY=X": "USD/CNY",
    "USDINR=X": "USD/INR", "USDKRW=X": "USD/KRW",
    "USDBRL=X": "USD/BRL", "USDPLN=X": "USD/PLN",
    "USDCZK=X": "USD/CZK", "USDHUF=X": "USD/HUF",
    "USDTHB=X": "USD/THB", "USDIDR=X": "USD/IDR",
    "USDPHP=X": "USD/PHP", "USDTWD=X": "USD/TWD",
    "USDARS=X": "USD/ARS", "USDCLP=X": "USD/CLP",
    "USDCOP=X": "USD/COP", "USDPEN=X": "USD/PEN",
    "USDEGP=X": "USD/EGP", "USDNGN=X": "USD/NGN",
    "USDKES=X": "USD/KES", "EURMXN=X": "EUR/MXN",
    "EURTRY=X": "EUR/TRY", "EURSEK=X": "EUR/SEK",
    "EURNOK=X": "EUR/NOK", "EURPLN=X": "EUR/PLN",
    "EURCZK=X": "EUR/CZK", "EURHUF=X": "EUR/HUF",

    # ETFs (breit)
    "SPY": "SPDR S&P 500", "QQQ": "Invesco Nasdaq 100",
    "IWM": "iShares Russell 2000", "DIA": "SPDR Dow Jones",
    "VTI": "Vanguard Total Market", "VOO": "Vanguard S&P 500",
    "IVV": "iShares Core S&P 500", "VT": "Vanguard Total World",
    "EEM": "iShares EM", "EFA": "iShares EAFE",
    "VWO": "Vanguard EM", "VEA": "Vanguard Developed",
    "VGK": "Vanguard FTSE Europe", "EWJ": "iShares MSCI Japan",
    "EWG": "iShares MSCI Germany", "EWU": "iShares MSCI UK",
    "EWQ": "iShares MSCI France", "EWZ": "iShares MSCI Brazil",
    "EWY": "iShares MSCI South Korea", "EWT": "iShares MSCI Taiwan",
    "INDA": "iShares MSCI India", "MCHI": "iShares MSCI China",
    "FXI": "iShares China Large-Cap", "KWEB": "KraneShares CSI China Internet",
    "GLD": "SPDR Gold", "IAU": "iShares Gold",
    "SLV": "iShares Silver", "USO": "US Oil Fund",
    "TLT": "iShares 20+ Treasury", "IEF": "iShares 7-10Y Treasury",
    "SHY": "iShares 1-3Y Treasury", "TIPS": "iShares TIPS",
    "BND": "Vanguard Total Bond", "AGG": "iShares Core Aggregate",
    "HYG": "iShares High Yield", "LQD": "iShares IG Corporate",
    "EMB": "iShares JP Morgan EM Bond",
    "XLF": "Financial Select", "XLE": "Energy Select",
    "XLK": "Tech Select", "XLV": "Healthcare Select",
    "XLI": "Industrial Select", "XLP": "Consumer Staples Select",
    "XLY": "Consumer Discretionary Select", "XLU": "Utilities Select",
    "XLB": "Materials Select", "XLRE": "Real Estate Select",
    "XLC": "Communication Services Select",
    "ARKK": "ARK Innovation", "ARKG": "ARK Genomic",
    "ARKF": "ARK Fintech", "ARKQ": "ARK Autonomous Tech",
    "ARKW": "ARK Next Gen Internet",
    "IBIT": "iShares Bitcoin Trust", "ETHE": "Grayscale Ethereum",
    "FBTC": "Fidelity Wise Origin Bitcoin",
    "SOXX": "iShares Semiconductor", "SMH": "VanEck Semiconductor",
    "HACK": "ETFMG Prime Cyber Security", "SKYY": "First Trust Cloud",
    "ROBO": "ROBO Global Robotics", "BOTZ": "Global X Robotics & AI",
    "TAN": "Invesco Solar", "ICLN": "iShares Global Clean Energy",
    "QCLN": "First Trust NASDAQ Clean Edge Green Energy",
    "JETS": "US Global Jets", "ITA": "iShares US Aerospace",
    "XBI": "SPDR S&P Biotech", "IBB": "iShares Biotechnology",
    "PBW": "Invesco WilderHill Clean Energy",
    "VIG": "Vanguard Dividend Appreciation", "DVY": "iShares Select Dividend",
    "SCHD": "Schwab US Dividend Equity", "HDV": "iShares Core High Dividend",
    "NOBL": "ProShares S&P 500 Dividend Aristocrats",
    # Leveraged / Inverse
    "TQQQ": "ProShares UltraPro QQQ 3x", "SQQQ": "ProShares UltraPro Short QQQ 3x",
    "SPXL": "Direxion S&P 500 Bull 3x", "SPXS": "Direxion S&P 500 Bear 3x",
    "UPRO": "ProShares UltraPro S&P 3x", "SH": "ProShares Short S&P 500",
    "SSO": "ProShares Ultra S&P 500 2x", "SDS": "ProShares UltraShort S&P 2x",
    "QLD": "ProShares Ultra QQQ 2x", "QID": "ProShares UltraShort QQQ 2x",
    "TNA": "Direxion Small Cap Bull 3x", "TZA": "Direxion Small Cap Bear 3x",
    "SOXL": "Direxion Semiconductor Bull 3x", "SOXS": "Direxion Semiconductor Bear 3x",
    "LABU": "Direxion Biotech Bull 3x", "LABD": "Direxion Biotech Bear 3x",
    "NUGT": "Direxion Gold Miners Bull 2x", "DUST": "Direxion Gold Miners Bear 2x",
    "UVXY": "ProShares Ultra VIX Short-Term", "SVXY": "ProShares Short VIX Short-Term",
    "VIXY": "ProShares VIX Short-Term",
}

# Gesamter Symbol-Katalog (flache Liste, sortiert)
SYMBOL_CATALOG: list[str] = sorted(SYMBOL_NAMES.keys())

@st.cache_data(ttl=30, show_spinner=False)   # 30-Sekunden Cache
def fetch_quotes(symbols: List[str]) -> Dict[str, Dict]:
    """
    Gibt für jedes Symbol zurück:
      price, change, change_pct, name
    """
    if not symbols:
        return {}

    try:
        data  = yf.download(symbols, period="5d", interval="1d",
                            progress=False, auto_adjust=True)
        close = _close_df(data, symbols)
        if close.empty:
            return {}
        result = {}
        for sym in symbols:
            if sym not in close.columns:
                continue
            series = close[sym].dropna()
            if len(series) < 2:
                continue
            price      = float(series.iloc[-1])
            prev       = float(series.iloc[-2])
            change     = price - prev
            change_pct = (change / prev * 100) if prev else 0
            result[sym] = {
                "price":      price,
                "change":     change,
                "change_pct": change_pct,
                "name":       SYMBOL_NAMES.get(sym, sym),
            }
        return result
    except Exception:
        return {}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Lädt historische OHLCV-Daten für ein Symbol."""
    try:
        df = yf.download(symbol, period=period, interval=interval,
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        # yfinance 1.x liefert auch für einzelne Ticker MultiIndex-Spalten.
        # Für Abwärtskompatibilität mit bestehendem Code (df["Close"] als Series)
        # die obere Ebene entfernen.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return pd.DataFrame()
