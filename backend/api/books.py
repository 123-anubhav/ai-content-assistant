import os
import uuid
import tempfile

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from backend.services.s3_service import (
    upload_file,
    download_file
)

from backend.services.pdf_service import (
    extract_pages
)

from backend.utils.chunking import (
    create_chunks
)

from backend.services.vector_service import (
    store_chunks
)

from backend.services.rag_service import (
    ask_book
)

from backend.services.summary_service import (
    summarize_pages
)

from backend.models.schemas import (
    AskBookRequest,
    SummaryRequest
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# =========================================================
# TEST
# =========================================================

@router.get("/test")
def test_books():

    return {
        "message": "Books API is working"
    }


# =========================================================
# UPLOAD BOOK
# =========================================================

@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    book_id = str(
        uuid.uuid4()
    )

    s3_key = (
        f"books/{book_id}/"
        f"{file.filename}"
    )

    temp_path = os.path.join(
        tempfile.gettempdir(),
        f"{book_id}.pdf"
    )

    try:

        # -----------------------------------------
        # 1. Upload original PDF to S3
        # -----------------------------------------

        upload_file(
            file.file,
            s3_key
        )

        # -----------------------------------------
        # 2. Download temporary PDF
        # -----------------------------------------

        download_file(
            s3_key,
            temp_path
        )

        # -----------------------------------------
        # 3. Extract pages
        # -----------------------------------------

        pages = extract_pages(
            temp_path
        )

        if not pages:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found. "
                    "This may be a scanned PDF."
                )
            )

        # -----------------------------------------
        # 4. Create chunks
        # -----------------------------------------

        chunks = create_chunks(
            pages,
            book_id
        )

        # -----------------------------------------
        # 5. Generate embeddings
        # 6. Store in Pinecone
        # -----------------------------------------

        vector_count = store_chunks(
            book_id,
            chunks
        )

        return {

            "book_id": book_id,

            "filename": file.filename,

            "s3_key": s3_key,

            "pages": len(pages),

            "chunks": len(chunks),

            "vectors": vector_count,

            "message": (
                "Book uploaded and "
                "indexed successfully"
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Book processing failed: {str(e)}"
            )
        )

    finally:

        if os.path.exists(
            temp_path
        ):

            os.remove(
                temp_path
            )


# =========================================================
# ASK QUESTION
# =========================================================

@router.post(
    "/{book_id}/ask"
)
async def ask_question(
    book_id: str,
    request: AskBookRequest
):

    try:

        return ask_book(
            book_id,
            request.question
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Question processing failed: {str(e)}"
            )
        )


# =========================================================
# SUMMARIZE PAGE RANGE
# =========================================================

@router.post(
    "/{book_id}/summary"
)
async def summarize_book(
    book_id: str,
    request: SummaryRequest
):

    if request.from_page > request.to_page:

        raise HTTPException(
            status_code=400,
            detail=(
                "from_page must be less than "
                "or equal to to_page"
            )
        )

    try:

        return summarize_pages(

            book_id,

            request.from_page,

            request.to_page
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Summary processing failed: {str(e)}"
            )
        )