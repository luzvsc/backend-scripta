from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogSistemaResponse(BaseModel):
    id: int
    id_coordenador: int
    nome_coordenador: Optional[str] = None
    acao: str
    entidade: str
    id_entidade: Optional[int] = None
    descricao: Optional[str] = None
    data_hora: Optional[datetime] = None


class LogSistemaFiltro(BaseModel):
    id_coordenador: Optional[int] = None
    entidade: Optional[str] = None
    acao: Optional[str] = None
