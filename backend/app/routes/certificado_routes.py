from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.certificado import (
    CertificadoResponse,
    CertificadoEmitirRequest,
    CertificadoCreateResponse,
)
import app.services.certificado_service as certificado_service

router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.post(
    "/emitir",
    response_model=CertificadoCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Projeto não encontrado ou sem integrantes"},
        409: {"description": "Certificados já emitidos para este projeto"},
    },
)
def emitir_certificados(payload: CertificadoEmitirRequest):
    """
    Emite certificados individuais para todos os integrantes de um projeto aprovado.
    Uso exclusivo da coordenação (RF-ADM-10).
    O projeto deve estar com status 'Aprovado' antes de chamar este endpoint.
    """
    try:
        ids = certificado_service.emitir_certificados_por_projeto(payload.id_projeto)
        return {
            "message": "Certificados emitidos com sucesso",
            "ids_certificados": ids,
        }
    except ValueError as e:
        msg = str(e)
        if "não encontrado" in msg or "Nenhum integrante" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)


@router.get(
    "/",
    response_model=List[CertificadoResponse],
    status_code=status.HTTP_200_OK,
)
def listar_todos_certificados():
    """
    Lista todos os certificados da plataforma.
    Uso exclusivo da coordenação (RF-ADM-11).
    """
    return certificado_service.listar_todos_certificados()


@router.get(
    "/{id_certificado}",
    response_model=CertificadoResponse,
    responses={404: {"description": "Certificado não encontrado"}},
)
def buscar_certificado_por_id(id_certificado: int):
    try:
        return certificado_service.buscar_certificado_por_id(id_certificado)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/aluno/{id_aluno}",
    response_model=List[CertificadoResponse],
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Aluno não encontrado"}},
)
def listar_certificados_do_aluno(id_aluno: int):
    """
    Lista todos os certificados de um aluno específico.
    Usado pelo próprio aluno (RF12) e pela coordenação (RF-ADM-11).
    """
    return certificado_service.listar_certificados_do_aluno(id_aluno)


@router.get(
    "/projeto/{id_projeto}",
    response_model=List[CertificadoResponse],
    status_code=status.HTTP_200_OK,
)
def listar_certificados_do_projeto(id_projeto: int):
    """
    Lista todos os certificados emitidos para um projeto específico.
    Uso da coordenação (RF-ADM-11).
    """
    return certificado_service.listar_certificados_do_projeto(id_projeto)
