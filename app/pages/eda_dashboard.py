import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EDA Dashboard", page_icon="📈", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "telco_churn.csv"

@st.cache_data
def load_raw_data():
    if not DATA_PATH.exists():
        st.error("Dataset not found. Please place 'telco_churn.csv' in the data folder.")
        st.stop()
    return pd.read_csv(DATA_PATH)

df = load_raw_data()

st.title("📈 Exploratory Data Analysis")
st.markdown("Analyze historical customer data to uncover underlying churn patterns.")

# Sidebar Filters
st.sidebar.header("Global Filters")
contract_filter = st.sidebar.multiselect("Contract Type", options=df['Contract'].unique(), default=df['Contract'].unique())
gender_filter = st.sidebar.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique())

# Apply filters
filtered_df = df[(df['Contract'].isin(contract_filter)) & (df['gender'].isin(gender_filter))]

# KPIs
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)

total_customers = len(filtered_df)
churn_count = len(filtered_df[filtered_df['Churn'] == 'Yes'])
churn_rate = (churn_count / total_customers) * 100 if total_customers > 0 else 0

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churn_count:,}")
col3.metric("Overall Churn Rate", f"{churn_rate:.1f}%")

st.markdown("---")

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Churn by Contract Type")
    fig1 = px.histogram(filtered_df, x="Contract", color="Churn", barmode="group",
                        color_discrete_sequence=["#2E86C1", "#E74C3C"])
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Insight: Month-to-month contracts historically show significantly higher churn compared to long-term commitments.")

with col_chart2:
    st.subheader("Tenure Distribution")
    fig2 = px.box(filtered_df, x="Churn", y="tenure", color="Churn",
                  color_discrete_sequence=["#2E86C1", "#E74C3C"])
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Insight: Customers who churn tend to have lower tenure, often leaving within the first year.")

st.subheader("Monthly Charges vs. Churn")
fig3 = px.violin(filtered_df, x="Churn", y="MonthlyCharges", color="Churn", box=True, points="all",
                 color_discrete_sequence=["#2E86C1", "#E74C3C"])
st.plotly_chart(fig3, use_container_width=True)
st.caption("Insight: Higher monthly charges are correlated with an increased likelihood of churn.")