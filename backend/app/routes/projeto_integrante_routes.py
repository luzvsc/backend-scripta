from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.projeto_integrante import (
    ProjetoIntegranteCreate,
    ProjetoIntegranteCreateResponse,
    ProjetoIntegranteResponse
)
import app.services.projeto_integrante_service as integrante_service

router = APIRouter(prefix="/projetos/{id_projeto}/integrantes", tags=["Projeto Integrantes"])

@router.post("/", response_model=ProjetoIntegranteCreateResponse, status_code=status.HTTP_201_CREATED)
def adicionar_integrante(id_projeto: int, integrante: ProjetoIntegranteCreate):
    try:
        integrante_service.adicionar_integrante(id_projeto, integrante)
        return {
            "message": "Integrante adicionado com sucesso"
        }
    except ValueError as e:
        if str(e) == "Projeto não encontrado" or str(e) == "Aluno não encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ProjetoIntegranteResponse], status_code=status.HTTP_200_OK)
def listar_integrantes(id_projeto: int):
    try:
        integrantes = integrante_service.listar_integrantes(id_projeto)
        return integrantes
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
