"""
test_user_retrieval.py

Test module focused on user retrieval operations (GET requests).
Covers listing users, retrieving single users, and related functionality.
"""

import pytest
import requests
import allure
from jsonschema import validate
from utils.api_utils import load_config, load_schema, get_headers

# Load base configuration from config.yaml
config = load_config()
BASE_URL = config["environments"][config["env"]]["base_url"]


@pytest.mark.user_retrieval
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Retrieval")
@allure.title("GET List of Users")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_list():
    """
    Test retrieving a paginated list of users.
    Validates response status and schema.
    """
    with allure.step("Send GET request to retrieve user list"):
        url = f"{BASE_URL}/users?page=2"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200

    with allure.step("Validate response against schema"):
        data = response.json()
        schema = load_schema("user_list_schema.json")
        validate(instance=data, schema=schema)

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)


@pytest.mark.user_retrieval
@pytest.mark.smoke
@allure.epic("User Management")
@allure.feature("User Retrieval")
@allure.title("GET Single User by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user_id", [1, 2, 5])
def test_get_single_user(user_id):
    """
    Test retrieving a single user by ID.
    Validates response status and schema.
    """
    with allure.step(f"Send GET request to retrieve user {user_id}"):
        url = f"{BASE_URL}/users/{user_id}"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200

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
def test_get_user_list_pagination(page):
    """
    Test retrieving user lists from different pages.
    Validates pagination functionality.
    """
    with allure.step(f"Send GET request to retrieve page {page}"):
        url = f"{BASE_URL}/users?page={page}"
        response = requests.get(url, headers=get_headers())

    with allure.step("Verify response status is 200"):
        assert response.status_code == 200

    with allure.step("Validate response contains pagination info"):
        data = response.json()
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert data["page"] == page

    with allure.step("Attach response details to report"):
        allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
