#!/bin/bash

# Setup development environment with uv
echo "Setting up AI Study Buddy development environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv --python 3.12

# Install dependencies using uv sync
echo "Installing dependencies..."
uv sync

echo "Development environment setup complete!"
echo "To run the application: uv run streamlit run application.py"
echo "Or activate the environment first: source .venv/bin/activate"
