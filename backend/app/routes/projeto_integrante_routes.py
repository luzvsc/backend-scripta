from fastapi import (APIRouter, Depends, HTTPException, status)
from app.core.auth_core import (
    obter_usuario_logado,
    exigir_aluno,
    exigir_perfis
)
from app.models.auth import UsuarioAutenticado
from app.models.projeto_integrante import (
    ProjetoIntegranteCreate,
    ProjetoIntegranteCreateResponse,
    ProjetoIntegranteResponse
)
import app.services.projeto_integrante_service as integrante_service


router = APIRouter(prefix="/projetos/{id_projeto}/integrantes", tags=["Projeto Integrantes"])


@router.post(
    "/",
    response_model=ProjetoIntegranteCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def adicionar_integrante(
    id_projeto: int,
    integrante: ProjetoIntegranteCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    exigir_perfis(
        usuario,
        [
            "aluno",
            "coordenador"
        ]
    )

    try:
        integrante_service.adicionar_integrante(
            projeto_id=id_projeto,
            integrante=integrante,
            usuario=usuario
        )

        return {
            "message": "Integrante adicionado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Projeto não encontrado",
            "Aluno não encontrado"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Apenas o aluno responsável ou a "
            "coordenação podem adicionar integrantes"
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
    "/",
    response_model=list[ProjetoIntegranteResponse],
    status_code=status.HTTP_200_OK
)
def listar_integrantes(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return integrante_service.listar_integrantes(
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
            "Você não tem permissão para visualizar "
            "os integrantes deste projeto"
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
    "/{id_aluno}",
    status_code=status.HTTP_200_OK
)
def remover_integrante(
    id_projeto: int,
    id_aluno: int,
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

    try:
        integrante_service.remover_integrante(
            projeto_id=id_projeto,
            aluno_id=id_aluno,
            usuario=usuario
        )

        return {
            "message": "Integrante removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Projeto não encontrado",
            "O aluno não faz parte deste projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Apenas o professor orientador ou a "
            "coordenação podem remover integrantes"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )
