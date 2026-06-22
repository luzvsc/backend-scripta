from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.professor import (
    ProfessorCreate,
    ProfessorCreateResponse,
    ProfessorResponse,
    ProfessorUpdate
)
import app.services.professor_service as professor_service


router = APIRouter(prefix="/professores", tags=["Professores"])


@router.post("/", response_model=ProfessorCreateResponse, responses={409: {"description": "Professor ja cadastrado"}}, status_code=status.HTTP_201_CREATED)
def cadastrar_professor(professor: ProfessorCreate):
    try:
        id_professor = professor_service.cadastrar_professor(professor)
        return {
            "message": "Professor cadastrado com sucesso",
            "id": id_professor
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{id_professor}", response_model=ProfessorResponse, responses={404: {"description": "Professor não encontrado"}})
def buscar_professor_por_id(id_professor: int):
    try:
        return professor_service.buscar_professor_por_id(id_professor)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[ProfessorResponse], status_code=status.HTTP_200_OK)
def listar_professores():
    professores = professor_service.listar_professores()
    return professores


@router.delete("/{id_professor}", status_code=status.HTTP_200_OK, responses={404: {"description": "Professor não encontrado"}})
def deletar_professor(id_professor: int):
    try:
        professor_service.deletar_professor(id_professor)
        return {
            "message": "Professor removido com sucesso"
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id_professor}", status_code=status.HTTP_200_OK, responses={404: {"description": "Professor não encontrado"}, 400: {"description": "Dados inválidos"}})
def atualizar_professor(id_professor: int, professor: ProfessorUpdate):
    try:
        professor_service.atualizar_professor(id_professor, professor)
        return {
            "message": "Professor atualizado com sucesso"
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))