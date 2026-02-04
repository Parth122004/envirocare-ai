import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def build_dummy_lstm():
    model = Sequential([
        LSTM(16, activation="relu", input_shape=(5, 1)),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")

    # Quick mini-training so outputs are sensible
    X = np.array([
        [95,100,105,110,120],
        [80,85,90,95,100],
        [120,115,110,105,100]
    ]).reshape(3,5,1)

    y = np.array([125, 105, 95])

    model.fit(X, y, epochs=10, verbose=0)
    return model

# Keep a single model in memory (IMPORTANT FIX)
_model_cache = None

def load_lstm():
    global _model_cache
    if _model_cache is None:
        _model_cache = build_dummy_lstm()
    return _model_cache

def predict_trend(values):
    model = load_lstm()

    # Convert to proper LSTM shape
    X = np.array(values, dtype=float).reshape(1, 5, 1)

    raw_pred = float(model.predict(X)[0][0])

    # --- SANITY FIXES FOR AQI ---
    base = values[-1]            # current AQI
    predicted = base + raw_pred * 0.05   # small realistic change
    predicted = max(0, predicted)        # no negative AQI

    return round(predicted, 2)
