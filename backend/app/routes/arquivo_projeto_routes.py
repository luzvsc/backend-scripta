from fastapi import APIRouter, HTTPException

from app.models.arquivo_projeto import (
    ArquivoProjetoCreate,
    ArquivoProjetoCreateResponse,
    ArquivoProjetoResponse,
    ArquivoProjetoListResponse
)

from app.services import arquivo_projeto_service

router = APIRouter(prefix="/arquivos", tags=["Arquivos Projeto"])

@router.post("", response_model=ArquivoProjetoCreateResponse, status_code=201)
def criar_arquivo(payload: ArquivoProjetoCreate):

    try:
        arquivo_id = arquivo_projeto_service.criar_arquivo(payload)

        return {
            "message": "Arquivo cadastrado com sucesso",
            "id": arquivo_id
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.get("", response_model=list[ArquivoProjetoListResponse])
def listar_arquivos():

    return arquivo_projeto_service.listar_arquivos()


@router.get("/projeto/{id_projeto}", response_model=list[ArquivoProjetoListResponse])
def listar_por_projeto(id_projeto: int):

    try:
        return arquivo_projeto_service.listar_por_projeto(id_projeto)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    

@router.get("/{id_arquivo}", response_model=ArquivoProjetoResponse)
def buscar_arquivo_por_id(id_arquivo: int):

    try:
        return arquivo_projeto_service.buscar_arquivo_por_id(id_arquivo)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/{id_arquivo}", status_code=200)
def deletar_arquivo(id_arquivo: int):

    try:

        arquivo_projeto_service.deletar_arquivo(id_arquivo)

        return {
            "message": "Arquivo removido com sucesso"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )