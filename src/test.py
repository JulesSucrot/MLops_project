import mlflow
model = mlflow.pyfunc.load_model("models:/hogwarts_house_classifier/Production")