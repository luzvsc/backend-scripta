from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional

class EmpresaBase(BaseModel):
    nome_empresa: str = Field(..., min_length=2, max_length=150)
    cnpj: str = Field(..., min_length=14, max_length=18)
    email_contato: EmailStr 
    setor: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    senha: str = Field(..., min_length=6)
    confirmar_senha: str

    @model_validator(mode='after')
    def verificar_senhas(self) -> 'EmpresaCreate':
        if self.senha != self.confirmar_senha:
            raise ValueError('A senha e a confirmação da senha não coincidem')
        return self

class EmpresaResponse(EmpresaBase):
    id: int

class EmpresaLogin(BaseModel):
    email_contato: EmailStr
    senha: str = Field(..., min_length=6)

class EmpresaUpdate(BaseModel):
    nome_empresa: Optional[str] = None
    cnpj: Optional[str] = None
    email_contato: Optional[EmailStr] = None
    setor: Optional[str] = None

class EmpresaCreateResponse(BaseModel):
    message: str
    id: int
