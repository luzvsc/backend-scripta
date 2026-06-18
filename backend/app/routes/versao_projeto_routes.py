from fastapi import APIRouter, HTTPException

from app.models.versao_projeto import (
    VersaoProjetoResponse,
    VersaoProjetoListResponse
)

from app.services import versao_projeto_service

router = APIRouter(prefix="/versoes", tags=["Versões Projeto"])


@router.get("", response_model=list[VersaoProjetoListResponse])
def listar_versoes():

    return versao_projeto_service.listar_versoes()


@router.get("/projeto/{id_projeto}", response_model=list[VersaoProjetoListResponse])
def listar_por_projeto(id_projeto: int):

    try:
        return versao_projeto_service.listar_por_projeto(
            id_projeto
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/{id_versao}", response_model=VersaoProjetoResponse)
def buscar_versao_por_id(id_versao: int):

    try:
        return versao_projeto_service.buscar_versao_por_id(
            id_versao
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )