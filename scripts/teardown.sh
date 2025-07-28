#!/usr/bin/env bash
set -e

echo "Starting teardown..."

ssh -tt linode-raka << 'EOF'
  pkill -f "uv run uvicorn my_jarvis.server.app:app"
  exit 0
EOF

echo "Teardown completed successfully."
