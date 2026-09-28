from backend.services.embedding_service import (
    create_embedding
)

from backend.services.llm_service import (
    generate_answer
)

from backend.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)

from pinecone import Pinecone


pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


def ask_book(
    book_id,
    question
):

    # ---------------------------------------------
    # 1. Convert question to embedding
    # ---------------------------------------------

    question_vector = create_embedding(
        question
    )

    # ---------------------------------------------
    # 2. Search Pinecone
    # ---------------------------------------------

    result = index.query(

        namespace=book_id,

        vector=question_vector,

        top_k=5,

        include_metadata=True
    )

    matches = result.get(
        "matches",
        []
    )

    if not matches:

        return {
            "answer": (
                "I could not find relevant "
                "information in this book."
            ),
            "pages": []
        }

    # ---------------------------------------------
    # 3. Build context
    # ---------------------------------------------

    context_parts = []

    pages = set()

    for match in matches:

        metadata = match.get(
            "metadata",
            {}
        )

        text = metadata.get(
            "text",
            ""
        )

        page = metadata.get(
            "page"
        )

        if text:

            context_parts.append(
                f"[Page {page}]\n{text}"
            )

        if page is not None:
            pages.add(page)

    context = "\n\n".join(
        context_parts
    )

    # ---------------------------------------------
    # 4. Ask LLM
    # ---------------------------------------------

    prompt = f"""
You are a book assistant.

Answer the user's question using ONLY
the provided book context.

If the answer is not present in the context,
say that the information was not found
in the provided book context.

Always mention the relevant page numbers.

BOOK CONTEXT:

{context}

USER QUESTION:

{question}
"""

    answer = generate_answer(
        prompt
    )

    return {

        "answer": answer,

        "pages": sorted(
            pages
        )
    }