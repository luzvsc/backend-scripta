from typing import Optional
import app.repositories.log_sistema_repository as log_sistema_repository

ACOES_VALIDAS = {"CREATE", "UPDATE", "DELETE"}

ENTIDADES_VALIDAS = {
    "alunos", "professores", "coordenadores",
    "empresas", "projetos", "certificados",
    "arquivos_projeto", "avaliacoes"
}


def registrar_acao(
    coordenador_id: int,
    acao: str,
    entidade: str,
    registro_id: int,
    detalhes: Optional[str] = None
) -> int:
    """
    Registra automaticamente uma ação da coordenação no log do sistema.

    Chamado internamente por outros services sempre que a coordenação
    executa uma ação de gestão — nunca exposto diretamente ao usuário
    como endpoint de criação.

    Parâmetros:
      - coordenador_id : quem realizou a ação (fk para coordenadores.id)
      - acao           : 'CREATE', 'UPDATE' ou 'DELETE' (ENUM do banco)
      - entidade       : tabela afetada (ex: 'alunos', 'projetos')
      - registro_id    : id do registro afetado na tabela
      - detalhes       : texto livre descrevendo o que foi alterado

    Regra RN06: toda alteração deve registrar usuário responsável,
    data/hora e o que foi realizado.
    RNF22/RNF23: logs armazenados por no mínimo 6 meses.
    """
    if acao not in ACOES_VALIDAS:
        raise ValueError(
            f"Ação inválida. Valores aceitos: {', '.join(ACOES_VALIDAS)}"
        )

    if entidade not in ENTIDADES_VALIDAS:
        raise ValueError(
            f"Entidade inválida. Valores aceitos: {', '.join(ENTIDADES_VALIDAS)}"
        )

    id_log = log_sistema_repository.registrar_log(
        coordenador_id=coordenador_id,
        acao=acao,
        entidade=entidade,
        registro_id=registro_id,
        detalhes=detalhes
    )
    return id_log


def listar_todos_logs() -> list[dict]:
    """
    Lista todos os logs — uso exclusivo da coordenação.
    """
    return log_sistema_repository.listar_logs()


def listar_logs_por_coordenador(coordenador_id: int) -> list[dict]:
    """
    Filtra logs de um coordenador específico.
    """
    return log_sistema_repository.listar_logs_por_coordenador(coordenador_id)


def listar_logs_por_entidade(entidade: str) -> list[dict]:
    """
    Filtra logs por entidade (ex: 'alunos', 'projetos').
    """
    if entidade not in ENTIDADES_VALIDAS:
        raise ValueError(
            f"Entidade inválida. Valores aceitos: {', '.join(ENTIDADES_VALIDAS)}"
        )
    return log_sistema_repository.listar_logs_por_entidade(entidade)


def buscar_log_por_id(id_log: int) -> dict:
    log = log_sistema_repository.buscar_log_por_id(id_log)
    if not log:
        raise ValueError("Log não encontrado")
    return log