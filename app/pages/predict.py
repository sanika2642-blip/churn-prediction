import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path so we can import predict
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from src.predict import predict_churn

st.set_page_config(page_title="Churn Prediction", page_icon="🎯", layout="wide")

st.title("🎯 Customer Churn Prediction")
st.markdown("Input customer details to predict their likelihood of churning.")

with st.form("prediction_form"):
    st.subheader("Customer Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tenure = st.slider("Tenure (Months)", min_value=0, max_value=72, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=10.0, max_value=150.0, value=70.0)
        
    with col2:
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        
    submit_button = st.form_submit_button("Predict Churn Risk")

if submit_button:
    user_data = {
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'Contract': contract,
        'InternetService': internet
    }
    
    with st.spinner("Analyzing profile..."):
        try:
            result = predict_churn(user_data)
            
            st.markdown("---")
            st.subheader("Prediction Results")
            
            # Layout for results
            res_col1, res_col2 = st.columns(2)
            
            probability = result['probability']
            risk = result['risk_level']
            
            # Dynamic styling based on risk
            risk_color = "red" if risk == "High" else "orange" if risk == "Medium" else "green"
            
            with res_col1:
                st.metric("Churn Probability", f"{probability:.1%}")
            
            with res_col2:
                st.markdown(f"### Risk Level: <span style='color:{risk_color}'>{risk}</span>", unsafe_allow_html=True)
                
            # Create a downloadable report
            report_df = pd.DataFrame([user_data])
            report_df['Predicted_Probability'] = f"{probability:.1%}"
            report_df['Risk_Level'] = risk
            
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Prediction Report",
                data=csv,
                file_name="churn_prediction_report.csv",
                mime="text/csv",
            )
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")