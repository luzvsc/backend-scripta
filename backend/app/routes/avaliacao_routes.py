from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from typing import List

from app.models.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoCreateResponse,
    AvaliacaoResponse,
    AvaliacaoListResponse,
    AvaliacaoUpdate
)
from app.models.auth import UsuarioAutenticado

from app.core.auth_core import (
    obter_usuario_logado,
    exigir_professor,
    exigir_perfis
)

import app.services.avaliacao_service as avaliacao_service


router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post(
    "/",
    response_model=AvaliacaoCreateResponse,
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
def criar_avaliacao(
    avaliacao: AvaliacaoCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_professor(usuario)

    try:
        id_avaliacao = (
            avaliacao_service.criar_avaliacao(
                avaliacao=avaliacao,
                professor_id=usuario.id
            )
        )

        return {
            "message": "Avaliação criada com sucesso",
            "id": id_avaliacao
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


@router.get(
    "/",
    response_model=List[AvaliacaoListResponse],
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        }
    }
)
def listar_avaliacoes(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_perfis(
        usuario,
        [
            "professor",
            "coordenador"
        ]
    )

    return avaliacao_service.listar_avaliacoes(
        usuario
    )


@router.get(
    "/projeto/{id_projeto}",
    response_model=List[AvaliacaoResponse],
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
def listar_avaliacoes_por_projeto(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return (
            avaliacao_service.listar_avaliacoes_por_projeto(
                projeto_id=id_projeto,
                usuario=usuario
            )
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você não tem permissão para visualizar "
            "as avaliações deste projeto"
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
    "/{id_avaliacao}",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Avaliação não encontrada"
        }
    }
)
def buscar_avaliacao_por_id(
    id_avaliacao: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return avaliacao_service.buscar_avaliacao_por_id(
            id_avaliacao=id_avaliacao,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Avaliação não encontrada":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você não tem permissão para "
            "visualizar esta avaliação"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.put(
    "/{id_avaliacao}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Dados inválidos"
        },
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Avaliação não encontrada"
        }
    }
)
def atualizar_avaliacao(
    id_avaliacao: int,
    avaliacao: AvaliacaoUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_professor(usuario)

    try:
        avaliacao_service.atualizar_avaliacao(
            id_avaliacao=id_avaliacao,
            avaliacao=avaliacao,
            professor_id=usuario.id
        )

        return {
            "message": "Avaliação atualizada com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Avaliação não encontrada",
            "Projeto não encontrado"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você só pode alterar avaliações "
            "criadas por você"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )