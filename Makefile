# Define source directories
SOURCE_DIRS = src tests


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
