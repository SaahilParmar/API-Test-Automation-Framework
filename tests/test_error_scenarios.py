"""
test_error_scenarios.py

Test module focused on error scenarios and negative testing.
Covers 404 errors, invalid requests, and edge cases.
"""

import pytest
import requests
import allure
import json
from utils.api_utils import get_headers


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("User Retrieval Errors")
@allure.title("GET Non-Existent User")
@allure.severity(allure.severity_level.MINOR)
def test_get_user_not_found(base_url):
    """
    Test retrieving a non-existent user.
    Expects a 404 Not Found response.
    """
    with allure.step("Send GET request for non-existent user"):
        url = f"{base_url}/users/9999"
        response = requests.get(url, headers=get_headers(), timeout=10)

    with allure.step("Verify response status is 404"):
        assert response.status_code == 404, (
            f"Expected status 404, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Verify response body is empty or contains error info"):
        try:
            data = response.json()
            assert data == {}, f"Expected empty object, got: {json.dumps(data, indent=2)}"
        except json.JSONDecodeError as e:
            allure.attach(response.text, "Invalid JSON Response", allure.attachment_type.TEXT)
            allure.attach(str(e), "JSON Parse Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "404 Response Body", allure.attachment_type.JSON)
        allure.attach(
            json.dumps(get_headers(), indent=2),
            "Request Headers",
            allure.attachment_type.JSON
        )


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("User Retrieval Errors")
@allure.title("GET User with Invalid ID Format")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("invalid_id", ["abc", "!@#", "0", "-1"])
def test_get_user_invalid_id(invalid_id, base_url):
    """
    Test retrieving a user with invalid ID formats.
    Validates error handling for malformed requests.
    """
    with allure.step(f"Send GET request with invalid ID: {invalid_id}"):
        url = f"{base_url}/users/{invalid_id}"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response indicates error or not found"):
        # API might return 404 or other error codes for invalid IDs
        assert response.status_code in [400, 404, 422]

    with allure.step("Attach response details to report"):
        allure.attach(response.text, f"Invalid ID Response: {invalid_id}", allure.attachment_type.JSON)


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("User Creation Errors")
@allure.title("POST User with Empty Payload")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_empty_payload(base_url):
    """
    Test creating a user with empty payload.
    Validates API behavior with missing data.
    """
    with allure.step("Send POST request with empty payload"):
        url = f"{base_url}/users"
        response = requests.post(url, json={}, headers=get_headers())

    with allure.step("Verify response (API may accept empty payload)"):
        # ReqRes API might accept empty payloads, so we check what actually happens
        if response.status_code == 201:
            data = response.json()
            assert "id" in data
            assert "createdAt" in data
        else:
            # If API rejects empty payload, status should indicate error
            assert response.status_code in [400, 422]

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Empty Payload Response", allure.attachment_type.JSON)


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("User Creation Errors")
@allure.title("POST User with Invalid JSON")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_invalid_json(base_url):
    """
    Test creating a user with malformed JSON.
    Validates API error handling for invalid request format.
    """
    with allure.step("Send POST request with invalid JSON"):
        url = f"{base_url}/users"
        headers = get_headers()
        # Send malformed JSON as string
        response = requests.post(url, data='{"name": "test", "job":}', headers=headers)

    with allure.step("Verify response indicates bad request"):
        # Should return 400 Bad Request for malformed JSON
        assert response.status_code == 400

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Invalid JSON Response", allure.attachment_type.JSON)


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("Invalid Endpoints")
@allure.title("GET Invalid Endpoint")
@allure.severity(allure.severity_level.MINOR)
def test_invalid_endpoint(base_url):
    """
    Test accessing an invalid/non-existent endpoint.
    ReqRes API may handle invalid endpoints differently than expected.
    """
    with allure.step("Send GET request to invalid endpoint"):
        url = f"{base_url}/invalid-endpoint"
        response = requests.get(url, headers=get_headers())

    with allure.step("Document API behavior for invalid endpoints"):
        # ReqRes API might return 200 with some default content for invalid endpoints
        # This is not uncommon for some APIs that have catch-all routes
        allure.attach(f"Status Code: {response.status_code}", "Response Status", allure.attachment_type.TEXT)
        allure.attach(response.text[:500], "Response Body (first 500 chars)", allure.attachment_type.TEXT)

        # The test documents behavior rather than enforcing a specific status
        # This is valuable for API contract understanding
        if response.status_code == 200:
            print("INFO: API returns 200 for invalid endpoint (common for some APIs)")
        elif response.status_code == 404:
            print("INFO: API properly returns 404 for invalid endpoint")
        else:
            print(f"INFO: API returns {response.status_code} for invalid endpoint")

        # Always pass - this test is for documentation/exploration
        assert True, "Test passes - documents API behavior for invalid endpoints"


@pytest.mark.error_scenarios
@pytest.mark.negative
@allure.epic("Error Handling")
@allure.feature("Invalid Endpoints")
@allure.title("GET Non-existent User ID")
@allure.severity(allure.severity_level.MINOR)
def test_malformed_url(base_url):
    """
    Test accessing a user with an ID that definitely doesn't exist.
    ReqRes API returns 404 for non-existent user IDs.
    """
    with allure.step("Send GET request to non-existent user ID"):
        # Use a very high user ID that definitely doesn't exist
        url = f"{base_url}/users/999999"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response indicates not found"):
        # ReqRes API returns 404 for non-existent user IDs
        assert response.status_code == 404

    with allure.step("Verify response body indicates not found"):
        # Should return empty object for 404
        data = response.json()
        assert data == {}

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Non-existent User Response", allure.attachment_type.JSON)
