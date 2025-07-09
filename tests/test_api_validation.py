"""
test_api_validation.py

Test module focused on API contract validation and data integrity.
Covers schema validation, header validation, and response format testing.
"""

import pytest
import requests
import allure
import json
import time
from jsonschema import validate
from utils.api_utils import load_schema, get_headers


@pytest.mark.api_validation
@pytest.mark.contract
@allure.epic("API Contract")
@allure.feature("Response Headers")
@allure.title("Validate Standard Headers")
@allure.severity(allure.severity_level.TRIVIAL)
def test_headers_validation(base_url):
    """
    Test that standard headers are present and correct in the API response.
    Validates content type, encoding, and other standard HTTP headers.
    """
    with allure.step("Send GET request to users endpoint"):
        try:
            url = f"{base_url}/users?page=1"
            response = requests.get(url, headers=get_headers(), timeout=10)
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), "Request Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Validate Content-Type header"):
        content_type = response.headers.get("Content-Type", "")
        assert content_type.startswith("application/json"), (
            f"Expected application/json Content-Type, got: {content_type}"
        )

    with allure.step("Validate response headers are present"):
        headers = dict(response.headers)
        allure.attach(
            json.dumps(headers, indent=2),
            "Response Headers",
            allure.attachment_type.JSON
        )

        # Check for Content-Type (always present)
        assert "Content-Type" in headers, "Missing Content-Type header"

        # Check for either Content-Length or Transfer-Encoding (both are valid)
        has_content_length = "Content-Length" in headers
        has_transfer_encoding = "Transfer-Encoding" in headers
        assert has_content_length or has_transfer_encoding, (
            "Missing both Content-Length and Transfer-Encoding headers"
        )

        # Validate Date header is present
        assert "Date" in headers, "Missing Date header"


@pytest.mark.api_validation
@pytest.mark.contract
@allure.epic("API Contract")
@allure.feature("Schema Validation")
@allure.title("Validate User List Schema Compliance")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_list_schema_validation(base_url):
    """
    Comprehensive schema validation for user list endpoint.
    Ensures all required fields and data types are correct.
    """
    with allure.step("Send GET request to user list endpoint"):
        url = f"{base_url}/users?page=1"
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
def test_single_user_schema_validation(base_url):
    """
    Comprehensive schema validation for single user endpoint.
    Ensures response structure matches expected contract.
    """
    with allure.step("Send GET request to single user endpoint"):
        url = f"{base_url}/users/2"
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
def test_response_time_validation(endpoint, base_url, config):
    """
    Test that API responses are returned within acceptable time limits.
    Validates performance requirements.

    Args:
        endpoint (str): The API endpoint to test
        base_url (str): Base URL from fixture
        config (dict): Configuration fixture containing timeout settings
    """
    with allure.step(f"Send GET request to {endpoint}"):
        try:
            url = f"{base_url}{endpoint}"
            start_time = time.perf_counter()
            response = requests.get(url, headers=get_headers(), timeout=10)
            response_time = time.perf_counter() - start_time
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), "Request Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Validate response time is acceptable"):
        max_response_time = config.get("timeout_seconds", 5)
        assert response_time < max_response_time, (
            f"Response time {response_time:.3f}s exceeded limit of {max_response_time}s. "
            f"Endpoint: {endpoint}"
        )

    with allure.step("Attach performance metrics"):
        metrics = {
            "endpoint": endpoint,
            "response_time": f"{response_time:.3f}s",
            "timeout_limit": f"{max_response_time}s",
            "status_code": response.status_code
        }
        allure.attach(
            json.dumps(metrics, indent=2),
            "Performance Metrics",
            allure.attachment_type.JSON
        )
