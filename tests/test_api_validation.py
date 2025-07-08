"""
test_api_validation.py

Test module focused on API contract validation and data integrity.
Covers schema validation, header validation, and response format testing.
"""

import pytest
import requests
import allure
from jsonschema import validate
from utils.api_utils import load_config, load_schema, get_headers

# Load base configuration from config.yaml
config = load_config()
BASE_URL = config["environments"][config["env"]]["base_url"]


@pytest.mark.api_validation
@pytest.mark.contract
@allure.epic("API Contract")
@allure.feature("Response Headers")
@allure.title("Validate Standard Headers")
@allure.severity(allure.severity_level.TRIVIAL)
def test_headers_validation():
    """
    Test that standard headers are present and correct in the API response.
    Validates content type, encoding, and other standard HTTP headers.
    """
    with allure.step("Send GET request to users endpoint"):
        url = f"{BASE_URL}/users?page=1"
        response = requests.get(url, headers=get_headers())
        
    with allure.step("Verify response status is 200"):
        assert response.status_code == 200
        
    with allure.step("Validate Content-Type header"):
        assert response.headers["Content-Type"].startswith("application/json")
        
    with allure.step("Validate response headers are present"):
        # Check for Content-Type (always present)
        assert "Content-Type" in response.headers
        
        # Check for either Content-Length or Transfer-Encoding (both are valid)
        has_content_length = "Content-Length" in response.headers
        has_transfer_encoding = "Transfer-Encoding" in response.headers
        assert has_content_length or has_transfer_encoding, "Either Content-Length or Transfer-Encoding should be present"
        
        # Validate Date header is present
        assert "Date" in response.headers
            
    with allure.step("Attach headers to report"):
        headers_info = dict(response.headers)
        allure.attach(str(headers_info), "Response Headers", allure.attachment_type.TEXT)


@pytest.mark.api_validation
@pytest.mark.contract
@allure.epic("API Contract")
@allure.feature("Schema Validation")
@allure.title("Validate User List Schema Compliance")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_list_schema_validation():
    """
    Comprehensive schema validation for user list endpoint.
    Ensures all required fields and data types are correct.
    """
    with allure.step("Send GET request to user list endpoint"):
        url = f"{BASE_URL}/users?page=1"
        response = requests.get(url, headers=get_headers())
        
    with allure.step("Verify response status is 200"):
        assert response.status_code == 200
        
    with allure.step("Load and apply schema validation"):
        data = response.json()
        schema = load_schema("user_list_schema.json")
        validate(instance=data, schema=schema)
        
    with allure.step("Validate specific data structure"):
        assert "data" in data
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert isinstance(data["data"], list)
        
    with allure.step("Validate user objects in data array"):
        for user in data["data"]:
            assert "id" in user
            assert "email" in user
            assert "first_name" in user
            assert "last_name" in user
            assert "avatar" in user
            assert isinstance(user["id"], int)
            assert isinstance(user["email"], str)
            assert "@" in user["email"]  # Basic email validation
            
    with allure.step("Attach response for verification"):
        allure.attach(response.text, "User List Response", allure.attachment_type.JSON)


@pytest.mark.api_validation
@pytest.mark.contract
@allure.epic("API Contract")
@allure.feature("Schema Validation")
@allure.title("Validate Single User Schema Compliance")
@allure.severity(allure.severity_level.CRITICAL)
def test_single_user_schema_validation():
    """
    Comprehensive schema validation for single user endpoint.
    Ensures response structure matches expected contract.
    """
    with allure.step("Send GET request to single user endpoint"):
        url = f"{BASE_URL}/users/2"
        response = requests.get(url, headers=get_headers())
        
    with allure.step("Verify response status is 200"):
        assert response.status_code == 200
        
    with allure.step("Load and apply schema validation"):
        data = response.json()
        schema = load_schema("single_user_schema.json")
        validate(instance=data, schema=schema)
        
    with allure.step("Validate user data structure"):
        assert "data" in data
        assert "support" in data
        user_data = data["data"]
        assert "id" in user_data
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "avatar" in user_data
        
    with allure.step("Validate support information"):
        support = data["support"]
        assert "url" in support
        assert "text" in support
        
    with allure.step("Attach response for verification"):
        allure.attach(response.text, "Single User Response", allure.attachment_type.JSON)


@pytest.mark.api_validation
@pytest.mark.performance
@allure.epic("API Performance")
@allure.feature("Response Time")
@allure.title("Validate Response Time Performance")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("endpoint", ["/users?page=1", "/users/1"])
def test_response_time_validation(endpoint):
    """
    Test that API responses are returned within acceptable time limits.
    Validates performance requirements.
    """
    with allure.step(f"Send GET request to {endpoint}"):
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=get_headers())
        
    with allure.step("Verify response status is 200"):
        assert response.status_code == 200
        
    with allure.step("Validate response time is acceptable"):
        response_time = response.elapsed.total_seconds()
        # Expecting response within 5 seconds (configurable)
        max_response_time = config.get("timeout_seconds", 5)
        assert response_time < max_response_time, f"Response time {response_time}s exceeded limit of {max_response_time}s"
        
    with allure.step("Attach performance metrics"):
        allure.attach(f"Response Time: {response_time:.3f} seconds", "Performance Metrics", allure.attachment_type.TEXT)
