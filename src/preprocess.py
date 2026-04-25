import pandas as pd
import numpy as np
from pathlib import Path

# Dynamic path resolution to handle execution from any directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "telco_churn.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed_churn.csv"

def load_data():
    """Loads raw data from the data directory."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Please add 'telco_churn.csv'.")
    return pd.read_csv(DATA_PATH)

def preprocess_data(df, is_training=True):
    """
    Cleans data, engineers features, and encodes categoricals.
    """
    df = df.copy()

    # 1. Handle Missing Values
    # TotalCharges is sometimes a blank string
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        # Fill missing with MonthlyCharges * tenure if available, else median
        df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['tenure'])
        
    # 2. Feature Engineering
    if 'tenure' in df.columns:
        df['tenure_group'] = pd.cut(
            df['tenure'], 
            bins=[-1, 12, 24, 48, 60, 100], 
            labels=['0-1 Yr', '1-2 Yrs', '2-4 Yrs', '4-5 Yrs', '5+ Yrs']
        )
        
    if 'MonthlyCharges' in df.columns:
        df['charge_category'] = pd.cut(
            df['MonthlyCharges'], 
            bins=[0, 35, 70, 200], 
            labels=['Low', 'Medium', 'High']
        )

    # 3. Target Variable (Only during training/evaluation)
    y = None
    if 'Churn' in df.columns:
        y = df['Churn'].map({'Yes': 1, 'No': 0})
        df = df.drop(columns=['Churn'])

    # Drop identifiers
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    # 4. Encoding
    # Convert categorical to dummy variables (One-Hot Encoding)
    X = pd.get_dummies(df, drop_first=True)

    if is_training:
        # Save processed dataset for record
        processed_df = X.copy()
        if y is not None:
            processed_df['Churn'] = y
        processed_df.to_csv(PROCESSED_DATA_PATH, index=False)
        return X, y
    else:
        return X

if __name__ == "__main__":
    # Test execution
    print("Loading data...")
    df = load_data()
    X, y = preprocess_data(df)
    print(f"Preprocessed Data Shape: X={X.shape}, y={y.shape}")