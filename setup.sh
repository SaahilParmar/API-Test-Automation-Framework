#!/bin/bash

# setup.sh - Setup script for API Test Automation Framework
# This script sets up the virtual environment and installs dependencies

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
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created successfully!"
else
    echo "📦 Virtual environment already exists."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing project dependencies..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python -c "import pytest, requests, allure, yaml, jsonschema; print('✅ All dependencies installed successfully!')"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run smoke tests: ./test_runner.sh smoke"
echo "   3. Run all tests: ./test_runner.sh all"
echo "   4. Generate report: allure serve reports/allure-results"
echo ""
echo "💡 Pro tip: Always activate the virtual environment before running tests!"
echo "   source venv/bin/activate"
