server:
	uv run uvicorn server:app --reload

#web-ui: OPENAI_BASE_URL=http://localhost:11434/v1
web-ui: OPENAI_BASE_URL=http://localhost:8000/v1
web-ui:
	uv run streamlit run web_ui.py

basic_chat:
	uv run -m basic_chat

multi_agent_chat:
	uv run -m multi_agent_chat

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
