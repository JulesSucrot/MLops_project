# deploy/deploy.ps1
$ErrorActionPreference = "Stop"

$IMAGE   = $env:IMAGE
$MODEL   = $env:MODEL_URI
$TRACK   = $env:TRACKING_URI
$USER    = $env:MLFLOW_TRACKING_USERNAME
$PASS    = $env:MLFLOW_TRACKING_PASSWORD

if (-not $IMAGE) { throw "DOCKER_IMAGE non défini (env IMAGE)" }

Write-Host "Deploy image = $IMAGE"

# Arrêt/suppression sans planter si absent
docker rm -f hogwarts 2>$null | Out-Null

# Pull (optionnel, mais utile en CI)
docker pull $IMAGE

# (Re)démarrage
docker run -d --rm --name hogwarts `
  -p 8000:8000 `
  -e MODEL_URI="$MODEL" `
  -e MLFLOW_TRACKING_URI="$TRACK" `
  -e MLFLOW_TRACKING_USERNAME="$USER" `
  -e MLFLOW_TRACKING_PASSWORD="$PASS" `
  $IMAGE
