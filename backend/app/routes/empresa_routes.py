from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.empresa import (
    EmpresaCreate,
    EmpresaCreateResponse,
    EmpresaResponse,
    EmpresaUpdate,
    EmpresaLogin
)
import app.services.empresa_service as empresa_service
from app.models.auth import TokenResponse

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=EmpresaCreateResponse, responses={409: {"description": "Empresa ja cadastrada"}} ,status_code=status.HTTP_201_CREATED)
def cadastrar_empresa(empresa: EmpresaCreate):
    try:
        id_empresa = empresa_service.cadastrar_empresa(empresa)
        return {
        "message": "Empresa cadastrada com sucesso",
        "id": id_empresa
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{id_empresa}", response_model=EmpresaResponse, responses={404: {"description": "Empresa não encontrada"}})
def buscar_empresa_por_id(id_empresa: int):
    try:
        empresa = empresa_service.buscar_empresa_por_id(id_empresa)
        return empresa
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[EmpresaResponse], status_code=status.HTTP_200_OK)
def listar_empresas():
    empresas = empresa_service.listar_empresas()
    return empresas


@router.delete("/{id_empresa}", status_code=status.HTTP_200_OK, responses={404: {"description": "Empresa não encontrada"}})
def deletar_empresa(id_empresa: int):
    try:
        empresa_service.deletar_empresa(id_empresa)
        return {
            "message": "Empresa removida com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id_empresa}", responses={404: {"description": "Empresa não encontrada"}})
def atualizar_empresa(id_empresa: int, empresa: EmpresaUpdate):
    try:
        empresa_service.atualizar_empresa(id_empresa, empresa)
        return {
            "message": "Empresa atualizada com sucesso"
        }
    
    except ValueError as e:
        if str(e) == "Empresa não encontrada":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.post("/login", response_model=TokenResponse,responses={401: {"description": "Email ou senha inválidos"}}, status_code=status.HTTP_200_OK)
def login_empresa(login: EmpresaLogin):
    try:
        token = empresa_service.login_empresa(login)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
