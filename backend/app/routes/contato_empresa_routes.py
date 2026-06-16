from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.contato_empresa import (
    ContatoEmpresaCreate,
    ContatoEmpresaCreateResponse,
    ContatoEmpresaResponse
)
import app.services.contato_empresa_service as contato_service

router = APIRouter(prefix="/contatos", tags=["Contatos Empresa"])

@router.post("/", response_model=ContatoEmpresaCreateResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_contato(contato: ContatoEmpresaCreate):
    try:
        id_contato = contato_service.cadastrar_contato(contato)
        return {
            "message": "Contato enviado com sucesso",
            "id": id_contato
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_contato}", response_model=ContatoEmpresaResponse, responses={404: {"description": "Contato não encontrado"}})
def buscar_contato_por_id(id_contato: int):
    try:
        contato = contato_service.buscar_contato_por_id(id_contato)
        return contato
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/aluno/{id_aluno}", response_model=List[ContatoEmpresaResponse], status_code=status.HTTP_200_OK)
def buscar_contatos_por_aluno(id_aluno: int):
    contatos = contato_service.buscar_contatos_por_aluno(id_aluno)
    return contatos
