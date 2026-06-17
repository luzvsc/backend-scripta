from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoCreateResponse,
    AvaliacaoResponse,
    AvaliacaoListResponse,
    AvaliacaoUpdate
)

import app.services.avaliacao_service as avaliacao_service

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post("/", response_model=AvaliacaoCreateResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "Dados inválidos"}})
def criar_avaliacao(avaliacao: AvaliacaoCreate):

    try:
        id_avaliacao = avaliacao_service.criar_avaliacao(avaliacao)

        return {
            "message": "Avaliação criada com sucesso",
            "id": id_avaliacao
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.get("/", response_model=List[AvaliacaoListResponse], status_code=status.HTTP_200_OK, responses={404: {"description": "Avaliação não encontrada"}})
def listar_avaliacoes():

    return avaliacao_service.listar_avaliacoes()


@router.get("/{id_avaliacao}", response_model=AvaliacaoResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Avaliação não encontrada"}})
def buscar_avaliacao_por_id(id_avaliacao: int):

    try:
        return avaliacao_service.buscar_avaliacao_por_id(
            id_avaliacao
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/projeto/{id_projeto}", response_model=List[AvaliacaoResponse], status_code=status.HTTP_200_OK, responses={404: {"description": "Projeto não encontrado"}})
def listar_avaliacoes_por_projeto(id_projeto: int):

    return avaliacao_service.listar_avaliacoes_por_projeto(id_projeto)


@router.put("/{id_avaliacao}", status_code=status.HTTP_200_OK, responses={404: {"description": "Avaliação não encontrada"}, 400: {"description": "Dados inválidos"}})
def atualizar_avaliacao(id_avaliacao: int, avaliacao: AvaliacaoUpdate):

    try:

        avaliacao_service.atualizar_avaliacao(
            id_avaliacao,
            avaliacao
        )

        return {
            "message": "Avaliação atualizada com sucesso"
        }

    except ValueError as e:

        mensagem = str(e)

        if mensagem == "Avaliação não encontrada":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )