"""REST API that serves house price predictions.

Usage:
    python PRE_07_deployment/src/api_server.py

    curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" \
        -d '{"bedrooms": 3, "bathrooms": 2, "sqft_living": 1800,
             "sqft_lot": 2200, "floors": 1, "waterfront": 0, "condition": 3}'
"""

import os

from flask import Flask, jsonify, request  # type: ignore

from house_model import FEATURES, load_model, predict_price

app = Flask(__name__)
model = load_model()


@app.route("/", methods=["POST"])
def predict():
    """Return the predicted price for the features in the JSON body."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Body must be a JSON object", features=FEATURES), 400

    try:
        price = predict_price(model, payload)
    except ValueError as error:
        return jsonify(error=str(error), features=FEATURES), 400

    return jsonify(price=price)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
