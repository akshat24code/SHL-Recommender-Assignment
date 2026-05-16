from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    LLM_MODEL
)


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_response(prompt: str):

    completion = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2,
    max_tokens=600,
    timeout=30
)

    return (
        completion
        .choices[0]
        .message.content
        .strip()
    )