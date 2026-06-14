from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class CoordenadorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    departamento: Optional[str] = None


class CoordenadorCreate(CoordenadorBase):
    senha: str = Field(..., min_length=6)
    confirmar_senha: str

    @model_validator(mode='after')
    def verificar_senhas(self) -> 'CoordenadorCreate':
        if self.senha != self.confirmar_senha:
            raise ValueError('A senha e a confirmação da senha não coincidem')
        return self


class CoordenadorResponse(CoordenadorBase):
    id: int
    ativo: Optional[bool] = True


class CoordenadorLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)


class CoordenadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    departamento: Optional[str] = None


class CoordenadorCreateResponse(BaseModel):
    message: str
    id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
