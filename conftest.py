"""
conftest.py - Pytest Configuration and Fixtures

This module provides pytest configuration and fixtures for the API testing framework.
It handles test setup, environment configuration, and common test dependencies.

Configuration:
    - Defines custom pytest markers
    - Sets up directory structure for reports
    - Creates Allure environment properties
    - Validates configuration files

Fixtures:
    config (session): Provides access to configuration data
    base_url (session): Base URL for API requests
    request_id (function): Unique identifier for each request
    log_test_start (function): Logs test start with metadata

Usage:
    The fixtures are automatically available to all test files.
    Example:
        def test_get_users(base_url, request_id):
            response = requests.get(f"{base_url}/users")
            assert response.status_code == 200

Environment Variables:
    TEST_ENV: Override the environment from config.yaml (default: 'dev')
    DEBUG: Enable debug logging (default: False)

Directory Structure:
    /config/
        config.yaml: Main configuration file
    /reports/
        environment.properties: Allure environment data
"""

import pytest
import allure
import os
from utils.api_utils import load_config


def pytest_configure(config):
    """
    Initialize test configuration and environment.
    """
    config.addinivalue_line(
        "markers",
        "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers",
        "user_retrieval: marks tests related to user retrieval operations"
    )
    config.addinivalue_line(
        "markers",
        "regression: marks tests as regression tests"
    )

    # Create reports directory if it doesn't exist
    import os
    os.makedirs("reports", exist_ok=True)

    # Create Allure environment properties file for reporting context
    try:
        config_data = load_config()
        with open("reports/environment.properties", "w") as f:
            f.write(f"BaseURL={config_data['environments'][config_data['env']]['base_url']}\n")
            f.write("Framework=API Test Automation\n")
            f.write("Language=Python\n")
    except Exception:
        # If config loading fails during pytest configure, skip environment file creation
        pass


@pytest.fixture(scope="session")
def config():
    """
    Load and provide the entire config dictionary to tests.
    Raises an error if configuration or schema files are missing.
    """
    # Ensure config file exists
    if not os.path.exists(os.path.join("config", "config.yaml")):
        raise FileNotFoundError("config.yaml not found in config directory")

    # Load config
    config_data = load_config()

    # Validate required config sections
    required_sections = ["env", "environments", "timeout_seconds", "default_headers"]
    for section in required_sections:
        if section not in config_data:
            raise KeyError(f"Missing required config section: {section}")

    # Ensure schemas directory exists with required schemas
    schemas_dir = os.path.join("schemas")
    if not os.path.exists(schemas_dir):
        raise FileNotFoundError("schemas directory not found")

    required_schemas = ["user_list_schema.json"]
    for schema in required_schemas:
        if not os.path.exists(os.path.join(schemas_dir, schema)):
            raise FileNotFoundError(f"Required schema file missing: {schema}")

    return config_data


@pytest.fixture(scope="session")
def base_url(config):
    """
    Provide the base URL for the current environment.
    Validates that the URL is properly configured.
    """
    env = config["env"]
    if env not in config["environments"]:
        raise KeyError(f"Environment '{env}' not found in config")
    url = config["environments"][env]["base_url"]
    if not url:
        raise ValueError(f"Base URL not configured for environment: {env}")

    return url


@pytest.fixture(scope="function")
def driver():
    """
    Dummy fixture for compatibility with tests that might expect a browser driver.

    In this API-only project, this fixture can remain unused or removed.
    """
    # For API testing, no browser driver is required.
    # We keep this fixture placeholder in case future tests integrate with UI.
    yield None


@pytest.fixture(autouse=True)
def attach_allure_logs(request):
    """
    Automatically attach request/response logs to Allure after each test.

    This runs automatically for every test.
    """

    yield

    # This hook executes after each test completes.
    # You could extend this to attach logs or artifacts dynamically.
    # For example, capturing logs from files or API responses.
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.failed:
            # Example: you could attach custom logs here on failure.
            allure.attach(
                "Test failed. Check logs or debug information here.",
                name="Failure Debug Info",
                attachment_type=allure.attachment_type.TEXT
            )
