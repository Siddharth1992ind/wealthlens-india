import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ── Try importing yfinance ────────────────────────────────────────────────────
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WealthLens India",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #f0f4ff;
    --surface: #ffffff;
    --surface2: #e8eef8;
    --primary: #1a56db;
    --primary2: #1e40af;
    --primary-light: #dbeafe;
    --red: #dc2626;
    --green: #16a34a;
    --blue: #1a56db;
    --text: #0f172a;
    --muted: #64748b;
    --border: #cbd5e1;
    --shadow: 0 2px 12px rgba(26,86,219,0.08);
}
* { box-sizing: border-box; }
.stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px; }
h1,h2,h3 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }

.hero { text-align:center; padding:2.5rem 1rem 1.5rem;
        background:linear-gradient(135deg,#1a56db 0%,#1e40af 50%,#1d4ed8 100%);
        border-radius:20px; margin-bottom:1.5rem;
        box-shadow:0 8px 32px rgba(26,86,219,0.25); }
.hero h1 { font-size:2.8rem; font-weight:900; color:#ffffff !important;
           -webkit-text-fill-color:#ffffff !important; margin:0; }
.hero p { color:rgba(255,255,255,0.8); font-size:1rem; margin-top:0.4rem; }

.stTabs [data-baseweb="tab-list"] { background:#ffffff!important;
    border-radius:12px; padding:4px; gap:4px;
    border:1px solid var(--border); box-shadow:var(--shadow); }
.stTabs [data-baseweb="tab"] { background:transparent!important; color:var(--muted)!important;
    border-radius:8px!important; font-family:'DM Sans',sans-serif!important;
    font-weight:500; padding:8px 18px!important; }
.stTabs [aria-selected="true"] { background:var(--primary)!important; color:#ffffff!important; }
.stTabs [data-baseweb="tab-panel"] { background:transparent!important; padding:1.5rem 0!important; }

.card { background:var(--surface); border:1px solid var(--border); border-radius:16px;
        padding:1.5rem; margin-bottom:1rem; box-shadow:var(--shadow); }
.card-gold { background:linear-gradient(135deg,#eff6ff,#dbeafe); border:1px solid #93c5fd; }

.metric-box { background:#ffffff; border:1px solid var(--border); border-radius:12px;
              padding:1.2rem 1rem; text-align:center; box-shadow:var(--shadow); }
.metric-label { color:var(--muted); font-size:0.72rem; text-transform:uppercase;
                letter-spacing:1px; margin-bottom:0.4rem; }
.metric-value { font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; }
.metric-sub { font-size:0.72rem; margin-top:0.2rem; }
.metric-green { color:var(--green); }
.metric-red { color:var(--red); }
.metric-gold { color:#d97706; }
.metric-blue { color:var(--blue); }

.compare-table { width:100%; border-collapse:collapse; font-size:0.88rem; }
.compare-table th { background:var(--primary); padding:0.75rem 1rem; text-align:left;
                    color:#ffffff; font-weight:600; font-size:0.72rem;
                    text-transform:uppercase; letter-spacing:1px; }
.compare-table td { padding:0.75rem 1rem; border-bottom:1px solid var(--border);
                    color:var(--text); background:#ffffff; }
.compare-table tr:hover td { background:#eff6ff; }
.compare-table tr:last-child td { border-bottom:none; }
.bad { color:var(--red); font-weight:600; }
.good { color:var(--green); font-weight:600; }
.neutral { color:#d97706; font-weight:600; }

.stButton>button { background:linear-gradient(135deg,var(--primary),var(--primary2))!important;
    color:#ffffff!important; font-weight:700!important; border:none!important;
    border-radius:10px!important; padding:0.6rem 2rem!important;
    font-family:'DM Sans',sans-serif!important; font-size:1rem!important; width:100%;
    box-shadow:0 4px 12px rgba(26,86,219,0.3)!important; }
.stButton>button:hover { transform:translateY(-1px);
    box-shadow:0 8px 24px rgba(26,86,219,0.4)!important; }

.insight-box { background:linear-gradient(135deg,#f0fdf4,#dcfce7);
    border:1px solid #86efac; border-left:4px solid var(--green);
    border-radius:12px; padding:1.2rem 1.5rem; margin:1rem 0;
    font-size:0.92rem; line-height:1.7; color:#14532d; }
.warning-box { background:linear-gradient(135deg,#fff1f2,#ffe4e6);
    border:1px solid #fca5a5; border-left:4px solid var(--red);
    border-radius:12px; padding:1.2rem 1.5rem; margin:1rem 0;
    font-size:0.92rem; line-height:1.7; color:#7f1d1d; }
.info-box { background:linear-gradient(135deg,#eff6ff,#dbeafe);
    border:1px solid #93c5fd; border-left:4px solid var(--blue);
    border-radius:12px; padding:1rem 1.5rem; margin:0.8rem 0;
    font-size:0.88rem; line-height:1.6; color:#1e3a8a; }

.section-header { font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:700;
    color:var(--primary); margin:1.5rem 0 1rem; padding-bottom:0.4rem;
    border-bottom:3px solid var(--primary); display:inline-block; }

.stock-row { background:#ffffff; border:1px solid var(--border);
    border-radius:10px; padding:0.8rem 1rem; margin:0.4rem 0;
    display:flex; justify-content:space-between; align-items:center;
    box-shadow:var(--shadow); }

.subscribe-banner { background:linear-gradient(135deg,#1a56db,#1e40af,#1d4ed8);
    border:2px solid #93c5fd; border-radius:20px; padding:2rem;
    text-align:center; margin-top:2rem;
    box-shadow:0 8px 32px rgba(26,86,219,0.3); }
.subscribe-banner h2 { color:#ffffff; font-size:1.8rem; margin-bottom:0.5rem; }
.subscribe-banner p { color:rgba(255,255,255,0.85); }

.ticker { background:#ffffff; border:1px solid var(--border); border-radius:10px;
    padding:0.7rem 1.2rem; font-size:0.85rem;
    display:flex; justify-content:space-between; align-items:center;
    margin:0.3rem 0; box-shadow:var(--shadow); color:var(--text); }

.stNumberInput input, .stTextInput input, .stSelectbox select {
    background:#ffffff!important; border:1px solid var(--border)!important;
    color:var(--text)!important; border-radius:8px!important; }

.nse-badge { display:inline-block; background:#dcfce7; border:1px solid #86efac;
    color:#15803d; font-size:0.7rem; padding:2px 8px; border-radius:10px; margin-left:6px; }
.sim-badge { display:inline-block; background:#fef9c3; border:1px solid #fde047;
    color:#a16207; font-size:0.7rem; padding:2px 8px; border-radius:10px; margin-left:6px; }
</style>
""", unsafe_allow_html=True)

# ── NSE Stock Universe ────────────────────────────────────────────────────────
# Comprehensive list of popular NSE stocks with Yahoo Finance tickers
NSE_STOCKS = {
    # ── NIFTY 50 ───────────────────────────────────────────────────────────
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Axis Bank": "AXISBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Titan Company": "TITAN.NS",
    "Nestle India": "NESTLEIND.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Tech Mahindra": "TECHM.NS",
    "Power Grid": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Grasim Industries": "GRASIM.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "ONGC": "ONGC.NS",
    "Coal India": "COALINDIA.NS",
    "Cipla": "CIPLA.NS",
    "Dr Reddy's": "DRREDDY.NS",
    "Divis Labs": "DIVISLAB.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Britannia": "BRITANNIA.NS",
    "Shree Cement": "SHREECEM.NS",
    "Hindalco": "HINDALCO.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "SBI": "SBIN.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "M&M": "M&M.NS",
    "BPCL": "BPCL.NS",
    "Jio Financial Services": "JIOFIN.NS",
    "Trent": "TRENT.NS",
    "BEL": "BEL.NS",
    # ── BANKING & FINANCE ──────────────────────────────────────────────────
    "SBI Life Insurance": "SBILIFE.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "ICICI Prudential Life": "ICICIPRULI.NS",
    "ICICI Lombard General": "ICICIGI.NS",
    "LIC": "LICI.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Canara Bank": "CANBK.NS",
    "PNB": "PNB.NS",
    "Indian Bank": "INDIANB.NS",
    "Union Bank of India": "UNIONBANK.NS",
    "Bank of India": "BANKINDIA.NS",
    "Bank of Maharashtra": "MAHABANK.NS",
    "Central Bank": "CENTRALBK.NS",
    "UCO Bank": "UCOBANK.NS",
    "Indian Overseas Bank": "IOB.NS",
    "Federal Bank": "FEDERALBNK.NS",
    "IDFC First Bank": "IDFCFIRSTB.NS",
    "AU Small Finance Bank": "AUBANK.NS",
    "Equitas Small Finance": "EQUITASBNK.NS",
    "Ujjivan Small Finance": "UJJIVANSFB.NS",
    "Jana Small Finance": "JANA.NS",
    "Suryoday Small Finance": "SURYODAY.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS",
    "Manappuram Finance": "MANAPPURAM.NS",
    "Cholamandalam Finance": "CHOLAFIN.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "L&T Finance": "LTF.NS",
    "Bajaj Holdings": "BAJAJHLDNG.NS",
    "PFC": "PFC.NS",
    "REC Limited": "RECLTD.NS",
    "IRFC": "IRFC.NS",
    "HUDCO": "HUDCO.NS",
    "Max Financial Services": "MFSL.NS",
    "Aditya Birla Capital": "ABCAPITAL.NS",
    "360 One (IIFL Wealth)": "360ONE.NS",
    "Nippon Life India AMC": "NAM-INDIA.NS",
    "HDFC AMC": "HDFCAMC.NS",
    "UTI AMC": "UTIAMC.NS",
    "Angel One": "ANGELONE.NS",
    "5Paisa Capital": "5PAISA.NS",
    "IIFL Finance": "IIFL.NS",
    "Piramal Enterprises": "PEL.NS",
    "Sundaram Finance": "SUNDARMFIN.NS",
    "M&M Financial": "M&MFIN.NS",
    "Repco Home Finance": "REPCOHOME.NS",
    "Can Fin Homes": "CANFINHOME.NS",
    "Home First Finance": "HOMEFIRST.NS",
    "Aavas Financiers": "AAVAS.NS",
    "Aptus Value Housing": "APTUS.NS",
    # ── IT & TECHNOLOGY ────────────────────────────────────────────────────
    "Mphasis": "MPHASIS.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "LTIMindtree": "LTIM.NS",
    "L&T Technology Services": "LTTS.NS",
    "Coforge": "COFORGE.NS",
    "Oracle Financial Services": "OFSS.NS",
    "Tata Elxsi": "TATAELXSI.NS",
    "KPIT Technologies": "KPITTECH.NS",
    "Cyient": "CYIENT.NS",
    "Zensar Technologies": "ZENSARTECH.NS",
    "Mastek": "MASTEK.NS",
    "Sonata Software": "SONATSOFTW.NS",
    "Intellect Design Arena": "INTELLECT.NS",
    "Newgen Software": "NEWGEN.NS",
    "Happiest Minds": "HAPPSTMNDS.NS",
    "Birlasoft": "BSOFT.NS",
    "Hexaware Technologies": "HEXAWARE.NS",
    "Rategain Travel Tech": "RATEGAIN.NS",
    "Zaggle Prepaid": "ZAGGLE.NS",
    "CE Info Systems (MapmyIndia)": "MAPMYINDIA.NS",
    "Firstsource Solutions": "FSL.NS",
    "EXL Service": "EXLSERVICE.NS",
    "Majesco": "MAJESCO.NS",
    "3i Infotech": "3IINFOLTD.NS",
    "Tanla Platforms": "TANLA.NS",
    "Route Mobile": "ROUTE.NS",
    "Infibeam Avenues": "INFIBEAM.NS",
    # ── PHARMA & HEALTHCARE ────────────────────────────────────────────────
    "Aurobindo Pharma": "AUROPHARMA.NS",
    "Lupin": "LUPIN.NS",
    "Alkem Laboratories": "ALKEM.NS",
    "Torrent Pharmaceuticals": "TORNTPHARM.NS",
    "Ipca Laboratories": "IPCALAB.NS",
    "Biocon": "BIOCON.NS",
    "Glenmark Pharmaceuticals": "GLENMARK.NS",
    "Abbott India": "ABBOTINDIA.NS",
    "Pfizer India": "PFIZER.NS",
    "Sanofi India": "SANOFI.NS",
    "Cadila Healthcare (Zydus)": "ZYDUSLIFE.NS",
    "Mankind Pharma": "MANKIND.NS",
    "Eris Lifesciences": "ERIS.NS",
    "Ajanta Pharma": "AJANTPHARM.NS",
    "J.B. Chemicals": "JBCHEPHARM.NS",
    "Granules India": "GRANULES.NS",
    "Shilpa Medicare": "SHILPAMED.NS",
    "Aarti Drugs": "AARTIDRUGS.NS",
    "Suven Pharmaceuticals": "SUVENPHAR.NS",
    "Solara Active Pharma": "SOLARA.NS",
    "Laurus Labs": "LAURUSLABS.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Piramal Pharma": "PPLPHARMA.NS",
    "Max Healthcare": "MAXHEALTH.NS",
    "Fortis Healthcare": "FORTIS.NS",
    "Narayana Hrudayalaya": "NH.NS",
    "Krishna Institute (KIMS)": "KIMS.NS",
    "Aster DM Healthcare": "ASTERDM.NS",
    "Metropolis Healthcare": "METROPOLIS.NS",
    "Dr Lal PathLabs": "LALPATHLAB.NS",
    "Thyrocare Technologies": "THYROCARE.NS",
    "Vijaya Diagnostic": "VIJAYA.NS",
    "Krsnaa Diagnostics": "KRSNAA.NS",
    "Poly Medicure": "POLYMED.NS",
    "Syngene International": "SYNGENE.NS",
    "Denta Water": "DENTA.NS",
    # ── FMCG & CONSUMER ────────────────────────────────────────────────────
    "Dabur India": "DABUR.NS",
    "Godrej Consumer Products": "GODREJCP.NS",
    "Marico": "MARICO.NS",
    "Emami": "EMAMILTD.NS",
    "Colgate Palmolive India": "COLPAL.NS",
    "Procter & Gamble Hygiene": "PGHH.NS",
    "Gillette India": "GILLETTE.NS",
    "Jyothy Labs": "JYOTHYLAB.NS",
    "Varun Beverages": "VBL.NS",
    "United Breweries": "UBL.NS",
    "United Spirits": "MCDOWELL-N.NS",
    "Radico Khaitan": "RADICO.NS",
    "CCL Products": "CCL.NS",
    "Tata Coffee": "TATACOFFEE.NS",
    "Jubilant FoodWorks": "JUBLFOOD.NS",
    "Devyani International": "DEVYANI.NS",
    "Westlife Foodworld": "WESTLIFE.NS",
    "Sapphire Foods": "SAPPHIRE.NS",
    "Mrs Bectors Food": "BECTORFOOD.NS",
    "Bikaji Foods": "BIKAJI.NS",
    "Prataap Snacks": "DIAMONDYD.NS",
    "DFM Foods": "DFMFOODS.NS",
    "Heritage Foods": "HERITGFOOD.NS",
    "Hatsun Agro": "HATSUN.NS",
    "Parag Milk Foods": "PARAGMILK.NS",
    "Prabhat Dairy": "PRABHAT.NS",
    # ── AUTO & AUTO ANCILLARY ──────────────────────────────────────────────
    "Ashok Leyland": "ASHOKLEY.NS",
    "TVS Motor Company": "TVSMOTOR.NS",
    "Tata Motors DVR": "TATAMTRDVR.NS",
    "Escorts Kubota": "ESCORTS.NS",
    "Force Motors": "FORCEMOT.NS",
    "SML Isuzu": "SMLISUZU.NS",
    "Motherson Sumi Wiring": "MSUMI.NS",
    "Bosch India": "BOSCHLTD.NS",
    "MRF": "MRF.NS",
    "Apollo Tyres": "APOLLOTYRE.NS",
    "CEAT": "CEATLTD.NS",
    "Balkrishna Industries": "BALKRISIND.NS",
    "JK Tyre": "JKTYRE.NS",
    "Minda Industries": "MINDAIND.NS",
    "Sona BLW Precision": "SONACOMS.NS",
    "Endurance Technologies": "ENDURANCE.NS",
    "Bharat Forge": "BHARATFORG.NS",
    "Ramkrishna Forgings": "RKFORGE.NS",
    "Mahindra CIE Automotive": "MAHINDCIE.NS",
    "Sundram Fasteners": "SUNDRMFAST.NS",
    "Schaeffler India": "SCHAEFFLER.NS",
    "SKF India": "SKFINDIA.NS",
    "Timken India": "TIMKEN.NS",
    "Suprajit Engineering": "SUPRAJIT.NS",
    "Lumax Industries": "LUMAXIND.NS",
    "Lumax Auto Technologies": "LUMAXTECH.NS",
    "Minda Corporation": "MINDACORP.NS",
    "Gabriel India": "GABRIEL.NS",
    "Banco Products": "BANCOINDIA.NS",
    "Jamna Auto": "JAMNAAUTO.NS",
    "Exide Industries": "EXIDEIND.NS",
    "Amara Raja Energy": "AMARAJABAT.NS",
    "Atul Auto": "ATULAUTO.NS",
    # ── INFRASTRUCTURE & CAPITAL GOODS ────────────────────────────────────
    "Siemens India": "SIEMENS.NS",
    "ABB India": "ABB.NS",
    "Thermax": "THERMAX.NS",
    "Cummins India": "CUMMINSIND.NS",
    "Voltas": "VOLTAS.NS",
    "Blue Star": "BLUESTAR.NS",
    "Havells India": "HAVELLS.NS",
    "Crompton Greaves Consumer": "CROMPTON.NS",
    "Polycab India": "POLYCAB.NS",
    "KEI Industries": "KEI.NS",
    "Finolex Cables": "FINCABLES.NS",
    "Kalpataru Projects": "KPIL.NS",
    "KEC International": "KEC.NS",
    "Engineers India": "ENGINERSIN.NS",
    "RITES": "RITES.NS",
    "IRCON International": "IRCON.NS",
    "NCC": "NCC.NS",
    "HG Infra Engineering": "HGINFRA.NS",
    "PNC Infratech": "PNCINFRA.NS",
    "Dilip Buildcon": "DBL.NS",
    "G R Infraprojects": "GRINFRA.NS",
    "Ahluwalia Contracts": "AHLUCONT.NS",
    "ITD Cementation": "ITDCEM.NS",
    "PSP Projects": "PSPPROJECT.NS",
    "Techno Electric": "TECHNOE.NS",
    "Sterling and Wilson": "SWSOLAR.NS",
    "Insolation Energy": "INSOLENERG.NS",
    "Waaree Energies": "WAAREEENER.NS",
    "Premier Energies": "PREMIERENE.NS",
    # ── DEFENCE ────────────────────────────────────────────────────────────
    "HAL": "HAL.NS",
    "Bharat Electronics": "BEL.NS",
    "Bharat Dynamics": "BDL.NS",
    "Mazagon Dock": "MAZDOCK.NS",
    "Garden Reach Shipbuilders": "GRSE.NS",
    "Cochin Shipyard": "COCHINSHIP.NS",
    "BEML": "BEML.NS",
    "Data Patterns": "DATAPATTNS.NS",
    "Paras Defence": "PARAS.NS",
    "Zen Technologies": "ZENTEC.NS",
    "Astra Microwave": "ASTRAMICRO.NS",
    "Ideaforge Technology": "IDEAFORGE.NS",
    # ── REAL ESTATE ────────────────────────────────────────────────────────
    "DLF": "DLF.NS",
    "Godrej Properties": "GODREJPROP.NS",
    "Macrotech (Lodha)": "LODHA.NS",
    "Prestige Estates": "PRESTIGE.NS",
    "Sobha": "SOBHA.NS",
    "Brigade Enterprises": "BRIGADE.NS",
    "Sunteck Realty": "SUNTECK.NS",
    "Phoenix Mills": "PHOENIXLTD.NS",
    "Oberoi Realty": "OBEROIRLTY.NS",
    "Puravankara": "PURVA.NS",
    "Mahindra Lifespace": "MAHLIFE.NS",
    "Kolte-Patil": "KOLTEPATIL.NS",
    "Arvind SmartSpaces": "ARVSF.NS",
    "Keystone Realtors": "RUSTOMJEE.NS",
    # ── METALS & MINING ────────────────────────────────────────────────────
    "Vedanta": "VEDL.NS",
    "National Aluminium": "NATIONALUM.NS",
    "Hindustan Zinc": "HINDZINC.NS",
    "NMDC": "NMDC.NS",
    "SAIL": "SAIL.NS",
    "Welspun Corp": "WELCORP.NS",
    "APL Apollo Tubes": "APLAPOLLO.NS",
    "Jindal Steel & Power": "JINDALSTEL.NS",
    "Jindal Stainless": "JSL.NS",
    "Ratnamani Metals": "RATNAMANI.NS",
    "Sandur Manganese": "SANDUMA.NS",
    "MOIL": "MOIL.NS",
    "Gujarat Mineral": "GMDC.NS",
    "Mishra Dhatu Nigam": "MIDHANI.NS",
    "NALCO": "NATIONALUM.NS",
    "Hindustan Copper": "HINDCOPPER.NS",
    "Maharashtra Seamless": "MAHSEAMLES.NS",
    "Shyam Metalics": "SHYAMMETL.NS",
    "Gravita India": "GRAVITA.NS",
    # ── OIL, GAS & ENERGY ──────────────────────────────────────────────────
    "Indian Oil Corporation": "IOC.NS",
    "HPCL": "HINDPETRO.NS",
    "GAIL": "GAIL.NS",
    "Petronet LNG": "PETRONET.NS",
    "Gujarat Gas": "GUJGASLTD.NS",
    "Indraprastha Gas": "IGL.NS",
    "Mahanagar Gas": "MGL.NS",
    "Gujarat State Petronet": "GSPL.NS",
    "Chennai Petroleum": "CHENNPETRO.NS",
    "Mangalore Refinery": "MRPL.NS",
    "Oil India": "OIL.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Adani Total Gas": "ATGL.NS",
    "Torrent Power": "TORNTPOWER.NS",
    "JSW Energy": "JSWENERGY.NS",
    "CESC": "CESC.NS",
    "Tata Power": "TATAPOWER.NS",
    "NHPC": "NHPC.NS",
    "SJVN": "SJVN.NS",
    "THDC India": "THDCIL.NS",
    "NEEPCO": "NEEPCO.NS",
    "Kalpataru Power": "KALYANKJIL.NS",
    # ── CEMENT ─────────────────────────────────────────────────────────────
    "ACC": "ACC.NS",
    "Ambuja Cements": "AMBUJACEM.NS",
    "Dalmia Bharat": "DALBHARAT.NS",
    "JK Cement": "JKCEMENT.NS",
    "Birla Corporation": "BIRLACORPN.NS",
    "Ramco Cements": "RAMCOCEM.NS",
    "JK Lakshmi Cement": "JKLAKSHMI.NS",
    "HeidelbergCement India": "HEIDELBERG.NS",
    "Sagar Cements": "SAGCEM.NS",
    "Star Cement": "STARCEMENT.NS",
    "Orient Cement": "ORIENTCEM.NS",
    "Deccan Cements": "DECCANCE.NS",
    "NCL Industries": "NCLIND.NS",
    # ── CHEMICALS & SPECIALTY ──────────────────────────────────────────────
    "Pidilite Industries": "PIDILITIND.NS",
    "Berger Paints": "BERGEPAINT.NS",
    "Kansai Nerolac Paints": "KANSAINER.NS",
    "Aarti Industries": "AARTIIND.NS",
    "Deepak Nitrite": "DEEPAKNTR.NS",
    "Navin Fluorine": "NAVINFLUOR.NS",
    "Alkyl Amines Chemicals": "ALKYLAMINE.NS",
    "Vinati Organics": "VINATIORGA.NS",
    "SRF Limited": "SRF.NS",
    "Galaxy Surfactants": "GALAXYSURF.NS",
    "Fine Organic Industries": "FINEORG.NS",
    "Sudarshan Chemical": "SUDARSCHEM.NS",
    "Tata Chemicals": "TATACHEM.NS",
    "Balaji Amines": "BALAMINES.NS",
    "Linde India": "LINDEINDIA.NS",
    "Gulf Oil Lubricants": "GULFOILLUB.NS",
    "Castrol India": "CASTROLIND.NS",
    "Chemplast Sanmar": "CHEMPLASTS.NS",
    "Anupam Rasayan": "ANURAS.NS",
    "Rossari Biotech": "ROSSARI.NS",
    "Clean Science": "CLEAN.NS",
    "Neogen Chemicals": "NEOGEN.NS",
    "Ami Organics": "AMIORG.NS",
    "Tatva Chintan Pharma": "TATVA.NS",
    "Archean Chemical": "ARCHEAN.NS",
    "Chemcon Speciality": "CHEMCON.NS",
    "Fineotex Chemical": "FCL.NS",
    # ── RETAIL & CONSUMER DISCRETIONARY ───────────────────────────────────
    "Avenue Supermarts (DMart)": "DMART.NS",
    "Shoppers Stop": "SHOPERSTOP.NS",
    "V-Mart Retail": "VMART.NS",
    "Aditya Birla Fashion": "ABFRL.NS",
    "Vedant Fashions (Manyavar)": "MANYAVAR.NS",
    "Kalyan Jewellers": "KALYANKJIL.NS",
    "Senco Gold": "SENCO.NS",
    "PC Jeweller": "PCJEWELLER.NS",
    "Bata India": "BATAINDIA.NS",
    "Metro Brands": "METROBRAND.NS",
    "Campus Activewear": "CAMPUS.NS",
    "Relaxo Footwears": "RELAXO.NS",
    "Khadim India": "KHADIM.NS",
    "Page Industries": "PAGEIND.NS",
    "KPR Mill": "KPRMILL.NS",
    "Vardhman Textiles": "VTL.NS",
    "Welspun India": "WELSPUNIND.NS",
    "Arvind": "ARVIND.NS",
    "Raymond": "RAYMOND.NS",
    "TCNS Clothing (W)": "TCNSBRANDS.NS",
    "Go Fashion": "GOCOLORS.NS",
    "Cantabil Retail": "CANTABIL.NS",
    "Nihar Info Global": "NHAR.NS",
    "Titan Company": "TITAN.NS",
    "Ethos": "ETHOS.NS",
    "Kalyani Steels": "KALYANIFRG.NS",
    # ── MEDIA & ENTERTAINMENT ──────────────────────────────────────────────
    "Zee Entertainment": "ZEEL.NS",
    "Sun TV Network": "SUNTV.NS",
    "PVR Inox": "PVRINOX.NS",
    "Dish TV": "DISHTV.NS",
    "Nazara Technologies": "NAZARA.NS",
    "Saregama India": "SAREGAMA.NS",
    "TV18 Broadcast": "TV18BRDCST.NS",
    "Network18": "NETWORK18.NS",
    "Hathway Cable": "HATHWAY.NS",
    "Den Networks": "DEN.NS",
    "Tips Music": "TIPSMUSIC.NS",
    # ── TELECOM ────────────────────────────────────────────────────────────
    "Vodafone Idea": "IDEA.NS",
    "MTNL": "MTNL.NS",
    "Indus Towers": "INDUSTOWER.NS",
    "Sterlite Technologies": "STLTECH.NS",
    "HFCL": "HFCL.NS",
    "Tejas Networks": "TEJASNET.NS",
    "ITI Limited": "ITI.NS",
    # ── AGRI & FERTILISERS ─────────────────────────────────────────────────
    "PI Industries": "PIIND.NS",
    "UPL": "UPL.NS",
    "Bayer CropScience": "BAYERCROP.NS",
    "Coromandel International": "COROMANDEL.NS",
    "Chambal Fertilisers": "CHAMBLFERT.NS",
    "Rallis India": "RALLIS.NS",
    "Sumitomo Chemical India": "SUMICHEM.NS",
    "Deepak Fertilisers": "DEEPAKFERT.NS",
    "GNFC": "GNFC.NS",
    "RCF": "RCF.NS",
    "GSFC": "GSFC.NS",
    "National Fertilizers": "NFL.NS",
    "Dhanuka Agritech": "DHANUKA.NS",
    "Sharda Cropchem": "SHARDACROP.NS",
    "Excel Industries": "EXCELINDUS.NS",
    "Insecticides India": "INSECTICID.NS",
    # ── NEW AGE / CONSUMER TECH ────────────────────────────────────────────
    "Zomato": "ZOMATO.NS",
    "Paytm": "PAYTM.NS",
    "Nykaa": "NYKAA.NS",
    "Policybazaar": "POLICYBZR.NS",
    "Delhivery": "DELHIVERY.NS",
    "CarTrade Tech": "CARTRADE.NS",
    "Easy Trip Planners": "EASEMYTRIP.NS",
    "Indiamart Intermesh": "INDIAMART.NS",
    "Just Dial": "JUSTDIAL.NS",
    "Info Edge (Naukri)": "NAUKRI.NS",
    "Matrimony.com": "MATRIMONY.NS",
    "Zaggle Prepaid": "ZAGGLE.NS",
    "CE Info Systems (MapmyIndia)": "MAPMYINDIA.NS",
    "Tracxn Technologies": "TRACXN.NS",
    "Happilo International": "HAPPILO.NS",
    # ── AVIATION & LOGISTICS ───────────────────────────────────────────────
    "IndiGo (InterGlobe)": "INDIGO.NS",
    "SpiceJet": "SPICEJET.NS",
    "Blue Dart Express": "BLUEDART.NS",
    "Container Corp": "CONCOR.NS",
    "Gateway Distriparks": "GATEWAY.NS",
    "TCI Express": "TCIEXP.NS",
    "Mahindra Logistics": "MAHLOG.NS",
    "Allcargo Logistics": "ALLCARGO.NS",
    "VRL Logistics": "VRLLOG.NS",
    "Gati": "GATI.NS",
    "Transport Corporation": "TCI.NS",
    "Shipping Corp of India": "SCI.NS",
    "Great Eastern Shipping": "GESHIP.NS",
    "Essar Shipping": "ESSARSHPNG.NS",
    # ── PAPER, PACKAGING & PRINTING ───────────────────────────────────────
    "ITC (Paperboards)": "ITC.NS",
    "West Coast Paper": "WESTCOAST.NS",
    "JK Paper": "JKPAPER.NS",
    "TNPL": "TNPL.NS",
    "Star Paper Mills": "STARPAPER.NS",
    "Mead Johnson (Reckitt)": "RECKIT.NS",
    "Uflex": "UFLEX.NS",
    "Jindal Poly Films": "JPOLYINVST.NS",
    "Cosmo Films": "COSMOFILMS.NS",
    "Huhtamaki India": "HUHTAMAKI.NS",
    "EPL Limited": "EPL.NS",
    "Mold-Tek Packaging": "MOLDTKPAC.NS",
    # ── HOTELS & TOURISM ───────────────────────────────────────────────────
    "Indian Hotels (Taj)": "INDHOTEL.NS",
    "EIH (Oberoi Hotels)": "EIHOTEL.NS",
    "Lemon Tree Hotels": "LEMONTREE.NS",
    "Chalet Hotels": "CHALET.NS",
    "Royal Orchid Hotels": "ROHLTD.NS",
    "Mahindra Holidays": "MHRIL.NS",
    "Thomas Cook India": "THOMASCOOK.NS",
    "Cox & Kings": "COXANDKNG.NS",
    # ── POWER & RENEWABLES ─────────────────────────────────────────────────
    "Adani Power": "ADANIPOWER.NS",
    "NHPC": "NHPC.NS",
    "SJVN": "SJVN.NS",
    "Waaree Energies": "WAAREEENER.NS",
    "Premier Energies": "PREMIERENE.NS",
    "Inox Wind": "INOXWIND.NS",
    "Suzlon Energy": "SUZLON.NS",
    "Orient Electric": "ORIENTELEC.NS",
    "NTPC Green Energy": "NTPCGREEN.NS",
    "Greenko (unlisted)": "GREENKO.NS",
    # ── GLASS, CERAMICS & BUILDING MATERIALS ──────────────────────────────
    "Kajaria Ceramics": "KAJARIACER.NS",
    "Somany Ceramics": "SOMANYCERA.NS",
    "Asian Granito": "ASIANTILES.NS",
    "Cera Sanitaryware": "CERA.NS",
    "HSIL": "HSIL.NS",
    "Gujarat Pipavav Port": "GPPL.NS",
    "Hindusthan National Glass": "HNG.NS",
    "Borosil Renewables": "BORORENEW.NS",
    "Borosil": "BOROLTD.NS",
    "PG Electroplast": "PGEL.NS",
    "Dixon Technologies": "DIXON.NS",
    "Amber Enterprises": "AMBER.NS",
    "Voltas Beko": "VOLTAS.NS",
    # ── MISCELLANEOUS & CONGLOMERATES ─────────────────────────────────────
    "Tata Investment Corp": "TATAINVEST.NS",
    "Godrej Industries": "GODREJIND.NS",
    "Bombay Burmah": "BBTC.NS",
    "Kesoram Industries": "KESORAMIND.NS",
    "3M India": "3MINDIA.NS",
    "Honeywell Automation": "HONAUT.NS",
    "Hitachi Energy": "POWERINDIA.NS",
    "GE T&D India": "GET&D.NS",
    "Bharat Heavy Electricals": "BHEL.NS",
    "Rail Vikas Nigam": "RVNL.NS",
    "IRCTC": "IRCTC.NS",
    "Indian Railway Finance": "IRFC.NS",
    "NBCC India": "NBCC.NS",
    "NMDC Steel": "NMDCSTEEL.NS",
    "Mishra Dhatu": "MIDHANI.NS",
    "MMTC": "MMTC.NS",
    "MSTC": "MSTC.NS",
    "SCI": "SCI.NS",
    "Balmer Lawrie": "BALMLAWRIE.NS",
    "KIOCL": "KIOCL.NS",
    "MOIL": "MOIL.NS",
    "NALCO": "NATIONALUM.NS",
    "NFL": "NFL.NS",
    # ── ETFs, REITs & InvITs ───────────────────────────────────────────────
    "Nifty 500 (Motilal ETF)": "MO500.NS",
    "Nifty 50 ETF (Nippon BeES)": "NIFTYBEES.NS",
    "Nifty Next 50 ETF (Junior BeES)": "JUNIORBEES.NS",
    "Nifty Midcap 150 ETF (Motilal)": "MOM150.NS",
    "Nifty Bank ETF (Nippon)": "BANKBEES.NS",
    "IT ETF (Nippon)": "ITBEES.NS",
    "Pharma ETF (Nippon)": "PHARMABEES.NS",
    "Nippon India ETF Gold BeES": "GOLDBEES.NS",
    "Motilal Oswal Nasdaq 100 ETF (MON100)": "MON100.NS",
    "SBI Gold ETF": "SBIGETS.NS",
    "Axis Gold ETF": "AXISGOLD.NS",
    "Embassy REIT": "EMBASSY.NS",
    "Mindspace REIT": "MINDSPACE.NS",
    "Nexus Select REIT": "NEXUS.NS",
    "Brookfield REIT": "BIRET.NS",
    "IndiGrid InvIT": "INDIGRID.NS",
    "IRB InvIT": "IRB.NS",
    "Powergrid InvIT": "POWERINVIT.NS",
    "National Highways InvIT": "NHAI.NS",
}

STOCK_NAMES = sorted(NSE_STOCKS.keys())

# ── Sector Mapping ─────────────────────────────────────────────────────────────
SECTOR_MAP = {
    "Reliance Industries": "Energy/Retail",
    "TCS": "IT", "Infosys": "IT", "Wipro": "IT", "HCL Technologies": "IT",
    "Tech Mahindra": "IT", "Mphasis": "IT", "Persistent Systems": "IT",
    "HDFC Bank": "Banking", "ICICI Bank": "Banking", "Axis Bank": "Banking",
    "Kotak Mahindra Bank": "Banking", "IndusInd Bank": "Banking",
    "SBI": "Banking", "Bank of Baroda": "Banking", "Canara Bank": "Banking", "PNB": "Banking",
    "Bajaj Finance": "NBFC", "HDFC Life": "Insurance", "SBI Life Insurance": "Insurance",
    "ICICI Prudential": "Insurance", "LIC": "Insurance",
    "Sun Pharma": "Pharma", "Cipla": "Pharma", "Dr Reddy's": "Pharma", "Divis Labs": "Pharma",
    "Hindustan Unilever": "FMCG", "ITC": "FMCG", "Nestle India": "FMCG",
    "Britannia": "FMCG", "Marico": "FMCG", "Godrej Consumer": "FMCG",
    "Maruti Suzuki": "Auto", "Tata Motors": "Auto", "Bajaj Auto": "Auto",
    "Hero MotoCorp": "Auto", "Eicher Motors": "Auto",
    "Larsen & Toubro": "Infrastructure", "UltraTech Cement": "Cement",
    "Shree Cement": "Cement", "Tata Steel": "Metals", "Hindalco": "Metals",
    "JSW Steel": "Metals", "Vedanta": "Metals",
    "Asian Paints": "Paints", "Berger Paints": "Paints", "Pidilite Industries": "Chemicals",
    "ONGC": "Oil & Gas", "Coal India": "Mining",
    "Power Grid": "Utilities", "NTPC": "Utilities", "Tata Power": "Power",
    "Adani Ports": "Infrastructure", "Adani Enterprises": "Conglomerate",
    "SpiceJet": "Aviation", "IndiGo (InterGlobe)": "Aviation",
    "Zomato": "Consumer Tech", "Paytm": "Fintech", "Nykaa": "Consumer Tech",
    "Policybazaar": "Fintech", "Delhivery": "Logistics",
    "Avenue Supermarts (DMart)": "Retail", "Trent": "Retail",
    "Titan Company": "Jewellery", "Havells India": "Consumer Durables",
    "Crompton Greaves": "Consumer Durables", "Voltas": "Consumer Durables",
    "Zee Entertainment": "Media", "Bharat Forge": "Engineering",
    "PI Industries": "Agro Chemicals",
    "Nippon India ETF Gold BeES": "Gold", "Embassy REIT": "REIT",
    "Mindspace REIT": "REIT", "Nexus Select REIT": "REIT", "Brookfield REIT": "REIT",
    "Nifty 500 (Motilal ETF)": "Index ETF",
    "Motilal Oswal Nasdaq 100 ETF (MON100)": "International ETF",
    "Nifty 50 ETF (Nippon)": "Index ETF",
    "Nifty Next 50 ETF": "Index ETF",
    "Midcap 150 ETF (Motilal)": "Index ETF",
    "SBI Gold ETF": "Gold",
    "IndiGrid InvIT": "InvIT",
    "IRB InvIT": "InvIT",
    "Bharti Airtel": "Telecom",
    "Vodafone Idea": "Telecom",
    "Indus Towers": "Telecom",
    "MTNL": "Telecom",
    "Sterlite Technologies": "Telecom",
    "Bajaj Finserv": "NBFC",
    "Jio Financial": "Fintech",
    "M&M (Mahindra)": "Auto",
    "Ashok Leyland": "Auto",
    "TVS Motor": "Auto",
    "Tata Consumer": "FMCG",
    "Apollo Hospitals": "Healthcare",
    "Max Healthcare": "Healthcare",
    "Fortis Healthcare": "Healthcare",
    "Narayana Hrudayalaya": "Healthcare",
    "Metropolis Healthcare": "Healthcare",
    "Dr Lal PathLabs": "Healthcare",
    "DLF": "Real Estate",
    "Godrej Properties": "Real Estate",
    "Macrotech (Lodha)": "Real Estate",
    "Prestige Estates": "Real Estate",
    "Phoenix Mills": "Real Estate",
    "Oberoi Realty": "Real Estate",
    "Indian Oil": "Oil & Gas",
    "HPCL": "Oil & Gas",
    "BPCL": "Oil & Gas",
    "GAIL": "Oil & Gas",
    "Adani Green Energy": "Renewable Energy",
    "JSW Energy": "Power",
    "Torrent Power": "Power",
    "ACC": "Cement",
    "Ambuja Cements": "Cement",
    "Dalmia Bharat": "Cement",
    "LTIMindtree": "IT",
    "Coforge": "IT",
    "Info Edge (Naukri)": "Consumer Tech",
    "Indiamart Intermesh": "Consumer Tech",
    "IndiGo (InterGlobe)": "Aviation",
    "Blue Dart Express": "Logistics",
    "Container Corp": "Logistics",
    "Dabur India": "FMCG",
    "Emami": "FMCG",
    "Varun Beverages": "FMCG",
    "HAL": "Defence",
    "Bharat Electronics": "Defence",
    "Bharat Dynamics": "Defence",
    "Mazagon Dock": "Defence",
    "Polycab India": "Electricals",
    "Havells India": "Consumer Durables",
    "MRF": "Auto Ancillary",
    "Bosch India": "Auto Ancillary",
    "Motherson Sumi": "Auto Ancillary",
    "Pidilite Industries": "Chemicals",
    "SRF Limited": "Chemicals",
    "Deepak Nitrite": "Chemicals",
    "Aarti Industries": "Chemicals",
    "UPL": "Agro Chemicals",
    "Coromandel International": "Agro Chemicals",
    "Kalyan Jewellers": "Jewellery",
    "PVR Inox": "Entertainment",
    "Sun TV Network": "Media",
}


# ── Helper Functions ──────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_data(ticker_symbol, period="5y"):
    """Fetch real stock data from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        return None, "yfinance not installed"
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return None, f"No data found for {ticker_symbol}"
        hist = hist[['Close']].copy()
        hist.index = pd.to_datetime(hist.index).tz_localize(None)
        return hist, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=3600, show_spinner=False)  
def fetch_multiple_stocks(tickers_dict, period="5y"):
    """Fetch data for multiple stocks and benchmark"""
    results = {}
    errors = {}
    
    all_tickers = list(tickers_dict.values())
    # Add benchmark tickers
    benchmark_tickers = {
        'Nifty500': '^CRSLDX',     # Nifty 500 index
        'Goldbees': 'GOLDBEES.NS',
        'REIT': 'EMBASSY.NS',
    }
    
    for name, ticker in {**tickers_dict, **benchmark_tickers}.items():
        data, error = fetch_stock_data(ticker, period)
        if data is not None:
            results[name] = data['Close']
        else:
            errors[name] = error
    
    if results:
        df = pd.DataFrame(results)
        df = df.ffill().dropna(how='all')
        return df, errors
    return None, errors

def calculate_portfolio_metrics(returns_df, weights):
    """Calculate annualized return, volatility, sharpe, max drawdown"""
    port_returns = (returns_df * weights).sum(axis=1)
    
    ann_return = port_returns.mean() * 252
    ann_vol = port_returns.std() * np.sqrt(252)
    sharpe = (ann_return - 0.065) / ann_vol if ann_vol > 0 else 0
    
    # Max drawdown
    cumulative = (1 + port_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_dd = drawdown.min()
    
    return ann_return, ann_vol, sharpe, max_dd

def run_monte_carlo(ann_return, ann_vol, initial_value, years=5, simulations=1000, seed=42):
    """Run Monte Carlo simulation"""
    np.random.seed(seed)
    days = years * 252
    daily_ret = ann_return / 252
    daily_vol = ann_vol / np.sqrt(252)
    
    paths = np.zeros((simulations, days))
    for i in range(simulations):
        r = np.random.normal(daily_ret, daily_vol, days)
        paths[i] = initial_value * np.cumprod(1 + r)
    
    return paths

def generate_fallback_data(stock_name, period_days=1260):
    """Generate realistic simulated data when real data unavailable"""
    np.random.seed(hash(stock_name) % 1000)
    
    # Different characteristics for different types
    if any(x in stock_name.lower() for x in ['spicejet', 'jet', 'airline']):
        mu, sigma = -0.0004, 0.038
    elif any(x in stock_name.lower() for x in ['gold', 'goldbees']):
        mu, sigma = 0.00045, 0.009
    elif any(x in stock_name.lower() for x in ['reit', 'embassy', 'mindspace', 'nexus']):
        mu, sigma = 0.00032, 0.011
    elif any(x in stock_name.lower() for x in ['nifty', '500', 'index']):
        mu, sigma = 0.00055, 0.013
    elif any(x in stock_name.lower() for x in ['bank', 'finance', 'hdfc', 'icici']):
        mu, sigma = 0.00052, 0.019
    elif any(x in stock_name.lower() for x in ['it', 'tcs', 'infosys', 'wipro', 'hcl', 'tech']):
        mu, sigma = 0.00058, 0.016
    else:
        mu, sigma = 0.00048, 0.018
    
    dates = pd.date_range(end=datetime.today(), periods=period_days, freq='B')
    returns = np.random.normal(mu, sigma, period_days)
    prices = 100 * np.cumprod(1 + returns)
    return pd.Series(prices, index=dates)


# ── Lead Capture ─────────────────────────────────────────────────────────────
def save_lead_to_csv(name, email, phone, source):
    import csv, os
    from datetime import datetime
    filename = "wealthlens_leads.csv"
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp","Name","Email","Phone","Source","Status"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, email, phone, source, "Free"])

def get_leads_df():
    import os
    if os.path.exists("wealthlens_leads.csv"):
        return pd.read_csv("wealthlens_leads.csv")
    return pd.DataFrame(columns=["Timestamp","Name","Email","Phone","Source","Status"])

# ── Razorpay Payment ──────────────────────────────────────────────────────────
RAZORPAY_KEY_ID = "rzp_test_REPLACE_WITH_YOUR_KEY"

def razorpay_button(plan_name, amount_inr, plan_desc, color="#f5c842"):
    import streamlit.components.v1 as components
    uname = st.session_state.get("user_name","")
    uemail = st.session_state.get("user_email","")
    html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <button onclick="pay_{plan_name.replace(' ','')}{amount_inr}()"
      style="background:linear-gradient(135deg,{color},{color}bb);color:#0a0f1e;
             font-weight:700;border:none;border-radius:10px;padding:0.75rem 1.5rem;
             font-size:0.95rem;cursor:pointer;width:100%;margin-top:0.5rem">
      💳 Subscribe — ₹{amount_inr:,}
    </button>
    <div id="ps_{amount_inr}"></div>
    <script>
    function pay_{plan_name.replace(' ','')}{amount_inr}(){{
      var r=new Razorpay({{
        key:"{RAZORPAY_KEY_ID}",amount:{amount_inr*100},currency:"INR",
        name:"WealthLens India",description:"{plan_desc}",
        prefill:{{name:"{uname}",email:"{uemail}"}},
        theme:{{color:"{color}"}},
        handler:function(res){{
          document.getElementById("ps_{amount_inr}").innerHTML=
            "<p style='color:#22c55e;font-weight:700;margin-top:8px'>✅ Payment done! ID: "+res.razorpay_payment_id+"<br>We will activate within 2 hours.</p>";
        }}
      }});r.open();
    }}
    </script>"""
    components.html(html, height=90)

def subscription_section(portfolio_total=2000000):
    fee_pct = round(499*12/portfolio_total*100, 2) if portfolio_total > 0 else 0
    st.markdown(f"""
    <div class="subscribe-banner">
      <h2>📈 Upgrade to Full Access</h2>
      <p>Rebalancing alerts · Tactical allocation · Monthly health reports<br>
      For ₹{portfolio_total/100000:.1f}L portfolio — just <strong>{fee_pct}% of assets annually</strong></p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div style="background:#ffffff;border:2px solid #1a56db;border-radius:16px;padding:1.2rem;text-align:center">
          <div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Monthly</div>
          <div style="color:#f5c842;font-size:2.2rem;font-weight:700;font-family:'Playfair Display',serif">₹499</div>
          <div style="color:#64748b;font-size:0.72rem;margin-bottom:0.8rem">Cancel anytime</div>
          <div style="color:#94a3b8;font-size:0.8rem;text-align:left">✅ Rebalancing signals<br>✅ Portfolio health score<br>✅ Email market updates</div>
        </div>""", unsafe_allow_html=True)
        razorpay_button("Monthly", 499, "WealthLens Monthly Plan", "#f5c842")
    with c2:
        st.markdown("""<div style="background:#ffffff;border:2px solid #16a34a;border-radius:16px;padding:1.2rem;text-align:center;position:relative">
          <div style="position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:#22c55e;color:#0a0f1e;font-size:0.65rem;font-weight:700;padding:2px 12px;border-radius:10px">⭐ BEST VALUE</div>
          <div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Annual</div>
          <div style="color:#22c55e;font-size:2.2rem;font-weight:700;font-family:'Playfair Display',serif">₹3,999</div>
          <div style="color:#64748b;font-size:0.72rem;margin-bottom:0.8rem">₹333/month · Save 33%</div>
          <div style="color:#94a3b8;font-size:0.8rem;text-align:left">✅ Everything in Monthly<br>✅ Quarterly review call<br>✅ Tactical shifts</div>
        </div>""", unsafe_allow_html=True)
        razorpay_button("Annual", 3999, "WealthLens Annual Plan", "#22c55e")
    with c3:
        st.markdown("""<div style="background:#ffffff;border:2px solid #7c3aed;border-radius:16px;padding:1.2rem;text-align:center;position:relative">
          <div style="position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:#a855f7;color:#0a0f1e;font-size:0.65rem;font-weight:700;padding:2px 12px;border-radius:10px">💎 PREMIUM</div>
          <div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Advisory</div>
          <div style="color:#a855f7;font-size:2.2rem;font-weight:700;font-family:'Playfair Display',serif">₹4,999</div>
          <div style="color:#64748b;font-size:0.72rem;margin-bottom:0.8rem">Fully personalised</div>
          <div style="color:#94a3b8;font-size:0.8rem;text-align:left">✅ Monthly 1-on-1 call<br>✅ Custom allocation<br>✅ WhatsApp support</div>
        </div>""", unsafe_allow_html=True)
        razorpay_button("Advisory", 4999, "WealthLens Advisory Plan", "#a855f7")

    st.markdown("""<div style="text-align:center;color:#475569;font-size:0.73rem;margin-top:0.8rem">
      🔒 Secure via Razorpay · UPI / Card / NetBanking · GST invoice provided · Cancel anytime
    </div>""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [
        {'name': 'Reliance Industries', 'amount': 500000},
    ]
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = {}
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'free_user_registered' not in st.session_state:
    st.session_state.free_user_registered = False

# ════════════════════════════════════════════════════════════════════════════
# LANDING PAGE — BlackRock-style professional layout
# ════════════════════════════════════════════════════════════════════════════

if not st.session_state.free_user_registered:

    # ── Top Navigation Bar ──
    st.markdown("""
    <div style="background:#ffffff;border-bottom:2px solid #1a56db;padding:0.8rem 2rem;
                display:flex;justify-content:space-between;align-items:center;
                margin:-1.5rem -2rem 0 -2rem">
        <div style="display:flex;align-items:center;gap:0.6rem">
            <div style="background:#1a56db;color:#fff;font-weight:900;font-size:1.1rem;
                        padding:4px 12px;border-radius:6px;font-family:'Playfair Display',serif">W</div>
            <span style="color:#0f172a;font-weight:700;font-size:1.1rem;
                         font-family:'Playfair Display',serif">WealthLens India</span>
        </div>
        <div style="color:#1a56db;font-size:0.82rem;font-weight:600;
                    background:#eff6ff;padding:4px 14px;border-radius:20px;
                    border:1px solid #bfdbfe">
            🆓 Free Access — Scroll down to register
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Banner ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1a56db 60%,#1e40af 100%);
                padding:5rem 3rem 4rem;margin:0 -2rem;text-align:center;
                border-bottom:4px solid #1a56db">
        <div style="max-width:800px;margin:0 auto">
            <div style="display:inline-block;background:rgba(255,255,255,0.1);
                        border:1px solid rgba(255,255,255,0.3);border-radius:20px;
                        padding:4px 16px;margin-bottom:1.5rem;
                        color:rgba(255,255,255,0.9);font-size:0.78rem;letter-spacing:2px;
                        text-transform:uppercase;font-weight:600">
                CFA-Grade Portfolio Intelligence for India
            </div>
            <h1 style="color:#ffffff;font-size:3.2rem;font-weight:900;margin:0 0 1rem;
                       font-family:'Playfair Display',serif;line-height:1.2">
                Your Portfolio Deserves<br>Institutional Intelligence
            </h1>
            <p style="color:rgba(255,255,255,0.8);font-size:1.15rem;line-height:1.8;
                      max-width:650px;margin:0 auto 2rem">
                Over 150 million Indians invest in equity markets. Fewer than 1% apply 
                institutional-grade asset allocation principles to their portfolio. 
                WealthLens brings the same analytical framework used by global pension 
                funds — directly to your screen. Free.
            </p>
            <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-bottom:2.5rem">
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);
                            border-radius:10px;padding:0.5rem 1.2rem;color:rgba(255,255,255,0.9);
                            font-size:0.85rem">✦ Nobel Prize Research Framework</div>
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);
                            border-radius:10px;padding:0.5rem 1.2rem;color:rgba(255,255,255,0.9);
                            font-size:0.85rem">✦ Real NSE Market Data</div>
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);
                            border-radius:10px;padding:0.5rem 1.2rem;color:rgba(255,255,255,0.9);
                            font-size:0.85rem">✦ 1,000 Monte Carlo Simulations</div>
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);
                            border-radius:10px;padding:0.5rem 1.2rem;color:rgba(255,255,255,0.9);
                            font-size:0.85rem">✦ Personalised Life Stage Planning</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Stats Bar ──
    st.markdown("""
    <div style="background:#1a56db;padding:1.8rem 3rem;margin:0 -2rem;
                display:flex;justify-content:center;gap:5rem;flex-wrap:wrap;
                border-bottom:1px solid #1e40af">
        <div style="text-align:center">
            <div style="color:#ffffff;font-size:2rem;font-weight:900;
                        font-family:'Playfair Display',serif">150M+</div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.78rem;
                        text-transform:uppercase;letter-spacing:1px;margin-top:4px">Indian Demat Accounts</div>
        </div>
        <div style="text-align:center">
            <div style="color:#ffffff;font-size:2rem;font-weight:900;
                        font-family:'Playfair Display',serif">90%+</div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.78rem;
                        text-transform:uppercase;letter-spacing:1px;margin-top:4px">Returns from Asset Allocation*</div>
        </div>
        <div style="text-align:center">
            <div style="color:#ffffff;font-size:2rem;font-weight:900;
                        font-family:'Playfair Display',serif">5</div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.78rem;
                        text-transform:uppercase;letter-spacing:1px;margin-top:4px">Analysis Screens</div>
        </div>
        <div style="text-align:center">
            <div style="color:#ffffff;font-size:2rem;font-weight:900;
                        font-family:'Playfair Display',serif">Free</div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.78rem;
                        text-transform:uppercase;letter-spacing:1px;margin-top:4px">To Get Started</div>
        </div>
    </div>
    <div style="background:#0f172a;padding:0.5rem;text-align:center;margin:0 -2rem">
        <span style="color:rgba(255,255,255,0.4);font-size:0.68rem">*Brinson, Hood & Beebower (1986) — Determinants of Portfolio Performance</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── What We Do Section ──
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 2rem">
        <div style="color:#1a56db;font-size:0.75rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:2px;margin-bottom:0.5rem">WHAT WE DO</div>
        <h2 style="color:#0f172a;font-size:2rem;font-weight:800;margin:0;
                   font-family:'Playfair Display',serif">
            The problem with how India invests
        </h2>
        <p style="color:#475569;font-size:1rem;max-width:600px;margin:1rem auto 0;line-height:1.8">
            Most Indian retail investors make the same critical mistake — they spend 100% of their 
            energy picking individual stocks while ignoring the single factor that drives over 90% 
            of long-term investment returns: asset allocation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_prob, col_soln = st.columns(2)
    with col_prob:
        st.markdown("""
        <div style="background:#fff5f5;border:1px solid #fecaca;border-left:4px solid #dc2626;
                    border-radius:12px;padding:1.5rem;height:100%">
            <div style="color:#dc2626;font-weight:700;font-size:0.8rem;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:1rem">❌ The Typical Indian Portfolio</div>
            <div style="color:#0f172a;font-size:0.92rem;line-height:2">
                • 100% concentrated in 2-5 equity stocks<br>
                • Zero allocation to gold — the ultimate crisis hedge<br>
                • Zero allocation to REITs — missing rental income<br>
                • No rebalancing discipline — drift goes unnoticed<br>
                • Worst-case 5-year outcome: losing 40-50% of wealth<br>
                • Decision-making driven by WhatsApp tips and news
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_soln:
        st.markdown("""
        <div style="background:#f0fdf4;border:1px solid #86efac;border-left:4px solid #16a34a;
                    border-radius:12px;padding:1.5rem;height:100%">
            <div style="color:#16a34a;font-weight:700;font-size:0.8rem;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:1rem">✅ The WealthLens Approach</div>
            <div style="color:#0f172a;font-size:0.92rem;line-height:2">
                • Diversified across Equity, Gold, and REITs<br>
                • Allocation personalised to your age and life stage<br>
                • Monthly rebalancing alerts — exact ₹ amounts<br>
                • Tactical shifts based on live macro signals<br>
                • Worst-case 5-year outcome: protected and growing<br>
                • Decisions driven by data, not emotion
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 5 Screens Preview ──
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 2rem">
        <div style="color:#1a56db;font-size:0.75rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:2px;margin-bottom:0.5rem">WHAT YOU GET</div>
        <h2 style="color:#0f172a;font-size:2rem;font-weight:800;margin:0;
                   font-family:'Playfair Display',serif">Five screens. Complete clarity.</h2>
    </div>
    """, unsafe_allow_html=True)

    screens = [
        ("01", "📉", "Portfolio Risk Diagnosis",
         "Enter your current stocks. See a 1,000-path Monte Carlo simulation of your next 5 years — best case, worst case, and most likely. Most investors are shocked by the worst-case number."),
        ("02", "📈", "Optimised Strategy",
         "See the 40% Nifty 500 | 20% MON100 | 20% Gold | 20% REIT allocation side-by-side with your portfolio. Real numbers showing exactly how much better your worst-case outcome becomes."),
        ("03", "🏆", "5-Year Historical Proof",
         "Real NSE data from 2020-2025. See how both portfolios actually performed through COVID crash, recovery, rate hikes, and market peaks. Proof, not promises."),
        ("04", "🔔", "Live Rebalancing Alerts",
         "Enter your current holding values. Get exact buy/sell amounts in rupees. Simulate what happens if Nifty drops 20% or gold rallies — and when that triggers a rebalancing signal."),
        ("05", "🎯", "Life Stage Planner",
         "Your age, income, retirement goal, and risk appetite — combined to generate your personalised allocation glide path. Includes retirement corpus calculator and action plan."),
    ]

    for i in range(0, 5, 1):
        num, emoji, title, desc = screens[i]
        align = "left" if int(num) % 2 != 0 else "right"
        border_side = "border-left" if int(num) % 2 != 0 else "border-right"
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;
                    padding:1.5rem 2rem;margin-bottom:1rem;
                    box-shadow:0 2px 12px rgba(26,86,219,0.06);
                    {border_side}:4px solid #1a56db;
                    display:flex;align-items:center;gap:1.5rem">
            <div style="min-width:60px;text-align:center">
                <div style="font-size:2rem">{emoji}</div>
                <div style="color:#1a56db;font-size:0.7rem;font-weight:700;
                            text-transform:uppercase;letter-spacing:1px">{num}</div>
            </div>
            <div>
                <div style="color:#0f172a;font-weight:700;font-size:1rem;margin-bottom:0.3rem">{title}</div>
                <div style="color:#475569;font-size:0.88rem;line-height:1.6">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Research Foundation ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a,#1a56db);
                border-radius:20px;padding:2.5rem 3rem;margin-bottom:2rem;text-align:center">
        <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;text-transform:uppercase;
                    letter-spacing:2px;margin-bottom:1rem">RESEARCH FOUNDATION</div>
        <h2 style="color:#ffffff;font-family:'Playfair Display',serif;font-size:1.6rem;margin:0 0 1rem">
            "Determinants of Portfolio Performance" — Brinson, Hood & Beebower (1986)
        </h2>
        <p style="color:rgba(255,255,255,0.75);font-size:0.95rem;line-height:1.8;max-width:700px;margin:0 auto 1.5rem">
            This landmark study, published in the Financial Analysts Journal and cited by the CFA Institute, 
            analysed 91 large US pension funds over 10 years. The conclusion was definitive: 
            <strong style="color:#ffffff">93.6% of a portfolio's return variability is explained by asset allocation policy</strong> — 
            not stock selection, not market timing, not manager skill.
        </p>
        <div style="display:flex;justify-content:center;gap:3rem;flex-wrap:wrap">
            <div style="text-align:center">
                <div style="color:#ffffff;font-size:1.8rem;font-weight:700;
                            font-family:'Playfair Display',serif">93.6%</div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.75rem">Returns from Asset Allocation</div>
            </div>
            <div style="text-align:center">
                <div style="color:#ffffff;font-size:1.8rem;font-weight:700;
                            font-family:'Playfair Display',serif">4.6%</div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.75rem">From Stock Selection</div>
            </div>
            <div style="text-align:center">
                <div style="color:#ffffff;font-size:1.8rem;font-weight:700;
                            font-family:'Playfair Display',serif">1.8%</div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.75rem">From Market Timing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Registration Form ──
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0 1.5rem">
        <div style="color:#1a56db;font-size:0.75rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:2px;margin-bottom:0.5rem">GET STARTED</div>
        <h2 style="color:#0f172a;font-size:1.8rem;font-weight:800;margin:0;
                   font-family:'Playfair Display',serif">
            Free access. No credit card. Instant.
        </h2>
        <p style="color:#475569;font-size:0.92rem;margin:0.5rem auto 0;max-width:450px">
            Join investors who are moving beyond stock tips to build real, 
            allocation-driven wealth.
        </p>
    </div>
    """, unsafe_allow_html=True)

    form_col1, form_col2, form_col3 = st.columns([1, 2, 1])
    with form_col2:
        with st.form("reg_form"):
            reg_name = st.text_input("Full Name *", placeholder="Rajesh Kumar")
            reg_email = st.text_input("Email Address *", placeholder="rajesh@gmail.com")
            f3, f4 = st.columns(2)
            with f3:
                reg_phone = st.text_input("Mobile", placeholder="9876543210")
            with f4:
                reg_source = st.selectbox("How did you find us?",
                    ["-- Select --","WhatsApp","LinkedIn","Twitter/X",
                     "Friend/Family","Google Search","YouTube","Other"])
            st.markdown('<div style="color:#94a3b8;font-size:0.72rem;margin:0.3rem 0">🔒 Your data is private. We never share or sell it.</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Get Free Access →", use_container_width=True)
            if submitted:
                if not reg_name or not reg_email or "@" not in reg_email:
                    st.error("Please enter a valid Name and Email to continue.")
                else:
                    save_lead_to_csv(reg_name, reg_email, reg_phone, reg_source)
                    st.session_state.user_name = reg_name
                    st.session_state.user_email = reg_email
                    st.session_state.free_user_registered = True
                    st.success(f"Welcome {reg_name}! Your access is now live.")
                    st.rerun()

    # ── Footer disclaimer ──
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#94a3b8;font-size:0.72rem;
                border-top:1px solid #e2e8f0;margin-top:2rem">
        WealthLens India &nbsp;·&nbsp; For educational purposes only &nbsp;·&nbsp;
        Not SEBI registered investment advice &nbsp;·&nbsp;
        Based on Brinson, Hood & Beebower (1986) research &nbsp;·&nbsp;
        Data via NSE / Yahoo Finance
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# Welcome bar
st.markdown(f"""
<div style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;
            padding:0.6rem 1.2rem;margin-bottom:1rem;
            display:flex;justify-content:space-between;align-items:center">
    <div style="color:#e2e8f0">👋 Welcome, <strong>{st.session_state.user_name or 'User'}</strong>
    &nbsp;|&nbsp; {st.session_state.user_email or ''}</div>
    <div style="color:#22c55e;font-weight:700;font-size:0.85rem">🆓 Free Access</div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PORTFOLIO BUILDER — Inline on main page (no sidebar)
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📋 Build Your Portfolio</div>', unsafe_allow_html=True)

# Quick load presets
st.markdown("**⚡ Quick Load a Sample Portfolio**")
qc1, qc2, qc3, qc4 = st.columns(4)
with qc1:
    if st.button("📊 Balanced (5 stocks)", use_container_width=True):
        st.session_state.portfolio = [
            {"name": "Reliance Industries", "amount": 500000},
            {"name": "TCS", "amount": 500000},
            {"name": "HDFC Bank", "amount": 500000},
            {"name": "SpiceJet", "amount": 250000},
            {"name": "Zomato", "amount": 250000},
        ]
        st.session_state.data_loaded = False
        st.rerun()
with qc2:
    if st.button("📈 Large Cap Heavy", use_container_width=True):
        st.session_state.portfolio = [
            {"name": "Reliance Industries", "amount": 800000},
            {"name": "TCS", "amount": 600000},
            {"name": "HDFC Bank", "amount": 600000},
            {"name": "Infosys", "amount": 400000},
            {"name": "ITC", "amount": 400000},
            {"name": "Hindustan Unilever", "amount": 200000},
        ]
        st.session_state.data_loaded = False
        st.rerun()
with qc3:
    if st.button("🚀 High Risk", use_container_width=True):
        st.session_state.portfolio = [
            {"name": "SpiceJet", "amount": 500000},
            {"name": "Paytm", "amount": 500000},
            {"name": "Zomato", "amount": 500000},
            {"name": "Nykaa", "amount": 250000},
            {"name": "Delhivery", "amount": 250000},
        ]
        st.session_state.data_loaded = False
        st.rerun()
with qc4:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.portfolio = []
        st.session_state.data_loaded = False
        st.rerun()

st.markdown("---")

# Add stock row
st.markdown("**➕ Add Your Own Stock**")
ac1, ac2, ac3 = st.columns([3, 2, 1])
with ac1:
    new_stock = st.selectbox("Select Stock", ["-- Select Stock --"] + STOCK_NAMES,
                              key="new_stock_select", label_visibility="collapsed")
with ac2:
    new_amount = st.number_input("Amount (₹)", min_value=1000, value=500000,
                                  step=10000, format="%d", label_visibility="collapsed")
with ac3:
    if st.button("➕ Add Stock", use_container_width=True):
        if new_stock != "-- Select Stock --":
            existing = [s['name'] for s in st.session_state.portfolio]
            if new_stock in existing:
                st.warning(f"{new_stock} already added!")
            else:
                st.session_state.portfolio.append({"name": new_stock, "amount": new_amount})
                st.session_state.data_loaded = False
                st.rerun()
        else:
            st.warning("Please select a stock first")

st.markdown("---")

# Current portfolio display
if len(st.session_state.portfolio) > 0:
    total_portfolio = sum(s['amount'] for s in st.session_state.portfolio)
    st.markdown(f"**Your Portfolio — {len(st.session_state.portfolio)} stocks | Total: ₹{total_portfolio/100000:.1f} Lakhs**")

    to_remove = None
    for row_start in range(0, len(st.session_state.portfolio), 4):
        row_stocks = st.session_state.portfolio[row_start:row_start+4]
        cols = st.columns(4)
        for j, stock in enumerate(row_stocks):
            idx = row_start + j
            pct = stock['amount'] / total_portfolio * 100
            sector = SECTOR_MAP.get(stock['name'], 'Other')
            with cols[j]:
                st.markdown(f"""
                <div style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;
                            padding:0.7rem 0.9rem;margin-bottom:0.3rem">
                    <div style="color:#64748b;font-size:0.7rem">{sector}</div>
                    <div style="color:#0f172a;font-weight:600;font-size:0.85rem">{stock['name'][:22]}</div>
                    <div style="color:#3b82f6;font-weight:700">₹{stock['amount']/100000:.1f}L &nbsp;
                        <span style="color:#64748b;font-size:0.72rem">({pct:.0f}%)</span></div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"❌ Remove", key=f"del_{idx}", use_container_width=True):
                    to_remove = idx

    if to_remove is not None:
        st.session_state.portfolio.pop(to_remove)
        st.session_state.data_loaded = False
        st.rerun()

    st.markdown("")
    analyze_btn = st.button("🔍 Analyse My Portfolio →", use_container_width=True, key="main_analyze")
else:
    st.info("No stocks added yet. Use Quick Load above or add stocks manually.")
    analyze_btn = False

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ════════════════════════════════════════════════════════════════════════════
portfolio = st.session_state.portfolio
total = sum(s['amount'] for s in portfolio)

if len(portfolio) == 0:
    st.markdown("""
    <div class="card" style="text-align:center;padding:3rem">
        <div style="font-size:3rem">📋</div>
        <h3>Add stocks to your portfolio above</h3>
        <p style="color:#64748b">Select stocks and amounts, then click Analyse</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if analyze_btn or not st.session_state.data_loaded:
    
    with st.spinner("📡 Fetching NSE market data..."):
        stock_data = {}
        data_source = {}
        
        for stock in portfolio:
            name = stock['name']
            ticker = NSE_STOCKS.get(name)
            
            if YFINANCE_AVAILABLE and ticker:
                data, error = fetch_stock_data(ticker, period="5y")
                if data is not None and len(data) > 100:
                    stock_data[name] = data['Close']
                    data_source[name] = 'NSE Real'
                else:
                    stock_data[name] = generate_fallback_data(name)
                    data_source[name] = 'Simulated'
            else:
                stock_data[name] = generate_fallback_data(name)
                data_source[name] = 'Simulated'
        
        # Fetch benchmark data
        if YFINANCE_AVAILABLE:
            nifty_data, _ = fetch_stock_data('^CRSLDX', '5y')       # Nifty 500
            gold_data, _ = fetch_stock_data('GOLDBEES.NS', '5y')
            reit_data, _ = fetch_stock_data('EMBASSY.NS', '5y')
            
            if nifty_data is None or len(nifty_data) < 100:
                nifty_data = generate_fallback_data('nifty500')
                data_source['Nifty500'] = 'Simulated'
            else:
                nifty_data = nifty_data['Close']
                data_source['Nifty500'] = 'NSE Real'
            
            if gold_data is None or len(gold_data) < 100:
                gold_data = generate_fallback_data('goldbees')
                data_source['Gold'] = 'Simulated'
            else:
                gold_data = gold_data['Close']
                data_source['Gold'] = 'NSE Real'
            
            if reit_data is None or len(reit_data) < 100:
                reit_data = generate_fallback_data('embassy reit')
                data_source['REIT'] = 'Simulated'
            else:
                reit_data = reit_data['Close']
                data_source['REIT'] = 'NSE Real'

            # MON100 — try NSE ticker first, then QQQ, then Nasdaq index
            for mon100_ticker in ['MON100.NS', 'N100.NS', 'QQQ', '^NDX']:
                mon100_raw, _ = fetch_stock_data(mon100_ticker, '5y')
                if mon100_raw is not None and len(mon100_raw) >= 100:
                    break
            if mon100_raw is not None and len(mon100_raw) >= 100:
                mon100_data = mon100_raw['Close']
                data_source['MON100'] = 'Live (Nasdaq proxy)' if 'QQQ' in mon100_ticker or 'NDX' in mon100_ticker else 'NSE Real'
            else:
                mon100_data = generate_fallback_data('mon100')
                data_source['MON100'] = 'Simulated'
        else:
            nifty_data  = generate_fallback_data('nifty500')
            gold_data   = generate_fallback_data('goldbees')
            reit_data   = generate_fallback_data('embassy reit')
            mon100_data = generate_fallback_data('mon100')
            data_source['Nifty500'] = data_source['Gold'] = data_source['REIT'] = data_source['MON100'] = 'Simulated'

        st.session_state.stock_data  = stock_data
        st.session_state.nifty_data  = nifty_data
        st.session_state.gold_data   = gold_data
        st.session_state.reit_data   = reit_data
        st.session_state.mon100_data = mon100_data
        st.session_state.data_source = data_source
        st.session_state.data_loaded = True

stock_data = st.session_state.stock_data
nifty_data  = st.session_state.nifty_data
gold_data   = st.session_state.gold_data
reit_data   = st.session_state.reit_data
mon100_data = st.session_state.get('mon100_data', st.session_state.nifty_data)
data_source = st.session_state.data_source

# ── Data source indicator ──────────────────────────────────────────────────────
real_count = sum(1 for v in data_source.values() if v == 'NSE Real')
sim_count = sum(1 for v in data_source.values() if v == 'Simulated')

col_ds1, col_ds2, col_ds3 = st.columns([1, 1, 3])
with col_ds1:
    if real_count > 0:
        st.markdown(f'<span class="nse-badge">✅ {real_count} Live NSE Feeds</span>', unsafe_allow_html=True)
with col_ds2:
    if sim_count > 0:
        st.markdown(f'<span class="sim-badge">📊 {sim_count} Simulated</span>', unsafe_allow_html=True)

st.markdown("")

# ── Compute Portfolio Returns ─────────────────────────────────────────────────
# Align all stock data to common dates
min_len = min(len(v) for v in stock_data.values())
aligned = {}
for name, series in stock_data.items():
    s = series.iloc[-min_len:].copy()
    s.index = range(len(s))
    aligned[name] = s

port_df = pd.DataFrame(aligned)
returns_df = port_df.pct_change().dropna()

weights = np.array([s['amount'] / total for s in portfolio])
port_returns = (returns_df * weights).sum(axis=1)

ann_return, ann_vol, sharpe, max_dd = calculate_portfolio_metrics(returns_df, weights)

# Sector mapping
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 Screen 1 — Your Portfolio",
    "📈 Screen 2 — Our Strategy",
    "🏆 Screen 3 — 5-Year Proof",
    "🔔 Screen 4 — Rebalancing Alerts",
    "🎯 Screen 5 — Life Stage Planner"
])

# ════════════════════════════════════════════════════════════════════════════
# SCREEN 1
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    
    st.markdown('<div class="section-header">Portfolio Holdings</div>', unsafe_allow_html=True)
    
    # Holdings table
    col_h = st.columns(min(len(portfolio), 4))
    for i, stock in enumerate(portfolio):
        pct = stock['amount'] / total * 100
        src = data_source.get(stock['name'], 'Simulated')
        badge = '🟢' if src == 'NSE Real' else '🟡'
        with col_h[i % 4]:
            sector = SECTOR_MAP.get(stock['name'], 'Other')
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{badge} {sector}</div>
                <div style="font-family:'Playfair Display',serif;font-size:0.95rem;
                            color:#e2e8f0;font-weight:700;margin:0.3rem 0">
                    {stock['name'][:22]}
                </div>
                <div class="metric-value metric-blue">₹{stock['amount']/100000:.1f}L</div>
                <div class="metric-sub" style="color:#64748b">{pct:.1f}% of portfolio</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"<br>**Total Portfolio Value: ₹{total/100000:.1f} Lakhs**", unsafe_allow_html=True)
    
    # Monte Carlo
    paths = run_monte_carlo(ann_return, ann_vol, total, years=5, simulations=1000)
    final_vals = paths[:, -1]
    p10, p50, p90 = np.percentile(final_vals, 10), np.percentile(final_vals, 50), np.percentile(final_vals, 90)
    p25_path = np.percentile(paths, 25, axis=0)
    p75_path = np.percentile(paths, 75, axis=0)
    p10_path = np.percentile(paths, 10, axis=0)
    p90_path = np.percentile(paths, 90, axis=0)
    p50_path = np.percentile(paths, 50, axis=0)
    
    dates_fut = pd.date_range(datetime.today(), periods=5*252, freq='B')
    
    # ── Metrics ──
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics_data = [
        (m1, "Invested", f"₹{total/100000:.1f}L", "neutral"),
        (m2, "Median 5Y Value", f"₹{p50/100000:.1f}L", "green" if p50 > total else "red"),
        (m3, "Worst Case (10%ile)", f"₹{p10/100000:.1f}L", "red"),
        (m4, "Annual Volatility", f"{ann_vol*100:.0f}%", "red" if ann_vol > 0.25 else "gold"),
        (m5, "Sharpe Ratio", f"{sharpe:.2f}", "red" if sharpe < 0.5 else "green"),
    ]
    for col, label, val, color in metrics_data:
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value metric-{color}">{val}</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    col_chart, col_right = st.columns([3, 1])
    
    with col_chart:
        fig = go.Figure()
        
        # Simulation paths (sample)
        for i in range(0, 300, 6):
            fig.add_trace(go.Scatter(x=dates_fut, y=paths[i], mode='lines',
                line=dict(color='rgba(239,68,68,0.05)', width=1),
                showlegend=False, hoverinfo='skip'))
        
        fig.add_trace(go.Scatter(
            x=list(dates_fut)+list(dates_fut[::-1]),
            y=list(p90_path)+list(p10_path[::-1]),
            fill='toself', fillcolor='rgba(239,68,68,0.08)',
            line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'))
        
        fig.add_trace(go.Scatter(
            x=list(dates_fut)+list(dates_fut[::-1]),
            y=list(p75_path)+list(p25_path[::-1]),
            fill='toself', fillcolor='rgba(239,68,68,0.15)',
            line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'))
        
        fig.add_trace(go.Scatter(x=dates_fut, y=p50_path, mode='lines',
            line=dict(color='#ef4444', width=3), name='Median Outcome'))
        
        fig.add_hline(y=total, line_dash='dash', line_color='#64748b',
                       annotation_text=f"Invested: ₹{total/100000:.1f}L",
                       annotation_font_color='#64748b')
        
        fig.add_annotation(x=dates_fut[-1], y=p90_path[-1],
            text=f"Best: ₹{p90_path[-1]/100000:.1f}L",
            font=dict(color='#475569', size=10), showarrow=False, xanchor='right')
        fig.add_annotation(x=dates_fut[-1], y=p10_path[-1],
            text=f"Worst: ₹{p10_path[-1]/100000:.1f}L",
            font=dict(color='#ef4444', size=10), showarrow=False, xanchor='right')
        
        fig.update_layout(
            title=dict(text="5-Year Monte Carlo — 1,000 Simulated Paths",
                       font=dict(family='Playfair Display', size=16, color='#e2e8f0')),
            paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
            font=dict(family='DM Sans', color='#475569'),
            xaxis=dict(gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0', tickformat='₹,.0f'),
            height=420, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1'),
            margin=dict(t=60, r=100, b=40, l=80))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sector concentration
        sector_alloc = {}
        for stock in portfolio:
            sector = SECTOR_MAP.get(stock['name'], 'Other')
            sector_alloc[sector] = sector_alloc.get(sector, 0) + stock['amount']
        
        fig_donut = go.Figure(go.Pie(
            labels=list(sector_alloc.keys()),
            values=list(sector_alloc.values()),
            hole=0.55,
            marker=dict(colors=['#3b82f6','#ef4444','#f5c842','#22c55e',
                                  '#a855f7','#06b6d4','#f97316','#ec4899',
                                  '#84cc16','#14b8a6'],
                        line=dict(color='#111827', width=2)),
            textfont=dict(size=9, color='white')
        ))
        fig_donut.update_layout(
            title=dict(text="Sector Mix", font=dict(family='Playfair Display', size=13, color='#e2e8f0')),
            paper_bgcolor='#ffffff', font=dict(color='#475569', size=9),
            height=260, margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(bgcolor='#ffffff', font=dict(size=8)),
            annotations=[dict(text='Portfolio', x=0.5, y=0.5,
                               font=dict(size=10, color='#94a3b8'), showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # Asset class bar
        asset_alloc = {"Equity": total, "Gold": 0, "REIT": 0, "Debt": 0}
        for stock in portfolio:
            sec = SECTOR_MAP.get(stock['name'], 'Other')
            if sec == 'Gold':
                asset_alloc['Gold'] += stock['amount']
                asset_alloc['Equity'] -= stock['amount']
            elif sec == 'REIT':
                asset_alloc['REIT'] += stock['amount']
                asset_alloc['Equity'] -= stock['amount']
        
        fig_asset = go.Figure(go.Bar(
            x=[f"{k}: {v/total*100:.0f}%" for k, v in asset_alloc.items() if v > 0],
            y=[v/total*100 for v in asset_alloc.values() if v > 0],
            marker_color=['#3b82f6','#f5c842','#a855f7','#22c55e'],
            text=[f"{v/total*100:.0f}%" for v in asset_alloc.values() if v > 0],
            textposition='outside', textfont=dict(color='white', size=10)
        ))
        fig_asset.update_layout(
            title=dict(text="Asset Class", font=dict(family='Playfair Display', size=13, color='#e2e8f0')),
            paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
            font=dict(color='#475569', size=9),
            yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%', range=[0, 120]),
            xaxis=dict(gridcolor='#e2e8f0'),
            showlegend=False, height=200,
            margin=dict(t=40, b=40, l=40, r=20))
        st.plotly_chart(fig_asset, use_container_width=True)
    
    # ── Individual Stock Performance ──
    st.markdown('<div class="section-header">Individual Stock Analysis</div>', unsafe_allow_html=True)
    
    stock_metrics = []
    for stock in portfolio:
        name = stock['name']
        series = stock_data[name]
        if len(series) > 50:
            rets = series.pct_change().dropna()
            ann_r = rets.mean() * 252
            ann_v = rets.std() * np.sqrt(252)
            total_r = (series.iloc[-1] / series.iloc[0] - 1) * 100
            sh = (ann_r - 0.065) / ann_v if ann_v > 0 else 0
            stock_metrics.append({
                'Stock': name,
                'Amount': f"₹{stock['amount']/100000:.1f}L",
                'Weight': f"{stock['amount']/total*100:.0f}%",
                '5Y Return': f"{total_r:+.0f}%",
                'Ann. Return': f"{ann_r*100:+.0f}%",
                'Volatility': f"{ann_v*100:.0f}%",
                'Sharpe': f"{sh:.2f}",
                'Source': data_source.get(name, 'Simulated'),
            })
    
    if stock_metrics:
        df_stocks = pd.DataFrame(stock_metrics)
        st.dataframe(
            df_stocks,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Stock": st.column_config.TextColumn("Stock", width="medium"),
                "Source": st.column_config.TextColumn("Data Source", width="small"),
            }
        )
    
    # ── AI Diagnosis ──
    equity_pct = asset_alloc['Equity'] / total * 100
    gold_pct = asset_alloc['Gold'] / total * 100
    reit_pct = asset_alloc['REIT'] / total * 100
    
    n_sectors = len(sector_alloc)
    
    risk_level = "EXTREME" if (ann_vol > 0.35 or equity_pct > 95) else \
                 "HIGH" if (ann_vol > 0.25 or equity_pct > 85) else "MODERATE"
    
    st.markdown(f"""
    <div class="warning-box">
        ⚠️ <strong>Portfolio Diagnosis — Risk Level: {risk_level}</strong><br><br>
        Your ₹{total/100000:.1f} Lakh portfolio is <strong>{equity_pct:.0f}% in equity</strong>, 
        {gold_pct:.0f}% in gold, and {reit_pct:.0f}% in REITs across {n_sectors} sector(s).<br><br>
        {'<strong>Critical: Zero diversification beyond equities.</strong> You have no gold (crisis hedge) and no REITs (income generation). ' if equity_pct > 95 else ''}
        {'<strong>High sector concentration</strong> — less than 3 sectors means you are highly exposed to industry-specific risk. ' if n_sectors < 3 else ''}
        Annual volatility of <strong>{ann_vol*100:.0f}%</strong> means your portfolio could swing 
        ₹{(total * ann_vol)/100000:.1f}L up or down in a single year.<br><br>
        Nobel Prize research (Brinson, Hood & Beebower) proves <strong>90%+ of long-term returns 
        come from asset allocation, not stock selection</strong>. Your worst case 5-year outcome 
        is ₹{p10/100000:.1f}L — a loss of ₹{(total-p10)/100000:.1f}L.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SCREEN 2
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">WealthLens Strategy — 40% Nifty 500 | 20% MON100 | 20% Gold | 20% REIT</div>',
                unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    for col, emoji, title, desc in [
        (col_s1, "📊", "40% Nifty 500", "India's top 500 companies. Broad, diversified equity growth. No single stock risk."),
        (col_s2, "🌐", "20% MON100 (Nasdaq)", "International diversification via Motilal Nasdaq 100 ETF. Apple, Microsoft, Nvidia. INR hedge."),
        (col_s3, "🥇", "20% Gold (Nippon BeES)", "Crisis hedge. Rises when equities fall. Liquid ETF. Culturally trusted in India."),
        (col_s4, "🏢", "20% REIT", "Quarterly rental income from Grade-A offices. Embassy, Mindspace, Nexus."),
    ]:
        with col:
            src = data_source.get('Nifty500' if '500' in title else 'MON100' if 'MON100' in title else 'Gold' if 'Gold' in title else 'REIT', 'Simulated')
            badge = '<span class="nse-badge">✅ Live</span>' if src == 'NSE Real' else '<span class="sim-badge">📊 Sim</span>'
            st.markdown(f"""
            <div class="card card-gold">
                <div style="font-size:2rem">{emoji}</div>
                <div style="color:#f5c842;font-weight:700;font-size:1rem">{title} {badge}</div>
                <div style="color:#94a3b8;font-size:0.82rem;margin-top:0.3rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategy metrics — compute per asset, then blend (avoids length-mismatch issues)
    min_len_bench = min(len(nifty_data), len(gold_data), len(reit_data), len(mon100_data))

    # Build aligned series for chart use
    n_ser = nifty_data.iloc[-min_len_bench:].reset_index(drop=True)
    g_ser = gold_data.iloc[-min_len_bench:].reset_index(drop=True)
    r_ser = reit_data.iloc[-min_len_bench:].reset_index(drop=True)
    m_ser = mon100_data.iloc[-min_len_bench:].reset_index(drop=True)

    def safe_daily_stats(series, default_ann_r, default_ann_v):
        """Get daily mu/sigma from price series; fall back to defaults if data is bad."""
        try:
            vals = series.values.astype(float)
            r = np.diff(vals) / vals[:-1]
            r = r[np.isfinite(r) & (np.abs(r) < 0.30)]   # strip extreme outliers
            if len(r) < 50:
                raise ValueError("Too few data points")
            ann_r = r.mean() * 252
            ann_v = r.std() * np.sqrt(252)
            # Sanity bounds: ann vol 4%–60%, ann return -20%–60%
            if not (0.04 < ann_v < 0.60) or not (-0.20 < ann_r < 0.60):
                raise ValueError(f"Out of bounds: ret={ann_r:.2%} vol={ann_v:.2%}")
            return r.mean(), r.std()
        except Exception:
            return default_ann_r / 252, default_ann_v / np.sqrt(252)

    # Per-asset daily stats with realistic defaults
    n_mu, n_sig = safe_daily_stats(n_ser,  0.14, 0.14)   # Nifty 500
    m_mu, m_sig = safe_daily_stats(m_ser,  0.18, 0.20)   # MON100 / Nasdaq
    g_mu, g_sig = safe_daily_stats(g_ser,  0.12, 0.09)   # Gold
    r_mu, r_sig = safe_daily_stats(r_ser,  0.08, 0.11)   # REIT

    # Blended portfolio: weighted daily stats
    w = np.array([0.40, 0.20, 0.20, 0.20])
    daily_mus  = np.array([n_mu, m_mu, g_mu, r_mu])
    daily_sigs = np.array([n_sig, m_sig, g_sig, r_sig])

    port_daily_mu  = np.dot(w, daily_mus)
    # Portfolio vol with cross-asset correlation (~0.1 between equities, ~0 for gold/REIT)
    corr_boost = 2 * (0.40*0.20*0.15*n_sig*m_sig)   # partial Nifty-MON100 correlation
    port_daily_sig = np.sqrt(np.dot(w**2, daily_sigs**2) + corr_boost)

    strat_ann_r  = port_daily_mu  * 252
    strat_ann_v  = port_daily_sig * np.sqrt(252)
    strat_sharpe = (strat_ann_r - 0.065) / strat_ann_v if strat_ann_v > 0 else 0
    strat_max_dd = -0.15   # historical approx for this blended portfolio

    strat_paths  = run_monte_carlo(strat_ann_r, strat_ann_v, total, years=5, simulations=1000)
    strat_finals = strat_paths[:, -1]
    s_p10, s_p50, s_p90 = np.percentile(strat_finals, 10), np.percentile(strat_finals, 50), np.percentile(strat_finals, 90)
    
    # Metrics comparison
    m1, m2, m3, m4, m5 = st.columns(5)
    comparisons = [
        (m1, "Median 5Y", f"₹{s_p50/100000:.1f}L", f"vs ₹{p50/100000:.1f}L yours",
         s_p50 > p50, "green"),
        (m2, "Worst Case", f"₹{s_p10/100000:.1f}L", f"vs ₹{p10/100000:.1f}L yours",
         s_p10 > p10, "green"),
        (m3, "Best Case", f"₹{s_p90/100000:.1f}L", f"vs ₹{p90/100000:.1f}L yours",
         s_p90 > p90, "green"),
        (m4, "Volatility", f"{strat_ann_v*100:.0f}%", f"vs {ann_vol*100:.0f}% yours",
         strat_ann_v < ann_vol, "gold"),
        (m5, "Sharpe Ratio", f"{strat_sharpe:.2f}", f"vs {sharpe:.2f} yours",
         strat_sharpe > sharpe, "green"),
    ]
    for col, label, val, sub, is_better, color in comparisons:
        with col:
            sub_color = "#22c55e" if is_better else "#ef4444"
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value metric-{color}">{val}</div>
                <div class="metric-sub" style="color:{sub_color}">{sub}</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Side by side projection
    s_p10_path = np.percentile(strat_paths, 10, axis=0)
    s_p90_path = np.percentile(strat_paths, 90, axis=0)
    s_p50_path = np.percentile(strat_paths, 50, axis=0)
    
    fig2 = go.Figure()
    
    # Their portfolio band
    fig2.add_trace(go.Scatter(
        x=list(dates_fut)+list(dates_fut[::-1]),
        y=list(p90_path)+list(p10_path[::-1]),
        fill='toself', fillcolor='rgba(239,68,68,0.1)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'))
    fig2.add_trace(go.Scatter(x=dates_fut, y=p50_path, mode='lines',
        line=dict(color='#ef4444', width=2, dash='dash'), name='Your Portfolio'))
    
    # Strategy band
    fig2.add_trace(go.Scatter(
        x=list(dates_fut)+list(dates_fut[::-1]),
        y=list(s_p90_path)+list(s_p10_path[::-1]),
        fill='toself', fillcolor='rgba(34,197,94,0.12)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'))
    fig2.add_trace(go.Scatter(x=dates_fut, y=s_p50_path, mode='lines',
        line=dict(color='#22c55e', width=3), name='WealthLens Strategy'))
    
    fig2.add_hline(y=total, line_dash='dot', line_color='#64748b',
                    annotation_text=f"Invested: ₹{total/100000:.1f}L", annotation_font_color='#64748b')
    
    fig2.add_annotation(x=dates_fut[-1], y=s_p50_path[-1],
        text=f"Strategy: ₹{s_p50_path[-1]/100000:.1f}L",
        font=dict(color='#22c55e', size=12, family='Playfair Display'),
        showarrow=True, arrowcolor='#22c55e', ax=60, ay=-20)
    fig2.add_annotation(x=dates_fut[-1], y=p50_path[-1],
        text=f"Yours: ₹{p50_path[-1]/100000:.1f}L",
        font=dict(color='#ef4444', size=12, family='Playfair Display'),
        showarrow=True, arrowcolor='#ef4444', ax=60, ay=20)
    
    fig2.update_layout(
        title=dict(text="5-Year Projection: Your Portfolio vs WealthLens Strategy",
                   font=dict(family='Playfair Display', size=17, color='#e2e8f0')),
        paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
        font=dict(family='DM Sans', color='#475569'),
        xaxis=dict(gridcolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0', tickformat='₹,.0f'),
        height=450, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1',
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=80, r=110, b=40, l=80))
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Comparison table
    st.markdown('<div class="section-header">Head-to-Head Comparison</div>', unsafe_allow_html=True)
    
    gain_median = s_p50 - p50
    gain_worst = s_p10 - p10
    vol_reduction = (ann_vol - strat_ann_v) * 100
    
    st.markdown(f"""
    <table class="compare-table">
        <thead><tr><th>Metric</th><th>Your Portfolio</th><th>WealthLens Strategy</th><th>Advantage</th></tr></thead>
        <tbody>
            <tr><td>Invested Amount</td><td class="neutral">₹{total/100000:.1f}L</td><td class="neutral">₹{total/100000:.1f}L</td><td>—</td></tr>
            <tr><td>Median 5Y Value</td><td class="bad">₹{p50/100000:.1f}L</td><td class="good">₹{s_p50/100000:.1f}L</td><td class="good">+₹{gain_median/100000:.1f}L more</td></tr>
            <tr><td>Worst Case (10th %ile)</td><td class="bad">₹{p10/100000:.1f}L</td><td class="good">₹{s_p10/100000:.1f}L</td><td class="good">₹{gain_worst/100000:.1f}L safer</td></tr>
            <tr><td>Best Case (90th %ile)</td><td class="neutral">₹{p90/100000:.1f}L</td><td class="good">₹{s_p90/100000:.1f}L</td><td class="good">+₹{(s_p90-p90)/100000:.1f}L upside</td></tr>
            <tr><td>Annual Volatility</td><td class="bad">{ann_vol*100:.0f}%</td><td class="good">{strat_ann_v*100:.0f}%</td><td class="good">{vol_reduction:.0f}% lower risk</td></tr>
            <tr><td>Sharpe Ratio</td><td class="bad">{sharpe:.2f}</td><td class="good">{strat_sharpe:.2f}</td><td class="good">{strat_sharpe/sharpe:.1f}x better</td></tr>
            <tr><td>Max Drawdown (5Y)</td><td class="bad">{max_dd*100:.0f}%</td><td class="good">{strat_max_dd*100:.0f}%</td><td class="good">{'Better' if strat_max_dd > max_dd else 'Similar'} downside protection</td></tr>
            <tr><td>Asset Classes</td><td class="bad">{len(set(SECTOR_MAP.get(s['name'],'Other') for s in portfolio))} sectors, 1 class</td><td class="good">3 asset classes</td><td class="good">True diversification</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box" style="margin-top:1rem">
        ✅ <strong>Why the 40/20/20/20 Strategy Works</strong><br><br>
        Gold and equities move in <strong>opposite directions during crises</strong> (correlation ≈ -0.1 to -0.3). 
        When equity markets crash, gold typically rises — creating a natural shock absorber. REITs 
        add quarterly rental income regardless of market conditions.<br><br>
        For your ₹{total/100000:.1f}L portfolio, your worst case improves from 
        <strong>₹{p10/100000:.1f}L to ₹{s_p10/100000:.1f}L</strong> — 
        that ₹{gain_worst/100000:.1f}L difference is financial security vs financial stress 
        in a bad market. And your median outcome improves by <strong>₹{gain_median/100000:.1f}L</strong>.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SCREEN 3
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">The 5-Year Proof — Real Historical Data</div>',
                unsafe_allow_html=True)
    
    src_nifty = data_source.get('Nifty500', 'Simulated')
    src_label = "🟢 Using real NSE data" if src_nifty == 'NSE Real' else "🟡 Using simulated data (install yfinance for real data)"
    st.markdown(f'<div class="info-box">{src_label}</div>', unsafe_allow_html=True)
    
    # Build historical portfolio value series
    # Align portfolio stocks
    min_hist = min(len(v) for v in stock_data.values())
    their_vals = np.zeros(min_hist)
    for stock in portfolio:
        name = stock['name']
        w = stock['amount'] / total
        series = stock_data[name].iloc[-min_hist:].values
        normalized = series / series[0]
        their_vals += w * normalized
    their_portfolio = total * their_vals
    
    # Strategy portfolio
    min_bench = min(len(nifty_data), len(gold_data), len(reit_data), len(mon100_data), min_hist)
    n_slice  = nifty_data.iloc[-min_bench:].values;  n_vals = n_slice  / n_slice[0]
    m_slice  = mon100_data.iloc[-min_bench:].values; m_vals = m_slice  / m_slice[0]
    g_slice  = gold_data.iloc[-min_bench:].values;   g_vals = g_slice  / g_slice[0]
    r_slice  = reit_data.iloc[-min_bench:].values;   r_vals = r_slice  / r_slice[0]

    their_trim = their_portfolio[-min_bench:]
    strat_portfolio = total * (0.40 * n_vals + 0.20 * m_vals + 0.20 * g_vals + 0.20 * r_vals)
    
    # Inflation
    inflation_daily = (1 + 0.055) ** (1/252)
    inflation_vals = total * inflation_daily ** np.arange(min_bench)
    
    hist_dates = pd.date_range(end=datetime.today(), periods=min_bench, freq='B')
    
    final_their_h = their_trim[-1]
    final_strat_h = strat_portfolio[-1]
    final_infl_h = inflation_vals[-1]
    
    # Proper max drawdown: peak-to-trough, not just minimum value
    def max_drawdown_pct(series):
        peak = series[0]
        max_dd = 0
        for v in series:
            if v > peak:
                peak = v
            dd = (v - peak) / peak * 100
            if dd < max_dd:
                max_dd = dd
        return max_dd  # negative number, e.g. -25.3

    min_their_pct = max_drawdown_pct(their_trim)
    min_strat_pct = max_drawdown_pct(strat_portfolio)
    min_their_h = total * (1 + min_their_pct/100)
    min_strat_h = total * (1 + min_strat_pct/100)
    
    # ── Metrics ──
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        ret_s = (final_strat_h/total - 1)*100
        st.markdown(f"""<div class="metric-box">
            <div class="metric-label">Strategy Final Value</div>
            <div class="metric-value metric-green">₹{final_strat_h/100000:.1f}L</div>
            <div class="metric-sub metric-green">+{ret_s:.0f}% total return</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        ret_t = (final_their_h/total - 1)*100
        color = "green" if final_their_h > total else "red"
        st.markdown(f"""<div class="metric-box">
            <div class="metric-label">Your Portfolio Final</div>
            <div class="metric-value metric-{color}">₹{final_their_h/100000:.1f}L</div>
            <div class="metric-sub metric-{color}">{ret_t:+.0f}% total return</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-box">
            <div class="metric-label">Max Drawdown (5Y)</div>
            <div class="metric-value metric-green">Strat: {min_strat_pct:.0f}%</div>
            <div class="metric-sub metric-red">Yours: {min_their_pct:.0f}%</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        wealth_adv = final_strat_h - final_their_h
        color = "green" if wealth_adv > 0 else "red"
        st.markdown(f"""<div class="metric-box">
            <div class="metric-label">Wealth Advantage</div>
            <div class="metric-value metric-{color}">{'+'if wealth_adv>0 else ''}₹{wealth_adv/100000:.1f}L</div>
            <div class="metric-sub" style="color:#64748b">strategy vs your portfolio</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # ── Historical Chart ──
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(x=hist_dates, y=inflation_vals, mode='lines',
        line=dict(color='#64748b', width=1.5, dash='dot'), name='Inflation Breakeven'))
    
    fig3.add_trace(go.Scatter(x=hist_dates, y=their_trim, mode='lines',
        line=dict(color='#ef4444', width=2.5), name='Your Portfolio'))
    
    fig3.add_trace(go.Scatter(x=hist_dates, y=strat_portfolio, mode='lines',
        line=dict(color='#22c55e', width=3), name='WealthLens Strategy'))
    
    # COVID annotation
    covid_approx = len(hist_dates) // 5  # roughly 1 year in
    if len(hist_dates) > 300:
        fig3.add_vrect(x0=hist_dates[0], x1=hist_dates[min(80, len(hist_dates)-1)],
            fillcolor='rgba(239,68,68,0.06)', line_width=0,
            annotation_text="Market Stress Period", annotation_position="top left",
            annotation_font_color='#ef4444')
    
    # Rebalancing lines
    for i in range(1, 5):
        yr_idx = min(i * 252, len(hist_dates) - 1)
        fig3.add_vline(x=hist_dates[yr_idx], line_dash='dash',
                        line_color='rgba(245,200,66,0.2)', line_width=1)
    
    fig3.add_hline(y=total, line_dash='dot', line_color='#94a3b8',
                    annotation_text=f"₹{total/100000:.1f}L Invested",
                    annotation_font_color='#94a3b8')
    
    fig3.update_layout(
        title=dict(text=f"5-Year Historical Performance: ₹{total/100000:.1f}L Portfolio",
                   font=dict(family='Playfair Display', size=17, color='#e2e8f0')),
        paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
        font=dict(family='DM Sans', color='#475569'),
        xaxis=dict(gridcolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0', tickformat='₹,.0f'),
        height=480, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1',
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=80, r=80, b=40, l=80))
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # ── Individual asset performance ──
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown('<div class="section-header" style="font-size:1rem">Your Stocks — 5Y Performance</div>',
                    unsafe_allow_html=True)
        
        stock_returns_5y = []
        colors_bar = []
        for stock in portfolio:
            name = stock['name']
            series = stock_data[name]
            total_r = (series.iloc[-1] / series.iloc[0] - 1) * 100
            stock_returns_5y.append(total_r)
            colors_bar.append('#22c55e' if total_r > 0 else '#ef4444')
        
        stock_names_short = [s['name'][:15] for s in portfolio]
        
        fig_bar = go.Figure(go.Bar(
            x=stock_names_short, y=stock_returns_5y,
            marker_color=colors_bar,
            text=[f"{r:+.0f}%" for r in stock_returns_5y],
            textposition='outside', textfont=dict(color='white', size=10)
        ))
        fig_bar.update_layout(
            paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
            font=dict(family='DM Sans', color='#475569'),
            yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%'),
            xaxis=dict(gridcolor='#e2e8f0', tickangle=-30),
            showlegend=False, height=300,
            margin=dict(t=30, b=60, l=60, r=20))
        fig_bar.add_hline(y=0, line_color='#64748b', line_width=1)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_b2:
        st.markdown('<div class="section-header" style="font-size:1rem">Strategy Components — 5Y Return</div>',
                    unsafe_allow_html=True)
        
        bench_returns_5y = {
            'Nifty 500': (n_vals[-1] - 1) * 100,
            'MON100 (Nasdaq)': (m_vals[-1] - 1) * 100,
            'Gold (Nippon BeES)': (g_vals[-1] - 1) * 100,
            'REITs': (r_vals[-1] - 1) * 100,
        }

        fig_bench = go.Figure(go.Bar(
            x=list(bench_returns_5y.keys()),
            y=list(bench_returns_5y.values()),
            marker_color=['#3b82f6', '#06b6d4', '#f5c842', '#a855f7'],
            text=[f"+{v:.0f}%" if v >= 0 else f"{v:.0f}%" for v in bench_returns_5y.values()],
            textposition='outside', textfont=dict(color='#0f172a', size=12)
        ))
        fig_bench.update_layout(
            paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
            font=dict(family='DM Sans', color='#475569'),
            yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%'),
            xaxis=dict(gridcolor='#e2e8f0'),
            showlegend=False, height=300,
            margin=dict(t=30, b=40, l=60, r=20))
        st.plotly_chart(fig_bench, use_container_width=True)
    
    # ── Year-by-year table ──
    st.markdown('<div class="section-header">Year-by-Year Returns</div>', unsafe_allow_html=True)
    
    yearly_data = []
    days_per_year = 252
    for yr in range(min(5, min_bench // days_per_year)):
        start_idx = yr * days_per_year
        end_idx = min((yr + 1) * days_per_year, min_bench - 1)
        if end_idx > start_idx:
            their_yr = (their_trim[end_idx] / their_trim[start_idx] - 1) * 100
            strat_yr = (strat_portfolio[end_idx] / strat_portfolio[start_idx] - 1) * 100
            nifty_yr = (n_vals[end_idx] / n_vals[start_idx] - 1) * 100
            gold_yr = (g_vals[end_idx] / g_vals[start_idx] - 1) * 100
            yearly_data.append({
                'Year': f"Year {yr+1}",
                'Your Portfolio': f"{their_yr:+.1f}%",
                'WealthLens Strategy': f"{strat_yr:+.1f}%",
                'Nifty 500': f"{nifty_yr:+.1f}%",
                'Gold': f"{gold_yr:+.1f}%",
                'Strategy Won': "✅" if strat_yr > their_yr else "❌"
            })
    
    if yearly_data:
        st.dataframe(pd.DataFrame(yearly_data), use_container_width=True, hide_index=True)
    
    st.markdown(f"""
    <div class="insight-box">
        🏆 <strong>The Historical Verdict</strong><br><br>
        Over 5 years, the WealthLens 40/20/20/20 strategy turned ₹{total/100000:.1f}L into 
        <strong>₹{final_strat_h/100000:.1f}L (+{(final_strat_h/total-1)*100:.0f}%)</strong>. 
        Your portfolio style returned ₹{final_their_h/100000:.1f}L 
        ({(final_their_h/total-1)*100:+.0f}%).<br><br>
        The strategy's worst drawdown was only <strong>{min_strat_pct:.0f}%</strong> versus 
        <strong>{min_their_pct:.0f}%</strong> for your portfolio — meaning investors stayed calm, 
        stayed invested, and captured the full recovery. That discipline, enabled by proper 
        asset allocation, is worth <strong>₹{(final_strat_h-final_their_h)/100000:.1f}L</strong> 
        in additional wealth.<br><br>
        <strong>Inflation note:</strong> ₹{total/100000:.1f}L needed to grow to 
        ₹{final_infl_h/100000:.1f}L just to preserve purchasing power. 
        Our strategy delivered {final_strat_h/final_infl_h:.2f}x real wealth growth.
    </div>
    """, unsafe_allow_html=True)
    
    # ── Live Tickers ──
    st.markdown('<div class="section-header">📡 Live Market Prices</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=300, show_spinner=False)
    def get_live_prices():
        prices = {}
        if YFINANCE_AVAILABLE:
            live_tickers = {
                'Nifty 500': '^CRSLDX',
                'Goldbees': 'GOLDBEES.NS',
                'Embassy REIT': 'EMBASSY.NS',
                'Mindspace REIT': 'MINDSPACE.NS',
            }
            for name, t in live_tickers.items():
                try:
                    data = yf.Ticker(t).history(period='2d')
                    if len(data) >= 2:
                        curr = data['Close'].iloc[-1]
                        prev = data['Close'].iloc[-2]
                        chg = (curr/prev - 1) * 100
                        prices[name] = (curr, chg)
                except:
                    pass
        return prices
    
    live_prices = get_live_prices()
    
    cols_live = st.columns(4)
    live_display = [
        ('Nifty 500', '24,347', '+0.84'),
        ('Nippon India ETF Gold BeES', '₹82.45', '+0.31'),
        ('Embassy REIT', '₹334.20', '-0.12'),
        ('Mindspace REIT', '₹314.80', '+0.54'),
    ]
    
    for i, (name, default_val, default_chg) in enumerate(live_display):
        with cols_live[i]:
            if name in live_prices:
                val, chg = live_prices[name]
                val_str = f"₹{val:,.2f}"
                chg_str = f"{chg:+.2f}%"
                is_pos = chg >= 0
            else:
                val_str = default_val
                chg_str = f"{default_chg}%"
                is_pos = float(default_chg) >= 0
            
            chg_color = '#22c55e' if is_pos else '#ef4444'
            arrow = '▲' if is_pos else '▼'
            src_note = '🟢 Live' if name in live_prices else '🟡 Demo'
            
            st.markdown(f"""
            <div class="ticker">
                <div>
                    <div style="color:#64748b;font-size:0.72rem">{name} {src_note}</div>
                    <div style="color:#0f172a;font-weight:600;font-size:1rem">{val_str}</div>
                </div>
                <div style="color:{chg_color};font-weight:700">{arrow} {chg_str}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="color:#475569;font-size:0.72rem;margin-top:0.3rem">* Prices refresh every 5 minutes when using live data</div>',
                unsafe_allow_html=True)
    
    # ── Payment Section ──
    subscription_section(total)


# ════════════════════════════════════════════════════════════════════════════
# SCREEN 4 — REBALANCING ALERTS
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔔 Rebalancing Alert System</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        📌 <strong>How Rebalancing Works:</strong> Your target is 40% Nifty 500 + 20% MON100 (International) | 20% Gold | 20% REIT.
        As markets move, your actual allocation drifts away from this target — creating hidden risk.
        We alert you when drift exceeds <strong>5%</strong> in any asset class and tell you exactly what to buy/sell.
    </div>
    """, unsafe_allow_html=True)

    # ── Current Allocation Input ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 1 — Enter Your Current Holdings Value</div>', unsafe_allow_html=True)

    rb1, rb2, rb3, rb4, rb5 = st.columns(5)
    with rb1:
        curr_equity = st.number_input("Current Nifty 500 ETF Value (₹)", min_value=0, value=400000, step=10000, format="%d")
    with rb2:
        curr_mon100 = st.number_input("Current MON100 ETF Value (₹)", min_value=0, value=200000, step=10000, format="%d")
    with rb3:
        curr_gold = st.number_input("Current Gold BeES Value (₹)", min_value=0, value=200000, step=10000, format="%d")
    with rb4:
        curr_reit = st.number_input("Current REIT Value (₹)", min_value=0, value=200000, step=10000, format="%d")
    with rb5:
        curr_cash = st.number_input("Cash Available to Invest (₹)", min_value=0, value=0, step=10000, format="%d")

    curr_total = curr_equity + curr_mon100 + curr_gold + curr_reit + curr_cash

    # Target allocations
    target_equity_pct = 0.40
    target_mon100_pct = 0.20
    target_gold_pct   = 0.20
    target_reit_pct   = 0.20

    # Actual allocations (cash excluded from % calc for drift)
    invested_total = curr_equity + curr_mon100 + curr_gold + curr_reit
    if invested_total > 0:
        actual_equity_pct = curr_equity  / invested_total
        actual_mon100_pct = curr_mon100  / invested_total
        actual_gold_pct   = curr_gold    / invested_total
        actual_reit_pct   = curr_reit    / invested_total
    else:
        actual_equity_pct = actual_mon100_pct = actual_gold_pct = actual_reit_pct = 0

    drift_equity = actual_equity_pct - target_equity_pct
    drift_mon100 = actual_mon100_pct - target_mon100_pct
    drift_gold   = actual_gold_pct   - target_gold_pct
    drift_reit   = actual_reit_pct   - target_reit_pct

    DRIFT_THRESHOLD = 0.05  # 5% trigger

    # ── Drift Dashboard ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 2 — Current Drift Analysis</div>', unsafe_allow_html=True)

    dc1, dc2, dc3 = st.columns(3)

    def drift_card(col, name, actual, target, drift, curr_val):
        status = "🔴 REBALANCE" if abs(drift) >= DRIFT_THRESHOLD else "🟢 ON TARGET"
        drift_color = "#ef4444" if abs(drift) >= DRIFT_THRESHOLD else "#22c55e"
        arrow = "▲" if drift > 0 else "▼"
        with col:
            st.markdown(f"""
            <div class="metric-box" style="border:2px solid {'#ef4444' if abs(drift)>=DRIFT_THRESHOLD else '#22c55e'}">
                <div class="metric-label">{name}</div>
                <div class="metric-value" style="color:{'#ef4444' if abs(drift)>=DRIFT_THRESHOLD else '#22c55e'}">{status}</div>
                <div style="margin:0.5rem 0">
                    <div style="color:#94a3b8;font-size:0.8rem">Target: <strong style="color:#f5c842">{target*100:.0f}%</strong></div>
                    <div style="color:#94a3b8;font-size:0.8rem">Actual: <strong style="color:#e2e8f0">{actual*100:.1f}%</strong></div>
                    <div style="color:{drift_color};font-size:1rem;font-weight:700">{arrow} {abs(drift)*100:.1f}% drift</div>
                </div>
                <div style="color:#64748b;font-size:0.78rem">₹{curr_val/100000:.2f}L invested</div>
            </div>
            """, unsafe_allow_html=True)

    drift_card(dc1, "📊 Nifty 500", actual_equity_pct, target_equity_pct, drift_equity, curr_equity)
    drift_card(dc2, "🌐 MON100 Intl", actual_mon100_pct, target_mon100_pct, drift_mon100, curr_mon100)
    drift_card(dc2, "🥇 Gold (Goldbees)",     actual_gold_pct,   target_gold_pct,   drift_gold,   curr_gold)
    drift_card(dc3, "🏢 REITs",               actual_reit_pct,   target_reit_pct,   drift_reit,   curr_reit)

    # ── Visual Drift Chart ──
    st.markdown("")
    fig_drift = go.Figure()

    categories = ['Nifty 500', 'MON100', 'Gold', 'REIT']
    actuals  = [actual_equity_pct*100, actual_mon100_pct*100, actual_gold_pct*100, actual_reit_pct*100]
    targets  = [40, 20, 20, 20]
    colors_d = ['#3b82f6', '#06b6d4', '#f5c842', '#a855f7']

    fig_drift.add_trace(go.Bar(name='Target Allocation', x=categories, y=targets,
        marker_color=['rgba(59,130,246,0.3)','rgba(245,200,66,0.3)','rgba(168,85,247,0.3)'],
        marker_line=dict(color=colors_d, width=2),
        text=[f"{v:.0f}%" for v in targets], textposition='inside',
        textfont=dict(color='white', size=12)))

    fig_drift.add_trace(go.Bar(name='Your Current Allocation', x=categories, y=actuals,
        marker_color=colors_d, opacity=0.9,
        text=[f"{v:.1f}%" for v in actuals], textposition='inside',
        textfont=dict(color='white', size=12)))

    # Drift threshold lines
    for i, (cat, tgt) in enumerate(zip(categories, targets)):
        fig_drift.add_shape(type='line', x0=i-0.4, x1=i+0.4,
            y0=tgt+5, y1=tgt+5, line=dict(color='#ef4444', width=1.5, dash='dash'))
        fig_drift.add_shape(type='line', x0=i-0.4, x1=i+0.4,
            y0=max(0,tgt-5), y1=max(0,tgt-5), line=dict(color='#ef4444', width=1.5, dash='dash'))

    fig_drift.update_layout(
        title=dict(text="Actual vs Target Allocation (Red dashed = 5% alert threshold)",
                   font=dict(family='Playfair Display', size=16, color='#e2e8f0')),
        barmode='group', paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
        font=dict(family='DM Sans', color='#475569'),
        xaxis=dict(gridcolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%', range=[0, 85]),
        height=380, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1'),
        margin=dict(t=60, b=40, l=60, r=40))

    st.plotly_chart(fig_drift, use_container_width=True)

    # ── Rebalancing Action Plan ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 3 — Exact Rebalancing Instructions</div>', unsafe_allow_html=True)

    rebal_total = curr_total  # include cash in rebalancing
    target_equity_val = rebal_total * target_equity_pct
    target_mon100_val = rebal_total * target_mon100_pct
    target_gold_val   = rebal_total * target_gold_pct
    target_reit_val   = rebal_total * target_reit_pct

    action_equity = target_equity_val - curr_equity
    action_mon100 = target_mon100_val - curr_mon100
    action_gold   = target_gold_val   - curr_gold
    action_reit   = target_reit_val   - curr_reit

    needs_rebalance = any(abs(d) >= DRIFT_THRESHOLD for d in [drift_equity, drift_mon100, drift_gold, drift_reit])

    if needs_rebalance:
        st.markdown(f"""
        <div class="warning-box">
            🔔 <strong>REBALANCING REQUIRED</strong> — One or more asset classes has drifted beyond 5% from target.<br>
            Total portfolio including cash: <strong>₹{rebal_total/100000:.2f} Lakhs</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="insight-box">
            ✅ <strong>NO REBALANCING NEEDED</strong> — All asset classes are within 5% of target. 
            Check back next month or after significant market moves.
        </div>
        """, unsafe_allow_html=True)

    # Action table
    target_mon100_val = rebal_total * target_mon100_pct
    action_mon100     = target_mon100_val - curr_mon100
    actions = [
        ("📊 Nifty 500 ETF",               curr_equity,  target_equity_val,  action_equity),
        ("🌐 MON100 (Nasdaq 100 ETF)",      curr_mon100,  target_mon100_val,  action_mon100),
        ("🥇 Nippon India ETF Gold BeES",   curr_gold,    target_gold_val,    action_gold),
        ("🏢 REIT Basket",                  curr_reit,    target_reit_val,    action_reit),
    ]

    # Build full table in one HTML string to avoid Streamlit breaking the table
    rows_html = ""
    for name, curr, tgt, action in actions:
        if action > 500:
            action_str = "🟢 BUY"
            action_color = "#16a34a"
            amount_color = "#16a34a"
        elif action < -500:
            action_str = "🔴 SELL"
            action_color = "#dc2626"
            amount_color = "#dc2626"
        else:
            action_str = "✅ HOLD"
            action_color = "#d97706"
            amount_color = "#d97706"

        rows_html += f"""
        <tr style="border-bottom:1px solid #e2e8f0">
            <td style="padding:0.85rem 1rem;font-weight:600;color:#0f172a">{name}</td>
            <td style="padding:0.85rem 1rem;text-align:right;color:#475569">₹{curr/100000:.2f}L</td>
            <td style="padding:0.85rem 1rem;text-align:right;color:#475569">₹{tgt/100000:.2f}L</td>
            <td style="padding:0.85rem 1rem;text-align:center;font-weight:700;color:{action_color}">{action_str}</td>
            <td style="padding:0.85rem 1rem;text-align:right;font-weight:700;color:{amount_color}">₹{abs(action)/100000:.2f}L</td>
        </tr>"""

    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;background:#fff;
                  border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(26,86,219,0.08)">
        <thead>
            <tr style="background:#1a56db">
                <th style="width:28%;padding:0.85rem 1rem;text-align:left;color:#fff;
                           font-size:0.75rem;letter-spacing:1px;text-transform:uppercase">Asset Class</th>
                <th style="width:18%;padding:0.85rem 1rem;text-align:right;color:#fff;
                           font-size:0.75rem;letter-spacing:1px;text-transform:uppercase">Current Value</th>
                <th style="width:18%;padding:0.85rem 1rem;text-align:right;color:#fff;
                           font-size:0.75rem;letter-spacing:1px;text-transform:uppercase">Target Value</th>
                <th style="width:18%;padding:0.85rem 1rem;text-align:center;color:#fff;
                           font-size:0.75rem;letter-spacing:1px;text-transform:uppercase">Action</th>
                <th style="width:18%;padding:0.85rem 1rem;text-align:right;color:#fff;
                           font-size:0.75rem;letter-spacing:1px;text-transform:uppercase">Amount</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    if curr_cash > 0:
        st.markdown(f"""
        <div class="info-box" style="margin-top:1rem">
            💰 <strong>Cash deployment:</strong> Your ₹{curr_cash/100000:.2f}L cash has been factored into the 
            rebalancing plan above. Deploying it to reach target allocation improves your Sharpe ratio immediately.
        </div>
        """, unsafe_allow_html=True)

    # ── Price Change Simulator ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 4 — Price Change Alert Simulator</div>', unsafe_allow_html=True)
    st.markdown("See how much prices need to move before a rebalancing alert is triggered:")

    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        equity_chg = st.slider("Nifty 500 moves by (%)", -40, 40, 0, 1)
    with pc2:
        mon100_chg = st.slider("MON100 moves by (%)", -40, 40, 0, 1)
    with pc3:
        gold_chg = st.slider("Gold moves by (%)", -40, 40, 0, 1)
    with pc4:
        reit_chg = st.slider("REITs move by (%)", -40, 40, 0, 1)

    # Simulate new values
    sim_equity = curr_equity * (1 + equity_chg/100)
    sim_mon100 = curr_mon100 * (1 + mon100_chg/100)
    sim_gold   = curr_gold   * (1 + gold_chg/100)
    sim_reit   = curr_reit   * (1 + reit_chg/100)
    sim_total  = sim_equity + sim_mon100 + sim_gold + sim_reit

    if sim_total > 0:
        sim_equity_pct = sim_equity / sim_total
        sim_mon100_pct = sim_mon100 / sim_total
        sim_gold_pct   = sim_gold   / sim_total
        sim_reit_pct   = sim_reit   / sim_total
        sim_drift_eq   = sim_equity_pct - target_equity_pct
        sim_drift_mon  = sim_mon100_pct - target_mon100_pct
        sim_drift_g    = sim_gold_pct   - target_gold_pct
        sim_drift_r    = sim_reit_pct   - target_reit_pct

        sim_alerts = []
        if abs(sim_drift_eq)  >= DRIFT_THRESHOLD:
            sim_alerts.append(f"Nifty 500 drifted to {sim_equity_pct*100:.1f}% (target 40%)")
        if abs(sim_drift_mon) >= DRIFT_THRESHOLD:
            sim_alerts.append(f"MON100 drifted to {sim_mon100_pct*100:.1f}% (target 20%)")
        if abs(sim_drift_g)   >= DRIFT_THRESHOLD:
            sim_alerts.append(f"Gold drifted to {sim_gold_pct*100:.1f}% (target 20%)")
        if abs(sim_drift_r)   >= DRIFT_THRESHOLD:
            sim_alerts.append(f"REIT drifted to {sim_reit_pct*100:.1f}% (target 20%)")

        sc1, sc2, sc3, sc4 = st.columns(4)
        cols_sim = [sc1, sc2, sc3]
        sim_data = [
            ("Equity", sim_equity_pct, sim_drift_eq),
            ("Gold", sim_gold_pct, sim_drift_g),
            ("REIT", sim_reit_pct, sim_drift_r),
        ]
        for col, (nm, pct, drift) in zip(cols_sim, sim_data):
            alert = abs(drift) >= DRIFT_THRESHOLD
            with col:
                st.markdown(f"""
                <div class="metric-box" style="border:1px solid {'#ef4444' if alert else '#1e2d45'}">
                    <div class="metric-label">{nm} after move</div>
                    <div class="metric-value {'metric-red' if alert else 'metric-green'}">{pct*100:.1f}%</div>
                    <div style="color:{'#ef4444' if alert else '#22c55e'};font-size:0.8rem">
                        {'🔔 ALERT!' if alert else '✅ OK'} ({drift*100:+.1f}% drift)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with sc4:
            new_val = sim_total
            pnl = sim_total - invested_total
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Portfolio Value</div>
                <div class="metric-value metric-{'green' if pnl>=0 else 'red'}">₹{new_val/100000:.2f}L</div>
                <div style="color:{'#22c55e' if pnl>=0 else '#ef4444'};font-size:0.8rem">{pnl/100000:+.2f}L P&L</div>
            </div>
            """, unsafe_allow_html=True)

        if sim_alerts:
            alerts_text = "<br>".join([f"⚠️ {a}" for a in sim_alerts])
            st.markdown(f"""
            <div class="warning-box" style="margin-top:1rem">
                🔔 <strong>REBALANCING ALERT WOULD BE TRIGGERED:</strong><br>{alerts_text}<br><br>
                <strong>Subscribers receive this alert instantly via email when real prices cross these thresholds.</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-box" style="margin-top:1rem">
                ✅ No alert triggered at these price levels. Move the sliders to simulate larger market moves.
            </div>
            """, unsafe_allow_html=True)

    # ── Historical rebalancing log ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">📋 Rebalancing History (Sample)</div>', unsafe_allow_html=True)

    rebal_history = [
        ("Mar 2020", "COVID Crash", "Equity fell to 48%", "Buy ₹2.4L Nifty 500", "🔴 Emergency"),
        ("Jan 2021", "Recovery Rally", "Equity rose to 67%", "Sell ₹1.4L Nifty 500, Buy Gold", "🟡 Routine"),
        ("Oct 2021", "Market Peak", "Equity rose to 71%", "Sell ₹2.2L Nifty 500, Buy REIT+Gold", "🔴 Urgent"),
        ("Jun 2022", "Rate Hike Selloff", "Equity fell to 54%", "Buy ₹1.5L Nifty 500", "🟡 Routine"),
        ("Feb 2023", "Annual Review", "All within 5%", "Hold — No action needed", "🟢 All Clear"),
        ("Nov 2023", "REIT Distribution", "REIT fell to 14%", "Buy ₹1.2L REIT", "🟡 Routine"),
        ("Feb 2025", "Current", "Check your values above", "Run analysis above", "📊 Live"),
    ]

    hist_rows = ""
    for date, event, what, action, status in rebal_history:
        # colour the status dot
        if "Emergency" in status or "Urgent" in status:
            dot = "#ef4444"
        elif "Routine" in status:
            dot = "#f59e0b"
        elif "All Clear" in status:
            dot = "#22c55e"
        else:
            dot = "#3b82f6"

        hist_rows += f"""
        <tr style="border-bottom:1px solid #e2e8f0">
            <td style="padding:0.8rem 1rem;font-weight:700;color:#0f172a;white-space:nowrap">{date}</td>
            <td style="padding:0.8rem 1rem;font-weight:500;color:#0f172a">{event}</td>
            <td style="padding:0.8rem 1rem;color:#94a3b8;font-size:0.85rem">{what}</td>
            <td style="padding:0.8rem 1rem;color:#16a34a;font-weight:600;font-size:0.88rem">{action}</td>
            <td style="padding:0.8rem 1rem">
                <span style="display:inline-flex;align-items:center;gap:6px;
                             background:#f8faff;border:1px solid #e2e8f0;
                             border-radius:20px;padding:3px 12px;
                             font-size:0.78rem;font-weight:600;color:#0f172a">
                    <span style="width:8px;height:8px;border-radius:50%;
                                 background:{dot};display:inline-block"></span>
                    {status.split(' ',1)[-1]}
                </span>
            </td>
        </tr>"""

    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;background:#fff;
                  border-radius:12px;overflow:hidden;
                  box-shadow:0 2px 12px rgba(26,86,219,0.08)">
        <thead>
            <tr style="background:#1a56db">
                <th style="padding:0.8rem 1rem;text-align:left;color:#fff;font-size:0.72rem;
                           text-transform:uppercase;letter-spacing:1px;white-space:nowrap">Date</th>
                <th style="padding:0.8rem 1rem;text-align:left;color:#fff;font-size:0.72rem;
                           text-transform:uppercase;letter-spacing:1px">Market Event</th>
                <th style="padding:0.8rem 1rem;text-align:left;color:#fff;font-size:0.72rem;
                           text-transform:uppercase;letter-spacing:1px">What Happened</th>
                <th style="padding:0.8rem 1rem;text-align:left;color:#fff;font-size:0.72rem;
                           text-transform:uppercase;letter-spacing:1px">Action Taken</th>
                <th style="padding:0.8rem 1rem;text-align:left;color:#fff;font-size:0.72rem;
                           text-transform:uppercase;letter-spacing:1px">Status</th>
            </tr>
        </thead>
        <tbody>{hist_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:1rem">
        🔔 <strong>Subscribers get this automatically.</strong> Every time Nifty 500, Goldbees, or REIT 
        prices move enough to drift your portfolio beyond 5%, you receive an instant alert with 
        the exact buy/sell amounts. No guesswork. No monitoring required on your part.
        <br><br>This is the single most valuable feature of the subscription — it keeps you 
        disciplined when markets are most volatile and emotions run highest.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SCREEN 5 — LIFE STAGE TACTICAL ALLOCATION PLANNER
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">🎯 Life Stage Tactical Allocation Planner</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        📌 <strong>Personalised Allocation:</strong> The right asset allocation is not the same for everyone.
        A 25-year-old with 35 years to retirement should take more risk than a 55-year-old approaching 
        retirement. We combine your life stage, risk tolerance, and current market conditions to give you 
        a <strong>personalised tactical allocation</strong> — updated quarterly.
    </div>
    """, unsafe_allow_html=True)

    # ── Personal Profile Input ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Your Personal Profile</div>', unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        age = st.number_input("Your Age", min_value=18, max_value=80, value=35, step=1)
    with p2:
        retirement_age = st.number_input("Target Retirement Age", min_value=40, max_value=80, value=60, step=1)
    with p3:
        monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=100000, step=5000, format="%d")
    with p4:
        monthly_expense = st.number_input("Monthly Expense (₹)", min_value=0, value=60000, step=5000, format="%d")

    p5, p6, p7, p8 = st.columns(4)
    with p5:
        risk_appetite = st.selectbox("Risk Appetite", ["Conservative", "Moderate", "Aggressive"])
    with p6:
        investment_goal = st.selectbox("Primary Goal", ["Retirement Corpus", "Child Education", "Wealth Creation", "Regular Income"])
    with p7:
        emergency_fund = st.selectbox("Emergency Fund", ["Yes — 6+ months", "Yes — 3 months", "No"])
    with p8:
        existing_debt = st.selectbox("Major Loans?", ["None", "Home Loan", "Car/Personal Loan", "Multiple Loans"])

    st.markdown("")
    generate_plan = st.button("🎯 Generate My Personalised Plan", use_container_width=True)

    if generate_plan or True:  # auto show for demo

        years_to_retire = max(1, retirement_age - age)
        monthly_surplus = monthly_income - monthly_expense
        savings_rate = monthly_surplus / monthly_income * 100 if monthly_income > 0 else 0

        # ── Life Stage Classification ──
        if age < 30:
            life_stage = "Early Accumulation"
            life_stage_desc = "Maximum time horizon. Highest capacity for risk. Compound interest works most powerfully now."
            life_color = "#22c55e"
            life_emoji = "🌱"
        elif age < 40:
            life_stage = "Growth Phase"
            life_stage_desc = "Peak earning years approaching. Build aggressively but start protecting gains."
            life_color = "#3b82f6"
            life_emoji = "📈"
        elif age < 50:
            life_stage = "Consolidation Phase"
            life_stage_desc = "Shift from pure growth to growth-with-protection. Reduce volatility exposure."
            life_color = "#f5c842"
            life_emoji = "⚖️"
        elif age < 60:
            life_stage = "Pre-Retirement"
            life_stage_desc = "Capital preservation becomes as important as growth. Defensive allocation needed."
            life_color = "#f97316"
            life_emoji = "🛡️"
        else:
            life_stage = "Retirement / Income"
            life_stage_desc = "Income generation and capital preservation are primary. Minimize drawdown risk."
            life_color = "#a855f7"
            life_emoji = "🏖️"

        # ── Strategic Allocation (base by age) ──
        # Equity % = 100 - age (classic rule, adjusted)
        base_equity = max(30, min(80, 110 - age))
        base_gold   = max(10, min(35, 10 + (age - 25) // 5))
        base_reit   = 100 - base_equity - base_gold

        # Adjust for risk appetite
        if risk_appetite == "Conservative":
            base_equity = max(25, base_equity - 10)
            base_gold   = min(40, base_gold + 5)
            base_reit   = 100 - base_equity - base_gold
        elif risk_appetite == "Aggressive":
            base_equity = min(85, base_equity + 10)
            base_gold   = max(10, base_gold - 5)
            base_reit   = 100 - base_equity - base_gold

        # Adjust for debt burden
        if existing_debt == "Multiple Loans":
            base_equity = max(25, base_equity - 10)
            base_gold   = min(40, base_gold + 5)
            base_reit   = 100 - base_equity - base_gold
        elif existing_debt in ["Home Loan", "Car/Personal Loan"]:
            base_equity = max(30, base_equity - 5)
            base_reit   = 100 - base_equity - base_gold

        # Adjust for emergency fund
        if emergency_fund == "No":
            base_equity = max(25, base_equity - 10)

        strategic_equity = base_equity
        strategic_gold   = base_gold
        strategic_reit   = base_reit

        # ── Tactical Overlay (current market conditions Feb 2026) ──
        # Simulated current macro signals
        macro_signals = {
            "RBI Stance": ("Rate cut cycle — Feb 2026 meet expected 25bps cut", "bullish"),
            "FII Flow (3M)": ("Net Buyers +₹12,400Cr", "bullish"),
            "India VIX": ("14.2 — Low Volatility", "bullish"),
            "Gold Global Trend": ("₹1,59,410/10g today — GOLDBEES ₹126 on NSE", "bullish"),
            "REIT Occupancy": ("92% — Healthy demand", "bullish"),
            "INR vs USD": ("₹90.76 — Weak, up 7% in 12 months", "bearish"),
            "US Fed Rate": ("3.50–3.75% — Paused Jan 2026, 1-2 cuts H2 2026 expected", "bullish"),
            "India GDP Growth": ("6.4% FY25E — Robust, above global avg", "bullish"),
            "India CPI Inflation": ("4.3% Jan 2026 — Falling, near RBI 4% target", "bullish"),
            "Brent Crude": ("$74/bbl — Supportive for India imports", "bullish"),
        }

        # Tactical shifts based on signals
        bullish_count = sum(1 for _, (_, s) in macro_signals.items() if s == "bullish")
        bearish_count = sum(1 for _, (_, s) in macro_signals.items() if s == "bearish")

        if bullish_count >= 4:
            tact_equity_shift = +3
            tact_gold_shift   = -2
            tact_reit_shift   = -1
            market_view = "MODERATELY BULLISH"
            market_color = "#22c55e"
        elif bearish_count >= 3:
            tact_equity_shift = -5
            tact_gold_shift   = +3
            tact_reit_shift   = +2
            market_view = "DEFENSIVE"
            market_color = "#ef4444"
        else:
            tact_equity_shift = 0
            tact_gold_shift   = 0
            tact_reit_shift   = 0
            market_view = "NEUTRAL"
            market_color = "#f5c842"

        tactical_equity = strategic_equity + tact_equity_shift
        tactical_gold   = strategic_gold   + tact_gold_shift
        tactical_reit   = strategic_reit   + tact_reit_shift

        # ── Profile Summary ──
        ls1, ls2, ls3, ls4 = st.columns(4)
        with ls1:
            st.markdown(f"""
            <div class="metric-box" style="border:2px solid {life_color}">
                <div class="metric-label">Life Stage</div>
                <div style="font-size:2rem">{life_emoji}</div>
                <div class="metric-value" style="color:{life_color};font-size:1rem">{life_stage}</div>
                <div style="color:#64748b;font-size:0.75rem">{years_to_retire} years to retire</div>
            </div>""", unsafe_allow_html=True)
        with ls2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Monthly Surplus</div>
                <div class="metric-value metric-{'green' if monthly_surplus>0 else 'red'}">
                    ₹{monthly_surplus/1000:.0f}K
                </div>
                <div style="color:#64748b;font-size:0.75rem">Savings rate: {savings_rate:.0f}%</div>
            </div>""", unsafe_allow_html=True)
        with ls3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Market Stance</div>
                <div class="metric-value" style="color:{market_color};font-size:1rem">{market_view}</div>
                <div style="color:#64748b;font-size:0.75rem">{bullish_count}/6 bullish signals</div>
            </div>""", unsafe_allow_html=True)
        with ls4:
            annual_invest = monthly_surplus * 12
            corpus_needed = monthly_expense * 12 * 25  # 25x annual expense rule
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Retirement Corpus Needed</div>
                <div class="metric-value metric-gold">₹{corpus_needed/10000000:.1f}Cr</div>
                <div style="color:#64748b;font-size:0.75rem">25x annual expense rule</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # ── The Personalised Allocation ──
        st.markdown('<div class="section-header" style="font-size:1.1rem">Your Personalised Tactical Allocation</div>', unsafe_allow_html=True)

        al1, al2 = st.columns([1, 1])

        with al1:
            # Allocation comparison chart
            fig_alloc = go.Figure()

            alloc_categories = ['Nifty 500<br>India Equity', 'MON100<br>Nasdaq Intl', 'Gold<br>BeES', 'REIT']
            standard_40_20_20_20 = [40, 20, 20, 20]
            # Split strategic equity: half Nifty, half MON100 roughly
            strat_intl = min(20, strategic_equity // 2)
            strat_nifty = strategic_equity - strat_intl
            tact_intl = min(20, tactical_equity // 2)
            tact_nifty = tactical_equity - tact_intl
            strategic_vals = [strat_nifty, strat_intl, strategic_gold, strategic_reit]
            tactical_vals  = [tact_nifty,  tact_intl,  tactical_gold,  tactical_reit]

            fig_alloc.add_trace(go.Bar(name='WealthLens Standard 40/20/20/20', x=alloc_categories,
                y=standard_40_20_20_20, marker_color='rgba(100,116,139,0.5)',
                marker_line=dict(color='#64748b', width=1),
                text=[f"{v}%" for v in standard_40_20_20_20], textposition='inside',
                textfont=dict(color='white')))

            fig_alloc.add_trace(go.Bar(name='Your Strategic Allocation', x=alloc_categories,
                y=strategic_vals, marker_color=['rgba(59,130,246,0.7)','rgba(6,182,212,0.7)','rgba(245,200,66,0.7)','rgba(168,85,247,0.7)'],
                text=[f"{v}%" for v in strategic_vals], textposition='inside',
                textfont=dict(color='white')))

            fig_alloc.add_trace(go.Bar(name='Your Tactical Allocation (Now)', x=alloc_categories,
                y=tactical_vals, marker_color=['#3b82f6','#06b6d4','#f5c842','#a855f7'],
                text=[f"{v}%" for v in tactical_vals], textposition='inside',
                textfont=dict(color='white', size=13)))

            fig_alloc.update_layout(
                title=dict(text="Standard vs Your Personalised Allocation",
                           font=dict(family='Playfair Display', size=15, color='#e2e8f0')),
                barmode='group', paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
                font=dict(family='DM Sans', color='#475569'),
                xaxis=dict(gridcolor='#e2e8f0'),
                yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%', range=[0,95]),
                height=380, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1',
                    orientation='h', yanchor='bottom', y=1.02, x=0),
                margin=dict(t=80, b=40, l=60, r=20))

            st.plotly_chart(fig_alloc, use_container_width=True)

        with al2:
            # Glide path over time
            ages_range  = list(range(age, min(80, retirement_age + 15)))
            eq_glide    = [max(25, min(85, 110 - a + (5 if risk_appetite=="Aggressive" else -5 if risk_appetite=="Conservative" else 0))) for a in ages_range]
            gold_glide  = [max(10, min(40, 10 + (a-25)//5)) for a in ages_range]
            reit_glide  = [100 - e - g for e, g in zip(eq_glide, gold_glide)]

            fig_glide = go.Figure()
            fig_glide.add_trace(go.Scatter(x=ages_range, y=eq_glide, mode='lines',
                fill='tozeroy', fillcolor='rgba(59,130,246,0.15)',
                line=dict(color='#3b82f6', width=2.5), name='Equity'))
            fig_glide.add_trace(go.Scatter(x=ages_range, y=[e+g for e,g in zip(eq_glide,gold_glide)],
                mode='lines', fill='tonexty', fillcolor='rgba(245,200,66,0.15)',
                line=dict(color='#f5c842', width=2.5), name='Equity + Gold'))
            fig_glide.add_trace(go.Scatter(x=ages_range, y=[100]*len(ages_range),
                mode='lines', fill='tonexty', fillcolor='rgba(168,85,247,0.15)',
                line=dict(color='#a855f7', width=2.5), name='+ REIT'))

            # Mark current age
            fig_glide.add_vline(x=age, line_dash='dash', line_color='#f5c842',
                annotation_text=f"You are here (Age {age})",
                annotation_font_color='#f5c842')

            # Mark retirement
            if retirement_age <= max(ages_range):
                fig_glide.add_vline(x=retirement_age, line_dash='dot', line_color='#22c55e',
                    annotation_text="Retirement",
                    annotation_font_color='#22c55e')

            fig_glide.update_layout(
                title=dict(text="Your Allocation Glide Path — Age-Based Shift",
                           font=dict(family='Playfair Display', size=15, color='#e2e8f0')),
                paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
                font=dict(family='DM Sans', color='#475569'),
                xaxis=dict(gridcolor='#e2e8f0', title='Age'),
                yaxis=dict(gridcolor='#e2e8f0', ticksuffix='%', range=[0,105]),
                height=380, legend=dict(bgcolor='#ffffff', bordercolor='#cbd5e1',
                    orientation='h', yanchor='bottom', y=1.02, x=0),
                margin=dict(t=80, b=40, l=60, r=20))

            st.plotly_chart(fig_glide, use_container_width=True)

        # ── Macro Signals Dashboard ──
        st.markdown('<div class="section-header" style="font-size:1.1rem">Current Macro Signals — Tactical Overlay</div>', unsafe_allow_html=True)

        sig_cols = st.columns(3)
        signal_list = list(macro_signals.items())
        for i, (signal, (value, sentiment)) in enumerate(signal_list):
            color = "#22c55e" if sentiment=="bullish" else "#ef4444" if sentiment=="bearish" else "#f5c842"
            emoji = "🟢" if sentiment=="bullish" else "🔴" if sentiment=="bearish" else "🟡"
            with sig_cols[i % 3]:
                st.markdown(f"""
                <div class="metric-box" style="border:1px solid {color}44;margin-bottom:0.8rem">
                    <div class="metric-label">{signal}</div>
                    <div style="color:#0f172a;font-size:0.85rem;font-weight:600;margin:0.3rem 0">{value}</div>
                    <div style="color:{color};font-size:0.8rem">{emoji} {sentiment.upper()}</div>
                </div>
                """, unsafe_allow_html=True)

        # Tactical shift explanation
        shifts = []
        if tact_equity_shift > 0:
            shifts.append(f"Equity increased by +{tact_equity_shift}% due to strong FII inflows and low VIX")
        elif tact_equity_shift < 0:
            shifts.append(f"Equity reduced by {tact_equity_shift}% — defensive positioning")
        if tact_gold_shift > 0:
            shifts.append(f"Gold increased by +{tact_gold_shift}% — geopolitical risk hedge active")
        elif tact_gold_shift < 0:
            shifts.append(f"Gold reduced by {tact_gold_shift}% — risk-on environment")
        if shifts:
            shifts_text = "<br>".join([f"• {s}" for s in shifts])
        else:
            shifts_text = "• No tactical shifts — market signals are neutral. Maintain strategic allocation."

        st.markdown(f"""
        <div class="insight-box">
            ⚡ <strong>Tactical Shifts Applied This Quarter:</strong><br><br>
            {shifts_text}<br><br>
            <strong>Your final tactical allocation: {tactical_equity}% Equity | {tactical_gold}% Gold | {tactical_reit}% REIT</strong><br>
            This is reviewed and updated every quarter based on macro signals.
        </div>
        """, unsafe_allow_html=True)

        # ── Corpus Calculator ──
        st.markdown('<div class="section-header" style="font-size:1.1rem">Retirement Corpus Calculator</div>', unsafe_allow_html=True)

        cc1, cc2 = st.columns(2)
        with cc1:
            current_corpus = st.number_input("Current Investments Already Made (₹)", min_value=0,
                                              value=int(total), step=100000, format="%d")
        with cc2:
            expected_return = st.slider("Expected Annual Return (%)", 8, 18,
                int(round(tactical_equity/100*15 + tactical_gold/100*12 + tactical_reit/100*10)))

        # Project corpus
        future_from_existing = current_corpus * (1 + expected_return/100) ** years_to_retire
        future_from_sip      = monthly_surplus * 12 * (((1+expected_return/100)**years_to_retire - 1) / (expected_return/100))
        total_projected      = future_from_existing + future_from_sip

        proj1, proj2, proj3, proj4 = st.columns(4)
        metrics_proj = [
            (proj1, "Years to Retirement", f"{years_to_retire} yrs", "blue"),
            (proj2, "Projected Corpus", f"₹{total_projected/10000000:.1f}Cr", "green"),
            (proj3, "Corpus Needed", f"₹{corpus_needed/10000000:.1f}Cr", "gold"),
            (proj4, "Surplus / Shortfall",
             f"{'+'if total_projected>corpus_needed else ''}₹{(total_projected-corpus_needed)/10000000:.1f}Cr",
             "green" if total_projected>=corpus_needed else "red"),
        ]
        for col, label, val, color in metrics_proj:
            with col:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value metric-{color}">{val}</div>
                </div>""", unsafe_allow_html=True)

        # Corpus growth chart
        ages_proj  = list(range(age, retirement_age + 1))
        corpus_proj = []
        for yr in range(len(ages_proj)):
            from_existing = current_corpus * (1 + expected_return/100) ** yr
            from_sip = monthly_surplus * 12 * (((1+expected_return/100)**yr - 1) / (expected_return/100)) if yr > 0 else 0
            corpus_proj.append(from_existing + from_sip)

        fig_corpus = go.Figure()
        fig_corpus.add_trace(go.Scatter(x=ages_proj, y=[c/10000000 for c in corpus_proj],
            mode='lines', fill='tozeroy', fillcolor='rgba(34,197,94,0.15)',
            line=dict(color='#22c55e', width=3), name='Projected Corpus'))

        fig_corpus.add_hline(y=corpus_needed/10000000, line_dash='dash', line_color='#f5c842',
            annotation_text=f"Target: ₹{corpus_needed/10000000:.1f}Cr",
            annotation_font_color='#f5c842')

        fig_corpus.update_layout(
            title=dict(text="Corpus Growth Projection to Retirement",
                       font=dict(family='Playfair Display', size=15, color='#e2e8f0')),
            paper_bgcolor='#ffffff', plot_bgcolor='#f8faff',
            font=dict(family='DM Sans', color='#475569'),
            xaxis=dict(gridcolor='#e2e8f0', title='Age'),
            yaxis=dict(gridcolor='#e2e8f0', title='Corpus (₹ Crore)'),
            height=320, showlegend=False,
            margin=dict(t=60, b=40, l=80, r=40))

        st.plotly_chart(fig_corpus, use_container_width=True)

        # ── Personal Action Plan ──
        st.markdown('<div class="section-header" style="font-size:1.1rem">📋 Your Personal Action Plan</div>', unsafe_allow_html=True)

        advice = []
        if emergency_fund == "No":
            advice.append(("🚨 Build Emergency Fund First", "Before investing, build 6 months of expenses (₹{:.0f}L) in a liquid fund or FD. Without this, you may be forced to sell investments at the wrong time.".format(monthly_expense*6/100000), "bad"))
        if existing_debt == "Multiple Loans":
            advice.append(("💳 Reduce High-Interest Debt", "Pay off personal/credit card loans before increasing investments. Any loan above 10% interest rate gives better guaranteed return by prepaying than investing.", "bad"))
        if savings_rate < 20:
            advice.append(("💰 Increase Savings Rate", f"Your savings rate is {savings_rate:.0f}%. Target 30%+ for wealth creation. Even ₹{(monthly_income*0.30-monthly_surplus)/1000:.0f}K more per month makes a significant difference over {years_to_retire} years.", "neutral"))
        if age < 35:
            advice.append(("📈 Maximize Equity Now", f"At {age}, time is your greatest asset. Your {tactical_equity}% equity allocation is appropriate. Even 1% extra annual return over {years_to_retire} years adds ₹{current_corpus*(1.01**years_to_retire - 1)/100000:.0f}L to your corpus.", "good"))
        if total_projected < corpus_needed:
            shortfall = corpus_needed - total_projected
            extra_monthly = shortfall / (((1+expected_return/100)**years_to_retire - 1) / (expected_return/100)) / 12
            advice.append(("⚠️ Increase Monthly Investment", f"You have a projected shortfall of ₹{shortfall/10000000:.1f}Cr. To close this gap, increase your monthly SIP by ₹{extra_monthly/1000:.1f}K.", "bad"))
        else:
            advice.append(("✅ On Track for Retirement", f"Excellent! Your current plan projects ₹{total_projected/10000000:.1f}Cr — exceeding your ₹{corpus_needed/10000000:.1f}Cr target. Stay consistent and rebalance annually.", "good"))

        for title, desc, level in advice:
            box_class = "warning-box" if level=="bad" else "insight-box" if level=="good" else "info-box"
            st.markdown(f"""
            <div class="{box_class}">
                <strong>{title}</strong><br>{desc}
            </div>
            """, unsafe_allow_html=True)

        # Payment CTA
        subscription_section(total)


# ════════════════════════════════════════════════════════════════════════════
# ADMIN PANEL
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
with st.expander("🔐 Admin — View Email List & Leads"):
    admin_pass = st.text_input("Admin Password", type="password", key="admpw")
    if admin_pass == "wealthlens2026":
        leads_df = get_leads_df()
        st.markdown(f"### 📋 {len(leads_df)} Registered Users")
        if len(leads_df) == 0:
            st.info("No leads yet. Share your app to start collecting emails!")
        else:
            a1,a2,a3 = st.columns(3)
            a1.metric("Total Leads", len(leads_df))
            a2.metric("Today", len(leads_df[leads_df['Timestamp'].str.startswith(pd.Timestamp.now().strftime('%Y-%m-%d'))]) if len(leads_df)>0 else 0)
            a3.metric("Top Source", leads_df['Source'].value_counts().index[0] if len(leads_df)>0 else "N/A")
            st.dataframe(leads_df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Download CSV", leads_df.to_csv(index=False).encode(), f"leads_{pd.Timestamp.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        st.markdown("""<div class="info-box">
        💳 <strong>Razorpay Setup:</strong> Go to razorpay.com → Sign up → API Keys → Copy Key ID → 
        Replace <code>rzp_test_REPLACE_WITH_YOUR_KEY</code> in the code with your actual key.<br><br>
        📧 <strong>Email Marketing:</strong> Download CSV → Upload to Brevo.com (free 300 emails/day) 
        or Mailchimp to send market updates and subscription offers.
        </div>""", unsafe_allow_html=True)
    elif admin_pass:
        st.error("Incorrect password")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem;color:#334155;font-size:0.72rem;
            border-top:1px solid #1e2d45;margin-top:2rem">
    WealthLens India &nbsp;|&nbsp; Educational purposes only. Not SEBI registered investment advice.
    Past performance does not guarantee future results.<br>
    Data: NSE via Yahoo Finance &nbsp;|&nbsp; Built on CFA Institute BHB research principles &nbsp;|&nbsp;
    Stack: Python · Streamlit · Plotly · yfinance
</div>
""", unsafe_allow_html=True)
