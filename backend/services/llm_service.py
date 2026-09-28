from openai import OpenAI

from backend.config import (
    OLLAMA_URL,
    LLM_MODEL
)


client = OpenAI(
    base_url=f"{OLLAMA_URL}/v1",
    api_key="ollama"
)


def generate_answer(
    prompt
):

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[
        0
    ].message.content