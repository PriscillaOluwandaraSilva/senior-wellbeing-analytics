# Dashboard service - main stakeholder Streamlit dashboard
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY random_forest_v2.pkl .
COPY model_dataset_v2.csv .
COPY X_test_v2.csv .
COPY y_test_v2.csv .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
