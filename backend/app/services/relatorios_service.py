from fpdf import FPDF

from app.models.relatorios import (
    RelatorioProjetosFiltros,
    RelatorioAcademicoFiltros,
)
import app.repositories.relatorios_repository as relatorios_repository

STATUS_VALIDOS = {"rascunho", "submetido", "em_avaliacao", "aprovado", "reprovado"}


def gerar_relatorio_projetos(filtros: RelatorioProjetosFiltros) -> dict:
    if filtros.status and filtros.status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido. Valores aceitos: {', '.join(STATUS_VALIDOS)}")

    projetos = relatorios_repository.buscar_relatorio_projetos(
        curso=filtros.curso,
        turma=filtros.turma,
        semestre=filtros.semestre,
        status=filtros.status
    )

    return {
        "total_projetos": len(projetos),
        "filtros_aplicados": filtros,
        "projetos": projetos
    }


def gerar_relatorio_academico(filtros: RelatorioAcademicoFiltros) -> dict:
    indicadores = relatorios_repository.buscar_indicadores_academicos(
        curso=filtros.curso,
        turma=filtros.turma,
        semestre=filtros.semestre
    )

    return {
        "filtros_aplicados": filtros,
        "indicadores": indicadores
    }


def exportar_relatorio_projetos_pdf(filtros: RelatorioProjetosFiltros) -> bytes:
    dados = gerar_relatorio_projetos(filtros)
    return _montar_pdf_projetos(dados)


def exportar_relatorio_academico_pdf(filtros: RelatorioAcademicoFiltros) -> bytes:
    dados = gerar_relatorio_academico(filtros)
    return _montar_pdf_academico(dados)


def _montar_pdf_projetos(dados: dict) -> bytes:
    pdf = FPDF(orientation="L")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Relatorio de Projetos - Scripta")
    pdf.ln(12)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Total de projetos: {dados['total_projetos']}")
    pdf.ln(12)

    colunas = ["Titulo", "Curso", "Turma", "Semestre", "Status", "Aluno Resp.", "Prof. Orientador", "Media"]
    larguras = [48, 28, 20, 20, 24, 40, 40, 18]

    pdf.set_font("Helvetica", "B", 9)
    for coluna, largura in zip(colunas, larguras):
        pdf.cell(largura, 8, coluna, border=1)
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 9)
    for projeto in dados["projetos"]:
        media = projeto.get("media_geral")
        media_str = f"{media:.2f}" if media is not None else "-"
        valores = [
            str(projeto["titulo"])[:26],
            str(projeto["curso"]),
            str(projeto["turma"]),
            str(projeto["semestre"]),
            str(projeto["status"]),
            str(projeto["aluno_responsavel"])[:22],
            str(projeto["professor_orientador"])[:22],
            media_str
        ]
        for valor, largura in zip(valores, larguras):
            pdf.cell(largura, 8, valor, border=1)
        pdf.ln(8)

    return bytes(pdf.output())


def _montar_pdf_academico(dados: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Relatorio Academico - Scripta")
    pdf.ln(12)

    colunas = ["Curso", "Turma", "Semestre", "Projetos", "Avaliacoes", "Media Geral"]
    larguras = [40, 25, 25, 25, 30, 30]

    pdf.set_font("Helvetica", "B", 9)
    for coluna, largura in zip(colunas, larguras):
        pdf.cell(largura, 8, coluna, border=1)
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 9)
    for indicador in dados["indicadores"]:
        media = indicador.get("media_geral")
        media_str = f"{media:.2f}" if media is not None else "-"
        valores = [
            str(indicador["curso"]),
            str(indicador["turma"]),
            str(indicador["semestre"]),
            str(indicador["total_projetos"]),
            str(indicador["total_avaliacoes"]),
            media_str
        ]
        for valor, largura in zip(valores, larguras):
            pdf.cell(largura, 8, valor, border=1)
        pdf.ln(8)

    return bytes(pdf.output())
