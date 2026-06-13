from datetime import datetime, timedelta, UTC
from jose import jwt
import os
from dotenv import load_dotenv
from typing import Any

load_dotenv()

SECRET_KEY_ENV = os.getenv("JWT_SECRET_KEY")

if SECRET_KEY_ENV is None:
    raise ValueError("JWT_SECRET_KEY não configurada no arquivo .env")

SECRET_KEY: str = SECRET_KEY_ENV

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def criar_access_token(dados: dict[str, Any]) -> str:
    dados_token = dados.copy()

    expira_em = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token.update({
        "exp": expira_em
    })

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verificar_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload