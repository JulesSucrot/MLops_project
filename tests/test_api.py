# tests/test_api.py
import os, mlflow, pandas as pd
from fastapi.testclient import TestClient
from src.serve import app, _load

def test_predict_endpoint():
    _load()
    c = TestClient(app)
    sample = {
      "Blood Status":"Half-blood","Bravery":5,"Intelligence":6,"Loyalty":6,
      "Ambition":4,"Dark Arts Knowledge":2,"Quidditch Skills":5,"Dueling Skills":5,"Creativity":6
    }
    r = c.post("/predict", json=sample)
    assert r.status_code == 200
    assert r.json()["house"] in {"Gryffindor","Ravenclaw","Hufflepuff","Slytherin"}