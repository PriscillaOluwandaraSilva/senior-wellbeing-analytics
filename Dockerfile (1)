# API service - CQC Engagement Prediction
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_v2.py .
COPY random_forest_v2.pkl .

EXPOSE 8000

CMD ["uvicorn", "app_v2:app", "--host", "0.0.0.0", "--port", "8000"]
