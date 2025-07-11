"""
test_user_retrieval.py
        try:
            url = f"{base_url}/users?page=1"
            response = requests.get(url, headers=get_headers(), timeout=10)
            log_request_response(response)  # Enhanced logging
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), "Request Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Verify response status is 200"):dule focused on user retrieval operations (GET requests).
Covers listing users, retrieving single users, and related functionality.
"""

import pytest
import requests
import allure
import json
from jsonschema import validate, ValidationError
from utils.api_utils import load_schema, get_headers, log_request_response


@pytest.mark.user_retrieval
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Retrieval")
@allure.title("GET List of Users")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_list(base_url):
    """
    Test retrieving a paginated list of users.
    Validates response status and schema.
    """
    with allure.step("Send GET request to retrieve user list"):
        try:
            url = f"{base_url}/users?page=2"
            response = requests.get(url, headers=get_headers(), timeout=10)
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), "Request Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Validate response against schema"):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            allure.attach(response.text, "Invalid JSON Response", allure.attachment_type.TEXT)
            allure.attach(str(e), "JSON Parse Error", allure.attachment_type.TEXT)
            raise

        try:
            schema = load_schema("user_list_schema.json")
            validate(instance=data, schema=schema)
        except ValidationError as e:
            allure.attach(
                json.dumps(data, indent=2),
                "Response Data",
                allure.attachment_type.JSON
            )
            allure.attach(str(e), "Schema Validation Error", allure.attachment_type.TEXT)
            raise
        except Exception as e:
            allure.attach(str(e), "Unexpected Error", allure.attachment_type.TEXT)
            raise

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
        allure.attach(
            json.dumps(get_headers(), indent=2),
            "Request Headers",
            allure.attachment_type.JSON
        )


@pytest.mark.user_retrieval
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Retrieval")
@allure.title("GET Single User by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user_id", [1, 2, 5])
def test_get_single_user(user_id, base_url):
    """
    Test retrieving a single user by ID.
    Validates response status and schema.
    """
    with allure.step(f"Send GET request to retrieve user {user_id}"):
        url = f"{base_url}/users/{user_id}"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    with allure.step("Validate response against schema"):
        data = response.json()
        schema = load_schema("single_user_schema.json")
        validate(instance=data, schema=schema)

    with allure.step("Verify user ID matches requested ID"):
        assert data["data"]["id"] == user_id

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)


@pytest.mark.user_retrieval
@pytest.mark.regression
@allure.epic("User Management")
@allure.feature("User Retrieval")
@allure.title("GET User List - Different Pages")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("page", [1, 2])
def test_get_user_list_pagination(page, base_url):
    """
    Test retrieving user lists from different pages.
    Validates pagination functionality.
    """
    with allure.step(f"Send GET request to retrieve page {page}"):
        url = f"{base_url}/users?page={page}"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    with allure.step("Validate response contains pagination info"):
        data = response.json()
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert data["page"] == page

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
