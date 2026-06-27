from pydantic import BaseModel, Field
from typing import Optional, Literal

class ProjetoBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=150)
    descricao: str = Field(..., min_length=10)
    curso: str = Field(..., min_length=2, max_length=100)
    turma: str = Field(..., min_length=1, max_length=50)
    semestre: str = Field(..., min_length=1, max_length=10)
    area_conhecimento: str = Field(..., min_length=3, max_length=150)


class ProjetoCreate(ProjetoBase):
    professor_orientador_id: int


class ProjetoResponse(ProjetoBase):
    id: int

    status: Literal[
        "rascunho",
        "submetido",
        "em_avaliacao",
        "aprovado",
        "reprovado"
    ]

    aluno_responsavel_id: int
    professor_orientador_id: int

    aluno_responsavel: str
    professor_orientador: str


class ProjetoUpdate(BaseModel):
    titulo: Optional[str] = Field(
        None,
        min_length=3,
        max_length=150
    )
    descricao: Optional[str] = Field(
        None,
        min_length=10
    )
    curso: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )
    turma: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50
    )
    semestre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=10
    )
    area_conhecimento: Optional[str] = Field(
        None,
        min_length=3,
        max_length=150
    )
    professor_orientador_id: Optional[int] = Field(
        None,
        ge=1
    )


class ProjetoStatusUpdate(BaseModel):
    status: Literal[
        "rascunho",
        "submetido",
        "em_avaliacao",
        "aprovado",
        "reprovado"
    ]


class ProjetoCreateResponse(BaseModel):
    message: str
    id: int


class ProjetoListResponse(BaseModel):
    id: int
    titulo: str
    curso: str
    turma: str
    semestre: str
    area_conhecimento: str

    status: Literal[
        "rascunho",
        "submetido",
        "em_avaliacao",
        "aprovado",
        "reprovado"
    ]

    aluno_responsavel: str
    professor_orientador: str