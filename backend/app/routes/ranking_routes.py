from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)
from app.core.auth_core import (obter_usuario_logado)
from app.models.auth import UsuarioAutenticado
from app.models.ranking import (
    DestaquesResponse,
    RankingFiltros,
    RankingResponse
)
import app.services.ranking_service as ranking_service


router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get(
    "/",
    response_model=RankingResponse,
    status_code=status.HTTP_200_OK
)
def listar_ranking(
    curso: str | None = Query(
        default=None
    ),
    turma: str | None = Query(
        default=None
    ),
    semestre: str | None = Query(
        default=None
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    filtros = RankingFiltros(
        curso=curso,
        turma=turma,
        semestre=semestre
    )

    return ranking_service.gerar_ranking(
        filtros=filtros,
        perfil=usuario.perfil
    )


@router.get(
    "/destaques",
    response_model=DestaquesResponse,
    status_code=status.HTTP_200_OK
)
def listar_destaques(
    curso: str | None = Query(
        default=None
    ),
    turma: str | None = Query(
        default=None
    ),
    semestre: str | None = Query(
        default=None
    ),
    limite: int = Query(
        default=3,
        ge=1,
        le=20
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    filtros = RankingFiltros(
        curso=curso,
        turma=turma,
        semestre=semestre
    )

    return ranking_service.listar_destaques(
        filtros=filtros,
        perfil=usuario.perfil,
        limite=limite
    )