"""
Monitoring Dashboard — CQC Engagement Prediction Model
BAN6800 Final Project

Tracks model performance and fairness metrics across logged MLflow runs
over time, plus a fairness drift monitoring plan. Deployable to
Streamlit Cloud, same pattern as the main stakeholder dashboard.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Model Monitoring Dashboard", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mlflow_experiment_tracking_v1_and_v2.db")

st.title("Model Monitoring Dashboard")
st.caption("Tracking performance, fairness, and drift over time — CQC Engagement Prediction Model")


@st.cache_data
def load_runs():
    conn = sqlite3.connect(DB_PATH)
    runs = pd.read_sql_query("SELECT run_uuid, name, start_time, status FROM runs", conn)
    metrics = pd.read_sql_query("SELECT run_uuid, key, value FROM metrics", conn)
    conn.close()
    metrics_wide = metrics.pivot_table(index="run_uuid", columns="key", values="value", aggfunc="last").reset_index()
    merged = runs.merge(metrics_wide, on="run_uuid", how="left")
    merged["start_time"] = pd.to_datetime(merged["start_time"], unit="ms")
    return merged.sort_values("start_time")


runs_df = load_runs()

tab1, tab2, tab3 = st.tabs(["Performance Over Time", "Run History", "Drift & Alerts"])

with tab1:
    st.header("Model Performance Across Logged Runs")

    metric_choice = st.selectbox("Metric to track", ["roc_auc", "accuracy", "recall", "precision", "f1"])

    if metric_choice in runs_df.columns:
        fig = px.line(runs_df, x="start_time", y=metric_choice, color="name", markers=True,
                       title=f"{metric_choice.upper()} across model runs over time")
        fig.add_hline(y=0.70, line_dash="dash", line_color="red",
                      annotation_text="Minimum acceptance threshold (0.70)")
        st.plotly_chart(fig, width="stretch")
    else:
        st.warning(f"No logged values found for '{metric_choice}' yet.")

    st.info("**Acceptance criteria (from Module 4):** ROC-AUC should remain above 0.70 for any "
            "operational use; any run falling below this line should trigger review before deployment.")

with tab2:
    st.header("Full Run History")
    st.dataframe(runs_df[["name", "start_time", "status", "accuracy", "roc_auc", "f1"]], width="stretch")
    st.caption(f"Total runs logged: {len(runs_df)}")

with tab3:
    st.header("Drift & Fairness Monitoring")
    st.markdown("""
    **Fairness drift check:** re-run the Fairlearn disparate impact and equalized odds
    calculations (Module 4) against new incoming data on a regular cadence (e.g., monthly),
    and compare against the baseline values below. A significant drop signals fairness drift
    requiring investigation before continued use.
    """)

    baseline = pd.DataFrame({
        "Metric": ["Disparate Impact Ratio", "Demographic Parity Difference", "Equalized Odds Difference"],
        "Baseline (Module 4)": [0.864, 0.123, 0.304],
        "Alert Threshold": ["< 0.80", "> 0.20", "> 0.40"],
    })
    st.table(baseline)

    st.warning("**This tab shows the monitoring PLAN and baseline values, not live drift detection** — "
               "live drift tracking requires a scheduled job re-scoring new data against these "
               "thresholds, which is proposed in the Implementation & Monitoring Plan but not yet "
               "running in production, since Amari Eden does not yet have a live stream of new data "
               "to monitor against.")

st.markdown("---")
st.caption("BAN6800 Final Project | Priscilla Oluwandara Silva | Monitoring baseline: Module 4 results")
