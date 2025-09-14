$ErrorActionPreference = "Stop"

# Lire depuis l'env
$IMAGE = $env:DOCKER_IMAGE
if (-not $IMAGE) { throw "DOCKER_IMAGE non défini" }

# Facultatif: logs
Write-Host "Deploy image = $IMAGE"

# Pull
docker pull $IMAGE

# Stop / remove si déjà lancé
docker stop hogwarts 2>$null | Out-Null
docker rm hogwarts 2>$null   | Out-Null

# Run
docker run -d --rm --name hogwarts -p 8000:8000 `
  -e MLFLOW_TRACKING_URI=$env:MLFLOW_TRACKING_URI `
  -e MLFLOW_TRACKING_USERNAME=$env:MLFLOW_TRACKING_USERNAME `
  -e MLFLOW_TRACKING_PASSWORD=$env:MLFLOW_TRACKING_PASSWORD `
  -e MODEL_URI=$env:MODEL_URI `
  $IMAGE
