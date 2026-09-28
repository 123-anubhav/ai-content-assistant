import os

from dotenv import load_dotenv

load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-1"
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME"
)

PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME"
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

EMBEDDING_DIMENSION = 768

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2"
)