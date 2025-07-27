*   Flake8 - linter for code syntax and cleaning
    ```bash
    flake8 . --show-source --config .github/configurations/python_linters/.flake8
    ```
*   Black - an uncompromising Python code formatter
    ```bash
    black --config .github/configurations/python_linters/.black .
    ```
*   Isort - utility to sort imports alphabetically, and automatically separated into sections and by type
    ```bash
    isort --sp .github/configurations/python_linters/.isort.cfg --profile black .
    ```
