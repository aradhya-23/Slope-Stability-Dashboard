


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

DATA_PATH = "data/labeled_data.csv"
MODEL_PATH = "model/slope_model.pkl"

def train_model(new_data=None):
    if new_data is not None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Model not found! Please train the model first.")
        model = joblib.load(MODEL_PATH)
        X_new = new_data[["NDVI", "slope", "rainfall"]]
        new_data["predicted_stability"] = model.predict(X_new)
        return new_data

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Dataset not found. Run data collection first.")

    df = pd.read_csv(DATA_PATH)
    X = df[["NDVI", "slope", "rainfall"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained successfully and saved to model/slope_model.pkl")
    return model


if __name__ == "__main__":
    train_model()

