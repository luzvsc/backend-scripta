from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ContatoEmpresaBase(BaseModel):
    empresa_id: int
    aluno_id: int
    assunto: str = Field(..., max_length=150)
    mensagem: str

class ContatoEmpresaCreate(ContatoEmpresaBase):
    pass

class ContatoEmpresaResponse(ContatoEmpresaBase):
    id: int
    data_envio: datetime

class ContatoEmpresaCreateResponse(BaseModel):
    message: str
    id: int
