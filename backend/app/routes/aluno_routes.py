from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.aluno import (
    AlunoCreate,
    AlunoCreateResponse,
    AlunoResponse,
    AlunoUpdate
)
import app.services.aluno_service as aluno_service

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=AlunoCreateResponse, responses={409: {"description": "Aluno ja cadastrado"}} ,status_code=status.HTTP_201_CREATED)
def cadastrar_aluno(aluno: AlunoCreate):
    try:
        id_aluno = aluno_service.cadastrar_aluno(aluno)
        return {
        "message": "Aluno cadastrado com sucesso",
        "id": id_aluno
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{id_aluno}", response_model=AlunoResponse, responses={404: {"description": "Aluno não encontrado"}})
def buscar_aluno_por_id(id_aluno: int):
    try:
        aluno = aluno_service.buscar_aluno_por_id(id_aluno)
        return aluno
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[AlunoResponse], status_code=status.HTTP_200_OK)
def listar_alunos():
    alunos = aluno_service.listar_alunos()
    return alunos


@router.delete("/{id_aluno}", status_code=status.HTTP_200_OK, responses={404: {"description": "Aluno não encontrado"}})
def deletar_aluno(id_aluno: int):
    try:
        aluno_service.deletar_aluno(id_aluno)
        return {
            "message": "Aluno removido com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id_aluno}", responses={404: {"description": "Aluno não encontrado"}})
def atualizar_aluno(id_aluno: int, aluno: AlunoUpdate):
    try:
        aluno_service.atualizar_aluno(id_aluno, aluno)
        return {
            "message": "Aluno atualizado com sucesso"
        }
    
    except ValueError as e:
        if str(e) == "Aluno não encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))