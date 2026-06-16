from pydantic import BaseModel
from typing import List

class ProjetoIntegranteCreate(BaseModel):
    aluno_id: int

class ProjetoIntegranteResponse(BaseModel):
    projeto_id: int
    aluno_id: int
    nome: str

class ProjetoIntegranteCreateResponse(BaseModel):
    message: str
