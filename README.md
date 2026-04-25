# Customer Churn Intelligence System

A production-quality machine learning application to predict and analyze customer churn, built with Python, scikit-learn, and Streamlit.

## Features
* **Modular Pipeline:** Separated source code for data preprocessing, model training, and prediction.
* **EDA Dashboard:** Interactive Plotly-based KPIs and visualizations.
* **Model Insights:** Transparent view into model metrics, confusion matrix, and feature importances.
* **Prediction Interface:** Form-based inference with risk segmentation (Low, Medium, High) and downloadable reports.

## Structure
* `/app`: Streamlit application and pages.
* `/data`: Raw data (place `telco_churn.csv` here).
* `/models`: Serialized machine learning models and artifacts.
* `/src`: Core logic (preprocessing, training, inference).

## How to Run
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Add Data:** Ensure the Kaggle Telco Customer Churn dataset is saved as `data/telco_churn.csv`.
3.  **Train the Model:** Generate the `.pkl` artifact.
    ```bash
    python src/train.py
    ```
4.  **Run the App:**
    ```bash
    streamlit run app/streamlit_app.py
    ```