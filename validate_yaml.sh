#!/bin/bash

# YAML validation script for GitHub Actions workflows
echo "🔍 Validating GitHub Actions workflow YAML syntax..."

WORKFLOW_FILE=".github/workflows/ci.yml"

if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python to validate YAML."
    exit 1
fi

# Validate YAML syntax
echo "📝 Checking YAML syntax..."
$PYTHON_CMD -c "
import yaml
import sys

try:
    with open('$WORKFLOW_FILE', 'r') as file:
        yaml.safe_load(file)
    print('✅ YAML syntax is valid')
except yaml.YAMLError as e:
    print(f'❌ YAML syntax error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error reading file: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "🎉 GitHub Actions workflow YAML is valid!"
else
    echo "💥 Please fix the YAML syntax errors before committing."
    exit 1
fi
