#!/bin/bash

# test_runner.sh - Script to run different test categories
# Usage: ./test_runner.sh [test_category]

set -e

echo "🧪 API Test Automation Framework - Test Runner"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import pytest" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed."
fi

# Function to display usage
show_usage() {
    echo "Usage: $0 [test_category]"
    echo ""
    echo "Available test categories:"
    echo "  smoke       - Run smoke tests (quick validation)"
    echo "  regression  - Run regression tests (comprehensive)"
    echo "  negative    - Run negative/error scenario tests"
    echo "  boundary    - Run boundary/edge case tests"
    echo "  contract    - Run API contract validation tests"
    echo "  performance - Run performance validation tests"
    echo "  retrieval   - Run user retrieval tests"
    echo "  creation    - Run user creation tests"
    echo "  validation  - Run API validation tests"
    echo "  errors      - Run error scenario tests"
    echo "  all         - Run all tests"
    echo ""
    echo "Examples:"
    echo "  $0 smoke"
    echo "  $0 regression"
    echo "  $0 all"
}

# Function to run tests with specific markers
run_tests() {
    local category=$1
    local marker=""
    local description=""
    
    case $category in
        "smoke")
            marker="smoke"
            description="Smoke Tests (Core Functionality Validation)"
            ;;
        "regression")
            marker="regression"
            description="Regression Tests (Comprehensive Testing)"
            ;;
        "negative")
            marker="negative"
            description="Negative Tests (Error Scenarios)"
            ;;
        "boundary")
            marker="boundary"
            description="Boundary Tests (Edge Cases)"
            ;;
        "contract")
            marker="contract"
            description="Contract Tests (API Schema Validation)"
            ;;
        "performance")
            marker="performance"
            description="Performance Tests (Response Time Validation)"
            ;;
        "retrieval")
            marker="user_retrieval"
            description="User Retrieval Tests (GET Operations)"
            ;;
        "creation")
            marker="user_creation"
            description="User Creation Tests (POST Operations)"
            ;;
        "validation")
            marker="api_validation"
            description="API Validation Tests (Headers, Schema, Contract)"
            ;;
        "errors")
            marker="error_scenarios"
            description="Error Scenario Tests (404, Invalid Data, etc.)"
            ;;
        "all")
            marker=""
            description="All Tests"
            ;;
        *)
            echo "❌ Invalid test category: $category"
            show_usage
            exit 1
            ;;
    esac
    
    echo "🚀 Running: $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ -z "$marker" ]; then
        # Run all tests
        pytest -v --alluredir=reports/allure-results
    else
        # Run tests with specific marker
        pytest -v -m "$marker" --alluredir=reports/allure-results
    fi
    
    echo ""
    echo "✅ Test execution completed!"
    echo "📊 View detailed reports: allure serve reports/allure-results"
}

# Main script logic
if [ $# -eq 0 ]; then
    echo "❌ No test category specified"
    show_usage
    exit 1
fi

category=$1

# Validate pytest installation
if ! python -c "import pytest" &> /dev/null; then
    echo "❌ pytest is not installed. Please install dependencies:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Run the tests
run_tests "$category"

echo ""
echo "💡 Tips:"
echo "   • Generate HTML report: allure generate reports/allure-results --clean -o reports/html"
echo "   • View live report: allure serve reports/allure-results"
echo "   • Run specific test file: pytest tests/test_user_retrieval.py -v"
echo "   • Run with coverage: pytest --cov=utils tests/"
