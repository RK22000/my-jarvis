#!/usr/bin/env bash
set -e

echo "Starting deployment..."

ssh -tt linode-raka << 'EOF'
  echo "Navigating to the project directory..."
  cd my-jarvis/
  echo "Pulling the latest changes from the repository..."
  git pull --prune
  echo "Installing dependencies..."
  uv sync
  echo "Launching the application..."
  uv run gunicorn -k uvicorn.workers.UvicornWorker my_jarvis.server.app:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
  disown
  echo "Application is running in the background..."
  exit 0
EOF

echo "Deployment completed successfully."
