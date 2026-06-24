from typing import Any
from fpdf import FPDF
from app.models.relatorios import (RelatorioAcademicoFiltros, RelatorioProjetosFiltros)
import app.repositories.relatorios_repository as relatorios_repository


STATUS_VALIDOS = (
    "rascunho",
    "submetido",
    "em_avaliacao",
    "aprovado",
    "reprovado"
)


def gerar_relatorio_projetos(filtros: RelatorioProjetosFiltros) -> dict:

    if (
        filtros.status
        and filtros.status not in STATUS_VALIDOS
    ):
        valores = ", ".join(STATUS_VALIDOS)

        raise ValueError(
            f"Status inválido. Valores aceitos: {valores}"
        )

    projetos = (
        relatorios_repository.buscar_relatorio_projetos(
            curso=filtros.curso,
            turma=filtros.turma,
            semestre=filtros.semestre,
            status=filtros.status,
            professor_id=filtros.professor_id
        )
    )

    return {
        "total_projetos": len(projetos),
        "filtros_aplicados": filtros,
        "projetos": projetos
    }


def gerar_relatorio_academico(filtros: RelatorioAcademicoFiltros) -> dict:

    indicadores = (
        relatorios_repository
        .buscar_indicadores_academicos(
            curso=filtros.curso,
            turma=filtros.turma,
            semestre=filtros.semestre,
            professor_id=filtros.professor_id
        )
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


def _texto_pdf(valor: Any) -> str:

    texto = "" if valor is None else str(valor)

    return texto.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")


def _resultado_pdf_bytes(pdf: FPDF) -> bytes:

    resultado = pdf.output()

    if isinstance(resultado, bytes):
        return resultado

    return bytes(resultado)


def _montar_pdf_projetos(dados: dict) -> bytes:

    pdf = FPDF(orientation="L")
    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )
    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        14
    )
    pdf.cell(
        0,
        10,
        "Relatorio de Projetos - Scripta"
    )
    pdf.ln(12)

    pdf.set_font(
        "Helvetica",
        "",
        10
    )
    pdf.cell(
        0,
        8,
        (
            "Total de projetos: "
            f"{dados['total_projetos']}"
        )
    )
    pdf.ln(12)

    colunas = [
        "Titulo",
        "Curso",
        "Turma",
        "Semestre",
        "Status",
        "Aluno Resp.",
        "Prof. Orientador",
        "Media"
    ]

    larguras = [
        48,
        28,
        20,
        20,
        24,
        40,
        40,
        18
    ]

    pdf.set_font(
        "Helvetica",
        "B",
        9
    )

    for coluna, largura in zip(
        colunas,
        larguras
    ):
        pdf.cell(
            largura,
            8,
            coluna,
            border=1
        )

    pdf.ln(8)

    pdf.set_font(
        "Helvetica",
        "",
        9
    )

    for projeto in dados["projetos"]:
        media = projeto.get("media_geral")

        media_str = (
            f"{float(media):.2f}"
            if media is not None
            else "-"
        )

        valores = [
            _texto_pdf(projeto["titulo"])[:26],
            _texto_pdf(projeto["curso"])[:15],
            _texto_pdf(projeto["turma"])[:10],
            _texto_pdf(projeto["semestre"])[:10],
            _texto_pdf(projeto["status"])[:15],
            _texto_pdf(
                projeto["aluno_responsavel"]
            )[:22],
            _texto_pdf(
                projeto["professor_orientador"]
            )[:22],
            media_str
        ]

        for valor, largura in zip(
            valores,
            larguras
        ):
            pdf.cell(
                largura,
                8,
                valor,
                border=1
            )

        pdf.ln(8)

    return _resultado_pdf_bytes(pdf)


def _montar_pdf_academico(dados: dict) -> bytes:
    
    pdf = FPDF()
    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )
    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        14
    )
    pdf.cell(
        0,
        10,
        "Relatorio Academico - Scripta"
    )
    pdf.ln(12)

    colunas = [
        "Curso",
        "Turma",
        "Semestre",
        "Projetos",
        "Avaliacoes",
        "Media Geral"
    ]

    larguras = [
        40,
        25,
        25,
        25,
        30,
        30
    ]

    pdf.set_font(
        "Helvetica",
        "B",
        9
    )

    for coluna, largura in zip(
        colunas,
        larguras
    ):
        pdf.cell(
            largura,
            8,
            coluna,
            border=1
        )

    pdf.ln(8)

    pdf.set_font(
        "Helvetica",
        "",
        9
    )

    for indicador in dados["indicadores"]:
        media = indicador.get("media_geral")

        media_str = (
            f"{float(media):.2f}"
            if media is not None
            else "-"
        )

        valores = [
            _texto_pdf(indicador["curso"])[:20],
            _texto_pdf(indicador["turma"])[:12],
            _texto_pdf(indicador["semestre"])[:12],
            str(indicador["total_projetos"]),
            str(indicador["total_avaliacoes"]),
            media_str
        ]

        for valor, largura in zip(
            valores,
            larguras
        ):
            pdf.cell(
                largura,
                8,
                valor,
                border=1
            )

        pdf.ln(8)

    return _resultado_pdf_bytes(pdf)