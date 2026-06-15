from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class CoordenadorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    departamento: Optional[str] = None



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


