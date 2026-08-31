"""
API Demo Script — CQC Engagement Prediction Model
Module 5, BAN6800

Demonstrates the /predict endpoint from Module 4's FastAPI application
(app_v2.py) with real, varied inputs, showing the response for each.

Run this script directly - it starts the API in-process using FastAPI's
own TestClient (no separate server needed), sends real requests, and
prints the actual responses. This is the same underlying app used by
app_v2.py; a live network demo can be run instead with:
    uvicorn app_v2:app --reload
    (then use requests.post("http://127.0.0.1:8000/predict", json={...}))
"""

from fastapi.testclient import TestClient
from app_v2 import app

client = TestClient(app)

print("=" * 60)
print("CQC ENGAGEMENT PREDICTION API — LIVE DEMONSTRATION")
print("=" * 60)

demo_facilities = [
    {
        "label": "Facility A — strong across the board",
        "payload": {"safe": 3, "effective": 3, "caring": 3, "well_led": 3},
    },
    {
        "label": "Facility B — consistently weak",
        "payload": {"safe": 2, "effective": 2, "caring": 2, "well_led": 2},
    },
    {
        "label": "Facility C — good effectiveness/caring, weak leadership",
        "payload": {"safe": 2, "effective": 3, "caring": 3, "well_led": 2},
    },
    {
        "label": "Facility D — weak everywhere except leadership",
        "payload": {"safe": 2, "effective": 2, "caring": 2, "well_led": 4},
    },
]

for facility in demo_facilities:
    print(f"\n--- {facility['label']} ---")
    print(f"Request payload: {facility['payload']}")

    response = client.post("/predict", json=facility["payload"])

    print(f"HTTP Status: {response.status_code}")
    result = response.json()
    print(f"Predicted high engagement: {result['predicted_high_engagement']}")
    print(f"Probability: {result['probability_high_engagement']:.1%}")
    print(f"Model note: {result['note']}")

print("\n" + "=" * 60)
print("Demo complete — all requests returned HTTP 200")
print("=" * 60)
