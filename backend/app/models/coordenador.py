from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class CoordenadorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr



class CoordenadorResponse(CoordenadorBase):
    id: int


class CoordenadorLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)


class CoordenadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

