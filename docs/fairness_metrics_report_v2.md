# Fairness Metrics Report v2
## CQC Engagement Prediction Model — Domain-Score Features

## Protected Attribute Tested
Region (9 groups)

## Results

| Metric | v1 (region/size features) | v2 (domain-score features) | Threshold |
|---|---|---|---|
| Demographic parity difference | 0.855 | 0.123 | Closer to 0 is better |
| Equalized odds difference | 0.882 | 0.304 | Closer to 0 is better |
| Disparate impact ratio | 0.145 (FAILS) | 0.864 (PASSES) | ≥ 0.80 |

## Interpretation
Reframing the model to predict from CQC quality-of-care domain scores
(Safe, Effective, Caring, Well-led) instead of administrative
attributes (region, provider size) resolved the majority of the
fairness problem identified in v1, without any explicit bias
mitigation technique applied. This suggests the v1 unfairness was
substantially driven by using region as a direct predictive feature —
once removed in favor of genuine quality signals, disparate impact
improved from a severe failure (0.145) to a passing result (0.864).

## Remaining Concern
Equalized odds difference (0.304) remains elevated relative to
demographic parity, indicating the model's error rates (false
positives/negatives) still differ somewhat across regions even though
its overall selection rate is now balanced. This is a genuine,
unresolved limitation — full fairness was not achieved, only
substantially improved — and would need further investigation
(e.g., equalized-odds-constrained mitigation) before any operational
deployment.

## Conclusion
No mitigation technique was applied in v2, since disparate impact
already clears the standard threshold; applying one preemptively
without a detected primary-metric failure was judged unnecessary and
would risk the same degenerate-accuracy ambiguity observed when
mitigation was applied in v1. Equalized odds should be monitored if
this model is ever extended toward real deployment.
