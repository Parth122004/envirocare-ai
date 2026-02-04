import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

MODEL_PATH = "models/lstm_aqi.h5"

# ----- Create synthetic AQI training data -----
def create_dataset():
    # Past 5 values → predict next value
    X = []
    y = []

    data = np.linspace(50, 200, 200)  # fake realistic AQI trend

    for i in range(len(data) - 5):
        X.append(data[i:i+5])
        y.append(data[i+5])

    X = np.array(X).reshape(-1, 5, 1)
    y = np.array(y)
    return X, y

def train_and_save_model():
    X, y = create_dataset()

    model = Sequential([
        LSTM(32, activation="relu", input_shape=(5,1)),
        Dense(16, activation="relu"),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")

    print("Training LSTM... (may take 20–40 seconds)")
    model.fit(X, y, epochs=30, batch_size=16, verbose=1)

    os.makedirs("models", exist_ok=True)
    model.save(MODEL_PATH)

    print("Saved trained model to:", MODEL_PATH)

if __name__ == "__main__":
    train_and_save_model()
