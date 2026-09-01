"""
Automated data quality tests for the modeling dataset — mirrors the
Great Expectations checks from Module 3, as fast-running CI assertions.
Run with: pytest tests/test_data_quality.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import pytest

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dashboards", "model_dataset_v2.csv")


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_dataset_has_minimum_row_count(df):
    assert len(df) >= 5000, "Dataset fell below the assignment's 5,000-row minimum"


def test_no_null_location_ids(df):
    assert df["Location ID"].isna().sum() == 0


def test_no_duplicate_location_ids(df):
    assert df["Location ID"].duplicated().sum() == 0


def test_quality_scores_within_valid_range(df):
    for col in ["Safe", "Effective", "Caring", "Well-led"]:
        assert df[col].dropna().between(1, 4).all(), f"{col} has values outside 1-4"


def test_engagement_target_is_binary(df):
    assert set(df["is_high_engagement"].unique()).issubset({0, 1})
