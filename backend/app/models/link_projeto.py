from pydantic import BaseModel, Field


class LinkProjetoCreate(BaseModel):
    url: str = Field(
        ...,
        min_length=8,
        max_length=500,
        pattern=r"^https?://"
    )

    descricao: str | None = Field(
        default=None,
        max_length=100
    )


class LinkProjetoUpdate(BaseModel):
    url: str | None = Field(
        default=None,
        min_length=8,
        max_length=500,
        pattern=r"^https?://"
    )

    descricao: str | None = Field(
        default=None,
        max_length=100
    )


class LinkProjetoResponse(BaseModel):
    id: int
    projeto_id: int
    url: str
    descricao: str | None = None


class LinkProjetoCreateResponse(BaseModel):
    message: str
    id: int