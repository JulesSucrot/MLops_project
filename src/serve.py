# src/serve.py
import os, pandas as pd, mlflow
from fastapi import FastAPI
from src.schema import Student

MODEL_URI = os.getenv("MODEL_URI", "models:/hogwarts_house_classifier/Production")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

app = FastAPI(title="Hogwarts House Predictor")

@app.on_event("startup")
def _load():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    global model
    model = mlflow.pyfunc.load_model(MODEL_URI)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(s: Student):
    X = pd.DataFrame([s.as_dataframe_row()])
    pred = model.predict(X)[0]
    return {"house": str(pred)}
