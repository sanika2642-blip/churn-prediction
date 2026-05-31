"""
train.py — Nexus Churn Intelligence
Trains a Random Forest classifier with feature engineering,
saves a complete artifact dict for use by the Streamlit app.

Run:  python train.py
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

from preprocess import load_data, preprocess_data

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_model.pkl"


def train_and_evaluate():
    print("=" * 55)
    print("  NEXUS CHURN INTELLIGENCE — Training Pipeline")
    print("=" * 55)

    print("\n[1/5] Loading and preprocessing data...")
    df = load_data()
    X, y = preprocess_data(df, is_training=True)
    print(f"      Features: {X.shape[1]}  |  Samples: {X.shape[0]}")
    print(f"      Churn rate: {y.mean()*100:.1f}%")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\n[2/5] Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    print("\n[3/5] Evaluating...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy":  round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall":    round(recall_score(y_test, y_pred), 4),
        "f1":        round(f1_score(y_test, y_pred), 4),
        "roc_auc":   round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    for k, v in metrics.items():
        if k != "confusion_matrix":
            print(f"      {k:<12}: {v}")

    print("\n[4/5] Computing feature importances...")
    feature_importance = pd.DataFrame({
        'Feature':    X.columns.tolist(),
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).reset_index(drop=True)

    print(f"      Top feature: {feature_importance.iloc[0]['Feature']}")

    print("\n[5/5] Saving artifact...")
    artifact = {
        "model":              model,
        "features":           X.columns.tolist(),
        "metrics":            metrics,
        "feature_importance": feature_importance,
        "train_shape":        X_train.shape,
        "test_shape":         X_test.shape,
        "churn_rate":         round(float(y.mean()), 4),
        "n_samples":          len(y),
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)

    print(f"      Saved → {MODEL_PATH}")
    print("\n  ✅  Training complete!")
    print("=" * 55)
    return artifact


if __name__ == "__main__":
    train_and_evaluate()
