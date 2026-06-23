from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.projeto import (
    ProjetoCreate,
    ProjetoCreateResponse,
    ProjetoResponse,
    ProjetoListResponse,
    ProjetoUpdate,
    ProjetoStatusUpdate
)

import app.services.projeto_service as projeto_service
from app.core.auth_core import obter_usuario_logado, exigir_aluno, exigir_coordenador
from app.models.auth import UsuarioAutenticado



router = APIRouter(prefix="/projetos", tags=["Projetos"])


@router.post(
    "/",
    response_model=ProjetoCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_projeto(
    projeto: ProjetoCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )):

    exigir_aluno(usuario)

    try:
        id_projeto = projeto_service.cadastrar_projeto(
            projeto=projeto,
            aluno_responsavel_id=usuario.id
            )

        return {
            "message": "Projeto cadastrado com sucesso",
            "id": id_projeto
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[ProjetoListResponse],
    status_code=status.HTTP_200_OK
)
def listar_projetos(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    return projeto_service.listar_projetos(
        usuario
    )


@router.get(
    "/{id_projeto}",
    response_model=ProjetoResponse,
    responses={
        403: {
            "description": "Acesso negado"
        },
        404: {
            "description": "Projeto não encontrado"
        }
    }
)
def buscar_projeto_por_id(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return projeto_service.buscar_projeto_por_id(
            id_projeto=id_projeto,
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
            "este projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.put("/{id_projeto}", responses={404: {"description": "Projeto não encontrado"}})
def atualizar_projeto(
    id_projeto: int,
    projeto: ProjetoUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_aluno(usuario)

    try:
        projeto_service.atualizar_projeto(
            id_projeto=id_projeto,
            projeto=projeto,
            quem_alterou_id=usuario.id,
            quem_alterou_tipo="aluno"
        )

        return {
            "message": "Projeto atualizado com sucesso"
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


@router.patch("/{id_projeto}/status", responses={404: {"description": "Projeto não encontrado"}})
def atualizar_status_projeto(
    id_projeto: int,
    status_update: ProjetoStatusUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )):
    novo_status = status_update.status
    if novo_status == "submetido":
        exigir_aluno(usuario)
    elif novo_status in (
        "aprovado",
        "reprovado"
    ):
        exigir_coordenador(usuario)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas alunos e coordenadores podem alterar status"
        )
    
    try:
        projeto_service.atualizar_status_projeto(
            id_projeto=id_projeto,
            status_update=status_update,
            usuario_id=usuario.id,
            usuario_perfil=usuario.perfil
        )

        return {
            "message": "Status atualizado com sucesso"
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


@router.delete("/{id_projeto}", status_code=status.HTTP_200_OK, responses={404: {"description": "Projeto não encontrado"}})
def deletar_projeto(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)
    
    try:
        projeto_service.deletar_projeto(
            id_projeto=id_projeto,
            coordenador_id=usuario.id
        )

        return {
            "message": "Projeto removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto nao encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )