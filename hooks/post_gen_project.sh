#!/usr/bin/env sh

set -e

# Generate the lockfile
uv lock

# Install dependencies locally
uv sync

# Initialize the git repository
git init .

# Install the prek hooks
uv run prek install -f

# Run the prek hooks
uv run prek run --all-files

# Make the initial commit
git add --all
git commit -m "Initial commit"
