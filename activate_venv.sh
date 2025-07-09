#!/bin/bash

# activate_venv.sh - Quick script to activate virtual environment
# Usage: source ./activate_venv.sh

if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo "🐍 Python: $(which python)"
    echo "📦 Pip: $(which pip)"
    echo "🔍 VIRTUAL_ENV: $VIRTUAL_ENV"
    echo ""
    echo "💡 You can now run:"
    echo "   • pytest tests/ -v"
    echo "   • pip install package_name"
    echo "   • python your_script.py"
    echo ""
    echo "📤 To deactivate: deactivate"
else
    echo "❌ Virtual environment not found!"
    echo "🔧 Run: ./setup.sh to create it"
fi
