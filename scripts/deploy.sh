#!/usr/bin/env bash
set -e

echo "Starting deployment..."

ssh -tt linode-raka << 'EOF'
  pkill -f 'gunicorn -k uvicorn.workers.UvicornWorker my_jarvis.server.app:app' || true
  echo "Navigating to the project directory..."
  cd my-jarvis/
  echo "Pulling the latest changes from the repository..."
  git fetch origin main
  git reset --hard origin/main
  echo "Installing dependencies..."
  uv sync
  echo "Launching the application..."
  uv run gunicorn -k uvicorn.workers.UvicornWorker my_jarvis.server.app:app --bind 0.0.0.0:8000 > app.log 2>&1 &
  disown
  echo "Application is running in the background..."
  exit 0
EOF

echo "Checking health endpoint at https://myjarvis.raka42.duckdns.org..."

max_retries=3
retry_delay=2  # seconds
attempt=1

while [ "$attempt" -le "$max_retries" ]; do
  echo "Attempt $attempt of $max_retries..."

  health_check=$(curl -s -X GET \
    'https://myjarvis.raka42.duckdns.org/health' \
    -H 'accept: application/json')

  if [ "$health_check" = '"OK"' ]; then
    echo "✅ App is up and healthy!"
    exit 0
  else
    echo "❌ Health check failed. Response: $health_check"
  fi

  attempt=$((attempt + 1))
  sleep "$retry_delay"
done

echo "❌ App did not become healthy after $max_retries attempts."
exit 1
