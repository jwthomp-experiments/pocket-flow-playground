# Define source directories
SOURCE_DIRS = src tests

server:
	uv run uvicorn src.pocket_flow_playground.server_openai:app --reload

#web-ui: OPENAI_BASE_URL=http://localhost:11434/v1
web-ui: OPENAI_BASE_URL=http://localhost:8000/v1
web-ui:
	uv run streamlit run src/pocket_flow_playground/web_ui.py


@PHONY: cli
cli:
	uv run python -m src.pocket_flow_playground.main


@PHONY: test
test:
	uv run pytest

@PHONY: lint
lint: ruff-check ty-check

@PHONY: format
format: ruff-fix $(SOURCE_DIRS)

@PHONY: ruff-check
ruff-check:
	uv run ruff check $(SOURCE_DIRS)

@PHONY: ruff-fix
ruff-fix:
	uv run ruff check $(SOURCE_DIRS) --fix

@PHONY: ty-check
ty-check:
	uv run ty check $(SOURCE_DIRS)

@PHONY: clean
clean:
	uv run ruff clean
	find . \( -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" \) -exec rm -rf {} +
	rm -rf .venv
	rm -rf dist
