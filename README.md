# ⚡ Nexus — Churn Intelligence Platform

> Predict customer churn before it costs you. Built with Random Forest, scikit-learn, and Streamlit.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=flat&logo=streamlit)](https://nexus-churn-intelligence.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-orange?style=flat)](https://scikit-learn.org)

---

## What This Does

Nexus is an end-to-end machine learning system for predicting customer churn on the Telco dataset (7,043 customers). It covers the full ML lifecycle — data cleaning, feature engineering, model training, evaluation, and a live inference UI.

**Key results:**
- ROC-AUC: **0.84**
- Recall: **71%** (catches 7 out of 10 churners)
- F1: **0.62** on an imbalanced dataset (26.5% churn rate)

---

## Features

| Page | What it does |
|------|-------------|
| **Data Insights** | EDA — churn by contract, internet service, tenure, charges, payment method, demographics |
| **Model Engine** | Full audit — accuracy, precision, recall, F1, ROC-AUC, confusion matrix, top 15 feature importances |
| **Live Predictor** | Real-time churn probability from any customer profile with risk tier and retention recommendation |

---

## Tech Stack

- **ML**: scikit-learn (Random Forest, train/test split, cross-validation)
- **Data**: pandas, numpy
- **Visualisation**: matplotlib
- **App**: Streamlit
- **Dataset**: [Telco Customer Churn — IBM](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Project Structure

```
nexus-churn/
├── streamlit_app.py       # Home page
├── pages/
│   ├── 1_insights.py      # EDA dashboard
│   ├── 2_model.py         # Model performance
│   └── 3_predict.py       # Live predictor
├── preprocess.py          # Feature engineering pipeline
├── train.py               # Training script
├── predict.py             # Inference logic
├── best_model.pkl         # Trained model artifact
├── telco_churn.csv        # Raw dataset
├── requirements.txt
└── runtime.txt            # Python 3.11
```

---

## Run Locally

```bash
git clone https://github.com/sanika2642-blip/churn-prediction
cd churn-prediction
pip install -r requirements.txt
python train.py          # retrain model
streamlit run streamlit_app.py
```

---

## Key Findings

1. **Month-to-month contracts** churn at ~42% — 4× higher than two-year contracts
2. **Fiber optic customers** churn at ~41% despite paying the most — a service quality signal
3. **First-year customers** are the most vulnerable — onboarding is the highest-leverage intervention

---

Built by **Sanika Jadhav** · [LinkedIn](https://linkedin.com/in/sanika-jadhav-b88215398) · [GitHub](https://github.com/sanika2642-blip)
