from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt_handler import verificar_token
from app.models.auth import UsuarioAutenticado, PerfilUsuario


security = HTTPBearer()


def obter_usuario_logado(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UsuarioAutenticado:

    try:

        payload = verificar_token(credentials.credentials)

        return UsuarioAutenticado(
            id=int(payload["sub"]),
            perfil=payload["perfil"],
            email=payload["email"]
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )


def exigir_aluno(usuario: UsuarioAutenticado) -> None:

    if usuario.perfil != "aluno":
        raise HTTPException(
            status_code=403,
            detail="Apenas alunos podem executar esta ação"
        )


def exigir_professor(usuario: UsuarioAutenticado) -> None:

    if usuario.perfil != "professor":
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem executar esta ação"
        )


def exigir_coordenador(usuario: UsuarioAutenticado) -> None:

    if usuario.perfil != "coordenador":
        raise HTTPException(
            status_code=403,
            detail="Apenas coordenadores podem executar esta ação"
        )


def exigir_perfis(usuario: UsuarioAutenticado, perfis_permitidos: list[str]) -> None:

    if usuario.perfil not in perfis_permitidos:
        raise HTTPException(
            status_code=403,
            detail=f"Esta ação é permitida apenas para perfis: {', '.join(perfis_permitidos)}"
        )


def exigir_empresa(usuario: UsuarioAutenticado) -> None:
    if usuario.perfil != "empresa":
        raise HTTPException(
            status_code=403,
            detail="Apenas empresas podem executar esta ação"
        )
    