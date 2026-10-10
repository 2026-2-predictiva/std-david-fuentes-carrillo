"""Train the house price model and save it to submission/."""

import pickle

import pandas as pd  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore
from sklearn.metrics import mean_absolute_error, r2_score  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore

from house_model import DATA_PATH, FEATURES, MODEL_PATH, TARGET


def main():
    df = pd.read_csv(DATA_PATH)
    x, y = df[FEATURES], df[TARGET]

    # Holdout evaluation, only to report how good the model is
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    evaluation = LinearRegression().fit(x_train, y_train)
    y_pred = evaluation.predict(x_test)
    print(f"Test R2:  {r2_score(y_test, y_pred):.4f}")
    print(f"Test MAE: {mean_absolute_error(y_test, y_pred):,.0f}")

    # Final model is fitted on the full dataset
    estimator = LinearRegression().fit(x, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as file:
        pickle.dump(estimator, file)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
