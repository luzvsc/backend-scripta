from pydantic import BaseModel
from datetime import datetime


class CertificadoBase(BaseModel):
    projeto_id: int
    aluno_id: int


class CertificadoResponse(CertificadoBase):
    id: int

    nome_aluno: str
    titulo_projeto: str
    curso: str
    semestre: str
    nome_professor: str

    data_emissao: datetime
    codigo_autenticidade: str


class CertificadoEmitirRequest(BaseModel):
    projeto_id: int


class CertificadoCreateResponse(BaseModel):
    message: str
    ids_certificados: list[int]