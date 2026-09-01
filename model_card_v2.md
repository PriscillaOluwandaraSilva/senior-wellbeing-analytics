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
Reframed from v1 to use quality-of-care signals — which are genuinely
actionable improvement targets — rather than fixed administrative
attributes. Proof-of-concept for a future Amari Eden internal
engagement-prediction tool; not yet trained on Amari Eden's own data.

## Training Data
13,685 CQC care homes (13,693 from Module 3, minus 8 with missing
domain scores). Target remains imbalanced: 93.5% high-engagement,
6.5% needs-improvement.

## Performance
| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 0.875 | 0.875 |
| Precision | 0.983 | 0.982 |
| Recall | 0.882 | 0.882 |
| F1 | 0.930 | 0.929 |
| ROC-AUC | 0.873 | 0.873 |

Both models perform near-identically and substantially better than v1
(ROC-AUC 0.59 → 0.87), confirming that quality-of-care domain scores
carry far more genuine predictive signal than administrative
attributes.

## Fairness Findings
- Demographic parity difference by Region: 0.123 (v1: 0.855)
- Equalized odds difference by Region: 0.304 (v1: 0.882)
- Disparate impact ratio: 0.864 — PASSES the 0.80 four-fifths threshold
  (v1: 0.145, failed)

No bias mitigation was required for this version, since the disparate
impact ratio already clears the standard threshold. This is itself a
notable finding: switching from proxy administrative features to
genuine quality features resolved most of the fairness problem as a
side effect, without any explicit mitigation step.

## Explainability Highlights
SHAP identifies Well-led as the dominant driver (importance 0.170),
more than double the next feature (Effective, 0.125), followed by
Caring (0.055) and Safe (0.049). Counterfactual analysis confirmed
that improving Safe, Caring, or Well-led by a single point each
independently flips a struggling facility's prediction to
high-engagement — a genuinely actionable finding, unlike v1's
region-driven counterfactual flips.

## Limitations
- Domain scores (Safe, Effective, Caring, Well-led) and the target
  (Responsive) are all assessed by the same CQC inspection visit,
  raising a documented "halo effect" concern: correlation may partly
  reflect shared inspector/day-level factors rather than a pure causal
  relationship between care quality and engagement
- Still UK CQC proof-of-concept data, not Amari Eden's own programming
- Equalized odds difference (0.304) remains higher than ideal even
  though disparate impact passes — worth monitoring, not fully resolved

## Ethical Considerations
This version is meaningfully more defensible for real use than v1, but
should still be paired with human review, given the equalized-odds gap
and the halo-effect caveat above.
