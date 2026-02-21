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
    --bg: #0a0f1e;
    --surface: #111827;
    --surface2: #1a2235;
    --gold: #f5c842;
    --gold2: #e8a020;
    --red: #ef4444;
    --green: #22c55e;
    --blue: #3b82f6;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: #1e2d45;
}
* { box-sizing: border-box; }
.stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px; }
h1,h2,h3 { font-family: 'Playfair Display', serif !important; }

.hero { text-align:center; padding:2.5rem 1rem 1.5rem;
        background:radial-gradient(ellipse at 50% 0%,#1a2f5e55 0%,transparent 70%);
        border-bottom:1px solid var(--border); margin-bottom:1.5rem; }
.hero h1 { font-size:2.8rem; font-weight:900;
           background:linear-gradient(135deg,#f5c842,#e8a020,#f5c842);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; }
.hero p { color:var(--muted); font-size:1rem; margin-top:0.4rem; }

.stTabs [data-baseweb="tab-list"] { background:var(--surface)!important;
    border-radius:12px; padding:4px; gap:4px; border:1px solid var(--border); }
.stTabs [data-baseweb="tab"] { background:transparent!important; color:var(--muted)!important;
    border-radius:8px!important; font-family:'DM Sans',sans-serif!important;
    font-weight:500; padding:8px 18px!important; }
.stTabs [aria-selected="true"] { background:var(--gold)!important; color:#0a0f1e!important; }
.stTabs [data-baseweb="tab-panel"] { background:transparent!important; padding:1.5rem 0!important; }

.card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:1.5rem; margin-bottom:1rem; }
.card-gold { background:linear-gradient(135deg,#1a1500,#2a2000); border:1px solid var(--gold2); }

.metric-box { background:var(--surface2); border:1px solid var(--border); border-radius:12px;
              padding:1.2rem 1rem; text-align:center; }
.metric-label { color:var(--muted); font-size:0.72rem; text-transform:uppercase;
                letter-spacing:1px; margin-bottom:0.4rem; }
.metric-value { font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; }
.metric-sub { font-size:0.72rem; margin-top:0.2rem; }
.metric-green { color:var(--green); }
.metric-red { color:var(--red); }
.metric-gold { color:var(--gold); }
.metric-blue { color:var(--blue); }

.compare-table { width:100%; border-collapse:collapse; font-size:0.88rem; }
.compare-table th { background:var(--surface2); padding:0.75rem 1rem; text-align:left;
                    color:var(--muted); font-weight:500; font-size:0.72rem;
                    text-transform:uppercase; letter-spacing:1px; }
.compare-table td { padding:0.75rem 1rem; border-bottom:1px solid var(--border); }
.compare-table tr:last-child td { border-bottom:none; }
.bad { color:var(--red); font-weight:600; }
.good { color:var(--green); font-weight:600; }
.neutral { color:var(--gold); font-weight:600; }

.stButton>button { background:linear-gradient(135deg,var(--gold),var(--gold2))!important;
    color:#0a0f1e!important; font-weight:700!important; border:none!important;
    border-radius:10px!important; padding:0.6rem 2rem!important;
    font-family:'DM Sans',sans-serif!important; font-size:1rem!important; width:100%; }
.stButton>button:hover { transform:translateY(-1px);
    box-shadow:0 8px 24px rgba(245,200,66,0.3)!important; }

.insight-box { background:linear-gradient(135deg,#0f1f0f,#1a2f1a);
    border:1px solid #22c55e44; border-left:4px solid var(--green);
    border-radius:12px; padding:1.2rem 1.5rem; margin:1rem 0;
    font-size:0.92rem; line-height:1.7; color:#a7f3d0; }
.warning-box { background:linear-gradient(135deg,#1f0f0f,#2f1a1a);
    border:1px solid #ef444444; border-left:4px solid var(--red);
    border-radius:12px; padding:1.2rem 1.5rem; margin:1rem 0;
    font-size:0.92rem; line-height:1.7; color:#fca5a5; }
.info-box { background:linear-gradient(135deg,#0f1525,#1a2535);
    border:1px solid #3b82f644; border-left:4px solid var(--blue);
    border-radius:12px; padding:1rem 1.5rem; margin:0.8rem 0;
    font-size:0.88rem; line-height:1.6; color:#93c5fd; }

.section-header { font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:700;
    color:var(--text); margin:1.5rem 0 1rem; padding-bottom:0.4rem;
    border-bottom:2px solid var(--gold); display:inline-block; }

.stock-row { background:var(--surface2); border:1px solid var(--border);
    border-radius:10px; padding:0.8rem 1rem; margin:0.4rem 0;
    display:flex; justify-content:space-between; align-items:center; }

.subscribe-banner { background:linear-gradient(135deg,#1a1500,#2d2200,#1a1500);
    border:2px solid var(--gold); border-radius:20px; padding:2rem;
    text-align:center; margin-top:2rem; }
.subscribe-banner h2 { color:var(--gold); font-size:1.8rem; margin-bottom:0.5rem; }

.ticker { background:var(--surface2); border:1px solid var(--border); border-radius:10px;
    padding:0.7rem 1.2rem; font-size:0.85rem;
    display:flex; justify-content:space-between; align-items:center; margin:0.3rem 0; }

.stNumberInput input, .stTextInput input, .stSelectbox select {
    background:var(--surface2)!important; border:1px solid var(--border)!important;
    color:var(--text)!important; border-radius:8px!important; }

.nse-badge { display:inline-block; background:#22c55e22; border:1px solid #22c55e55;
    color:#22c55e; font-size:0.7rem; padding:2px 8px; border-radius:10px; margin-left:6px; }
.sim-badge { display:inline-block; background:#f5c84222; border:1px solid #f5c84255;
    color:#f5c842; font-size:0.7rem; padding:2px 8px; border-radius:10px; margin-left:6px; }
</style>
""", unsafe_allow_html=True)

# ── NSE Stock Universe ────────────────────────────────────────────────────────
# Comprehensive list of popular NSE stocks with Yahoo Finance tickers
NSE_STOCKS = {
    # Nifty 50 & Large Caps
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
    # Mid Caps
    "Zee Entertainment": "ZEEL.NS",
    "SpiceJet": "SPICEJET.NS",
    "IndiGo (InterGlobe)": "INDIGO.NS",
    "Tata Power": "TATAPOWER.NS",
    "Bharat Forge": "BHARATFORG.NS",
    "Mphasis": "MPHASIS.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "PI Industries": "PIIND.NS",
    "Voltas": "VOLTAS.NS",
    "Havells India": "HAVELLS.NS",
    "Godrej Consumer": "GODREJCP.NS",
    "Marico": "MARICO.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Berger Paints": "BERGEPAINT.NS",
    "Crompton Greaves": "CROMPTON.NS",
    "Trent": "TRENT.NS",
    "Avenue Supermarts (DMart)": "DMART.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm": "PAYTM.NS",
    "Nykaa": "NYKAA.NS",
    "Policybazaar": "POLICYBZR.NS",
    "Delhivery": "DELHIVERY.NS",
    "LIC": "LICI.NS",
    "Vedanta": "VEDL.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Canara Bank": "CANBK.NS",
    "PNB": "PNB.NS",
    "SBI": "SBIN.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "ICICI Prudential": "ICICIPRULI.NS",
    # ETFs / Index
    "Nifty 500 (Motilal ETF)": "MO500.NS",
    "Goldbees (Gold ETF)": "GOLDBEES.NS",
    "Embassy REIT": "EMBASSY.NS",
    "Mindspace REIT": "MINDSPACE.NS",
    "Nexus Select REIT": "NEXUS.NS",
    "Brookfield REIT": "BIRET.NS",
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
    "Goldbees (Gold ETF)": "Gold", "Embassy REIT": "REIT",
    "Mindspace REIT": "REIT", "Nexus Select REIT": "REIT", "Brookfield REIT": "REIT",
    "Nifty 500 (Motilal ETF)": "Index ETF",
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

# ── Session State ─────────────────────────────────────────────────────────────
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [
        {"name": "Reliance Industries", "amount": 1000000},
        {"name": "SpiceJet", "amount": 1000000},
    ]
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = {}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>WealthLens India</h1>
    <p>Institutional-grade asset allocation intelligence for Indian retail investors</p>
</div>
""", unsafe_allow_html=True)

if not YFINANCE_AVAILABLE:
    st.markdown("""
    <div class="info-box">
        ℹ️ <strong>To enable real NSE data:</strong> Run this in your Command Prompt: 
        <code>py -m pip install yfinance</code> then restart the app. 
        Currently showing realistic simulated data.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
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
                <div style="background:#1a2235;border:1px solid #1e2d45;border-radius:10px;
                            padding:0.7rem 0.9rem;margin-bottom:0.3rem">
                    <div style="color:#64748b;font-size:0.7rem">{sector}</div>
                    <div style="color:#e2e8f0;font-weight:600;font-size:0.85rem">{stock['name'][:22]}</div>
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
        else:
            nifty_data = generate_fallback_data('nifty500')
            gold_data = generate_fallback_data('goldbees')
            reit_data = generate_fallback_data('embassy reit')
            data_source['Nifty500'] = data_source['Gold'] = data_source['REIT'] = 'Simulated'
        
        st.session_state.stock_data = stock_data
        st.session_state.nifty_data = nifty_data
        st.session_state.gold_data = gold_data
        st.session_state.reit_data = reit_data
        st.session_state.data_source = data_source
        st.session_state.data_loaded = True

stock_data = st.session_state.stock_data
nifty_data = st.session_state.nifty_data
gold_data = st.session_state.gold_data
reit_data = st.session_state.reit_data
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
            font=dict(color='#94a3b8', size=10), showarrow=False, xanchor='right')
        fig.add_annotation(x=dates_fut[-1], y=p10_path[-1],
            text=f"Worst: ₹{p10_path[-1]/100000:.1f}L",
            font=dict(color='#ef4444', size=10), showarrow=False, xanchor='right')
        
        fig.update_layout(
            title=dict(text="5-Year Monte Carlo — 1,000 Simulated Paths",
                       font=dict(family='Playfair Display', size=16, color='#e2e8f0')),
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2d45'),
            yaxis=dict(gridcolor='#1e2d45', tickformat='₹,.0f'),
            height=420, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45'),
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
            paper_bgcolor='#111827', font=dict(color='#94a3b8', size=9),
            height=260, margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(bgcolor='#111827', font=dict(size=8)),
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
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(color='#94a3b8', size=9),
            yaxis=dict(gridcolor='#1e2d45', ticksuffix='%', range=[0, 120]),
            xaxis=dict(gridcolor='#1e2d45'),
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
    st.markdown('<div class="section-header">WealthLens Strategy — 60% Nifty 500 | 20% Gold | 20% REIT</div>',
                unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    for col, emoji, title, desc in [
        (col_s1, "📊", "60% Nifty 500", "India's top 500 companies. Broad, diversified equity growth. No single stock risk."),
        (col_s2, "🥇", "20% Gold (Goldbees)", "Crisis hedge. Rises when equities fall. Liquid ETF. Culturally trusted in India."),
        (col_s3, "🏢", "20% REIT", "Quarterly rental income from Grade-A offices. Embassy, Mindspace, Nexus."),
    ]:
        with col:
            src = data_source.get('Nifty500' if '500' in title else 'Gold' if 'Gold' in title else 'REIT', 'Simulated')
            badge = '<span class="nse-badge">✅ Live</span>' if src == 'NSE Real' else '<span class="sim-badge">📊 Sim</span>'
            st.markdown(f"""
            <div class="card card-gold">
                <div style="font-size:2rem">{emoji}</div>
                <div style="color:#f5c842;font-weight:700;font-size:1rem">{title} {badge}</div>
                <div style="color:#94a3b8;font-size:0.82rem;margin-top:0.3rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategy metrics
    min_len_bench = min(len(nifty_data), len(gold_data), len(reit_data))
    n_ser = nifty_data.iloc[-min_len_bench:].reset_index(drop=True)
    g_ser = gold_data.iloc[-min_len_bench:].reset_index(drop=True)
    r_ser = reit_data.iloc[-min_len_bench:].reset_index(drop=True)
    
    bench_df = pd.DataFrame({'nifty': n_ser, 'gold': g_ser, 'reit': r_ser})
    bench_returns = bench_df.pct_change().dropna()
    strat_weights = np.array([0.60, 0.20, 0.20])
    
    strat_ann_r, strat_ann_v, strat_sharpe, strat_max_dd = calculate_portfolio_metrics(
        bench_returns, strat_weights)
    
    strat_paths = run_monte_carlo(strat_ann_r, strat_ann_v, total, years=5, simulations=1000)
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
        paper_bgcolor='#111827', plot_bgcolor='#111827',
        font=dict(family='DM Sans', color='#94a3b8'),
        xaxis=dict(gridcolor='#1e2d45'),
        yaxis=dict(gridcolor='#1e2d45', tickformat='₹,.0f'),
        height=450, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45',
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
            <tr><td>Max Drawdown</td><td class="bad">{strat_max_dd*100:.0f}% (est)</td><td class="good">{abs(strat_max_dd)*100:.0f}%</td><td class="good">Better downside protection</td></tr>
            <tr><td>Asset Classes</td><td class="bad">{len(set(SECTOR_MAP.get(s['name'],'Other') for s in portfolio))} sectors, 1 class</td><td class="good">3 asset classes</td><td class="good">True diversification</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box" style="margin-top:1rem">
        ✅ <strong>Why the 60/20/20 Strategy Works</strong><br><br>
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
    min_bench = min(len(nifty_data), len(gold_data), len(reit_data), min_hist)
    n_vals = nifty_data.iloc[-min_bench:].values / nifty_data.iloc[-min_bench]
    g_vals = gold_data.iloc[-min_bench:].values / gold_data.iloc[-min_bench]
    r_vals = reit_data.iloc[-min_bench:].values / reit_data.iloc[-min_bench]
    
    their_trim = their_portfolio[-min_bench:]
    strat_portfolio = total * (0.60 * n_vals + 0.20 * g_vals + 0.20 * r_vals)
    
    # Inflation
    inflation_daily = (1 + 0.055) ** (1/252)
    inflation_vals = total * inflation_daily ** np.arange(min_bench)
    
    hist_dates = pd.date_range(end=datetime.today(), periods=min_bench, freq='B')
    
    final_their_h = their_trim[-1]
    final_strat_h = strat_portfolio[-1]
    final_infl_h = inflation_vals[-1]
    
    min_their_h = their_trim.min()
    min_strat_h = strat_portfolio.min()
    min_their_pct = (min_their_h / total - 1) * 100
    min_strat_pct = (min_strat_h / total - 1) * 100
    
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
            <div class="metric-label">Worst Drawdown</div>
            <div class="metric-value metric-gold">Strat: {min_strat_pct:.0f}%</div>
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
        paper_bgcolor='#111827', plot_bgcolor='#111827',
        font=dict(family='DM Sans', color='#94a3b8'),
        xaxis=dict(gridcolor='#1e2d45'),
        yaxis=dict(gridcolor='#1e2d45', tickformat='₹,.0f'),
        height=480, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45',
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
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            yaxis=dict(gridcolor='#1e2d45', ticksuffix='%'),
            xaxis=dict(gridcolor='#1e2d45', tickangle=-30),
            showlegend=False, height=300,
            margin=dict(t=30, b=60, l=60, r=20))
        fig_bar.add_hline(y=0, line_color='#64748b', line_width=1)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_b2:
        st.markdown('<div class="section-header" style="font-size:1rem">Strategy Components — 5Y Return</div>',
                    unsafe_allow_html=True)
        
        bench_returns_5y = {
            'Nifty 500': (n_vals[-1] - 1) * 100,
            'Gold (Goldbees)': (g_vals[-1] - 1) * 100,
            'REITs': (r_vals[-1] - 1) * 100,
        }
        
        fig_bench = go.Figure(go.Bar(
            x=list(bench_returns_5y.keys()),
            y=list(bench_returns_5y.values()),
            marker_color=['#3b82f6', '#f5c842', '#a855f7'],
            text=[f"+{v:.0f}%" for v in bench_returns_5y.values()],
            textposition='outside', textfont=dict(color='white', size=12)
        ))
        fig_bench.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            yaxis=dict(gridcolor='#1e2d45', ticksuffix='%'),
            xaxis=dict(gridcolor='#1e2d45'),
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
        Over 5 years, the WealthLens 60/20/20 strategy turned ₹{total/100000:.1f}L into 
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
        ('Goldbees ETF', '₹82.45', '+0.31'),
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
                    <div style="color:#e2e8f0;font-weight:600;font-size:1rem">{val_str}</div>
                </div>
                <div style="color:{chg_color};font-weight:700">{arrow} {chg_str}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="color:#475569;font-size:0.72rem;margin-top:0.3rem">* Prices refresh every 5 minutes when using live data</div>',
                unsafe_allow_html=True)
    
    # ── Subscribe Banner ──
    fee_pct = (499 * 12 / total) * 100
    st.markdown(f"""
    <div class="subscribe-banner">
        <h2>📈 Start Your Wealth Journey</h2>
        <p>From today — track this exact 60/20/20 strategy live. Every rupee of movement, 
        every rebalancing signal, explained in plain language.<br>
        For your ₹{total/100000:.1f}L portfolio, this is just <strong>{fee_pct:.2f}% of assets annually</strong> 
        for institutional-quality guidance.</p>
        <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1.5rem;flex-wrap:wrap">
            <div style="background:#1a2235;border:1px solid #f5c842;border-radius:12px;padding:1rem 2rem">
                <div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase">Monthly</div>
                <div style="color:#f5c842;font-size:2rem;font-weight:700;font-family:'Playfair Display',serif">₹499</div>
            </div>
            <div style="background:#1a2235;border:2px solid #22c55e;border-radius:12px;padding:1rem 2rem;position:relative">
                <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);
                            background:#22c55e;color:#0a0f1e;font-size:0.65rem;font-weight:700;
                            padding:2px 10px;border-radius:10px">BEST VALUE</div>
                <div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase">Annual</div>
                <div style="color:#22c55e;font-size:2rem;font-weight:700;font-family:'Playfair Display',serif">₹3,999</div>
                <div style="color:#64748b;font-size:0.72rem">Save 33%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SCREEN 4 — REBALANCING ALERTS
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔔 Rebalancing Alert System</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        📌 <strong>How Rebalancing Works:</strong> Your target is 60% Equity (Nifty 500) | 20% Gold | 20% REIT.
        As markets move, your actual allocation drifts away from this target — creating hidden risk.
        We alert you when drift exceeds <strong>5%</strong> in any asset class and tell you exactly what to buy/sell.
    </div>
    """, unsafe_allow_html=True)

    # ── Current Allocation Input ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 1 — Enter Your Current Holdings Value</div>', unsafe_allow_html=True)

    rb1, rb2, rb3, rb4 = st.columns(4)
    with rb1:
        curr_equity = st.number_input("Current Nifty 500 / Equity Value (₹)", min_value=0, value=700000, step=10000, format="%d")
    with rb2:
        curr_gold = st.number_input("Current Gold / Goldbees Value (₹)", min_value=0, value=150000, step=10000, format="%d")
    with rb3:
        curr_reit = st.number_input("Current REIT Value (₹)", min_value=0, value=150000, step=10000, format="%d")
    with rb4:
        curr_cash = st.number_input("Cash Available to Invest (₹)", min_value=0, value=0, step=10000, format="%d")

    curr_total = curr_equity + curr_gold + curr_reit + curr_cash

    # Target allocations
    target_equity_pct = 0.60
    target_gold_pct   = 0.20
    target_reit_pct   = 0.20

    # Actual allocations (cash excluded from % calc for drift)
    invested_total = curr_equity + curr_gold + curr_reit
    if invested_total > 0:
        actual_equity_pct = curr_equity / invested_total
        actual_gold_pct   = curr_gold   / invested_total
        actual_reit_pct   = curr_reit   / invested_total
    else:
        actual_equity_pct = actual_gold_pct = actual_reit_pct = 0

    drift_equity = actual_equity_pct - target_equity_pct
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

    drift_card(dc1, "📊 Nifty 500 / Equity", actual_equity_pct, target_equity_pct, drift_equity, curr_equity)
    drift_card(dc2, "🥇 Gold (Goldbees)",     actual_gold_pct,   target_gold_pct,   drift_gold,   curr_gold)
    drift_card(dc3, "🏢 REITs",               actual_reit_pct,   target_reit_pct,   drift_reit,   curr_reit)

    # ── Visual Drift Chart ──
    st.markdown("")
    fig_drift = go.Figure()

    categories = ['Nifty 500', 'Gold', 'REIT']
    actuals  = [actual_equity_pct*100, actual_gold_pct*100, actual_reit_pct*100]
    targets  = [60, 20, 20]
    colors_d = ['#3b82f6', '#f5c842', '#a855f7']

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
        barmode='group', paper_bgcolor='#111827', plot_bgcolor='#111827',
        font=dict(family='DM Sans', color='#94a3b8'),
        xaxis=dict(gridcolor='#1e2d45'),
        yaxis=dict(gridcolor='#1e2d45', ticksuffix='%', range=[0, 85]),
        height=380, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45'),
        margin=dict(t=60, b=40, l=60, r=40))

    st.plotly_chart(fig_drift, use_container_width=True)

    # ── Rebalancing Action Plan ──
    st.markdown('<div class="section-header" style="font-size:1.1rem">Step 3 — Exact Rebalancing Instructions</div>', unsafe_allow_html=True)

    rebal_total = curr_total  # include cash in rebalancing
    target_equity_val = rebal_total * target_equity_pct
    target_gold_val   = rebal_total * target_gold_pct
    target_reit_val   = rebal_total * target_reit_pct

    action_equity = target_equity_val - curr_equity
    action_gold   = target_gold_val   - curr_gold
    action_reit   = target_reit_val   - curr_reit

    needs_rebalance = any(abs(d) >= DRIFT_THRESHOLD for d in [drift_equity, drift_gold, drift_reit])

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
    actions = [
        ("📊 Nifty 500 ETF", curr_equity, target_equity_val, action_equity),
        ("🥇 Goldbees ETF",   curr_gold,   target_gold_val,   action_gold),
        ("🏢 REIT Basket",    curr_reit,   target_reit_val,   action_reit),
    ]

    st.markdown(f"""
    <table class="compare-table">
        <thead>
            <tr>
                <th>Asset Class</th>
                <th>Current Value</th>
                <th>Target Value</th>
                <th>Action Required</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for name, curr, tgt, action in actions:
        if action > 500:
            action_str = "🟢 BUY"
            action_class = "good"
        elif action < -500:
            action_str = "🔴 SELL"
            action_class = "bad"
        else:
            action_str = "✅ HOLD"
            action_class = "neutral"
        st.markdown(f"""
            <tr>
                <td><strong>{name}</strong></td>
                <td>₹{curr/100000:.2f}L</td>
                <td>₹{tgt/100000:.2f}L</td>
                <td class="{action_class}">{action_str}</td>
                <td class="{action_class}">₹{abs(action)/100000:.2f}L</td>
            </tr>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)

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

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        equity_chg = st.slider("Nifty 500 moves by (%)", -40, 40, 0, 1)
    with pc2:
        gold_chg = st.slider("Gold moves by (%)", -40, 40, 0, 1)
    with pc3:
        reit_chg = st.slider("REITs move by (%)", -40, 40, 0, 1)

    # Simulate new values
    sim_equity = curr_equity * (1 + equity_chg/100)
    sim_gold   = curr_gold   * (1 + gold_chg/100)
    sim_reit   = curr_reit   * (1 + reit_chg/100)
    sim_total  = sim_equity + sim_gold + sim_reit

    if sim_total > 0:
        sim_equity_pct = sim_equity / sim_total
        sim_gold_pct   = sim_gold   / sim_total
        sim_reit_pct   = sim_reit   / sim_total
        sim_drift_eq   = sim_equity_pct - target_equity_pct
        sim_drift_g    = sim_gold_pct   - target_gold_pct
        sim_drift_r    = sim_reit_pct   - target_reit_pct

        sim_alerts = []
        if abs(sim_drift_eq) >= DRIFT_THRESHOLD:
            sim_alerts.append(f"Equity drifted to {sim_equity_pct*100:.1f}% (target 60%)")
        if abs(sim_drift_g)  >= DRIFT_THRESHOLD:
            sim_alerts.append(f"Gold drifted to {sim_gold_pct*100:.1f}% (target 20%)")
        if abs(sim_drift_r)  >= DRIFT_THRESHOLD:
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

    st.markdown("""
    <table class="compare-table">
        <thead><tr><th>Date</th><th>Market Event</th><th>What Happened</th><th>Action Taken</th><th>Status</th></tr></thead>
        <tbody>
    """, unsafe_allow_html=True)

    for date, event, what, action, status in rebal_history:
        st.markdown(f"""
        <tr>
            <td><strong>{date}</strong></td>
            <td>{event}</td>
            <td style="color:#94a3b8">{what}</td>
            <td class="good">{action}</td>
            <td>{status}</td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)

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
            "RBI Stance": ("Neutral — Rate pause", "neutral"),
            "FII Flow (3M)": ("Net Buyers +₹12,400Cr", "bullish"),
            "India VIX": ("14.2 — Low Volatility", "bullish"),
            "Gold Global Trend": ("Strong — Geopolitical risk", "bullish"),
            "REIT Occupancy": ("92% — Healthy", "bullish"),
            "INR vs USD": ("₹86.4 — Mild weakness", "neutral"),
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

            alloc_categories = ['Nifty 500<br>Equity', 'Gold<br>Goldbees', 'REIT']
            standard_60_20_20 = [60, 20, 20]
            strategic_vals = [strategic_equity, strategic_gold, strategic_reit]
            tactical_vals  = [tactical_equity,  tactical_gold,  tactical_reit]

            fig_alloc.add_trace(go.Bar(name='Standard 60/20/20', x=alloc_categories,
                y=standard_60_20_20, marker_color='rgba(100,116,139,0.5)',
                marker_line=dict(color='#64748b', width=1),
                text=[f"{v}%" for v in standard_60_20_20], textposition='inside',
                textfont=dict(color='white')))

            fig_alloc.add_trace(go.Bar(name='Your Strategic Allocation', x=alloc_categories,
                y=strategic_vals, marker_color=['rgba(59,130,246,0.7)','rgba(245,200,66,0.7)','rgba(168,85,247,0.7)'],
                text=[f"{v}%" for v in strategic_vals], textposition='inside',
                textfont=dict(color='white')))

            fig_alloc.add_trace(go.Bar(name='Your Tactical Allocation (Now)', x=alloc_categories,
                y=tactical_vals, marker_color=['#3b82f6','#f5c842','#a855f7'],
                text=[f"{v}%" for v in tactical_vals], textposition='inside',
                textfont=dict(color='white', size=13)))

            fig_alloc.update_layout(
                title=dict(text="Standard vs Your Personalised Allocation",
                           font=dict(family='Playfair Display', size=15, color='#e2e8f0')),
                barmode='group', paper_bgcolor='#111827', plot_bgcolor='#111827',
                font=dict(family='DM Sans', color='#94a3b8'),
                xaxis=dict(gridcolor='#1e2d45'),
                yaxis=dict(gridcolor='#1e2d45', ticksuffix='%', range=[0,95]),
                height=380, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45',
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
                paper_bgcolor='#111827', plot_bgcolor='#111827',
                font=dict(family='DM Sans', color='#94a3b8'),
                xaxis=dict(gridcolor='#1e2d45', title='Age'),
                yaxis=dict(gridcolor='#1e2d45', ticksuffix='%', range=[0,105]),
                height=380, legend=dict(bgcolor='#1a2235', bordercolor='#1e2d45',
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
                    <div style="color:#e2e8f0;font-size:0.85rem;font-weight:600;margin:0.3rem 0">{value}</div>
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
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2d45', title='Age'),
            yaxis=dict(gridcolor='#1e2d45', title='Corpus (₹ Crore)'),
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

        # Subscribe CTA
        st.markdown(f"""
        <div class="subscribe-banner">
            <h2>🎯 Your Plan. Tracked Live.</h2>
            <p>This personalised {tactical_equity}/{tactical_gold}/{tactical_reit} allocation is reviewed quarterly.<br>
            Get rebalancing alerts, tactical shift updates, and your monthly portfolio health score.<br>
            <strong>Everything above — live, personalised, and updated for you every month.</strong></p>
            <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1.5rem;flex-wrap:wrap">
                <div style="background:#1a2235;border:1px solid #f5c842;border-radius:12px;padding:1rem 2rem">
                    <div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase">Monthly</div>
                    <div style="color:#f5c842;font-size:2rem;font-weight:700;font-family:'Playfair Display',serif">₹499</div>
                    <div style="color:#64748b;font-size:0.75rem">Rebalancing alerts + Monthly report</div>
                </div>
                <div style="background:#1a2235;border:2px solid #22c55e;border-radius:12px;padding:1rem 2rem;position:relative">
                    <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);
                                background:#22c55e;color:#0a0f1e;font-size:0.65rem;font-weight:700;
                                padding:2px 10px;border-radius:10px">BEST VALUE</div>
                    <div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase">Annual</div>
                    <div style="color:#22c55e;font-size:2rem;font-weight:700;font-family:'Playfair Display',serif">₹3,999</div>
                    <div style="color:#64748b;font-size:0.75rem">+ Quarterly personal review call</div>
                </div>
                <div style="background:#1a2235;border:2px solid #a855f7;border-radius:12px;padding:1rem 2rem;position:relative">
                    <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);
                                background:#a855f7;color:#0a0f1e;font-size:0.65rem;font-weight:700;
                                padding:2px 10px;border-radius:10px">PREMIUM</div>
                    <div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase">Advisory</div>
                    <div style="color:#a855f7;font-size:2rem;font-weight:700;font-family:'Playfair Display',serif">₹4,999</div>
                    <div style="color:#64748b;font-size:0.75rem">Monthly call + Full personalisation</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
