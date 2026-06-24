from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from fastapi.responses import Response
from app.core.auth_core import (obter_usuario_logado, exigir_coordenador)
from app.models.auth import UsuarioAutenticado
from app.models.relatorios import (
    RelatorioAcademicoFiltros,
    RelatorioAcademicoResponse,
    RelatorioProjetosFiltros,
    RelatorioProjetosResponse
)
import app.services.relatorios_service as relatorio_service


router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


def _validar_coordenador(usuario: UsuarioAutenticado) -> None:

    exigir_coordenador(usuario)


@router.get(
    "/projetos",
    response_model=RelatorioProjetosResponse,
    status_code=status.HTTP_200_OK
)
def relatorio_de_projetos(
    curso: str | None = Query(default=None),
    turma: str | None = Query(default=None),
    semestre: str | None = Query(default=None),
    status_projeto: str | None = Query(
        default=None,
        alias="status"
    ),
    professor_id: int | None = Query(
        default=None,
        ge=1
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    _validar_coordenador(usuario)

    try:
        filtros = RelatorioProjetosFiltros(
            curso=curso,
            turma=turma,
            semestre=semestre,
            status=status_projeto,
            professor_id=professor_id
        )

        return (
            relatorio_service.gerar_relatorio_projetos(
                filtros
            )
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/academico",
    response_model=RelatorioAcademicoResponse,
    status_code=status.HTTP_200_OK
)
def relatorio_academico(
    curso: str | None = Query(default=None),
    turma: str | None = Query(default=None),
    semestre: str | None = Query(default=None),
    professor_id: int | None = Query(
        default=None,
        ge=1
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    _validar_coordenador(usuario)

    filtros = RelatorioAcademicoFiltros(
        curso=curso,
        turma=turma,
        semestre=semestre,
        professor_id=professor_id
    )

    return relatorio_service.gerar_relatorio_academico(
        filtros
    )


@router.get(
    "/projetos/export",
    response_class=Response,
    status_code=status.HTTP_200_OK
)
def exportar_relatorio_de_projetos(
    curso: str | None = Query(default=None),
    turma: str | None = Query(default=None),
    semestre: str | None = Query(default=None),
    status_projeto: str | None = Query(
        default=None,
        alias="status"
    ),
    professor_id: int | None = Query(
        default=None,
        ge=1
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    _validar_coordenador(usuario)

    try:
        filtros = RelatorioProjetosFiltros(
            curso=curso,
            turma=turma,
            semestre=semestre,
            status=status_projeto,
            professor_id=professor_id
        )

        pdf_bytes = (
            relatorio_service
            .exportar_relatorio_projetos_pdf(
                filtros
            )
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    "attachment; "
                    "filename=relatorio_projetos.pdf"
                )
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/academico/export",
    response_class=Response,
    status_code=status.HTTP_200_OK
)
def exportar_relatorio_academico(
    curso: str | None = Query(default=None),
    turma: str | None = Query(default=None),
    semestre: str | None = Query(default=None),
    professor_id: int | None = Query(
        default=None,
        ge=1
    ),
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    _validar_coordenador(usuario)

    filtros = RelatorioAcademicoFiltros(
        curso=curso,
        turma=turma,
        semestre=semestre,
        professor_id=professor_id
    )

    pdf_bytes = (
        relatorio_service
        .exportar_relatorio_academico_pdf(
            filtros
        )
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; "
                "filename=relatorio_academico.pdf"
            )
        }
    )