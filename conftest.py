import pytest
import allure
import requests
from utils.api_utils import load_config, log_request_response

@pytest.fixture(scope="session")
def config():
    """
    Load and provide the entire config dictionary to tests.
    """
    return load_config()

@pytest.fixture(scope="session")
def base_url(config):
    """
    Provide the base URL for the current environment.
    """
    env = config["env"]
    return config["environments"][env]["base_url"]

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

def pytest_configure(config):
    """
    Pytest hook to customize test configuration.

    - Sets up custom markers for smoke and regression tests.
    - Generates Allure environment properties file for reporting.
    """
    # Register custom markers for test categorization
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")

    # Create reports directory if it doesn't exist
    import os
    os.makedirs("reports", exist_ok=True)
    
    # Create Allure environment properties file for reporting context
    with open("reports/environment.properties", "w") as f:
        f.write(f"BaseURL={load_config()['environments'][load_config()['env']]['base_url']}\n")
        f.write("Framework=API Test Automation\n")
        f.write("Language=Python\n")