# CS6620 Project

## Project Overview
This project demonstrates basic function operations and unit testing.

## Install Dependencies
Before running the tests, you need to install the project dependencies. Ensure you have Python installed and follow these steps:

1. Open a terminal.
2. Navigate to the project directory.
3. Run the following command to install the dependencies:

```sh
pip install -r requirements.txt
python tests/test_main.py
```
## CI/CD Pipeline

This repository contains a CI/CD pipeline that runs automatically on every push and pull request to the `main` branch. Additionally, you can run the workflow manually.

### Running the Workflow Manually

To run the workflow manually, follow these steps:

1. Navigate to the `Actions` tab in your GitHub repository.
2. In the left sidebar, select the workflow named `CI/CD Pipeline`.
3. Click the `Run workflow` button on the right side of the page.
4. Select the branch (if necessary) and click the `Run workflow` button to trigger the workflow.

The workflow will then run, and you can monitor its progress under the `Actions` tab.
