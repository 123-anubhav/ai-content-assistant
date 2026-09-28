from backend.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)

from backend.services.llm_service import (
    generate_answer
)

from pinecone import Pinecone


pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


def summarize_pages(
    book_id,
    from_page,
    to_page
):

    # ---------------------------------------------
    # 1. Get all vectors for this page range
    # ---------------------------------------------

    result = index.query(

        namespace=book_id,

        vector=[0.0] * 768,

        top_k=10000,

        filter={
            "page": {
                "$gte": from_page,
                "$lte": to_page
            }
        },

        include_metadata=True
    )

    matches = result.get(
        "matches",
        []
    )

    if not matches:

        return {
            "summary": (
                "No content found for "
                "the requested pages."
            ),
            "pages": []
        }

    # ---------------------------------------------
    # 2. Build context
    # ---------------------------------------------

    page_chunks = {}

    for match in matches:

        metadata = match.get(
            "metadata",
            {}
        )

        page = metadata.get(
            "page"
        )

        text = metadata.get(
            "text",
            ""
        )

        if page is not None:

            page_chunks.setdefault(
                page,
                []
            ).append(
                text
            )

    context_parts = []

    for page in sorted(
        page_chunks
    ):

        page_text = "\n".join(
            page_chunks[page]
        )

        context_parts.append(
            f"[Page {page}]\n{page_text}"
        )

    context = "\n\n".join(
        context_parts
    )

    # ---------------------------------------------
    # 3. Ask LLM to summarize
    # ---------------------------------------------

    prompt = f"""
You are an AI book summarization assistant.

Summarize the following pages of a book.

Requested page range:
{from_page} to {to_page}

Give a clear and useful summary.

Mention important:
- concepts
- explanations
- examples
- conclusions

Do not invent information that is not present
in the provided content.

BOOK CONTENT:

{context}
"""

    summary = generate_answer(
        prompt
    )

    return {

        "from_page": from_page,

        "to_page": to_page,

        "summary": summary,

        "pages": sorted(
            page_chunks.keys()
        )
    }