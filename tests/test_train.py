# tests/test_train.py
import os, yaml, pandas as pd

def test_dataset_columns():
    p = yaml.safe_load(open("params.yaml"))
    df = pd.read_csv(p["data_path"])
    expected = {
        "Blood Status","Bravery","Intelligence","Loyalty","Ambition",
        "Dark Arts Knowledge","Quidditch Skills","Dueling Skills","Creativity","House"
    }
    assert set(df.columns) == expected
    assert len(df) >= 100