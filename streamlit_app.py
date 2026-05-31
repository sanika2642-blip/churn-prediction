import streamlit as st

st.set_page_config(
    page_title="Nexus — Churn Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #06060f !important;
    font-family: 'DM Sans', sans-serif;
    color: #e8e8f0;
}
[data-testid="stSidebar"], header, footer { display: none !important; }
[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 48px 56px 80px !important; max-width: 1300px !important; }

/* GRID NOISE TEXTURE */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 10%, rgba(88,101,242,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 85%, rgba(235,69,158,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(0,212,170,0.04) 0%, transparent 60%);
}

/* NAV */
.nav { display:flex; align-items:center; justify-content:space-between; margin-bottom:72px; }
.nav-logo { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; letter-spacing:0.15em; color:#fff; text-transform:uppercase; }
.nav-tag { font-size:0.7rem; color:#444; letter-spacing:0.2em; text-transform:uppercase; }

/* HERO */
.hero { margin-bottom: 80px; }
.hero-eyebrow { font-size:0.75rem; letter-spacing:0.25em; text-transform:uppercase; color:#5865F2; margin-bottom:20px; font-weight:500; }
.hero-h1 {
    font-family:'Syne',sans-serif; font-size:clamp(3.5rem,7vw,6.5rem);
    font-weight:800; letter-spacing:-3px; line-height:0.95;
    color:#fff; margin-bottom:28px;
}
.hero-h1 span {
    background: linear-gradient(135deg, #5865F2 0%, #EB459E 60%, #FF8C42 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-sub { font-size:1.15rem; color:#666; max-width:560px; line-height:1.65; font-weight:300; }

/* STAT STRIP */
.stat-strip { display:flex; gap:0; margin-bottom:72px; border:1px solid rgba(255,255,255,0.06); border-radius:16px; overflow:hidden; }
.stat-item { flex:1; padding:28px 32px; border-right:1px solid rgba(255,255,255,0.06); }
.stat-item:last-child { border-right:none; }
.stat-num { font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; color:#fff; line-height:1; margin-bottom:6px; }
.stat-num span { font-size:1.4rem; color:#5865F2; }
.stat-lbl { font-size:0.75rem; color:#444; text-transform:uppercase; letter-spacing:0.12em; }

/* CARDS */
.card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:64px; }
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius:20px; padding:36px 32px;
    position:relative; overflow:hidden;
    transition: border-color 0.3s, background 0.3s, transform 0.3s;
    cursor:pointer; min-height:240px;
    display:flex; flex-direction:column; justify-content:space-between;
}
.card::before {
    content:''; position:absolute; inset:0; border-radius:20px; opacity:0;
    background: radial-gradient(circle at 30% 30%, rgba(88,101,242,0.08), transparent 60%);
    transition: opacity 0.4s;
}
.card:hover { border-color:rgba(88,101,242,0.35); background:rgba(88,101,242,0.04); transform:translateY(-3px); }
.card:hover::before { opacity:1; }
.card-icon { font-size:2rem; margin-bottom:20px; display:block; }
.card-title { font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700; color:#fff; margin-bottom:10px; }
.card-desc { font-size:0.875rem; color:#555; line-height:1.6; flex:1; }
.card-arrow { color:#5865F2; font-size:1.2rem; margin-top:20px; display:block; }

/* FOOTER */
.footer { border-top:1px solid rgba(255,255,255,0.05); padding-top:28px; display:flex; justify-content:space-between; align-items:center; }
.footer-left { font-size:0.8rem; color:#333; }
.footer-right { font-size:0.75rem; color:#2a2a3a; letter-spacing:0.08em; }

/* BUTTONS */
.stButton > button {
    background: rgba(88,101,242,0.12) !important;
    border: 1px solid rgba(88,101,242,0.25) !important;
    border-radius:12px !important; color:#a0aaff !important;
    font-family:'DM Sans',sans-serif !important; font-size:0.85rem !important;
    font-weight:500 !important; padding:10px 20px !important;
    transition:all 0.2s !important; width:100% !important;
}
.stButton > button:hover {
    background: rgba(88,101,242,0.22) !important;
    border-color:rgba(88,101,242,0.5) !important; color:#fff !important;
    transform:translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
    <div class="nav-logo">⚡ Nexus</div>
    <div class="nav-tag">Churn Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Customer Analytics</div>
    <h1 class="hero-h1">Predict churn.<br><span>Before it costs you.</span></h1>
    <p class="hero-sub">A machine learning system built on 7,043 Telco customers. Random Forest · 84% ROC-AUC · Real-time inference.</p>
</div>
""", unsafe_allow_html=True)

# STATS
st.markdown("""
<div class="stat-strip">
    <div class="stat-item"><div class="stat-num">7<span>k+</span></div><div class="stat-lbl">Customers Analysed</div></div>
    <div class="stat-item"><div class="stat-num">84<span>%</span></div><div class="stat-lbl">ROC-AUC Score</div></div>
    <div class="stat-item"><div class="stat-num">26<span>%</span></div><div class="stat-lbl">Churn Rate Detected</div></div>
    <div class="stat-item"><div class="stat-num">38</div><div class="stat-lbl">Engineered Features</div></div>
    <div class="stat-item"><div class="stat-num">200</div><div class="stat-lbl">Decision Trees</div></div>
</div>
""", unsafe_allow_html=True)

# CARDS
st.markdown("""
<div class="card-grid">
    <div class="card">
        <div>
            <span class="card-icon">📊</span>
            <div class="card-title">Data Insights</div>
            <div class="card-desc">Interactive EDA across churn drivers — contracts, billing, tenure, internet service, and revenue at risk.</div>
        </div>
        <span class="card-arrow">→</span>
    </div>
    <div class="card">
        <div>
            <span class="card-icon">🧠</span>
            <div class="card-title">Model Engine</div>
            <div class="card-desc">Full performance audit — accuracy, precision, recall, F1, ROC-AUC, confusion matrix and top feature importances.</div>
        </div>
        <span class="card-arrow">→</span>
    </div>
    <div class="card">
        <div>
            <span class="card-icon">🎯</span>
            <div class="card-title">Live Predictor</div>
            <div class="card-desc">Enter any customer profile and get instant churn probability, risk tier, and a recommended retention action.</div>
        </div>
        <span class="card-arrow">→</span>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    if st.button("Open Insights →", key="go_eda"):
        st.switch_page("pages/1_insights.py")
with c2:
    if st.button("Audit Model →", key="go_model"):
        st.switch_page("pages/2_model.py")
with c3:
    if st.button("Run Predictor →", key="go_predict"):
        st.switch_page("pages/3_predict.py")

st.markdown("""
<div class="footer">
    <div class="footer-left">Built by <strong style="color:#666">Sanika Jadhav</strong> · B.Sc. Computer Science · Telco Churn Dataset</div>
    <div class="footer-right">github.com/sanika2642-blip</div>
</div>
""", unsafe_allow_html=True)
