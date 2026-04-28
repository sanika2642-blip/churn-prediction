import streamlit as st

st.set_page_config(page_title="Nexus AI", page_icon="⚡", layout="wide")

# --- THE "LIQUID DARK" CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 110, 250, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(239, 85, 59, 0.1) 0px, transparent 50%);
    }

    .stApp { background: transparent; }

    /* Glass Card Design */
    .bento-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 40px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .bento-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(99, 110, 250, 0.5);
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .icon-circle {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #636EFA, #AB63FA);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(99, 110, 250, 0.3);
    }

    .hero-text {
        font-weight: 800;
        font-size: 4rem;
        letter-spacing: -2px;
        background: linear-gradient(to bottom, #fff 40%, #666 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    /* Modern Buttons */
    .stButton>button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 10px 24px !important;
        transition: 0.3s !important;
    }

    .stButton>button:hover {
        border-color: #636EFA !important;
        background: rgba(99, 110, 250, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<h1 class="hero-text">Nexus.ai</h1>', unsafe_allow_html=True)
st.markdown("<p style='color: #888; font-size: 1.5rem; margin-top: -10px;'>Predicting churn before it happens.</p>", unsafe_allow_html=True)

st.write("##")
st.write("##")

# --- BENTO NAVIGATION ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class="bento-card">
            <div class="icon-circle">📈</div>
            <h2>Insights</h2>
            <p style='color: #777;'>Deep-dive into customer behavior patterns and revenue leakage.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Dashboard", use_container_width=True):
        st.switch_page("pages/eda_dashboard.py")

with col2:
    st.markdown("""
        <div class="bento-card">
            <div class="icon-circle">🧠</div>
            <h2>Engine</h2>
            <p style='color: #777;'>Explainable AI metrics, feature weights, and performance audits.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Audit Model", use_container_width=True):
        st.switch_page("pages/model_insights.py")

with col3:
    st.markdown("""
        <div class="bento-card">
            <div class="icon-circle">🎯</div>
            <h2>Predict</h2>
            <p style='color: #777;'>Real-time churn risk profiling and customer segmentation.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Run Inference", use_container_width=True):
        st.switch_page("pages/predict.py")