"""
FastAPI application for the v2 CQC engagement prediction model.
Predicts high-engagement likelihood from CQC quality domain scores
(Safe, Effective, Caring, Well-led) rather than administrative
attributes - a business-actionable reframing over the v1 model.
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="CQC Engagement Prediction API v2")
model = joblib.load("random_forest_v2.pkl")

class FacilityScores(BaseModel):
    safe: int = Field(ge=1, le=4, description="CQC Safe domain score, 1-4")
    effective: int = Field(ge=1, le=4, description="CQC Effective domain score, 1-4")
    caring: int = Field(ge=1, le=4, description="CQC Caring domain score, 1-4")
    well_led: int = Field(ge=1, le=4, description="CQC Well-led domain score, 1-4")

@app.post("/predict")
def predict(facility: FacilityScores):
    X = pd.DataFrame([{
        "Safe": facility.safe, "Effective": facility.effective,
        "Caring": facility.caring, "Well-led": facility.well_led,
    }])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]
    return {
        "predicted_high_engagement": bool(pred),
        "probability_high_engagement": round(float(proba), 4),
        "top_driver": "Well-led",
        "note": "Model trained on CQC domain scores (ROC-AUC ~0.87, disparate impact ratio ~0.86 by region). More business-actionable than administrative features, but still a UK regulatory-data proof-of-concept, not Amari Eden's own data."
    }

@app.get("/")
def root():
    return {"status": "ok", "model": "RandomForestClassifier v2", "endpoint": "/predict (POST)"}
