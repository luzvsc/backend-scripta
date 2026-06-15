from fastapi import APIRouter, HTTPException, status
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


router = APIRouter(prefix="/projetos", tags=["Projetos"])


@router.post(
    "/",
    response_model=ProjetoCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_projeto(projeto: ProjetoCreate):
    try:
        id_projeto = projeto_service.cadastrar_projeto(projeto)

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
def listar_projetos():
    return projeto_service.listar_projetos()


@router.get(
    "/{id_projeto}",
    response_model=ProjetoResponse,
    responses={
        404: {"description": "Projeto não encontrado"}
    }
)
def buscar_projeto_por_id(id_projeto: int):
    try:
        return projeto_service.buscar_projeto_por_id(
            id_projeto
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{id_projeto}",
    responses={
        404: {"description": "Projeto não encontrado"}
    }
)
def atualizar_projeto(
    id_projeto: int,
    projeto: ProjetoUpdate
):
    try:
        projeto_service.atualizar_projeto(
            id_projeto,
            projeto
        )

        return {
            "message": "Projeto atualizado com sucesso"
        }

    except ValueError as e:

        if str(e) == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{id_projeto}/status", responses={404: {"description": "Projeto não encontrado"}})
def atualizar_status_projeto(id_projeto: int, status_update: ProjetoStatusUpdate):
    try:
        projeto_service.atualizar_status_projeto(id_projeto, status_update)

        return {
            "message": "Status atualizado com sucesso"
        }

    except ValueError as e:
        if str(e) == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_projeto}", status_code=status.HTTP_200_OK, responses={404: {"description": "Projeto não encontrado"}})
def deletar_projeto(id_projeto: int):
    
    try:
        projeto_service.deletar_projeto(
            id_projeto
        )

        return {
            "message": "Projeto removido com sucesso"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )