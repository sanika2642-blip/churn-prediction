import pickle
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from preprocess import load_data, preprocess_data

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "churn_model.pkl"

def train_and_evaluate():
    # Ensure model directory exists
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading and preprocessing data...")
    df = load_data()
    X, y = preprocess_data(df, is_training=True)

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train Model
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")

    # Feature importances (Coefficients)
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_[0]
    }).sort_values(by='Coefficient', ascending=False)

    # Save artifact containing model, features, metrics, and importance
    artifact = {
        "model": model,
        "features": X.columns.tolist(),
        "metrics": metrics,
        "feature_importance": feature_importance
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)
    
    print(f"Model and artifacts successfully saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_evaluate()