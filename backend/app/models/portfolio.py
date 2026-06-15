from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class VisibilidadeEnum(str, Enum):
    publico = 'publico'
    apenas_senac = 'apenas_senac'
    privado = 'privado'

class PortfolioBase(BaseModel):
    aluno_id: int
    projeto_id: int
    visibilidade: VisibilidadeEnum = VisibilidadeEnum.privado

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    visibilidade: VisibilidadeEnum

class PortfolioResponse(PortfolioBase):
    id: int

class PortfolioCreateResponse(BaseModel):
    message: str
    id: int
