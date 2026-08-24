"""
Privacy Audit Logging - CQC Care Home Engagement Pipeline

Logs every pipeline run: when it happened, what stage ran, and
whether it succeeded - creating an auditable record of data access
and transformation activity.
"""

import logging
from datetime import datetime, timezone

logging.basicConfig(
    filename="pipeline_audit_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_stage(stage_name, row_count=None, status="SUCCESS"):
    msg = f"Stage='{stage_name}' | Status={status}"
    if row_count is not None:
        msg += f" | RowCount={row_count}"
    logging.info(msg)
    print(msg)  # also print, so it's visible during interactive runs

if __name__ == "__main__":
    import pandas as pd

    log_stage("pipeline_run_started")

    df = pd.read_csv("final_engagement_dataset_clean.csv")
    log_stage("data_accessed", row_count=len(df))

    log_stage("pipeline_run_completed")
    print("\nAudit log written to pipeline_audit_log.txt")
