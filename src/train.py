import os, json, yaml, pandas as pd, mlflow
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from mlflow.tracking import MlflowClient

# ---- config
with open("params.yaml", "r", encoding="utf-8") as f:
    p = yaml.safe_load(f)

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_experiment(p["experiment_name"])

# ---- data
df = pd.read_csv(p["data_path"])
y = df["House"]
X = df.drop(columns=["House"])
cat = ["Blood Status"]
num = [c for c in X.columns if c not in cat]

# ---- pipeline
pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
    ("num", StandardScaler(), num),
])
clf = RandomForestClassifier(
    n_estimators=p["n_estimators"],
    max_depth=p["max_depth"],
    random_state=p["random_state"],
)
pipe = Pipeline([("pre", pre), ("clf", clf)])

# ---- train + log
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=p["test_size"], random_state=p["random_state"], stratify=y
)

with mlflow.start_run() as run:
    mlflow.log_params({
        "n_estimators": p["n_estimators"],
        "max_depth": p["max_depth"],
        "test_size": p["test_size"],
        "random_state": p["random_state"],
    })

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", acc)

    # 1) log artefact du modèle dans le run
    mlflow.sklearn.log_model(sk_model=pipe, artifact_path="model")

    # 2) register dans le Model Registry (compatible DagsHub)
    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/model"
    client = MlflowClient()
    try:
        client.create_registered_model(p["model_name"])
    except Exception:
        pass  # déjà créé

    mv = mlflow.register_model(model_uri=model_uri, name=p["model_name"])

    # 3) promotion optionnelle en Production
    if p.get("promote_to_production", True):
        client.transition_model_version_stage(
            name=p["model_name"],
            version=mv.version,
            stage="Production",
            archive_existing_versions=True,
        )

# ---- métriques pour DVC
os.makedirs("metrics", exist_ok=True)
with open("metrics/metrics.json", "w", encoding="utf-8") as f:
    json.dump({"accuracy": acc}, f)
