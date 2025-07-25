#!/bin/bash
# Usage: ./create_pypack.sh <package-name>
# Creates a new pypack package structure in pypacks/<package-name>

set -e


# Ensure script is run from the my-jarvis directory (by name)
if [ "$(basename "$PWD")" != "my-jarvis" ]; then
  echo "Error: Please run this script from the my-jarvis directory."
  exit 1
fi

if [ -z "$1" ]; then
  echo "Usage: $0 <package-name>"
  exit 1
fi


PKG_NAME="$1"
PKG_DIR="pypacks/$PKG_NAME"
MODULE_DIR="$PKG_DIR/my_jarvis/$PKG_NAME"

# Confirm action with user
echo "About to create new pypack: $PKG_NAME"
echo "Location: $PKG_DIR"
read -p "Proceed? [y/N]: " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Aborted. No changes made."
  exit 0
fi

# Create directories
mkdir -p "$MODULE_DIR"

# Now resolve and print the relative path


# Create pyproject.toml
cat > "$PKG_DIR/pyproject.toml" <<EOF
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-jarvis-$PKG_NAME"
version = "0.1.0"
description = "$PKG_NAME package for my-jarvis"
requires-python = ">=3.12"
dependencies = []

[tool.hatch.metadata]
allow-direct-references = true

[tool.hatch.build.targets.wheel]
packages = ["my_jarvis"]
EOF

# Create __init__.py
touch "$MODULE_DIR/__init__.py"

echo "Created pypack: $PKG_NAME at $PKG_DIR"
