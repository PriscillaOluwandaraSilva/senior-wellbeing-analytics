# Model Card v2: CQC Engagement Prediction Model
## (Domain-Score Features — Superseding v1)

## Model Details
- Type: Random Forest Classifier (tuned via 5-fold cross-validated grid
  search: n_estimators=200, max_depth=4, class_weight=balanced)
- Also compared: Logistic Regression (tuned: C=0.1, StandardScaler
  applied, class_weight=balanced)
- Version: 2.0 (tuned) — reframed from v1 after identifying that
  administrative features were weakly predictive and a source of
  severe unfairness
- Registered in MLflow Model Registry as "cqc_engagement_predictor",
  version 1, stage: Staging
- Framework: scikit-learn, tracked via MLflow

## Intended Use
Predicts whether a UK care home is likely to be rated "high engagement"
from its CQC Safe, Effective, Caring, and Well-led domain scores.
Reframe
