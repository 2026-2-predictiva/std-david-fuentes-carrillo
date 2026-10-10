"""Example client for api_server.py.

Usage:
    python PRE_07_deployment/src/api_client.py [--url http://127.0.0.1:5000]
"""

import argparse
import os

import requests

EXAMPLE_HOUSE = {
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft_living": 1800,
    "sqft_lot": 2200,
    "floors": 1,
    "waterfront": 0,
    "condition": 3,
}


def make_request(url, data):
    """POST the house features to the API and return the JSON response."""
    response = requests.post(url, json=data, timeout=5)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url", default=os.environ.get("API_URL", "http://127.0.0.1:5000")
    )
    args = parser.parse_args()

    print(make_request(args.url, EXAMPLE_HOUSE))


if __name__ == "__main__":
    main()
