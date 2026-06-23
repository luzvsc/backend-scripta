from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (
    obter_usuario_logado,
    exigir_coordenador
)
from app.models.auth import UsuarioAutenticado
from app.models.coordenador import (
    CoordenadorResponse,
    CoordenadorUpdate
)
from app.models.projeto import ProjetoStatusUpdate
import app.services.coordenador_service as coordenador_service
import app.services.projeto_service as projeto_service


router = APIRouter(prefix="/coordenadores", tags=["Coordenadores"])


def validar_coordenador_da_rota(
    id_coordenador: int,
    usuario: UsuarioAutenticado
) -> None:
    if usuario.id != id_coordenador:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "O coordenador informado não corresponde "
                "ao usuário autenticado"
            )
        )


@router.get(
    "/",
    response_model=list[CoordenadorResponse],
    status_code=status.HTTP_200_OK
)
def listar_coordenadores(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    return coordenador_service.listar_coordenadores()


@router.get(
    "/{id_coordenador}",
    response_model=CoordenadorResponse,
    status_code=status.HTTP_200_OK
)
def buscar_coordenador_por_id(
    id_coordenador: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    validar_coordenador_da_rota(
        id_coordenador,
        usuario
    )

    try:
        return coordenador_service.buscar_coordenador_por_id(
            id_coordenador
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{id_coordenador}",
    status_code=status.HTTP_200_OK
)
def atualizar_coordenador(
    id_coordenador: int,
    coordenador: CoordenadorUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    validar_coordenador_da_rota(
        id_coordenador,
        usuario
    )

    try:
        coordenador_service.atualizar_coordenador(
            id_coordenador,
            coordenador
        )

        return {
            "message": "Coordenador atualizado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Coordenador não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.patch(
    "/{coordenador_id}/projetos/{id_projeto}/aprovar",
    status_code=status.HTTP_200_OK
)
def aprovar_projeto(
    coordenador_id: int,
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    validar_coordenador_da_rota(
        coordenador_id,
        usuario
    )

    try:
        projeto_service.atualizar_status_projeto(
            id_projeto=id_projeto,
            status_update=ProjetoStatusUpdate(
                status="aprovado"
            ),
            usuario_id=usuario.id,
            usuario_perfil=usuario.perfil
        )

        return {
            "message": "Projeto aprovado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.patch(
    "/{coordenador_id}/projetos/{id_projeto}/reprovar",
    status_code=status.HTTP_200_OK
)
def reprovar_projeto(
    coordenador_id: int,
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    validar_coordenador_da_rota(
        coordenador_id,
        usuario
    )

    try:
        projeto_service.atualizar_status_projeto(
            id_projeto=id_projeto,
            status_update=ProjetoStatusUpdate(
                status="reprovado"
            ),
            usuario_id=usuario.id,
            usuario_perfil=usuario.perfil
        )

        return {
            "message": "Projeto reprovado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )