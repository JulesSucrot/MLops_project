# src/serve.py
import os, pandas as pd, mlflow
from fastapi import FastAPI
from src.schema import Student

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hogwarts House Predictor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local file:// ou http://localhost
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_URI = os.getenv("MODEL_URI", "models:/hogwarts_house_classifier/Production")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
SKIP_MLFLOW = os.getenv("SKIP_MLFLOW") == "1"


@app.on_event("startup")
def _load():
    global model
    if SKIP_MLFLOW:
        class _Dummy:
            def predict(self, df):
                return ["Hufflepuff"] * len(df)
        model = _Dummy()
    else:
        if MLFLOW_TRACKING_URI:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model = mlflow.pyfunc.load_model(MODEL_URI)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(s: Student):
    X = pd.DataFrame([s.as_dataframe_row()])
    pred = model.predict(X)[0]
    return {"house": str(pred)}
