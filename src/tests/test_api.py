"""
Automated tests for the CQC Engagement Prediction API.
Run with: pytest tests/test_api.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app_v2 import app

client = TestClient(app)


def test_root_endpoint_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_predict_returns_200_for_valid_input():
    response = client.post("/predict", json={
        "safe": 3, "effective": 3, "caring": 3, "well_led": 3
    })
    assert response.status_code == 200


def test_predict_response_has_expected_fields():
    response = client.post("/predict", json={
        "safe": 3, "effective": 3, "caring": 3, "well_led": 3
    })
    body = response.json()
    assert "predicted_high_engagement" in body
    assert "probability_high_engagement" in body
    assert "note" in body


def test_predict_probability_is_valid_range():
    response = client.post("/predict", json={
        "safe": 2, "effective": 2, "caring": 2, "well_led": 2
    })
    proba = response.json()["probability_high_engagement"]
    assert 0.0 <= proba <= 1.0


def test_predict_rejects_invalid_score_out_of_range():
    # Scores must be 1-4; 9 is invalid and should be rejected by FastAPI's validation
    response = client.post("/predict", json={
        "safe": 9, "effective": 3, "caring": 3, "well_led": 3
    })
    assert response.status_code == 422  # FastAPI validation error


def test_high_scores_predict_higher_probability_than_low_scores():
    high = client.post("/predict", json={"safe": 4, "effective": 4, "caring": 4, "well_led": 4})
    low = client.post("/predict", json={"safe": 1, "effective": 1, "caring": 1, "well_led": 1})
    high_proba = high.json()["probability_high_engagement"]
    low_proba = low.json()["probability_high_engagement"]
    assert high_proba > low_proba
