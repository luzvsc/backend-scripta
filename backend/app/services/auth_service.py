from app.models.auth import (LoginRequest, TokenResponse)
from app.repositories import auth_repository
from app.core.security import verificar_senha
from app.core.jwt_handler import criar_access_token


def login(payload: LoginRequest) -> TokenResponse:

    usuario = auth_repository.buscar_por_email(payload.email)

    if not usuario:
        raise ValueError(
            "Email ou senha inválidos"
        )

    senha_valida = verificar_senha(
        payload.senha,
        usuario["senha"]
    )

    if not senha_valida:
        raise ValueError(
            "Email ou senha inválidos"
        )

    token = criar_access_token(
        {
            "sub": str(usuario["id"]),
            "perfil": usuario["perfil"],
            "email": usuario["email"]
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )