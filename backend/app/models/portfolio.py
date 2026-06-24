from enum import Enum
from pydantic import BaseModel


class VisibilidadeEnum(str, Enum):
    publico = "publico"
    apenas_senac = "apenas_senac"
    privado = "privado"


class PortfolioCreate(BaseModel):
    projeto_id: int
    visibilidade: VisibilidadeEnum = VisibilidadeEnum.privado


class PortfolioUpdate(BaseModel):
    visibilidade: VisibilidadeEnum


class PortfolioResponse(BaseModel):
    id: int
    aluno_id: int
    projeto_id: int
    visibilidade: VisibilidadeEnum

    nome_aluno: str
    titulo_projeto: str
    curso: str
    semestre: str


class PortfolioCreateResponse(BaseModel):
    message: str
    id: int
