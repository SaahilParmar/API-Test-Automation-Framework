#!/bin/bash

# Test script to validate CI workflow locally
echo "🚀 Starting local CI validation..."

echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "🧪 Running tests with Allure results generation..."
python -m pytest tests/ --alluredir=allure-results -v

if [ $? -eq 0 ]; then
    echo "✅ Tests passed successfully!"
    
    if [ -d "allure-results" ]; then
        echo "✅ Allure results generated successfully!"
        echo "📊 Allure results files: $(ls -1 allure-results | wc -l) files"
        
        if command -v allure &> /dev/null; then
            echo "🎨 Generating Allure HTML report..."
            allure generate allure-results --clean -o allure-report
            echo "✅ Allure HTML report generated!"
            echo "📁 Report location: $(pwd)/allure-report/index.html"
        else
            echo "⚠️  Allure CLI not found - HTML report not generated"
        fi
    else
        echo "❌ Allure results directory not found!"
        exit 1
    fi
else
    echo "❌ Tests failed!"
    exit 1
fi

echo "🎉 Local CI validation completed successfully!"
