# CS6620 Project

# REST API with Docker

This project demonstrates a simple REST API with endpoints for GET, POST, PUT, and DELETE operations. It also includes tests for each endpoint and uses Docker for consistent and reproducible environments.

## Prerequisites

- Docker

## Setup

### 1. Running the API

To build and run the REST API container, execute the following commands:

```sh
chmod +x run_api.sh
./run_api.sh
```

### 2. Running the Tests

To build and run the tests, execute the following commands:

```sh
chmod +x run_tests.sh
./run_tests.sh
```

## REST API Endpoints

- GET /items/<item_id>: Retrieve an item by ID.
- POST /items: Create a new item.
- PUT /items/<item_id>: Update an existing item by ID.
- DELETE /items/<item_id>: Delete an item by ID.

## Testing
The tests are written using pytest and are located in test/test_rest.py. The tests check the following:

- Creating an item (test_create_item)
- Retrieving an item (test_get_item)
- Updating an item (test_update_item)
- Deleting an item (test_delete_item)

## CI/CD
This project includes a GitHub Actions workflow to automatically build and test the API on every push to the main branch or on pull requests targeting the main branch. The workflow is defined in .github/workflows/ci.yml