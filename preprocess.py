import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "telco_churn.csv"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    return pd.read_csv(DATA_PATH)

def preprocess_data(df, is_training=True):
    df = df.copy()

    # Fix TotalCharges (sometimes blank string)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['tenure'])

    # Feature engineering
    df['tenure_group'] = pd.cut(
        df['tenure'],
        bins=[-1, 12, 24, 48, 60, 72],
        labels=['0-1yr', '1-2yr', '2-4yr', '4-5yr', '5+yr']
    )
    df['avg_monthly_to_total'] = df['MonthlyCharges'] / (df['TotalCharges'] + 1)
    df['has_streaming'] = (
        (df['StreamingTV'] == 'Yes') | (df['StreamingMovies'] == 'Yes')
    ).astype(int)
    df['has_security_backup'] = (
        (df['OnlineSecurity'] == 'Yes') | (df['OnlineBackup'] == 'Yes')
    ).astype(int)
    df['num_services'] = (
        (df['PhoneService'] == 'Yes').astype(int) +
        (df['MultipleLines'] == 'Yes').astype(int) +
        (df['InternetService'] != 'No').astype(int) +
        (df['OnlineSecurity'] == 'Yes').astype(int) +
        (df['OnlineBackup'] == 'Yes').astype(int) +
        (df['DeviceProtection'] == 'Yes').astype(int) +
        (df['TechSupport'] == 'Yes').astype(int) +
        (df['StreamingTV'] == 'Yes').astype(int) +
        (df['StreamingMovies'] == 'Yes').astype(int)
    )

    # Target
    y = None
    if 'Churn' in df.columns:
        y = df['Churn'].map({'Yes': 1, 'No': 0})
        df = df.drop(columns=['Churn'])

    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    X = pd.get_dummies(df, drop_first=True)

    if is_training:
        return X, y
    else:
        return X
