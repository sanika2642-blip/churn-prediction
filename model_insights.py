import streamlit as st
import pickle
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path

st.set_page_config(page_title="Model Insights", page_icon="🧠", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"

st.title("🧠 Model Insights & Evaluation")

@st.cache_resource
def load_model_artifact():
    if not MODEL_PATH.exists():
        st.error("Model not found. Please train the model first by running 'src/train.py'.")
        st.stop()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

artifact = load_model_artifact()
metrics = artifact['metrics']
importance_df = artifact['feature_importance']

# Metrics
st.subheader("Model Performance (Test Set)")
col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
col2.metric("Precision", f"{metrics['precision']:.1%}")
col3.metric("Recall", f"{metrics['recall']:.1%}")

st.markdown("---")

col_cm, col_fi = st.columns([1, 1.5])

with col_cm:
    st.subheader("Confusion Matrix")
    cm = metrics['confusion_matrix']
    fig_cm = ff.create_annotated_heatmap(
        z=cm, 
        x=['Predicted No', 'Predicted Yes'], 
        y=['Actual No', 'Actual Yes'], 
        colorscale='Blues',
        showscale=True
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    st.caption("Visualizes True Positives, True Negatives, False Positives, and False Negatives.")

with col_fi:
    st.subheader("Top Churn Drivers (Feature Importance)")
    # Take top 10 absolute coefficients for visualization
    importance_df['Absolute_Coef'] = importance_df['Coefficient'].abs()
    top_features = importance_df.nlargest(10, 'Absolute_Coef')
    
    fig_fi = px.bar(
        top_features, 
        x='Coefficient', 
        y='Feature', 
        orientation='h',
        color='Coefficient',
        color_continuous_scale=px.colors.diverging.RdBu
    )
    st.plotly_chart(fig_fi, use_container_width=True)
    st.caption("Positive values increase churn probability (e.g., Fiber optic, Short contracts). Negative values decrease it (e.g., Long tenure).")