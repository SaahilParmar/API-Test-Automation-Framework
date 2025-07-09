"""
api_utils.py

Utility functions for API test automation:
- Loads configuration and schema files.
- Provides default HTTP headers.
- Implements request retry logic.
- Attaches request/response details to Allure reports.
- Validates API responses against JSON schemas.
"""

import yaml
import json
import os
import time
import requests
import allure
from functools import wraps
from jsonschema import validate


def load_config():
    """
    Load configuration data from config.yaml file.

    Returns:
        dict: Configuration dictionary.
    """
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_schema(schema_filename):
    """
    Load a JSON schema from the schemas folder.

    Args:
        schema_filename (str): Filename of the schema (e.g. 'user_list_schema.json')

    Returns:
        dict: Loaded JSON schema.
    """
    schema_path = os.path.join("schemas", schema_filename)
    with open(schema_path, "r") as f:
        return json.load(f)


def get_headers():
    """
    Get default headers defined in config.yaml.

    Returns:
        dict: HTTP headers.
    """
    config = load_config()
    headers = config.get("default_headers", {})
    allowed = {"Content-Type", "Accept", "x-api-key"}
    filtered_headers = {k: v for k, v in headers.items() if k in allowed}
    print("DEBUG: get_headers() returns:", filtered_headers)  # Debug print
    return filtered_headers


def retry_request(func):
    """
    Decorator to retry a request on certain errors.

    Uses:
      - config.retry_count
      - config.retry_delay

    Example:
        @retry_request
        def my_func():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        config = load_config()
        retries = config.get("retry_count", 1)
        delay = config.get("retry_delay", 1)

        last_exception = None
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                last_exception = e
                print(f"Retrying ({attempt+1}/{retries}) after error: {e}")
                time.sleep(delay)

        raise last_exception

    return wrapper


def log_request_response(response):
    """
    Attach HTTP request and response details to Allure reports.

    Args:
        response (requests.Response): Response object from requests library.
    """
    if response is None:
        return

    # Attach request details to Allure report
    allure.attach(
        f"{response.request.method} {response.request.url}\n\n"
        f"Headers:\n{response.request.headers}\n\n"
        f"Body:\n{response.request.body}",
        name="Request Details",
        attachment_type=allure.attachment_type.TEXT
    )

    # Attach response details to Allure report
    allure.attach(
        f"Status Code: {response.status_code}\n\n"
        f"Headers:\n{response.headers}\n\n"
        f"Body:\n{response.text}",
        name="Response Details",
        attachment_type=allure.attachment_type.TEXT
    )


def validate_response_schema(response, schema_filename):
    """
    Validate a JSON response body against a schema.

    Args:
        response (requests.Response): Response object.
        schema_filename (str): Name of the JSON schema file.

    Raises:
        jsonschema.exceptions.ValidationError: if the response doesn't match the schema.
    """
    schema = load_schema(schema_filename)
    data = response.json()
    validate(instance=data, schema=schema)
