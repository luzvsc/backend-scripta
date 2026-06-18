from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class VersaoProjetoCreate(BaseModel):
    
    projeto_id: int
    quem_alterou_tipo: Literal[
    "aluno",
    "professor",
    "coordenador"
]
    quem_alterou_id: int


class VersaoProjetoResponse(BaseModel):
    
    id: int
    projeto_id: int
    projeto_titulo: str
    titulo_na_epoca: str
    descricao_na_epoca: str
    quem_alterou_tipo: Literal[
    "aluno",
    "professor",
    "coordenador"
]
    quem_alterou_id: int
    data_alteracao: datetime
    


class VersaoProjetoListResponse(VersaoProjetoResponse):
    pass


class VersaoProjetoCreateResponse(BaseModel):

    message: str
    id: int