from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.coordenador import (
    CoordenadorCreate,
    CoordenadorCreateResponse,
    CoordenadorResponse,
    CoordenadorUpdate,
    CoordenadorLogin,
    TokenResponse
)
import app.services.coordenador_service as coordenador_service

router = APIRouter(prefix="/coordenadores", tags=["Coordenadores"])


@router.post("/", response_model=CoordenadorCreateResponse, responses={409: {"description": "Coordenador já cadastrado"}}, status_code=status.HTTP_201_CREATED)
def cadastrar_coordenador(coordenador: CoordenadorCreate):
    try:
        id_coordenador = coordenador_service.cadastrar_coordenador(coordenador)
        return {
            "message": "Coordenador cadastrado com sucesso",
            "id": id_coordenador
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=List[CoordenadorResponse], status_code=status.HTTP_200_OK)
def listar_coordenadores():
    coordenadores = coordenador_service.listar_coordenadores()
    return coordenadores


@router.get("/{id_coordenador}", response_model=CoordenadorResponse, responses={404: {"description": "Coordenador não encontrado"}})
def buscar_coordenador_por_id(id_coordenador: int):
    try:
        coordenador = coordenador_service.buscar_coordenador_por_id(id_coordenador)
        return coordenador
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id_coordenador}", responses={404: {"description": "Coordenador não encontrado"}})
def atualizar_coordenador(id_coordenador: int, coordenador: CoordenadorUpdate):
    try:
        coordenador_service.atualizar_coordenador(id_coordenador, coordenador)
        return {
            "message": "Coordenador atualizado com sucesso"
        }
    except ValueError as e:
        if str(e) == "Coordenador não encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_coordenador}", status_code=status.HTTP_200_OK, responses={404: {"description": "Coordenador não encontrado"}})
def deletar_coordenador(id_coordenador: int):
    try:
        coordenador_service.deletar_coordenador(id_coordenador)
        return {
            "message": "Coordenador removido com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/login", response_model=TokenResponse, responses={401: {"description": "Email ou senha inválidos"}}, status_code=status.HTTP_200_OK)
def login_coordenador(login: CoordenadorLogin):
    try:
        token = coordenador_service.login_coordenador(login)
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
