"""
test_user_creation.py

Test module focused on user creation operations (POST requests).
Covers data-driven testing, boundary testing, and user creation scenarios.
"""

import pytest
import requests
import json
import allure
from jsonschema import validate
from utils.api_utils import load_config, load_schema, get_headers

# Load base configuration from config.yaml
config = load_config()
BASE_URL = config["environments"][config["env"]]["base_url"]


@pytest.mark.user_creation
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Creation")
@allure.title("POST Create Users from Payloads")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("payload", json.load(open("data/post_user_payloads.json")))
def test_create_user(payload):
    """
    Test creating users with multiple payloads (data-driven).
    Validates response status and schema.
    """
    with allure.step(f"Send POST request to create user: {payload['name']}"):
        url = f"{BASE_URL}/users"
        response = requests.post(url, json=payload, headers=get_headers())

    with allure.step("Verify response status is 201"):
        assert response.status_code == 201

    with allure.step("Validate response against schema"):
        response_data = response.json()
        schema = load_schema("create_user_schema.json")
        validate(instance=response_data, schema=schema)

    with allure.step("Verify created user data matches input"):
        assert response_data["name"] == payload["name"]
        assert response_data["job"] == payload["job"]
        assert "id" in response_data
        assert "createdAt" in response_data

    with allure.step("Attach request and response details"):
        allure.attach(json.dumps(payload, indent=2), "Request Payload", allure.attachment_type.JSON)
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)


@pytest.mark.user_creation
@pytest.mark.boundary
@allure.epic("User Management")
@allure.feature("User Creation")
@allure.title("POST with Large Payload (Boundary Test)")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_with_large_payload():
    """
    Test creating a user with a large payload (boundary test).
    Validates response status and checks for required fields in response.
    """
    with allure.step("Load large payload from test data"):
        payload = json.load(open("data/large_payload.json"))

    with allure.step("Send POST request with large payload"):
        url = f"{BASE_URL}/users"
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
def test_create_user_minimal_data():
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
        url = f"{BASE_URL}/users"
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
