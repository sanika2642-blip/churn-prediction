import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title="Model Engine — Nexus", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

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
    background:radial-gradient(ellipse 60% 50% at 80% 20%, rgba(171,99,250,0.08) 0%, transparent 55%);
}
.page-title { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; letter-spacing:-1.5px; color:#fff; }
.page-sub { color:#555; font-size:1rem; margin-top:8px; margin-bottom:40px; font-weight:300; }
.kpi { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:22px 20px; text-align:center; }
.kpi-val { font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:800; color:#5865F2; line-height:1; }
.kpi-lbl { font-size:0.72rem; color:#444; text-transform:uppercase; letter-spacing:0.12em; margin-top:6px; }
.section-title { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.12em; margin:40px 0 16px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:12px; }
.cm-legend { background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:18px 20px; font-size:0.85rem; color:#555; line-height:2.0; }
.stButton>button { background:rgba(88,101,242,0.1) !important; border:1px solid rgba(88,101,242,0.25) !important; border-radius:10px !important; color:#a0aaff !important; font-family:'DM Sans',sans-serif !important; }
.stButton>button:hover { background:rgba(88,101,242,0.2) !important; color:#fff !important; }
.model-info { background:rgba(0,204,150,0.05); border:1px solid rgba(0,204,150,0.15); border-radius:14px; padding:20px 24px; font-size:0.88rem; color:#666; line-height:1.9; }
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

st.markdown('<div class="page-title">🧠 Model Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Random Forest Classifier · 200 trees · class_weight=balanced · ROC-AUC 0.84</div>', unsafe_allow_html=True)

@st.cache_resource
def load_artifact():
    path = ROOT / "best_model.pkl"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return pickle.load(f)

artifact = load_artifact()

if artifact is None:
    st.error("best_model.pkl not found. Run python train.py first.")
    st.stop()

metrics = artifact["metrics"]
fi = artifact["feature_importance"]
cm = np.array(metrics["confusion_matrix"])

# KPIs
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (f"{metrics['accuracy']*100:.1f}%", "Accuracy"),
    (f"{metrics['precision']*100:.1f}%", "Precision"),
    (f"{metrics['recall']*100:.1f}%", "Recall"),
    (f"{metrics['f1']*100:.1f}%", "F1 Score"),
    (f"{metrics['roc_auc']*100:.1f}%", "ROC-AUC"),
]
for col, (val, lbl) in zip([k1, k2, k3, k4, k5], kpis):
    col.markdown(f'<div class="kpi"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Feature Importances & Confusion Matrix</div>', unsafe_allow_html=True)
ca, cb = st.columns([3, 2], gap="large")

with ca:
    st.markdown("**Top 15 Feature Importances**")
    top = fi.head(15).sort_values('Importance', ascending=True)
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    ax.set_facecolor(BG)
    norm = plt.Normalize(top['Importance'].min(), top['Importance'].max())
    colors = plt.cm.Blues(norm(top['Importance'].values) * 0.7 + 0.3)
    bars = ax.barh(top['Feature'], top['Importance'], color=colors, height=0.6)
    for b, v in zip(bars, top['Importance']):
        ax.text(v + 0.001, b.get_y() + b.get_height()/2, f'{v:.3f}', va='center', color='#666', fontsize=8)
    ax.set_xlabel('Importance Score', color='#444', fontsize=9)
    ax.tick_params(colors='#666', labelsize=8)
    ax.spines[:].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with cb:
    st.markdown("**Confusion Matrix**")
    fig, ax = plt.subplots(figsize=(4.5, 4), facecolor=BG)
    ax.set_facecolor(BG)
    im = ax.imshow(cm, cmap='Blues', aspect='auto')
    labels = [['TN', 'FP'], ['FN', 'TP']]
    for i in range(2):
        for j in range(2):
            color = 'white' if cm[i,j] > cm.max()/2 else '#888'
            ax.text(j, i, f'{labels[i][j]}\n{cm[i,j]:,}', ha='center', va='center',
                    color=color, fontsize=13, fontweight='bold')
    ax.set_xticks([0,1]); ax.set_yticks([0,1])
    ax.set_xticklabels(['Pred: No', 'Pred: Yes'], color='#555', fontsize=9)
    ax.set_yticklabels(['Actual: No', 'Actual: Yes'], color='#555', fontsize=9)
    ax.spines[:].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    tn, fp, fn, tp = cm[0,0], cm[0,1], cm[1,0], cm[1,1]
    st.markdown(f"""
    <div class="cm-legend">
    ✅ <strong style="color:#ccc">True Negatives</strong>: {tn:,} correctly predicted staying<br>
    ✅ <strong style="color:#ccc">True Positives</strong>: {tp:,} correctly predicted churning<br>
    ⚠️ <strong style="color:#ccc">False Positives</strong>: {fp:,} wrongly flagged as churn<br>
    ❌ <strong style="color:#ccc">False Negatives</strong>: {fn:,} missed churners
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Model Configuration</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="model-info">
<strong style="color:#ccc">Algorithm</strong>: Random Forest Classifier (scikit-learn)<br>
<strong style="color:#ccc">Hyperparameters</strong>: n_estimators=200 · max_depth=12 · min_samples_split=5 · class_weight=balanced<br>
<strong style="color:#ccc">Train / Test Split</strong>: 80% / 20% · stratified · random_state=42<br>
<strong style="color:#ccc">Training samples</strong>: {artifact['train_shape'][0]:,} · Test samples: {artifact['test_shape'][0]:,}<br>
<strong style="color:#ccc">Features</strong>: {artifact['train_shape'][1]} (after one-hot encoding + feature engineering)<br>
<strong style="color:#ccc">Class imbalance handling</strong>: class_weight='balanced' (No oversampling needed — RF handles it natively)<br>
<strong style="color:#ccc">Top feature</strong>: {fi.iloc[0]['Feature']} (importance: {fi.iloc[0]['Importance']:.4f})
</div>
""", unsafe_allow_html=True)
