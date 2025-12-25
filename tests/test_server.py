from fastapi.testclient import TestClient

from pocket_flow_playground import server_openai as server

# This file has been AI generated and not tested yet.
# Please review and review this notice after confirming code
# is correct.


def test_run_my_agent_with_messages():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": "How are you?"},
    ]

    resp = server.run_my_agent(messages)

    assert isinstance(resp, dict)
    assert resp["role"] == "assistant"
    assert resp["content"] == "Agent says: How are you?"


def test_run_my_agent_empty_messages():
    resp = server.run_my_agent([])

    assert resp["role"] == "assistant"
    assert resp["content"] == "Agent says: No message provided."


def test_chat_completions_endpoint_echo():
    client = TestClient(server.app)

    payload = {"model": "test-model", "messages": [{"role": "user", "content": "Ping"}]}
    r = client.post("/v1/chat/completions", json=payload)

    assert r.status_code == 200
    data = r.json()

    # model is echoed
    assert data["model"] == "test-model"

    # choices structure
    assert "choices" in data
    assert isinstance(data["choices"], list) and len(data["choices"]) >= 1

    choice = data["choices"][0]
    assert choice["index"] == 0
    assert choice["message"] == server.run_my_agent(payload["messages"])


def test_chat_completions_default_model_and_empty_messages():
    client = TestClient(server.app)

    r = client.post("/v1/chat/completions", json={})
    assert r.status_code == 200
    data = r.json()

    # default model
    assert data["model"] == "your-agent-model"

    # message reflects no input
    assert (
        data["choices"][0]["message"]["content"] == "Agent says: No message provided."
    )
