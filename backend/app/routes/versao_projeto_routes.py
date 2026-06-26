from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (exigir_coordenador, obter_usuario_logado)
from app.models.auth import UsuarioAutenticado
from app.models.versao_projeto import (VersaoProjetoListResponse, VersaoProjetoResponse)
import app.services.versao_projeto_service as versao_projeto_service


router = APIRouter(prefix="/versoes", tags=["Versões Projeto"])


@router.get(
    "",
    response_model=list[VersaoProjetoListResponse],
    status_code=status.HTTP_200_OK
)
def listar_versoes(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_coordenador(usuario)

    try:
        return versao_projeto_service.listar_versoes(
            usuario=usuario
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/projeto/{id_projeto}",
    response_model=list[VersaoProjetoListResponse],
    status_code=status.HTTP_200_OK
)
def listar_por_projeto(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return versao_projeto_service.listar_por_projeto(
            projeto_id=id_projeto,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.get(
    "/{id_versao}",
    response_model=VersaoProjetoResponse,
    status_code=status.HTTP_200_OK
)
def buscar_versao_por_id(
    id_versao: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return versao_projeto_service.buscar_versao_por_id(
            id_versao=id_versao,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Versão não encontrada",
            "Projeto não encontrado"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )