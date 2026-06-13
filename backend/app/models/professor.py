from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class ProfessorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr 


class ProfessorCreate(ProfessorBase):
    senha: str = Field(..., min_length=6)
    confirmar_senha: str
    area_atuacao: Optional[str] = None

    @model_validator(mode='after')
    def verificar_senhas(self) -> 'ProfessorCreate':
        if self.senha != self.confirmar_senha:
            raise ValueError('A senha e a confirmação da senha não coincidem')
        return self


class ProfessorResponse(ProfessorBase):
    id: int
    area_atuacao: Optional[str] = None


class ProfessorLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    area_atuacao: Optional[str] = None


class ProfessorCreateResponse(BaseModel):
    message: str
    id: int