from typing import Optional

from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import Response

from app.models.relatorios import (
    RelatorioProjetosFiltros,
    RelatorioAcademicoFiltros,
    RelatorioProjetosResponse,
    RelatorioAcademicoResponse,
)
import app.services.relatorios_service as relatorio_service

# TODO: adicionar Depends de autenticacao/autorizacao (restringir a coordenacao)
# quando o modulo de auth estiver finalizado. Por enquanto, sem protecao,
# seguindo o mesmo padrao usado nas demais rotas do projeto.

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/projetos", response_model=RelatorioProjetosResponse, status_code=status.HTTP_200_OK)
def relatorio_de_projetos(
    curso: Optional[str] = Query(default=None),
    turma: Optional[str] = Query(default=None),
    semestre: Optional[str] = Query(default=None),
    status_projeto: Optional[str] = Query(default=None, alias="status")
):
    try:
        filtros = RelatorioProjetosFiltros(curso=curso, turma=turma, semestre=semestre, status=status_projeto)
        return relatorio_service.gerar_relatorio_projetos(filtros)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/academico", response_model=RelatorioAcademicoResponse, status_code=status.HTTP_200_OK)
def relatorio_academico(
    curso: Optional[str] = Query(default=None),
    turma: Optional[str] = Query(default=None),
    semestre: Optional[str] = Query(default=None)
):
    filtros = RelatorioAcademicoFiltros(curso=curso, turma=turma, semestre=semestre)
    return relatorio_service.gerar_relatorio_academico(filtros)


@router.get("/projetos/export", responses={400: {"description": "Filtro inválido"}})
def exportar_relatorio_de_projetos(
    curso: Optional[str] = Query(default=None),
    turma: Optional[str] = Query(default=None),
    semestre: Optional[str] = Query(default=None),
    status_projeto: Optional[str] = Query(default=None, alias="status")
):
    try:
        filtros = RelatorioProjetosFiltros(curso=curso, turma=turma, semestre=semestre, status=status_projeto)
        pdf_bytes = relatorio_service.exportar_relatorio_projetos_pdf(filtros)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=relatorio_projetos.pdf"}
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/academico/export")
def exportar_relatorio_academico(
    curso: Optional[str] = Query(default=None),
    turma: Optional[str] = Query(default=None),
    semestre: Optional[str] = Query(default=None)
):
    filtros = RelatorioAcademicoFiltros(curso=curso, turma=turma, semestre=semestre)
    pdf_bytes = relatorio_service.exportar_relatorio_academico_pdf(filtros)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_academico.pdf"}
    )
