from fastapi import APIRouter, status, HTTPException
from typing import List, Optional
from app.models.logs_sistema import LogSistemaResponse
import app.services.logs_sistema_service as logs_sistema_service

router = APIRouter(prefix="/logs", tags=["Log Sistema"])


@router.get(
    "/",
    response_model=List[LogSistemaResponse],
    status_code=status.HTTP_200_OK,
)
def listar_logs(
    entidade: Optional[str] = None,
    coordenador_id: Optional[int] = None,
):

    try:
        if entidade and coordenador_id:
            logs = logs_sistema_service.listar_logs_por_entidade(entidade)
            return [log for log in logs if log["coordenador_id"] == coordenador_id]

        if entidade:
            return logs_sistema_service.listar_logs_por_entidade(entidade)

        if coordenador_id:
            return logs_sistema_service.listar_logs_por_coordenador(coordenador_id)

        return logs_sistema_service.listar_todos_logs()

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{id_log}",
    response_model=LogSistemaResponse,
    responses={404: {"description": "Log não encontrado"}},
)
def buscar_log_por_id(id_log: int):
    
    try:
        return logs_sistema_service.buscar_log_por_id(id_log)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
