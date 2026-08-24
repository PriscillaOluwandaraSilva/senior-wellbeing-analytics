# ---- Base image ----
# Start from an official, minimal Python 3.12 environment.
# "slim" means it excludes extra OS tools we don't need, keeping the
# image smaller and faster to build/download.
FROM python:3.12-slim

# ---- Set the working directory ----
# All following commands run from this folder inside the container.
WORKDIR /app

# ---- Copy dependency list first (before the code) ----
# This is a deliberate ordering trick: Docker caches each step, and
# only re-runs a step if the files it depends on changed.
COPY requirements.txt .

# ---- Install exact library versions ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy the actual pipeline code and data, matching the real repo structure ----
COPY src/etl/cqc_pipeline_dag.py src/etl/cqc_pipeline_dag.py
COPY data/raw/Locations_ratings_correct_extract.csv data/raw/Locations_ratings_correct_extract.csv
COPY data/raw/19_August_2026_CQC_directory.csv data/raw/19_August_2026_CQC_directory.csv

# ---- Default command when the container starts ----
# Runs a smoke test confirming the raw extract loads correctly.
CMD ["python3", "-c", "import pandas as pd; df = pd.read_csv('data/raw/Locations_ratings_correct_extract.csv'); print('Container OK. Rows loaded:', len(df))"]
