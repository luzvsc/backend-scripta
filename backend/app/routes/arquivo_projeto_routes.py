from fastapi import (APIRouter, Depends, HTTPException, status)
from app.models.arquivo_projeto import (
    ArquivoProjetoCreate,
    ArquivoProjetoCreateResponse,
    ArquivoProjetoResponse,
    ArquivoProjetoListResponse
)
from app.models.auth import UsuarioAutenticado
from app.core.auth_core import (
    obter_usuario_logado,
    exigir_aluno,
    exigir_coordenador
)
from app.services import arquivo_projeto_service


router = APIRouter(prefix="/arquivos", tags=["Arquivos Projeto"])


@router.post(
    "",
    response_model=ArquivoProjetoCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Dados inválidos"
        },
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Projeto não encontrado"
        }
    }
)
def criar_arquivo(
    payload: ArquivoProjetoCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_aluno(usuario)

    try:
        arquivo_id = (
            arquivo_projeto_service.criar_arquivo(
                arquivo=payload,
                aluno_id=usuario.id
            )
        )

        return {
            "message": "Arquivo cadastrado com sucesso",
            "id": arquivo_id
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == "Você não faz parte deste projeto":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.get(
    "",
    response_model=list[ArquivoProjetoListResponse],
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        }
    }
)
def listar_arquivos(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    return arquivo_projeto_service.listar_arquivos()


@router.get(
    "/projeto/{id_projeto}",
    response_model=list[ArquivoProjetoListResponse],
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Projeto não encontrado"
        }
    }
)
def listar_por_projeto(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return arquivo_projeto_service.listar_por_projeto(
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

        if mensagem == (
            "Você não tem permissão para "
            "visualizar os arquivos deste projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.get(
    "/{id_arquivo}",
    response_model=ArquivoProjetoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Arquivo não encontrado"
        }
    }
)
def buscar_arquivo_por_id(
    id_arquivo: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return (
            arquivo_projeto_service.buscar_arquivo_por_id(
                id_arquivo=id_arquivo,
                usuario=usuario
            )
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Arquivo não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você não tem permissão para "
            "visualizar este arquivo"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.delete(
    "/{id_arquivo}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Não foi possível remover"
        },
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Arquivo não encontrado"
        }
    }
)
def deletar_arquivo(
    id_arquivo: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    try:
        arquivo_projeto_service.deletar_arquivo(
            id_arquivo=id_arquivo,
            coordenador_id=usuario.id
        )

        return {
            "message": "Arquivo removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Arquivo não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )
