"""
test_user_creation.py - User Creation API Tests

This module implements data-driven tests for user creation endpoints in the ReqRes API.
It focuses on POST operations with various payload combinations and validates the
creation responses.

Features Tested:
    1. User Creation
        - Valid user data
        - Required fields only
        - All fields populated
        - Special characters in names
    2. Response Validation
        - Status code (201)
        - Response schema
        - Created user data
    3. Edge Cases
        - Minimum/maximum field lengths
        - Unicode characters
        - Whitespace handling

Test Data:
    Location: data/post_user_payloads.json
    Format: List of user creation payloads
    Example:
        [
            {
                "name": "John Doe",
                "job": "Developer"
            },
            ...
        ]

Test Categories:
    - Smoke Tests (@pytest.mark.smoke)
    - User Creation (@pytest.mark.user_creation)
    - Data Validation (@pytest.mark.validation)

Required Fixtures:
    - base_url: API base URL from config
    - request_id: Unique identifier for each request
"""

import pytest
import requests
import json
import allure
import os
from jsonschema import validate
from utils.api_utils import load_schema, get_headers, log_request_response, validate_response_schema


def load_test_data():
    """Load test data from JSON file, with error handling"""
    data_path = os.path.join("data", "post_user_payloads.json")
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Test data file not found: {data_path}. "
            "Please ensure data/post_user_payloads.json exists."
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in test data file: {str(e)}")


# Load test data at module level to fail fast if there are issues
TEST_PAYLOADS = load_test_data()


@pytest.mark.user_creation
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Creation")
@allure.title("POST Create Users from Payloads")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("payload", TEST_PAYLOADS)
def test_create_user(base_url, payload):
    """
    Test creating users with multiple payloads (data-driven).
    Validates response status and schema.
    """
    with allure.step(f"Send POST request to create user: {payload['name']}"):
        try:
            url = f"{base_url}/users"
            response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
            log_request_response(response)  # Enhanced logging
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), "Request Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Verify response status is 201"):
        assert response.status_code == 201, (
            f"Expected status 201, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Validate response against schema"):
        validate_response_schema(response, "create_user_schema.json")  # Using utility function
        response_data = response.json()

    with allure.step("Verify created user data matches input"):
        assert response_data["name"] == payload["name"], (
            f"Name mismatch. Expected: {payload['name']}, Got: {response_data['name']}"
        )
        assert response_data["job"] == payload["job"], (
            f"Job mismatch. Expected: {payload['job']}, Got: {response_data['job']}"
        )
        assert "id" in response_data, "Missing 'id' in response"
        assert "createdAt" in response_data, "Missing 'createdAt' in response"

    with allure.step("Attach request and response details"):
        allure.attach(
            json.dumps(payload, indent=2),
            "Request Payload",
            allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(response_data, indent=2),
            "Response Data",
            allure.attachment_type.JSON
        )


@pytest.mark.user_creation
@pytest.mark.boundary
@allure.epic("User Management")
@allure.feature("User Creation")
@allure.title("POST with Large Payload (Boundary Test)")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_with_large_payload(base_url):
    """
    Test creating a user with a large payload (boundary test).
    Validates response status and checks for required fields in response.
    """
    with allure.step("Load large payload from test data"):
        payload = json.load(open("data/large_payload.json"))

    with allure.step("Send POST request with large payload"):
        url = f"{base_url}/users"
        response = requests.post(url, json=payload, headers=get_headers())

    with allure.step("Verify response status is 201"):
        assert response.status_code == 201

    with allure.step("Validate response contains required fields"):
        data = response.json()
        assert "id" in data
        assert "createdAt" in data

    with allure.step("Attach request and response details"):
        allure.attach(json.dumps(payload, indent=2), "Large Request Payload", allure.attachment_type.JSON)
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)


@pytest.mark.user_creation
@pytest.mark.regression
@allure.epic("User Management")
@allure.feature("User Creation")
@allure.title("POST Create User with Minimal Data")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_minimal_data(base_url):
    """
    Test creating a user with minimal required data.
    Validates that the API accepts minimal payloads.
    """
    with allure.step("Prepare minimal payload"):
        payload = {
            "name": "TestUser",
            "job": "Tester"
        }

    with allure.step("Send POST request with minimal data"):
        url = f"{base_url}/users"
        response = requests.post(url, json=payload, headers=get_headers())

    with allure.step("Verify response status is 201"):
        assert response.status_code == 201

    with allure.step("Validate response contains required fields"):
        data = response.json()
        assert "id" in data
        assert "createdAt" in data
        assert data["name"] == payload["name"]
        assert data["job"] == payload["job"]

    with allure.step("Attach request and response details"):
        allure.attach(json.dumps(payload, indent=2), "Minimal Request Payload", allure.attachment_type.JSON)
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
