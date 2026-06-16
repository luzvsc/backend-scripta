from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogSistemaResponse(BaseModel):
    id: int
    coordenador_id: int
    entidade: str
    acao: str
    registro_id: int
    detalhes: Optional[str] = None
    data_hora: Optional[datetime] = None


class LogSistemaFiltro(BaseModel):
    coordenador_id: Optional[int] = None
    entidade: Optional[str] = None
    acao: Optional[str] = None
