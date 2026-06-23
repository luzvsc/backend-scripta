from pydantic import BaseModel
from typing import Optional, List


class RelatorioProjetosFiltros(BaseModel):
    curso: Optional[str] = None
    turma: Optional[str] = None
    semestre: Optional[str] = None
    status: Optional[str] = None


class RelatorioAcademicoFiltros(BaseModel):
    curso: Optional[str] = None
    turma: Optional[str] = None
    semestre: Optional[str] = None


class ProjetoRelatorioItem(BaseModel):
    id: int
    titulo: str
    curso: str
    turma: str
    semestre: str
    status: str
    area_conhecimento: str
    aluno_responsavel: str
    professor_orientador: str
    total_avaliacoes: int
    media_geral: Optional[float] = None


class RelatorioProjetosResponse(BaseModel):
    total_projetos: int
    filtros_aplicados: RelatorioProjetosFiltros
    projetos: List[ProjetoRelatorioItem]


class IndicadorAcademico(BaseModel):
    curso: str
    turma: str
    semestre: str
    total_projetos: int
    total_avaliacoes: int
    media_inovacao: Optional[float] = None
    media_tecnica: Optional[float] = None
    media_aplicabilidade: Optional[float] = None
    media_clareza: Optional[float] = None
    media_geral: Optional[float] = None


class RelatorioAcademicoResponse(BaseModel):
    filtros_aplicados: RelatorioAcademicoFiltros
    indicadores: List[IndicadorAcademico]
