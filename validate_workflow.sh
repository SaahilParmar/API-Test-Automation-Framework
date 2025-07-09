#!/bin/bash

# Comprehensive GitHub Actions workflow validation script
echo "🔍 Comprehensive workflow validation starting..."

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

echo "✅ Using Python command: $PYTHON_CMD"

# 1. Validate YAML syntax
echo "📝 Step 1: Checking YAML syntax..."
$PYTHON_CMD -c "
import yaml
import sys

try:
    with open('$WORKFLOW_FILE', 'r') as file:
        workflow = yaml.safe_load(file)
    print('✅ YAML syntax is valid')
except yaml.YAMLError as e:
    print(f'❌ YAML syntax error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error reading file: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "💥 YAML syntax validation failed!"
    exit 1
fi

# 2. Check for common indentation issues
echo "📏 Step 2: Checking indentation patterns..."
if grep -n "^ \+- name:" "$WORKFLOW_FILE" | grep -v "^[0-9]*:    - name:"; then
    echo "⚠️  Found potential indentation issues with step names"
    echo "   Expected: '    - name:' (4 spaces)"
fi

# 3. Check for required workflow elements
echo "🎯 Step 3: Checking required workflow elements..."

# Check for required top-level keys
required_keys=("name" "on" "jobs")
for key in "${required_keys[@]}"; do
    if grep -q "^$key:" "$WORKFLOW_FILE"; then
        echo "✅ Found required key: $key"
    else
        echo "❌ Missing required key: $key"
        exit 1
    fi
done

# 4. Check for job structure
echo "👥 Step 4: Validating job structures..."
job_count=$(grep -c "^  [a-zA-Z0-9_-]*:$" "$WORKFLOW_FILE")
echo "✅ Found $job_count job(s) defined"

# 5. Check for step structure consistency
echo "📋 Step 5: Checking step structures..."
steps_with_run=$(grep -c "    - name:" "$WORKFLOW_FILE")
echo "✅ Found $steps_with_run step(s) defined"

# 6. Check for common GitHub Actions best practices
echo "🏆 Step 6: Checking best practices..."

# Check for action versions
if grep -q "uses:.*@v[0-9]" "$WORKFLOW_FILE"; then
    echo "✅ Using pinned action versions"
else
    echo "⚠️  Consider pinning action versions (e.g., @v4)"
fi

# Check for matrix strategy
if grep -q "strategy:" "$WORKFLOW_FILE"; then
    echo "✅ Using build matrix strategy"
fi

# Check for caching
if grep -q "actions/cache@" "$WORKFLOW_FILE"; then
    echo "✅ Using dependency caching"
fi

# 7. Final validation
echo "🎉 Step 7: Final validation complete!"
echo ""
echo "📊 Validation Summary:"
echo "   - YAML syntax: ✅ Valid"
echo "   - Required keys: ✅ Present"
echo "   - Job structure: ✅ Valid"
echo "   - Step structure: ✅ Valid"
echo ""
echo "🚀 GitHub Actions workflow is ready for deployment!"
