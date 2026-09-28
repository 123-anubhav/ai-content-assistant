from pinecone import Pinecone

from backend.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_DIMENSION
)

from backend.services.embedding_service import (
    create_embedding
)


pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


def store_chunks(
    book_id,
    chunks
):

    vectors = []

    for chunk in chunks:

        embedding = create_embedding(
            chunk["text"]
        )

        vectors.append({

            "id": chunk["id"],

            "values": embedding,

            "metadata": {

                "book_id": chunk["book_id"],

                "page": chunk["page"],

                "chunk": chunk["chunk"],

                "text": chunk["text"]
            }
        })

    # Pinecone accepts batches more efficiently
    batch_size = 50

    total = 0

    for i in range(
        0,
        len(vectors),
        batch_size
    ):

        batch = vectors[
            i:i + batch_size
        ]

        index.upsert(
            vectors=batch,
            namespace=book_id
        )

        total += len(batch)

    return total