import app.repositories.certificado_repository as certificado_repository
import app.services.projeto_service as projeto_service


def emitir_certificados_por_projeto(projeto_id: int) -> list[int]:

    projeto = projeto_service.buscar_projeto_por_id(projeto_id)

    if projeto["status"] != "aprovado":
        raise ValueError(
            "Certificados só podem ser emitidos para projetos aprovados"
        )

    integrantes = (
        certificado_repository
        .buscar_integrantes_do_projeto(projeto_id)
    )

    if not integrantes:
        raise ValueError(
            "Nenhum integrante encontrado para este projeto"
        )

    ids_gerados = []

    for integrante in integrantes:

        aluno_id = integrante["aluno_id"]

        if certificado_repository.certificado_ja_existe(
            projeto_id,
            aluno_id
        ):
            continue

        id_certificado = (
            certificado_repository.criar_certificado(
                projeto_id,
                aluno_id
            )
        )

        ids_gerados.append(id_certificado)

    if not ids_gerados:
        raise ValueError(
            "Todos os integrantes já possuem certificado"
        )

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
