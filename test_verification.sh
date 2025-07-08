#!/bin/bash

# Run a quick final verification
source venv/bin/activate

echo "🧪 Final Test Verification"
echo "=========================="

echo "1. Testing the fixed malformed URL test..."
python -m pytest tests/test_error_scenarios.py::test_malformed_url -v

echo ""
echo "2. Running all tests with summary..."
python -m pytest --tb=short -q

echo ""
echo "3. Test organization summary:"
echo "   ✅ test_user_retrieval.py   - GET operations"
echo "   ✅ test_user_creation.py    - POST operations" 
echo "   ✅ test_error_scenarios.py  - Error handling"
echo "   ✅ test_api_validation.py   - Contract validation"
echo ""

echo "🎉 Test suite verification complete!"
