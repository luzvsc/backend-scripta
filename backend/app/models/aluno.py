from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr 
    curso: str 

class AlunoCreate(AlunoBase):
    senha: str = Field(..., min_length=6)
    confirmar_senha: str

    @model_validator(mode='after')
    def verificar_senhas(self) -> 'AlunoCreate':
        if self.senha != self.confirmar_senha:
            raise ValueError('A senha e a confirmação da senha não coincidem')
        return self

class AlunoResponse(AlunoBase):
    id: int
    matricula: Optional[str] = None
    turma: Optional[str] = None
    semestre_ingresso: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    competencias: Optional[str] = None


class AlunoLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    curso: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    competencias: Optional[str] = None