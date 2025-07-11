# API Schema Documentation

This directory contains JSON Schema definitions for validating API responses from the ReqRes API.

## Schema Files

### 1. user_list_schema.json
- **Endpoint**: GET /api/users?page={page}
- **Purpose**: Validates paginated user list responses
- **Key Properties**:
  - page: Current page number
  - per_page: Items per page
  - total: Total number of users
  - data: Array of user objects
  - support: Support information

### 2. single_user_schema.json
- **Endpoint**: GET /api/users/{id}
- **Purpose**: Validates single user responses
- **Key Properties**:
  - data: Single user object
  - support: Support information

### 3. create_user_schema.json
- **Endpoint**: POST /api/users
- **Purpose**: Validates user creation response
- **Key Properties**:
  - name: User's name
  - job: User's job
  - id: Generated user ID
  - createdAt: Creation timestamp

## Schema Validation
All schemas are JSON Schema Draft-07 compliant and are used in the test suite for response validation. They ensure that:
- Required fields are present
- Field types are correct
- Data structures are consistent
- Additional properties are handled appropriately

## Usage Example
```python
from jsonschema import validate
from utils.api_utils import load_schema

# Load schema
schema = load_schema('user_list_schema.json')

# Validate response
validate(instance=response.json(), schema=schema)
```
