import app.repositories.certificado_repository as certificado_repository


def emitir_certificados_por_projeto(id_projeto: int) -> list[int]:
    """
    Emite certificados individuais para todos os integrantes de um projeto aprovado.
    Chamado pela coordenação após validação do projeto.
    Regras:
      - RN01: O projeto deve estar aprovado (validado externamente antes de chamar).
      - RN02: Cada integrante recebe um certificado individual.
      - RN04: Um certificado só existe vinculado a um projeto aprovado.
    """
    integrantes = certificado_repository.buscar_integrantes_do_projeto(id_projeto)
    if not integrantes:
        raise ValueError("Nenhum integrante encontrado para este projeto")

    ids_gerados = []
    for integrante in integrantes:
        id_aluno = integrante["id_aluno"]

        ja_existe = certificado_repository.certificado_ja_existe(id_projeto, id_aluno)
        if ja_existe:
            continue

        id_certificado = certificado_repository.criar_certificado(
            id_projeto=id_projeto,
            id_aluno=id_aluno
        )
        ids_gerados.append(id_certificado)

    if not ids_gerados:
        raise ValueError("Todos os integrantes já possuem certificado para este projeto")

    return ids_gerados


def buscar_certificado_por_id(id_certificado: int) -> dict:
    certificado = certificado_repository.buscar_por_id(id_certificado)
    if not certificado:
        raise ValueError("Certificado não encontrado")
    return certificado


def listar_certificados_do_aluno(id_aluno: int) -> list[dict]:
    """
    Permite ao aluno consultar e baixar seus próprios certificados (RF12).
    """
    return certificado_repository.buscar_por_aluno(id_aluno)


def listar_certificados_do_projeto(id_projeto: int) -> list[dict]:
    """
    Permite à coordenação consultar certificados emitidos por projeto (RF-ADM-11).
    """
    return certificado_repository.buscar_por_projeto(id_projeto)


def listar_todos_certificados() -> list[dict]:
    """
    Lista todos os certificados da plataforma — uso exclusivo da coordenação (RF-ADM-11).
    """
    return certificado_repository.listar_certificados()
