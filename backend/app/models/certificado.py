from pydantic import BaseModel
from typing import Optional
from datetime import date


class CertificadoBase(BaseModel):
    id_projeto: int
    id_aluno: int


class CertificadoResponse(BaseModel):
    id: int
    id_projeto: int
    id_aluno: int
    nome_aluno: Optional[str] = None
    titulo_projeto: Optional[str] = None
    curso: Optional[str] = None
    semestre: Optional[str] = None
    nome_professor: Optional[str] = None
    data_emissao: Optional[date] = None
    codigo_verificacao: Optional[str] = None


class CertificadoEmitirRequest(BaseModel):
    id_projeto: int


class CertificadoCreateResponse(BaseModel):
    message: str
    ids_certificados: list[int]
