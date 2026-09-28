from openai import OpenAI

from backend.config import (
    OLLAMA_URL,
    EMBEDDING_MODEL
)


# --------------------------------------------------
# Ollama OpenAI-compatible client
# --------------------------------------------------

client = OpenAI(
    base_url=f"{OLLAMA_URL}/v1",
    api_key="ollama"
)


# --------------------------------------------------
# Single text embedding
# --------------------------------------------------

def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


# --------------------------------------------------
# Multiple text embeddings
# --------------------------------------------------

def create_embeddings(texts):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    # OpenAI-compatible response contains
    # one embedding object for every input text.

    embeddings = sorted(
        response.data,
        key=lambda item: item.index
    )

    return [
        item.embedding
        for item in embeddings
    ]