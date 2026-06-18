from pydantic import BaseModel, Field


class ArquivoProjetoBase(BaseModel):

    projeto_id: int
    nome_original: str = Field(..., min_length=1, max_length=255)
    tamanho_mb: float = Field(..., gt=0)


class ArquivoProjetoCreate(ArquivoProjetoBase):
    
    projeto_id: int
    nome_original: str
    caminho_servidor: str
    tamanho_mb: float


class ArquivoProjetoUpdate(BaseModel):

    nome_original: str | None = Field(None, min_length=1, max_length=255)
    tamanho_mb: float | None = Field(None, gt=0)


class ArquivoProjetoResponse(BaseModel):

    id: int
    projeto_id: int
    nome_original: str
    caminho_servidor: str
    tamanho_mb: float



class ArquivoProjetoCreateResponse(BaseModel):

    message: str
    id: int


class ArquivoProjetoListResponse(BaseModel):

    id: int
    projeto_id: int
    nome_original: str
    tamanho_mb: float