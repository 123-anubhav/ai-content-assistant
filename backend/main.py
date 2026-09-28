from fastapi import FastAPI

from backend.api.books import router as books_router


app = FastAPI(
    title="AI Content Assistant",
    description=(
        "AI assistant for books, documents "
        "and videos"
    ),
    version="1.0.0"
)


app.include_router(
    books_router
)


@app.get("/")
def root():

    return {
        "application": "AI Content Assistant",
        "status": "running"
    }