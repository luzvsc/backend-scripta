from fastapi import APIRouter, status, HTTPException
from typing import List, Optional
from app.models.log_sistema import LogSistemaResponse
import app.services.log_sistema_service as log_sistema_service

router = APIRouter(prefix="/logs", tags=["Log Sistema"])


@router.get(
    "/",
    response_model=List[LogSistemaResponse],
    status_code=status.HTTP_200_OK,
)
def listar_logs(
    entidade: Optional[str] = None,
    id_coordenador: Optional[int] = None,
):
    """
    Lista logs do sistema com filtros opcionais.
    Uso exclusivo da coordenação (RNF22 / RNF23).

    Parâmetros de query (opcionais):
      - entidade       : filtra por domínio afetado (ex: 'usuarios', 'projetos')
      - id_coordenador : filtra por coordenador específico
    """
    try:
        if entidade and id_coordenador:
            logs = log_sistema_service.listar_logs_por_entidade(entidade)
            return [l for l in logs if l["id_coordenador"] == id_coordenador]

        if entidade:
            return log_sistema_service.listar_logs_por_entidade(entidade)

        if id_coordenador:
            return log_sistema_service.listar_logs_por_coordenador(id_coordenador)

        return log_sistema_service.listar_todos_logs()

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{id_log}",
    response_model=LogSistemaResponse,
    responses={404: {"description": "Log não encontrado"}},
)
def buscar_log_por_id(id_log: int):
    """
    Busca um registro de log específico pelo ID.
    Uso exclusivo da coordenação.
    """
    try:
        return log_sistema_service.buscar_log_por_id(id_log)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
