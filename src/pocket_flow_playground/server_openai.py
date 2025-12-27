from fastapi import FastAPI, Request

from .logging_config import logger

# from openai import OpenAI

app = FastAPI()


# Initialize your agent or its core logic here
# For demonstration, we'll just echo the prompt
def run_my_agent(messages):
    # In a real scenario, this would involve your agent's complex logic
    last_message_content = (
        messages[-1]["content"] if messages else "No message provided."
    )
    return {"role": "assistant", "content": f"Agent says: {last_message_content}"}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()

    # Log the incoming request
    logger.info(
        f"Received chat completions request with model: {data.get('model', 'default')}"
    )

    # Extract relevant data for your agent
    messages = data.get("messages", [])
    model = data.get("model", "your-agent-model") # You can define your own model name
    # Log message count
    if messages:
        logger.debug(f"Processing {len(messages)} messages")

    # Run your agent
    agent_response = run_my_agent(messages)

    # Log successful response
    logger.info(f"Generated response: {agent_response['content'][:100]}...")

    # Format the response to be OpenAI-compatible
    response_payload = {
        "id": "chatcmpl-your_id",  # Generate a unique ID
        "object": "chat.completion",
        "created": 1677652288,  # Timestamp
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": agent_response,
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,  # Calculate based on input
            "completion_tokens": 0,  # Calculate based on output
            "total_tokens": 0,
        },
    }
    return response_payload


# To run this with uvicorn:
# uvicorn main:app --reload
