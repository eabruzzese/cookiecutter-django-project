#!/usr/bin/env sh

set -e

# Generate the lockfile
uv lock

# Install dependencies locally
uv sync

# Initialize the git repository
git init .
git add --all
git commit -m "Initial commit"
