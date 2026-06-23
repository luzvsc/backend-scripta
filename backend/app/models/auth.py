from pydantic import BaseModel, EmailStr
from typing import Literal


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


PerfilUsuario = Literal[
    "aluno",
    "professor",
    "coordenador",
    "empresa"
]

class UsuarioAutenticado(BaseModel):
    id: int
    perfil: PerfilUsuario
    email: str