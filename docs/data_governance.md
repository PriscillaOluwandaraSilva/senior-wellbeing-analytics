# Data Governance Framework — CQC Care Home Engagement Pipeline

## Data Classification
This pipeline uses publicly published, facility-level regulatory data
from the Care Quality Commission (CQC). It contains no individual-level
personal data (no resident, patient, or staff records). Classification:
Public / Low Sensitivity.

A separate, clearly labeled illustrative/simulated dataset (used to
demonstrate a proposed efficiency-ratio metric) is not part of, and
must never be treated as a substitute for, the real 13,693-row
validated dataset. It is not linked to any real facility identity.

## Access Control
- The project's GitHub repository is public, consistent with the
  Public / Low Sensitivity classification above — no restricted or
  confidential data is stored here.
- Raw source files (CQC .ods/.csv downloads) and derived datasets are
  stored openly in this repository under data/raw/, matching the fact
  that CQC has already published this data publicly.
- No individual-level or restricted data is stored in this repository
  at any point.

## Retention Policy
- Source files are re-downloadable at any time from CQC's public data
  portal (updated regularly), so there is no requirement to retain raw
  copies indefinitely.
- Processed/derived datasets are retained only for the duration of this
  academic project (BAN6800, through course completion).

## Update Policy
- CQC republishes ratings data on an ongoing basis. This pipeline is
  designed to be re-run against updated source files rather than
  assuming a single static snapshot remains accurate long-term.

## Data Quality Ownership
- Validation rules (Great Expectations suite) define the minimum
  quality bar data must meet before being used downstream. Any future
  pipeline run that fails validation should not be used for analysis
  until the failure is investigated.
