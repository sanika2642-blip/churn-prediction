import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title="Insights — Nexus", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
*, *::before, *::after { box-sizing:border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background:#06060f !important; font-family:'DM Sans',sans-serif; color:#e8e8f0;
}
[data-testid="stSidebar"], header, footer { display:none !important; }
.block-container { padding:48px 56px 80px !important; max-width:1300px !important; }
body::before {
    content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
    background: radial-gradient(ellipse 70% 50% at 15% 15%, rgba(88,101,242,0.10) 0%, transparent 55%);
}
.page-title { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; letter-spacing:-1.5px; color:#fff; }
.page-sub { color:#555; font-size:1rem; margin-top:8px; margin-bottom:40px; font-weight:300; }
.kpi { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:22px 20px; text-align:center; }
.kpi-val { font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:800; color:#5865F2; line-height:1; }
.kpi-lbl { font-size:0.72rem; color:#444; text-transform:uppercase; letter-spacing:0.12em; margin-top:6px; }
.section-title { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.12em; margin:40px 0 16px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:12px; }
.insight-box { background:rgba(88,101,242,0.06); border:1px solid rgba(88,101,242,0.18); border-radius:14px; padding:22px 26px; margin-top:32px; }
.insight-title { color:#a0aaff; font-weight:600; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:12px; }
.insight-text { color:#666; font-size:0.9rem; line-height:1.85; }
.stButton>button { background:rgba(88,101,242,0.1) !important; border:1px solid rgba(88,101,242,0.25) !important; border-radius:10px !important; color:#a0aaff !important; font-family:'DM Sans',sans-serif !important; }
.stButton>button:hover { background:rgba(88,101,242,0.2) !important; color:#fff !important; }
</style>
""", unsafe_allow_html=True)

BG = '#0d0d1a'
ACCENT = '#5865F2'
RED = '#EF553B'
GREEN = '#00CC96'
ORANGE = '#FFA15A'
PURPLE = '#AB63FA'

if st.button("← Home"):
    st.switch_page("streamlit_app.py")

st.markdown('<div class="page-title">📊 Data Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Exploratory analysis of 7,043 Telco customers across 20 features.</div>', unsafe_allow_html=True)

@st.cache_data
def load():
    path = ROOT / "telco_churn.csv"
    df = pd.read_csv(path)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['tenure'])
    return df

df = load()

churn_rate = (df['Churn'] == 'Yes').mean() * 100
avg_tenure_churned = df[df['Churn'] == 'Yes']['tenure'].mean()
avg_monthly_churned = df[df['Churn'] == 'Yes']['MonthlyCharges'].mean()
revenue_risk = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()
fiber_churn = (df[df['InternetService'] == 'Fiber optic']['Churn'] == 'Yes').mean() * 100
mtm_churn = (df[df['Contract'] == 'Month-to-month']['Churn'] == 'Yes').mean() * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (f"{churn_rate:.1f}%", "Overall Churn Rate"),
    (f"{avg_tenure_churned:.0f}mo", "Avg Tenure at Churn"),
    (f"${avg_monthly_churned:.0f}", "Avg Charge (Churned)"),
    (f"${revenue_risk:,.0f}", "Monthly Revenue at Risk"),
    (f"{fiber_churn:.0f}%", "Fiber Optic Churn"),
    (f"{mtm_churn:.0f}%", "Month-to-Month Churn"),
]
for col, (val, lbl) in zip([k1, k2, k3, k4, k5, k6], kpis):
    col.markdown(f'<div class="kpi"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

# --- CHARTS ---
def make_fig(w=6, h=3.8):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.spines[:].set_visible(False)
    ax.tick_params(colors='#555', labelsize=9)
    return fig, ax

st.markdown('<div class="section-title">Contract & Internet Service</div>', unsafe_allow_html=True)
r1a, r1b = st.columns(2, gap="large")

with r1a:
    st.markdown("**Churn Rate by Contract Type**")
    data = df.groupby('Contract')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
    data.columns = ['Contract', 'Rate']
    data = data.sort_values('Rate', ascending=True)
    fig, ax = make_fig()
    colors = [RED if v > 30 else ORANGE if v > 10 else GREEN for v in data['Rate']]
    bars = ax.barh(data['Contract'], data['Rate'], color=colors, height=0.45)
    for b, v in zip(bars, data['Rate']):
        ax.text(v + 0.8, b.get_y() + b.get_height()/2, f'{v:.1f}%', va='center', color='#aaa', fontsize=9)
    ax.set_xlabel('Churn Rate (%)', color='#444', fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with r1b:
    st.markdown("**Churn Rate by Internet Service**")
    data = df.groupby('InternetService')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
    data.columns = ['Service', 'Rate']
    fig, ax = make_fig()
    colors = [RED if v > 30 else ORANGE if v > 15 else GREEN for v in data['Rate']]
    bars = ax.bar(data['Service'], data['Rate'], color=colors, width=0.45)
    for b, v in zip(bars, data['Rate']):
        ax.text(b.get_x() + b.get_width()/2, v + 0.8, f'{v:.1f}%', ha='center', color='#aaa', fontsize=9)
    ax.set_ylabel('Churn Rate (%)', color='#444', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

st.markdown('<div class="section-title">Tenure & Charges Distribution</div>', unsafe_allow_html=True)
r2a, r2b = st.columns(2, gap="large")

with r2a:
    st.markdown("**Tenure: Churned vs Retained**")
    fig, ax = make_fig()
    ax.hist(df[df['Churn']=='No']['tenure'], bins=30, alpha=0.55, color=GREEN, label='Retained', density=True)
    ax.hist(df[df['Churn']=='Yes']['tenure'], bins=30, alpha=0.7, color=RED, label='Churned', density=True)
    ax.set_xlabel('Tenure (months)', color='#444', fontsize=9)
    ax.set_ylabel('Density', color='#444', fontsize=9)
    ax.legend(facecolor='#111', labelcolor='#aaa', fontsize=8, framealpha=0.8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with r2b:
    st.markdown("**Monthly Charges: Churned vs Retained**")
    fig, ax = make_fig()
    ax.hist(df[df['Churn']=='No']['MonthlyCharges'], bins=30, alpha=0.55, color=GREEN, label='Retained', density=True)
    ax.hist(df[df['Churn']=='Yes']['MonthlyCharges'], bins=30, alpha=0.7, color=RED, label='Churned', density=True)
    ax.set_xlabel('Monthly Charges ($)', color='#444', fontsize=9)
    ax.set_ylabel('Density', color='#444', fontsize=9)
    ax.legend(facecolor='#111', labelcolor='#aaa', fontsize=8, framealpha=0.8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

st.markdown('<div class="section-title">Payment & Demographics</div>', unsafe_allow_html=True)
r3a, r3b = st.columns(2, gap="large")

with r3a:
    st.markdown("**Churn Rate by Payment Method**")
    data = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
    data.columns = ['Method', 'Rate']
    data['Method'] = data['Method'].str.replace(' (automatic)', '\n(auto)', regex=False)
    data = data.sort_values('Rate', ascending=True)
    fig, ax = make_fig(6, 4)
    colors = [RED if v > 30 else ORANGE if v > 20 else GREEN for v in data['Rate']]
    bars = ax.barh(data['Method'], data['Rate'], color=colors, height=0.45)
    for b, v in zip(bars, data['Rate']):
        ax.text(v + 0.5, b.get_y() + b.get_height()/2, f'{v:.1f}%', va='center', color='#aaa', fontsize=9)
    ax.set_xlabel('Churn Rate (%)', color='#444', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with r3b:
    st.markdown("**Senior Citizen vs Non-Senior Churn**")
    data = df.groupby('SeniorCitizen')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
    data.columns = ['Senior', 'Rate']
    data['Senior'] = data['Senior'].map({0: 'Non-Senior', 1: 'Senior Citizen'})
    fig, ax = make_fig(5, 3.8)
    colors = [GREEN, RED]
    bars = ax.bar(data['Senior'], data['Rate'], color=colors, width=0.4)
    for b, v in zip(bars, data['Rate']):
        ax.text(b.get_x() + b.get_width()/2, v + 0.5, f'{v:.1f}%', ha='center', color='#aaa', fontsize=10, fontweight='bold')
    ax.set_ylabel('Churn Rate (%)', color='#444', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

st.markdown("""
<div class="insight-box">
    <div class="insight-title">🔍 Key Findings</div>
    <div class="insight-text">
        <strong style="color:#ccc">1. Contract type is the strongest churn lever.</strong> Month-to-month customers churn at ~42% — nearly 4× the rate of two-year contracts. Migrating customers to longer contracts is the single highest-ROI retention action.<br><br>
        <strong style="color:#ccc">2. Fiber optic customers are paradoxically high-risk.</strong> Despite paying the most (~$80/month avg), they churn at ~41%. This signals a service quality or value perception problem, not a price problem.<br><br>
        <strong style="color:#ccc">3. First-year customers are the most vulnerable.</strong> Churn is heavily front-loaded — customers who survive past 24 months become dramatically more loyal. Onboarding experience is critical.
    </div>
</div>
""", unsafe_allow_html=True)
