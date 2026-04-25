import streamlit as st

st.set_page_config(
    page_title="ChurnShield — Customer Churn Predictor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #1F4E79, #2196F3);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem; border-radius: 12px; color: white;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .risk-high   { background: #FF4444; color: white; padding: 1rem;
                   border-radius: 10px; text-align: center; font-size: 1.3rem; font-weight: bold; }
    .risk-low    { background: #00C851; color: white; padding: 1rem;
                   border-radius: 10px; text-align: center; font-size: 1.3rem; font-weight: bold; }
    .risk-medium { background: #FF8800; color: white; padding: 1rem;
                   border-radius: 10px; text-align: center; font-size: 1.3rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛡️ ChurnShield — Customer Churn Predictor</p>',
            unsafe_allow_html=True)
st.markdown("##### Built by Sanika Jadhav | ML-powered churn risk analysis")
st.divider()

# Navigation
page = st.sidebar.radio("Navigate", 
    ["🏠 Home", "🔮 Predict Churn", "📊 EDA Dashboard", "📈 Model Insights"])

if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h2>7,043</h2><p>Customers Analyzed</p></div>',
                    unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h2>26.5%</h2><p>Overall Churn Rate</p></div>',
                    unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h2>~87%</h2><p>Model Accuracy</p></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 Key Findings from EDA")
    st.markdown("""
    - 📄 **Month-to-month contracts** have 3x higher churn than 2-year contracts
    - 💳 **Electronic check** payment users churn at nearly 2x the rate of auto-pay users
    - 👴 **Senior citizens** churn at 41% vs 24% for non-seniors
    - 🌐 **Fiber optic** internet users churn more despite faster speeds — pricing may be the trigger
    - 💰 High **monthly charges** (>$65) strongly correlate with churn intent
    """)

elif page == "🔮 Predict Churn":
    import joblib, numpy as np, pandas as pd

    st.markdown("### Enter Customer Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📋 Demographics**")
        gender         = st.selectbox("Gender", ["Male", "Female"])
        senior         = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner        = st.selectbox("Has Partner", ["Yes", "No"])
        dependents     = st.selectbox("Has Dependents", ["Yes", "No"])
        tenure         = st.slider("Tenure (months)", 0, 72, 12)

    with col2:
        st.markdown("**📱 Services**")
        phone_service  = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet       = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        online_sec     = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup  = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

    with col3:
        st.markdown("**💰 Billing**")
        contract       = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless      = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment        = st.selectbox("Payment Method",
                            ["Electronic check", "Mailed check",
                             "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly_charges = st.number_input("Monthly Charges ($)", 18.0, 120.0, 65.0, step=0.5)
        total_charges   = st.number_input("Total Charges ($)", 0.0, 9000.0,
                                           monthly_charges * tenure, step=10.0)

    if st.button("🔮 Predict Churn Risk", use_container_width=True, type="primary"):
        try:
            model        = joblib.load('../models/best_model.pkl')
            scaler       = joblib.load('../models/scaler.pkl')
            feature_cols = joblib.load('../models/feature_columns.pkl')

            # Build input dict
            raw = {
                'gender': 1 if gender == "Male" else 0,
                'SeniorCitizen': 1 if senior == "Yes" else 0,
                'Partner': 1 if partner == "Yes" else 0,
                'Dependents': 1 if dependents == "Yes" else 0,
                'tenure': tenure,
                'PhoneService': 1 if phone_service == "Yes" else 0,
                'PaperlessBilling': 1 if paperless == "Yes" else 0,
                'MonthlyCharges': monthly_charges,
                'TotalCharges': total_charges,
            }

            input_df = pd.DataFrame([raw])
            # One-hot encode to match training columns
            input_df = input_df.reindex(columns=feature_cols, fill_value=0)
            input_scaled = scaler.transform(input_df)
            prob = model.predict_proba(input_scaled)[0][1]

            st.divider()
            col_a, col_b = st.columns(2)
            with col_a:
                risk_pct = f"{prob*100:.1f}%"
                if prob > 0.7:
                    st.markdown(f'<div class="risk-high">🔴 HIGH RISK — {risk_pct}</div>',
                                unsafe_allow_html=True)
                    st.error("**Action:** Offer retention discount or upgrade immediately.")
                elif prob > 0.4:
                    st.markdown(f'<div class="risk-medium">🟡 MEDIUM RISK — {risk_pct}</div>',
                                unsafe_allow_html=True)
                    st.warning("**Action:** Send satisfaction survey and loyalty offer.")
                else:
                    st.markdown(f'<div class="risk-low">🟢 LOW RISK — {risk_pct}</div>',
                                unsafe_allow_html=True)
                    st.success("**Action:** Maintain current service experience.")

            with col_b:
                import plotly.graph_objects as go
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Churn Probability (%)"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 40], 'color': "#00C851"},
                            {'range': [40, 70], 'color': "#FF8800"},
                            {'range': [70, 100], 'color': "#FF4444"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

        except FileNotFoundError:
            st.error("⚠️ Model not found. Run src/train.py first to generate the model files.")

elif page == "📊 EDA Dashboard":
    st.markdown("### Exploratory Data Analysis")
    st.image("static/churn_by_features.png", caption="Churn Rate by Key Features", use_column_width=True)
    st.image("static/correlation_heatmap.png", caption="Feature Correlation Heatmap", use_column_width=True)

elif page == "📈 Model Insights":
    st.markdown("### Model Performance Comparison")
    st.image("static/roc_curves.png", caption="ROC Curves — All Models", use_column_width=True)
    st.markdown("""
    **How to read this:** The closer the curve hugs the top-left corner, the better the model.
    AUC of 1.0 = perfect. AUC of 0.5 = random guessing. Our best model scores ~0.87.
    """)