"""
Airflow DAG for the CQC Care Home Engagement Pipeline.

This file defines the same six stages we already ran manually,
but as a formal, ordered task graph that Airflow can execute,
retry, and schedule automatically.
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

# ---- 1. DAG-level settings ----
# This block tells Airflow: what to call this pipeline, and how it
# should behave if something fails (retry twice, wait 5 min between tries).
default_args = {
    "owner": "priscilla",
    "retries": 2,
    "retry_delay": 300,  # seconds
}

dag = DAG(
    dag_id="cqc_engagement_pipeline",
    default_args=default_args,
    description="Ingest, clean, and validate CQC care home engagement data",
    schedule=None,  # run manually / on demand, not on a timer
    start_date=datetime(2026, 8, 23),
    catchup=False,
)


# ---- 2. Each stage becomes its own function ----
# Each function does exactly one job, matching one stage of our
# pipeline. Airflow will call these in the order we define below.

def ingest():
    ratings = pd.read_csv("data/processed/Locations_ratings.csv")
    ratings.to_pickle("/tmp/stage1_ingested.pkl")


def filter_data():
    ratings = pd.read_pickle("/tmp/stage1_ingested.pkl")
    responsive = ratings[ratings["Domain"] == "Responsive"]
    responsive_ch = responsive[responsive["Care Home?"] == "Y"].copy()
    responsive_ch.to_pickle("/tmp/stage2_filtered.pkl")


def clean():
    df = pd.read_pickle("/tmp/stage2_filtered.pkl")
    df = df.dropna(subset=["Latest Rating"])
    df.to_pickle("/tmp/stage3_cleaned.pkl")


def transform():
    df = pd.read_pickle("/tmp/stage3_cleaned.pkl")
    rating_map = {"Outstanding": 4, "Good": 3, "Requires improvement": 2, "Inadequate": 1}
    df["engagement_score"] = df["Latest Rating"].map(rating_map)
    df = df.dropna(subset=["engagement_score"])
    df.to_pickle("/tmp/stage4_transformed.pkl")


def integrate():
    df = pd.read_pickle("/tmp/stage4_transformed.pkl")
    directory = pd.read_csv("data/raw/cqc_directory.csv", skiprows=4)
    merged = df.merge(
        directory,
        left_on="Location ID",
        right_on="CQC Location ID (for office use only)",
        how="left",
    )
    merged = merged.drop_duplicates(subset=["Location ID"], keep="first")
    merged.to_pickle("/tmp/stage5_merged.pkl")


def validate():
    df = pd.read_pickle("/tmp/stage5_merged.pkl")
    assert df["engagement_score"].between(1, 4).all(), "Score out of range!"
    assert len(df) >= 5000, "Below record minimum!"
    assert df["Location ID"].duplicated().sum() == 0, "Duplicates found!"
    assert df["Location ID"].isna().sum() == 0, "Null IDs found!"
    df.to_csv("/tmp/final_validated_dataset.csv", index=False)
    print(f"Validation passed. Final row count: {len(df)}")


# ---- 3. Wrap each function as an Airflow Task ----
# PythonOperator is Airflow's way of saying "run this Python function
# as one step in the pipeline."
t1 = PythonOperator(task_id="ingest", python_callable=ingest, dag=dag)
t2 = PythonOperator(task_id="filter_data", python_callable=filter_data, dag=dag)
t3 = PythonOperator(task_id="clean", python_callable=clean, dag=dag)
t4 = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
t5 = PythonOperator(task_id="integrate", python_callable=integrate, dag=dag)
t6 = PythonOperator(task_id="validate", python_callable=validate, dag=dag)


# ---- 4. Declare the order — this is the actual "formal structure" ----
# The >> operator means "must finish before the next one starts."
# This single line IS the pipeline diagram, written as code.
t1 >> t2 >> t3 >> t4 >> t5 >> t6
