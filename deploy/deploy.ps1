
# deploy/deploy.ps1

Write-Host "Deploy image = $env:IMAGE"

# Stoppe et supprime le conteneur s’il existe, sinon ignore
docker stop hogwarts 2>$null | Out-Null
docker rm -f hogwarts 2>$null | Out-Null

# Lance le nouveau conteneur
docker run -d --rm --name hogwarts `
  -p 8000:8000 `
  -e MLFLOW_TRACKING_URI=$env:TRACKING_URI `
  -e MLFLOW_TRACKING_USERNAME=$env:MLFLOW_TRACKING_USERNAME `
  -e MLFLOW_TRACKING_PASSWORD=$env:MLFLOW_TRACKING_PASSWORD `
  -e MODEL_URI=$env:MODEL_URI `
  $env:IMAGE
