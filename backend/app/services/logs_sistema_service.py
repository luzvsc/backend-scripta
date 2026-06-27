from typing import Optional
import app.repositories.logs_sistema_repository as logs_sistema_repository

ACOES_VALIDAS = {"CREATE", "UPDATE", "DELETE"}

ENTIDADES_VALIDAS = {
    "alunos",
    "professores",
    "coordenadores",
    "empresas",
    "projetos",
    "projeto_integrantes",
    "certificados",
    "arquivos_projeto",
    "avaliacoes"
}


def registrar_acao(
    coordenador_id: int,
    acao: str,
    entidade: str,
    registro_id: int,
    detalhes: Optional[str] = None
) -> int:

    if acao not in ACOES_VALIDAS:
        raise ValueError(
            f"Ação inválida. Valores aceitos: {', '.join(ACOES_VALIDAS)}"
        )

    if entidade not in ENTIDADES_VALIDAS:
        raise ValueError(
            f"Entidade inválida. Valores aceitos: {', '.join(ENTIDADES_VALIDAS)}"
        )

    id_log = logs_sistema_repository.registrar_log(
        coordenador_id=coordenador_id,
        acao=acao,
        entidade=entidade,
        registro_id=registro_id,
        detalhes=detalhes
    )
    return id_log


def listar_todos_logs() -> list[dict]:
    return logs_sistema_repository.listar_logs()


def listar_logs_por_coordenador(coordenador_id: int) -> list[dict]:
    return logs_sistema_repository.listar_logs_por_coordenador(coordenador_id)


def listar_logs_por_entidade(entidade: str) -> list[dict]:
    if entidade not in ENTIDADES_VALIDAS:
        raise ValueError(
            f"Entidade inválida. Valores aceitos: {', '.join(ENTIDADES_VALIDAS)}"
        )
    return logs_sistema_repository.listar_logs_por_entidade(entidade)


def buscar_log_por_id(id_log: int) -> dict:
    log = logs_sistema_repository.buscar_log_por_id(id_log)
    if not log:
        raise ValueError("Log não encontrado")
    return log
