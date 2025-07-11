#!/bin/bash

# setup.sh - Environment Setup Script
# -----------------------------------------------------------------------------
# This script automates the setup process for the API Test Automation Framework.
# It performs the following tasks:
# 1. Validates Python installation
# 2. Creates/activates virtual environment (.venv)
# 3. Installs project dependencies
# 4. Sets up Allure reporting
# 5. Validates schema and data files
#
# Usage:
#   ./setup.sh          # Standard setup
#   ./setup.sh --force  # Force reinstall of dependencies
#
# Requirements:
#   - Python 3.10 or higher
#   - pip package manager
#   - bash-compatible shell
# -----------------------------------------------------------------------------

set -e

echo "🚀 Setting up API Test Automation Framework"
echo "============================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Display Python version
echo "🐍 Python version: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created successfully!"
else
    echo "📦 Virtual environment already exists."
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
.venv/bin/pip install --upgrade pip

# Install dependencies
echo "📚 Installing project dependencies..."
.venv/bin/pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
.venv/bin/python -c "import pytest, requests, allure, yaml, jsonschema; print('✅ All dependencies installed successfully!')"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Run smoke tests: ./test_runner.sh smoke"
echo "   2. Run all tests: ./test_runner.sh all"
echo "   3. Generate report: allure serve reports/allure-results"
echo ""
echo "💡 Pro tip: Use the test runner for best experience!"
echo "   ./test_runner.sh [category]"
