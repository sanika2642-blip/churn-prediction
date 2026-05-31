import pickle
import sys
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from preprocess import preprocess_data

MODEL_PATH = BASE_DIR / "best_model.pkl"

_artifact = None

def _load():
    global _artifact
    if _artifact is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _artifact = pickle.load(f)
    return _artifact


def predict_churn(user_input: dict) -> dict:
    artifact = _load()
    model = artifact["model"]
    expected_features = artifact["features"]

    defaults = {
        'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No',
        'Dependents': 'No', 'PhoneService': 'Yes', 'MultipleLines': 'No',
        'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No',
        'TechSupport': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No',
        'PaperlessBilling': 'Yes', 'PaymentMethod': 'Electronic check',
    }
    defaults['TotalCharges'] = (
        user_input.get('MonthlyCharges', 65) * user_input.get('tenure', 12)
    )
    defaults.update(user_input)

    df = pd.DataFrame([defaults])
    X = preprocess_data(df, is_training=False)
    X = X.reindex(columns=expected_features, fill_value=0)

    prob = float(model.predict_proba(X)[0][1])
    label = "Yes" if prob >= 0.5 else "No"
    risk = "High" if prob > 0.70 else ("Medium" if prob >= 0.40 else "Low")

    return {"probability": round(prob, 4), "label": label, "risk_level": risk}
