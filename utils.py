import ollama
#from openai import OpenAI
import os


def call_llm(messages, use_cache: bool = True):
    """
    Calls an Ollama model to generate a text response.

    Args:
        messages (list): The list of message dictionaries to send to the model.
        use_cache (bool, optional): Whether to use Ollama's caching mechanism. Defaults to True.

    Returns:
        str: The generated text response from the model.
    """
    try:
        response = ollama.chat(
            model='qwen3:4b',
            messages=messages,
            stream=False, # important to set stream to false to get the response.
            options = {
                'use_cache': use_cache,
            }

        )
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"Ollama Error: {e}")
        return None  # Or handle the error as needed.

def stream_llm(messages, use_cache: bool = True):
    """
    Calls an Ollama model to generate a text response.

    Args:
        messages (list): The list of message dictionaries to send to the model.
        use_cache (bool, optional): Whether to use Ollama's caching mechanism. Defaults to True.

    Returns:
        str: The generated text response from the model.
    """
    try:
        response = ollama.chat(
            model='qwen3:4b',
            messages=messages,
            stream=True, # important to set stream to false to get the response.
            options = {
                'use_cache': use_cache,
            }

        )
        return response
    except ollama.ResponseError as e:
        print(f"Ollama Error: {e}")
        return None  # Or handle the error as needed.
