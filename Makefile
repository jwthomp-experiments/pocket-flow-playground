basic_chat:
	uv run -m basic_chat

multi_agent_chat:
	uv run -m multi_agent_chat

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
