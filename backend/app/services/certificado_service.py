from app.models.auth import UsuarioAutenticado
import app.repositories.certificado_repository as certificado_repository
import app.repositories.projeto_repository as projeto_repository
import app.repositories.projeto_integrante_repository as integrante_repository
import app.services.logs_sistema_service as logs_sistema_service


def emitir_certificados_por_projeto(projeto_id: int, coordenador_id: int) -> list[int]:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    if projeto["status"] != "aprovado":
        raise ValueError(
            "Certificados só podem ser emitidos "
            "para projetos aprovados"
        )

    integrantes = (
        integrante_repository
        .listar_integrantes(projeto_id)
    )

    alunos_ids = {
        int(
            projeto[
                "aluno_responsavel_id"
            ]
        )
    }

    alunos_ids.update(
        int(integrante["aluno_id"])
        for integrante in integrantes
        if integrante.get("aluno_id")
        is not None
    )

    ids_gerados: list[int] = []

    for aluno_id in alunos_ids:
        certificado_existente = (
            certificado_repository
            .certificado_ja_existe(
                id_projeto=projeto_id,
                id_aluno=aluno_id
            )
        )

        if certificado_existente:
            continue

        id_certificado = (
            certificado_repository
            .criar_certificado(
                projeto_id=projeto_id,
                aluno_id=aluno_id
            )
        )

        ids_gerados.append(
            id_certificado
        )

        logs_sistema_service.registrar_acao(
            coordenador_id=coordenador_id,
            acao="CREATE",
            entidade="certificados",
            registro_id=id_certificado,
            detalhes=(
                "Certificado emitido para "
                f"o aluno {aluno_id} no "
                f"projeto {projeto_id}"
            )
        )

    return ids_gerados


def buscar_certificado_por_id(id_certificado: int, usuario: UsuarioAutenticado) -> dict:

    certificado = certificado_repository.buscar_por_id(id_certificado)

    if not certificado:
        raise ValueError(
            "Certificado não encontrado"
        )

    if usuario.perfil == "coordenador":
        return certificado

    if (
        usuario.perfil == "aluno"
        and certificado["aluno_id"] == usuario.id
    ):
        return certificado

    raise ValueError(
        "Você não tem permissão para visualizar "
        "este certificado"
    )


def listar_meus_certificados(aluno_id: int) -> list[dict]:

    return certificado_repository.buscar_por_aluno(aluno_id)


def listar_certificados_do_aluno(id_aluno: int) -> list[dict]:

    return certificado_repository.buscar_por_aluno(id_aluno)


def listar_certificados_do_projeto(id_projeto: int) -> list[dict]:

    projeto = projeto_repository.buscar_por_id(id_projeto)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    return certificado_repository.buscar_por_projeto(id_projeto)


def listar_todos_certificados() -> list[dict]:

    return certificado_repository.listar_certificados()
