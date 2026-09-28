from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)


def create_chunks(
    pages,
    book_id
):

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        page_chunks = splitter.split_text(
            text
        )

        for chunk_number, chunk_text in enumerate(
            page_chunks
        ):

            chunks.append({

                "id": (
                    f"{book_id}-"
                    f"page-{page_number}-"
                    f"chunk-{chunk_number}"
                ),

                "text": chunk_text,

                "book_id": book_id,

                "page": page_number,

                "chunk": chunk_number
            })

    return chunks