from pydantic import BaseModel, Field


class AskBookRequest(BaseModel):

    question: str = Field(
        min_length=1
    )


class SummaryRequest(BaseModel):

    from_page: int = Field(
        ge=1
    )

    to_page: int = Field(
        ge=1
    )