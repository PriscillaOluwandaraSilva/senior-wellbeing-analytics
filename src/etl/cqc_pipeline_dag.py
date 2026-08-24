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

def ingest():
    ratings = pd.read_csv("data/raw/Locations_ratings_correct_extract.csv")
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
    directory = pd.read_csv("data/raw/19_August_2026_CQC_directory.csv", skiprows=4)
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

t1 = PythonOperator(task_id="ingest", python_callable=ingest, dag=dag)
t2 = PythonOperator(task_id="filter_data", python_callable=filter_data, dag=dag)
t3 = PythonOperator(task_id="clean", python_callable=clean, dag=dag)
t4 = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
t5 = PythonOperator(task_id="integrate", python_callable=integrate, dag=dag)
t6 = PythonOperator(task_id="validate", python_callable=validate, dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6
