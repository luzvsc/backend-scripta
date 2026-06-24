from pydantic import BaseModel


class RankingFiltros(BaseModel):
    curso: str | None = None
    turma: str | None = None
    semestre: str | None = None


class RankingProjetoItem(BaseModel):
    posicao: int
    projeto_id: int
    titulo: str
    curso: str
    turma: str
    semestre: str
    area_conhecimento: str
    aluno_responsavel: str
    professor_orientador: str
    total_avaliacoes: int
    media_geral: float


class RankingResponse(BaseModel):
    total_projetos: int
    filtros_aplicados: RankingFiltros
    ranking: list[RankingProjetoItem]


class DestaquesResponse(BaseModel):
    limite: int
    destaques: list[RankingProjetoItem]