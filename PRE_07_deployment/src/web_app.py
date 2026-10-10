"""Web interface for the house price model.

Usage:
    python PRE_07_deployment/src/web_app.py
    then open http://127.0.0.1:5000
"""

import os

from flask import Flask, render_template, request  # type: ignore

from house_model import load_model, predict_price

app = Flask(__name__)
model = load_model()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    prediction, error = None, None

    if request.method == "POST":
        # Radio buttons send "Yes"/"No"; the model expects 1/0
        values = request.form.to_dict()
        values["waterfront"] = 1 if values.get("waterfront") == "Yes" else 0
        try:
            prediction = f"{predict_price(model, values):,.2f}"
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html", prediction=prediction, error=error, form=request.form
    )


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
