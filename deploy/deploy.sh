# deploy/deploy.sh
#!/usr/bin/env bash
set -euo pipefail
IMAGE="${DOCKER_IMAGE:-$DOCKERHUB_USERNAME/mlops-hogwarts:latest}"
APP_NAME=hogwarts
docker pull "$IMAGE"
docker rm -f "$APP_NAME" >/dev/null 2>&1 || true
docker run -d --name "$APP_NAME" -p 8000:8000 \
  -e MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" \
  -e MLFLOW_TRACKING_USERNAME="${MLFLOW_TRACKING_USERNAME:-}" \
  -e MLFLOW_TRACKING_PASSWORD="${MLFLOW_TRACKING_PASSWORD:-}" \
  "$IMAGE"