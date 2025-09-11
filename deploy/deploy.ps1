# deploy/deploy.ps1
$ErrorActionPreference = "Stop"
$IMAGE = $env:DOCKER_IMAGE
if (-not $IMAGE) { throw "DOCKER_IMAGE non défini" }

docker pull $IMAGE | Out-Host
docker rm -f hogwarts 2>$null | Out-Null

docker run -d --name hogwarts -p 8000:8000 `
  -e MLFLOW_TRACKING_URI=$env:MLFLOW_TRACKING_URI `
  -e MLFLOW_TRACKING_USERNAME=$env:MLFLOW_TRACKING_USERNAME `
  -e MLFLOW_TRACKING_PASSWORD=$env:MLFLOW_TRACKING_PASSWORD `
  $IMAGE | Out-Host
