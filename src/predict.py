import pickle
import pandas as pd
from pathlib import Path
from .preprocess import preprocess_data

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"

# Load artifact once globally for performance
artifact = None
if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        artifact = pickle.load(f)

def predict_churn(user_input_dict):
    """
    Takes user input, maps to required features, and returns prediction.
    """
    if artifact is None:
        raise FileNotFoundError("Model artifact not found. Run train.py first.")

    model = artifact["model"]
    expected_features = artifact["features"]

    # Provide reasonable defaults for features not exposed in the simple UI
    default_data = {
        'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
        'PhoneService': 'Yes', 'MultipleLines': 'No', 'OnlineSecurity': 'No',
        'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
        'StreamingTV': 'No', 'StreamingMovies': 'No', 'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check', 
        'TotalCharges': user_input_dict.get('MonthlyCharges', 0) * user_input_dict.get('tenure', 0)
    }
    
    # Overwrite defaults with actual user input
    default_data.update(user_input_dict)

    # Convert to DataFrame
    df = pd.DataFrame([default_data])

    # Preprocess (creates OHE features)
    X_processed = preprocess_data(df, is_training=False)

    # Align columns to match what the model was trained on
    X_aligned = X_processed.reindex(columns=expected_features, fill_value=0)

    # Predict
    probability = model.predict_proba(X_aligned)[0][1]
    label = "Yes" if probability >= 0.5 else "No"
    
    # Risk Segmentation
    if probability > 0.7:
        risk_level = "High"
    elif probability >= 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "probability": probability,
        "label": label,
        "risk_level": risk_level
    }