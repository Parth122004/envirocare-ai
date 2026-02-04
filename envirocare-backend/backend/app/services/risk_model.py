import xgboost as xgb
import numpy as np
import os
from pathlib import Path

MODEL_PATH = Path("models/xgb_risk.json")

def build_dummy_model():
    """
    Creates a very small demo XGBoost model so your project
    actually HAS a model file (important for viva + GitHub).
    """
    X = np.array([
        [20, 0, 0, 1],  # young, no asthma, no allergy, medium
        [65, 1, 0, 2],  # elderly + asthma
        [30, 0, 1, 2],  # allergy + high sensitivity
    ])
    y = np.array([0.2, 0.8, 0.6])

    model = xgb.XGBRegressor(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1
    )
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    model.save_model(MODEL_PATH)
    return model

def load_model():
    if not MODEL_PATH.exists():
        return build_dummy_model()

    model = xgb.XGBRegressor()
    model.load_model(MODEL_PATH)
    return model

def predict_risk(age: int, has_asthma: bool, has_allergy: bool, sensitivity: float):
    model = load_model()

    # Convert float sensitivity → category
    if sensitivity <= 0.33:
        sens_code = 0   # low
    elif sensitivity <= 0.66:
        sens_code = 1   # medium
    else:
        sens_code = 2   # high

    X = np.array([[age, int(has_asthma), int(has_allergy), sens_code]])

    risk = float(model.predict(X)[0])
    return round(min(1.0, max(0.0, risk)), 2)
