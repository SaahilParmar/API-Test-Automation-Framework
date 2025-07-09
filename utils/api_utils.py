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

    Raises:
        FileNotFoundError: If config.yaml doesn't exist.
        yaml.YAMLError: If config.yaml is invalid.
    """
    config_path = os.path.join("config", "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
            if not config:
                raise ValueError("Empty configuration file")
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config.yaml: {str(e)}")


def load_schema(schema_filename):
    """
    Load a JSON schema from the schemas folder.

    Args:
        schema_filename (str): Filename of the schema (e.g. 'user_list_schema.json')

    Returns:
        dict: Loaded JSON schema.

    Raises:
        FileNotFoundError: If schema file doesn't exist.
        json.JSONDecodeError: If schema is invalid JSON.
    """
    schema_path = os.path.join("schemas", schema_filename)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_filename}")

    with open(schema_path, "r") as f:
        try:
            schema = json.load(f)
            if not schema:
                raise ValueError(f"Empty schema file: {schema_filename}")
            return schema
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in schema {schema_filename}: {str(e)}", e.doc, e.pos)


def get_headers():
    """
    Get default headers defined in config.yaml.

    Returns:
        dict: Headers from configuration.

    Raises:
        KeyError: If default_headers section is missing from config.
    """
    config = load_config()
    if 'default_headers' not in config:
        raise KeyError("default_headers section missing from config.yaml")
    return config['default_headers']


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
