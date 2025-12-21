# AGENTS.md

## System Context
You are an AI assistant helping with a modern Python project. The project uses `uv` for all dependency management and environment operations, and `pytest` as the testing framework.

**Crucially, you must never invoke `pip` or `python` directly.** Always use `uv` to run commands within the project's prescribed environment (e.g., `uv run python` or `uv run pytest`).

## Development Workflow and Commands

### Package Management
*   **Install/Sync Dependencies**: Install and synchronize all dependencies defined in `pyproject.toml` (and `uv.lock`, if present).
    ```bash
    uv sync --locked
    ```
*   **Install Development Dependencies**: If the project uses dependency groups (e.g., `[tool.uv.dev-dependencies]` or extras like `[project.optional-dependencies]`), use the appropriate flags to install development tools.
    ```bash
    uv sync --dev
    # or
    uv sync --all-extras
    ```
*   **Add/Remove Packages**: Use `uv add` and `uv remove` to modify project dependencies.
    ```bash
    uv add <package-name>
    uv remove <package-name>
    ```

### Testing
Tests are located in the `tests/` directory and use the `pytest` framework.
*   **Run All Tests**: Execute the entire test suite.
    ```bash
    uv run pytest
    ```
*   **Run Specific Test File**: Run tests within a specific file.
    ```bash
    uv run pytest tests/test_example.py
    ```
*   **Run Tests with Verbose Output**:
    ```bash
    uv run pytest -v
    ```
*   **Run Tests with Coverage**: Generate a test coverage report (requires the `pytest-cov` package to be installed as a dev dependency).
    ```bash
    uv run pytest --cov=<package_name> --cov-report=term-missing
    ```

### Code Quality and Formatting
*   **Linting (Ruff)**: Check code for linting issues (requires `ruff` to be installed as a dev dependency).
    ```bash
    uv run ruff check .
    ```
*   **Auto-formatting (Ruff or Black)**: Automatically format the code.
    ```bash
    uv run ruff format .
    ```

## Review Checklist
Before marking a task as complete, ensure the following:
*   [ ] All new functionality includes appropriate tests in the `tests/` directory.
*   [ ] All tests pass when running `uv run pytest`.
*   [ ] Code is formatted and linted (e.g., `uv run ruff check --fix .` and `uv run ruff format .`).
*   [ ] No bare `print()` statements or broad `except:` blocks are present in production code.
