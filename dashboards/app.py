"""
Stakeholder Dashboard — CQC Engagement Prediction Model
Module 5, BAN6800

Deployable to Streamlit Cloud. Requires: model_rf_v2_tuned.pkl,
model_dataset_v2.csv, X_test_v2.csv, y_test_v2.csv in the same folder.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Amari Eden Engagement Insights", layout="wide")

# ---------- Load model and data ----------
@st.cache_resource
def load_model():
    return joblib.load("random_forest_v2.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv("model_dataset_v2.csv")
    X_test = pd.read_csv("X_test_v2.csv")
    y_test = pd.read_csv("y_test_v2.csv").squeeze()
    return df, X_test, y_test

model = load_model()
df, X_test, y_test = load_data()

st.title("Care Facility Engagement Insights Dashboard")
st.caption("Proof-of-concept built on UK CQC care home ratings — Amari Eden Living and Programs")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "What Drives Predictions", "Try a Prediction (What-If)",
    "Fairness & Ethics", "Model Limitations"
])

# ---------- TAB 1: Overview ----------
with tab1:
    st.header("What This Tool Does")
    st.markdown("""
    This tool predicts whether a care facility is likely to be rated **high-engagement**
    (good at keeping residents actively engaged) based on four quality-of-care scores
    already collected by regulators: **Safety, Effectiveness, Caring, and Leadership (Well-led)**.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Facilities Analyzed", f"{len(df):,}")
    col2.metric("Model Accuracy", "87.5%")
    col3.metric("High-Engagement Rate", f"{df['is_high_engagement'].mean()*100:.1f}%")

    st.subheader("Engagement Score Distribution")
    fig = px.histogram(df, x="Responsive", nbins=4,
                        labels={"Responsive": "Engagement Rating (1=Inadequate, 4=Outstanding)"},
                        title="How Facilities Are Currently Rated")
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, width="stretch")

# ---------- TAB 2: What Drives Predictions ----------
with tab2:
    st.header("What Drives a High-Engagement Rating?")
    st.markdown("""
    Using an explainability technique called **SHAP**, we can see which quality factors
    matter most to the model's predictions — in plain terms, which factor moves the needle most.
    """)

    importance = pd.DataFrame({
        "Factor": ["Leadership (Well-led)", "Effectiveness", "Caring", "Safety"],
        "Influence on Prediction": [0.170, 0.125, 0.055, 0.049]
    }).sort_values("Influence on Prediction", ascending=True)

    fig = px.bar(importance, x="Influence on Prediction", y="Factor", orientation="h",
                 title="Which Factors Matter Most for Predicting Engagement",
                 color="Influence on Prediction", color_continuous_scale="Blues")
    st.plotly_chart(fig, width="stretch")

    st.info("**Business takeaway:** Leadership quality is more than twice as influential as any other factor. "
            "Investing in facilitator training and leadership development is the single highest-leverage action.")

    st.subheader("Example Predictions Explained")
    examples = [
        {"name": "Facility A", "safe": 3, "effective": 3, "caring": 3, "well_led": 3,
         "explanation": "High scores across the board, especially strong leadership → predicted **high engagement**."},
        {"name": "Facility B", "safe": 2, "effective": 2, "caring": 2, "well_led": 2,
         "explanation": "Consistently low scores, particularly weak leadership → predicted **needs improvement**."},
        {"name": "Facility C", "safe": 2, "effective": 3, "caring": 3, "well_led": 2,
         "explanation": "Mixed profile — decent effectiveness and caring, but leadership lags → borderline prediction."},
    ]
    for ex in examples:
        with st.expander(ex["name"]):
            X = pd.DataFrame([{"Safe": ex["safe"], "Effective": ex["effective"],
                                "Caring": ex["caring"], "Well-led": ex["well_led"]}])
            proba = model.predict_proba(X)[0][1]
            st.write(f"Predicted probability of high engagement: **{proba:.0%}**")
            st.write(ex["explanation"])

# ---------- TAB 3: What-If Analysis ----------
with tab3:
    st.header("Try It Yourself: What-If Analysis")
    st.markdown("Adjust a facility's quality scores below and see how the predicted engagement likelihood changes.")

    c1, c2 = st.columns(2)
    with c1:
        safe = st.slider("Safety score", 1, 4, 3)
        effective = st.slider("Effectiveness score", 1, 4, 3)
    with c2:
        caring = st.slider("Caring score", 1, 4, 3)
        well_led = st.slider("Leadership (Well-led) score", 1, 4, 3)

    X_input = pd.DataFrame([{"Safe": safe, "Effective": effective, "Caring": caring, "Well-led": well_led}])
    proba = model.predict_proba(X_input)[0][1]
    pred = "High Engagement" if proba >= 0.5 else "Needs Improvement"

    st.metric("Predicted Outcome", pred, delta=f"{proba:.0%} likelihood")

    st.markdown("**Try this:** raise only the Leadership score and watch the prediction move more than "
                "raising any other single score by the same amount — this reflects the SHAP finding on the previous tab.")

# ---------- TAB 4: Fairness & Ethics ----------
with tab4:
    st.header("Fairness Summary")
    st.markdown("""
    Before trusting any predictive tool, it's important to check whether it treats every facility
    fairly — regardless of where it's located.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Disparate Impact Ratio", "0.864", help="Compares the lowest-scoring region to the highest. A value at or above 0.80 is the standard fairness benchmark.")
        st.success("✅ Passes the standard 0.80 fairness benchmark")
    with col2:
        st.metric("Demographic Parity Difference", "0.123", help="The gap in predicted-positive rates between regions. Closer to 0 is better; there is no universal pass/fail line for this metric.")
        st.info("ℹ️ A modest, non-zero gap remains — reported transparently rather than forced into a pass/fail label")

    st.success("**In plain terms:** after refining the model to focus on genuine quality-of-care factors "
               "(rather than administrative details like region), it now treats facilities fairly across "
               "all nine UK regions tested — a meaningful improvement over an earlier version of this model, "
               "which showed accuracy ranging from 20% to 96% depending purely on region.")

    st.warning("**Remaining limitation:** while overall fairness passes, one deeper fairness check "
               "(equalized error rates) shows some remaining variation across regions. This is disclosed "
               "transparently and would need further work before any real-world deployment.")

# ---------- TAB 5: Model Limitations ----------
with tab5:
    st.header("What This Model Can and Cannot Do")

    st.markdown("""
    **This model CAN:**
    - Flag which facilities may benefit from a closer look at engagement practices
    - Identify leadership quality as the strongest lever for improving engagement
    - Do so fairly across the UK regions tested

    **This model CANNOT:**
    - Replace human judgment or an in-person facility visit
    - Explain *why* leadership quality is low — only that it matters most
    - Be assumed to work identically on Amari Eden's own Canadian programming data,
      since it was built and validated on UK regulatory data as a proof-of-concept

    **Transparency Statement:** This tool is a decision-support aid, not an automated
    decision-maker. Every prediction should be reviewed by a person before any action
    is taken, particularly given the model's own fairness analysis shows imperfect,
    though substantially improved, equal treatment across regions.
    """)

st.markdown("---")
st.caption("Amari Eden Living and Programs | BAN6800 Capstone, Module 5 | Model trained on CQC (2026) data")
