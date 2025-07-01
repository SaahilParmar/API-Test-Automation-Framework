import pytest
import requests
import json
import allure
from jsonschema import validate
from utils.api_utils import load_config, load_schema, get_headers

# Load base configuration from config.yaml
config = load_config()
BASE_URL = config["environments"][config["env"]]["base_url"]

# ---------------------------
# Test: GET /users?page=2
# ---------------------------
@allure.title("GET List of Users")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_list():
    url = f"{BASE_URL}/users?page=2"
    response = requests.get(url, headers=get_headers())

    assert response.status_code == 200
    data = response.json()
    schema = load_schema("user_list_schema.json")
    validate(instance=data, schema=schema)

# ---------------------------
# Test: GET /users/{id}
# ---------------------------
@allure.title("GET Single User by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("user_id", [1, 2, 5])
def test_get_single_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url, headers=get_headers())

    assert response.status_code == 200
    data = response.json()
    schema = load_schema("single_user_schema.json")
    validate(instance=data, schema=schema)

# ---------------------------
# Test: GET /users/{id} - Negative
# ---------------------------
@allure.title("GET Non-Existent User")
@allure.severity(allure.severity_level.MINOR)
def test_get_user_not_found():
    url = f"{BASE_URL}/users/9999"
    response = requests.get(url, headers=get_headers())

    assert response.status_code == 404

# ---------------------------
# Test: POST /users (Data-Driven)
# ---------------------------
@allure.title("POST Create Users from Payloads")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("payload", json.load(open("data/post_user_payloads.json")))
def test_create_user(payload):
    url = f"{BASE_URL}/users"
    response = requests.post(url, json=payload, headers=get_headers())

    assert response.status_code == 201
    response_data = response.json()
    schema = load_schema("create_user_schema.json")
    validate(instance=response_data, schema=schema)

# ---------------------------
# Test: POST /users with Large Payload
# ---------------------------
@allure.title("POST with Large Payload (Boundary Test)")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user_with_large_payload():
    payload = json.load(open("data/large_payload.json"))
    url = f"{BASE_URL}/users"
    response = requests.post(url, json=payload, headers=get_headers())

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "createdAt" in data

# ---------------------------
# Test: Validate Headers
# ---------------------------
@allure.title("Validate Standard Headers")
@allure.severity(allure.severity_level.TRIVIAL)
def test_headers_validation():
    url = f"{BASE_URL}/users?page=1"
    response = requests.get(url, headers=get_headers())

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")