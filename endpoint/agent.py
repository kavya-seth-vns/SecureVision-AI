import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
import requests
import datetime
import socket

DATA_PATH = "telemetry.csv"
AGGREGATOR_URL = "http://localhost:5000/update"

# Load telemetry (simulated endpoint data)
data = pd.read_csv(DATA_PATH)

# Train local anomaly detector
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(data)

severity = "LOW"
if model.contamination >= 0.05:
    severity = "MEDIUM"
if model.contamination >= 0.1:
    severity = "HIGH"

endpoint_name = socket.gethostname()


# Generate model summary instead of raw data
model_update = {
    "endpoint_id": socket.gethostname(),
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "n_estimators": model.n_estimators,
    "contamination": model.contamination,
    "feature_count": data.shape[1],
    "severity": severity,
}

# Send update to aggregator (NO RAW DATA)
requests.post(AGGREGATOR_URL, json=model_update)

print("✔ Local model trained and private update sent")
