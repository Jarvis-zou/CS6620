# CS6620 Project

# REST API with Docker

This project demonstrates a simple REST API with endpoints for GET, POST, PUT, and DELETE operations. It also includes tests for each endpoint and uses Docker for consistent and reproducible environments.

## Prerequisites

- Docker

## Setup

### 1. Running the API

To build and run the REST API container, execute the following commands:

```sh
chmod +x run_localstack.sh
./run_localstack.sh
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
The tests are written using pytest and are located in `tests/test_rest.py`. The tests cover the following scenarios:

- **Sending a GET request with appropriate parameters returns expected JSON from the database**
  - Test case: `test_get_item`
  - Description: Checks if retrieving an existing item with correct parameters returns the expected JSON response.

- **Sending a GET request that finds no results returns the appropriate response**
  - Test case: `test_get_item_not_found`
  - Description: Checks if retrieving a non-existing item returns a 404 response with the appropriate error message.

- **Sending a GET request with no parameters returns the appropriate response**
  - Test case: `test_get_item_no_parameters`
  - Description: Checks if sending a GET request without parameters returns a 400 response indicating missing parameters.

- **Sending a GET request with incorrect parameters returns the appropriate response**
  - Test case: `test_get_item_incorrect_parameters`
  - Description: Checks if sending a GET request with incorrect parameters returns a 400 response indicating incorrect parameters.

- **Sending a POST request results in the JSON body being stored as an item in the database, and an object in an S3 bucket**
  - Test case: `test_create_item`
  - Description: Checks if creating a new item with a POST request stores the item in DynamoDB and the corresponding object in S3, and returns a 201 response with the item data.

- **Sending a duplicate POST request returns the appropriate response**
  - Test case: `test_post_duplicate_item`
  - Description: Checks if sending a POST request with an existing item ID returns a 409 response indicating the item already exists.

- **Sending a PUT request that targets an existing resource results in updates to the appropriate item in the database and object in the S3 bucket**
  - Test case: `test_update_item`
  - Description: Checks if updating an existing item with a PUT request modifies the item in DynamoDB and the corresponding object in S3, and returns a 200 response with the updated item data.

- **Sending a PUT request with no valid target returns the appropriate response**
  - Test case: `test_update_item_not_found`
  - Description: Checks if updating a non-existing item with a PUT request returns a 404 response indicating the item was not found.

- **Sending a DELETE request results in the appropriate item being removed from the database and object being removed from the S3 bucket**
  - Test case: `test_delete_item`
  - Description: Checks if deleting an existing item with a DELETE request removes the item from DynamoDB and the corresponding object from S3, and returns a 200 response confirming the deletion.

- **Sending a DELETE request with no valid target returns the appropriate response**
  - Test case: `test_delete_item_not_found`
  - Description: Checks if deleting a non-existing item with a DELETE request returns a 404 response indicating the item was not found.

### Running Tests
To run the tests, execute the following command in the project's root directory:
```sh
pytest tests/test_rest.py


## CI/CD
This project includes a GitHub Actions workflow to automatically build and test the API on every push to the main branch or on pull requests targeting the main branch. The workflow is defined in .github/workflows/ci.yml