# Test Data Documentation

This directory contains test data used by the API Test Automation Framework.

## Data Files

### 1. post_user_payloads.json
Contains test data for user creation tests (POST /api/users):
- Valid user data with different combinations
- Edge cases for validation
- Various job titles and user names

### 2. large_payload.json
Test data for performance and boundary testing:
- Large data payload (>1MB)
- Complex nested structures
- Used for testing API handling of large requests

## Data Structure
Each test data file follows a specific structure for consistent testing:
```json
[
    {
        "name": "test user name",
        "job": "test job title",
        "expectedStatus": 201,
        "description": "Test case description"
    }
]
```

## Usage
The test data is loaded and used in parameterized tests:
```python
import json
def load_test_data():
    with open("data/post_user_payloads.json") as f:
        return json.load(f)

@pytest.mark.parametrize("payload", load_test_data())
def test_create_user(payload):
    # Test implementation
```

## Maintenance
- Keep data files under 5MB
- Use meaningful test data that represents real-world scenarios
- Include both positive and negative test cases
- Document special test cases or edge conditions
