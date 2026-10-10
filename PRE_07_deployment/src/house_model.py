"""Shared configuration and helpers for the house price model."""

import pickle
from pathlib import Path

import pandas as pd  # type: ignore

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "house_data.csv"
MODEL_PATH = PROJECT_DIR / "submission" / "house_predictor.pkl"

FEATURES = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "condition",
]
TARGET = "price"


def load_model(path=MODEL_PATH):
    """Load the trained estimator from disk."""
    with open(path, "rb") as file:
        return pickle.load(file)


def parse_features(values):
    """Build a one-row DataFrame from a mapping of feature values.

    Raises ValueError if a feature is missing or is not numeric.
    """
    missing = [name for name in FEATURES if name not in values]
    if missing:
        raise ValueError(f"Missing features: {', '.join(missing)}")

    row = {}
    for name in FEATURES:
        try:
            row[name] = float(values[name])
        except (TypeError, ValueError) as error:
            raise ValueError(f"Feature '{name}' must be numeric") from error

    return pd.DataFrame([row], columns=FEATURES)


def predict_price(model, values):
    """Return the predicted price for a mapping of feature values."""
    return float(model.predict(parse_features(values))[0])
