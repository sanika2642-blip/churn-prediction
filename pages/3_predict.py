import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from predict import predict_churn

st.set_page_config(page_title="Predictor — Nexus", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

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
    background:radial-gradient(ellipse 60% 50% at 80% 80%, rgba(235,69,158,0.07) 0%, transparent 55%);
}
.page-title { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; letter-spacing:-1.5px; color:#fff; }
.page-sub { color:#555; font-size:1rem; margin-top:8px; margin-bottom:40px; font-weight:300; }
.result-panel { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:40px 36px; height:100%; }
.prob-big { font-family:'Syne',sans-serif; font-size:5rem; font-weight:800; line-height:1; }
.risk-label { font-size:0.75rem; text-transform:uppercase; letter-spacing:0.2em; font-weight:600; margin-bottom:6px; }
.divider { border:none; border-top:1px solid rgba(255,255,255,0.06); margin:24px 0; }
.fact-row { display:flex; justify-content:space-between; font-size:0.88rem; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04); }
.fact-key { color:#444; }
.fact-val { color:#aaa; font-weight:500; }
.action-box { border-radius:14px; padding:18px 20px; font-size:0.88rem; line-height:1.7; margin-top:20px; }
.action-high { background:rgba(239,85,59,0.08); border:1px solid rgba(239,85,59,0.2); color:#EF553B; }
.action-medium { background:rgba(255,161,90,0.08); border:1px solid rgba(255,161,90,0.2); color:#FFA15A; }
.action-low { background:rgba(0,204,150,0.08); border:1px solid rgba(0,204,150,0.2); color:#00CC96; }
.empty-state { text-align:center; padding:80px 40px; color:#333; }
.empty-icon { font-size:3.5rem; margin-bottom:16px; }

/* Form labels */
label { color:#666 !important; font-size:0.82rem !important; text-transform:uppercase !important; letter-spacing:0.08em !important; }
.stSlider > div > div { background:rgba(88,101,242,0.3) !important; }
.stSelectbox > div > div { background:rgba(255,255,255,0.03) !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:10px !important; color:#aaa !important; }

/* Main predict button */
.stButton > button {
    background:linear-gradient(135deg, #5865F2, #AB63FA) !important;
    border:none !important; border-radius:12px !important; color:#fff !important;
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    font-size:1rem !important; padding:14px !important; width:100% !important;
    transition:opacity 0.2s !important;
}
.stButton > button:hover { opacity:0.85 !important; }
div[data-testid="column"]:first-child .stButton > button {
    background: rgba(88,101,242,0.1) !important;
    border: 1px solid rgba(88,101,242,0.25) !important;
    color:#a0aaff !important;
    font-size:0.85rem !important; padding:10px !important;
}
</style>
""", unsafe_allow_html=True)

if st.button("← Home"):
    st.switch_page("streamlit_app.py")

st.markdown('<div class="page-title">🎯 Live Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Enter a customer profile for real-time churn probability and retention advice.</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("##### Customer Profile")

    c1, c2 = st.columns(2)
    with c1:
        tenure = st.slider("Tenure (months)", 0, 72, 12)
    with c2:
        monthly_charges = st.slider("Monthly Charges ($)", 18.0, 120.0, 65.0, step=1.0)

    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])

    c3, c4 = st.columns(2)
    with c3:
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    with c4:
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    payment = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])

    c5, c6 = st.columns(2)
    with c5:
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Has Partner", ["No", "Yes"])
    with c6:
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents", ["No", "Yes"])

    st.write("")
    run = st.button("⚡ Predict Churn Risk", use_container_width=True)

with right:
    st.markdown("##### Risk Assessment")
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)

    if run:
        user_input = {
            'tenure': tenure,
            'MonthlyCharges': monthly_charges,
            'Contract': contract,
            'InternetService': internet,
            'TechSupport': tech_support,
            'OnlineSecurity': online_security,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'PaymentMethod': payment,
            'SeniorCitizen': 1 if senior == "Yes" else 0,
            'Partner': partner,
            'PaperlessBilling': paperless,
            'Dependents': dependents,
        }

        with st.spinner("Running inference..."):
            result = predict_churn(user_input)

        prob = result['probability']
        risk = result['risk_level']
        label = result['label']
        pct = prob * 100

        color_map = {'High': '#EF553B', 'Medium': '#FFA15A', 'Low': '#00CC96'}
        emoji_map = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        color = color_map[risk]

        st.markdown(f'<div class="risk-label" style="color:{color}">{emoji_map[risk]} {risk} Risk</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prob-big" style="color:{color}">{pct:.1f}<span style="font-size:2rem; color:#333">%</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#444; font-size:0.85rem; margin-top:6px;">Churn Probability · Prediction: <strong style="color:#aaa">{"Will Churn" if label=="Yes" else "Will Stay"}</strong></div>', unsafe_allow_html=True)

        st.progress(prob)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Key factors displayed
        factors = [
            ("Contract", contract),
            ("Tenure", f"{tenure} months"),
            ("Monthly Charges", f"${monthly_charges:.0f}"),
            ("Internet", internet),
            ("Payment Method", payment),
            ("Senior Citizen", senior),
        ]
        for k, v in factors:
            st.markdown(f'<div class="fact-row"><span class="fact-key">{k}</span><span class="fact-val">{v}</span></div>', unsafe_allow_html=True)

        # Retention recommendation
        if risk == "High":
            st.markdown("""
            <div class="action-box action-high">
            <strong>⚠️ Immediate Action Required</strong><br>
            Offer a contract upgrade incentive or loyalty discount. High-risk customers on month-to-month plans with fiber optic and electronic check are 3× more likely to churn within 30 days.
            </div>""", unsafe_allow_html=True)
        elif risk == "Medium":
            st.markdown("""
            <div class="action-box action-medium">
            <strong>👀 Monitor & Engage</strong><br>
            Schedule a proactive check-in. Consider bundling tech support or online security — customers with 2+ add-ons churn at half the rate.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="action-box action-low">
            <strong>✅ Low Risk — Customer is Stable</strong><br>
            Long-tenure customer on a term contract. Focus retention spend on higher-risk segments. Consider upsell opportunities.
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎯</div>
            <div style="color:#333; font-size:0.95rem;">Fill in the customer profile<br>and click <strong style="color:#5865F2">Predict Churn Risk</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
