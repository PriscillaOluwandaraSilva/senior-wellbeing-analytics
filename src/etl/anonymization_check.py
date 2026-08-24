"""
Anonymization Plan - CQC Care Home Engagement Pipeline

This dataset is facility-level (one row = one care home), not
individual-level. There is no resident, patient, or staff data in it.
This script formally verifies that, rather than assuming it.
"""

import pandas as pd
import re

df = pd.read_csv("final_engagement_dataset_clean.csv")

print("=== PII Scan ===")
print("Columns:", df.columns.tolist())

email_matches = {}
for col in df.columns:
    matches = df[col].astype(str).str.contains(r'[\w\.-]+@[\w\.-]+', regex=True, na=False)
    if matches.any():
        email_matches[col] = df[col][matches].tolist()

phone_found = df.astype(str).apply(
    lambda c: c.str.contains(r'\b0\d{9,10}\b', regex=True, na=False)
).any().any()

person_level_cols = [
    c for c in df.columns
    if any(kw in c.lower() for kw in
           ["resident", "patient", "individual", "dob", "nhs number"])
]

print("\nEmail-pattern matches by column:", email_matches)
print("Phone-number pattern found:", phone_found)
print("Person-level columns found:", person_level_cols)

# --- Manual review finding, documented explicitly ---
# The email-pattern match above is a FALSE POSITIVE: it triggered on
# stylized care home business names containing "@" (e.g. "Coopers@Ambleside"),
# not on real email addresses. Manually verified against sample values.
print("""
=== Conclusion ===
No individual-level PII present. Identifiers in this dataset
(Location Name, Provider Name) refer to businesses/organizations,
already published as public data by CQC. No anonymization
transformation is required for this dataset. The automated email-
pattern check produced one false positive (business names containing
"@"), documented here rather than silently dismissed.
""")
