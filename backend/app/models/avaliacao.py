from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class AvaliacaoBase(BaseModel):

    nota_inovacao: float = Field(..., ge=0, le=100)
    nota_tecnica: float = Field(..., ge=0, le=100)
    nota_aplicabilidade: float = Field(..., ge=0, le=100)
    nota_clareza: float = Field(..., ge=0, le=100)
    parecer_descritivo: str = Field(..., min_length=10)


class AvaliacaoCreate(AvaliacaoBase):

    projeto_id: int


class AvaliacaoUpdate(BaseModel):

    nota_inovacao: float | None = Field(None, ge=0, le=100)
    nota_tecnica: float | None = Field(None, ge=0,le=100)
    nota_aplicabilidade: float | None = Field(None, ge=0, le=100)
    nota_clareza: float | None = Field(None, ge=0, le=100)
    parecer_descritivo: str | None = Field(None, min_length=10)


class AvaliacaoResponse(AvaliacaoBase):

    id: int
    projeto_id: int
    professor_id: int
    media_geral: float
    conceito: Literal[
        "Excelente",
        "Ótimo",
        "Bom",
        "Ainda não suficiente",
        "Insuficiente"
    ]
    data_avaliacao: datetime
    professor_nome: str
    projeto_titulo: str


class AvaliacaoCreateResponse(BaseModel):

    message: str
    id: int


class AvaliacaoListResponse(BaseModel):

    id: int
    projeto_id: int
    professor_id: int
    media_geral: float
    conceito: Literal[
        "Excelente",
        "Ótimo",
        "Bom",
        "Ainda não suficiente",
        "Insuficiente"
    ]
    professor_nome: str
    projeto_titulo: str