from app.models.ranking import RankingFiltros
import app.repositories.ranking_repository as ranking_repository


def gerar_ranking(filtros: RankingFiltros, perfil: str) -> dict:

    somente_publicos = (perfil == "empresa")

    projetos = ranking_repository.buscar_ranking(
        curso=filtros.curso,
        turma=filtros.turma,
        semestre=filtros.semestre,
        somente_publicos=somente_publicos
    )

    ranking: list[dict] = []

    for posicao, projeto in enumerate(
        projetos,
        start=1
    ):
        item = dict(projeto)

        item["posicao"] = posicao
        item["total_avaliacoes"] = int(
            item["total_avaliacoes"]
        )
        item["media_geral"] = float(
            item["media_geral"]
        )

        ranking.append(item)

    return {
        "total_projetos": len(ranking),
        "filtros_aplicados": filtros,
        "ranking": ranking
    }


def listar_destaques(
    filtros: RankingFiltros,
    perfil: str,
    limite: int
) -> dict:
    
    dados_ranking = gerar_ranking(
        filtros=filtros,
        perfil=perfil
    )

    destaques = dados_ranking["ranking"][
        :limite
    ]

    return {
        "limite": limite,
        "destaques": destaques
    }