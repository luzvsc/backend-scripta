from app.models.auth import UsuarioAutenticado
from app.models.projeto_integrante import (ProjetoIntegranteCreate)
import app.repositories.aluno_repository as aluno_repository
import app.repositories.projeto_repository as projeto_repository
import app.repositories.projeto_integrante_repository as integrante_repository
import app.services.logs_sistema_service as logs_sistema_service


def _buscar_projeto(projeto_id: int) -> dict:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    return projeto


def _validar_projeto_em_rascunho(projeto: dict) -> None:

    if projeto["status"] != "rascunho":
        raise ValueError(
            "Os integrantes só podem ser alterados "
            "enquanto o projeto estiver em rascunho"
        )


def _validar_responsavel_para_adicao(projeto: dict, usuario: UsuarioAutenticado) -> None:

    if usuario.perfil == "coordenador":
        return

    if (
        usuario.perfil == "aluno"
        and projeto["aluno_responsavel_id"]
        == usuario.id
    ):
        return

    raise ValueError(
        "Apenas o aluno responsável ou a "
        "coordenação podem adicionar integrantes"
    )


def _validar_permissao_para_remocao(projeto: dict, usuario: UsuarioAutenticado) -> None:

    if usuario.perfil == "coordenador":
        return

    if (
        usuario.perfil == "professor"
        and projeto["professor_orientador_id"] == usuario.id
    ):
        return

    raise ValueError(
        "Apenas o professor orientador ou a "
        "coordenação podem remover integrantes"
    )


def _validar_status_para_alterar_integrantes(projeto: dict, usuario: UsuarioAutenticado) -> None:

    if usuario.perfil == "coordenador":
        return

    _validar_projeto_em_rascunho(projeto)


def adicionar_integrante(projeto_id: int, integrante: ProjetoIntegranteCreate, usuario: UsuarioAutenticado) -> bool:

    projeto = _buscar_projeto(projeto_id)

    _validar_responsavel_para_adicao(
        projeto,
        usuario
    )

    _validar_status_para_alterar_integrantes(
    projeto,
    usuario
    )

    aluno = aluno_repository.buscar_por_id(integrante.aluno_id)

    if not aluno:
        raise ValueError(
            "Aluno não encontrado"
        )

    if (
        integrante.aluno_id
        == projeto["aluno_responsavel_id"]
    ):
        raise ValueError(
            "O aluno responsável já faz parte do projeto"
        )

    integrante_existente = (
        integrante_repository.buscar_por_projeto_e_aluno(
            projeto_id=projeto_id,
            aluno_id=integrante.aluno_id
        )
    )

    if integrante_existente:
        raise ValueError(
            "O aluno já faz parte deste projeto"
        )

    sucesso = integrante_repository.adicionar_integrante(
        projeto_id=projeto_id,
        aluno_id=integrante.aluno_id
    )

    if not sucesso:
        raise ValueError(
            "Não foi possível adicionar o integrante"
        )

    if usuario.perfil == "coordenador":

        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="CREATE",
            entidade="projeto_integrantes",
            registro_id=projeto_id,
            detalhes=(
                f"Aluno {integrante.aluno_id} "
                f"adicionado ao projeto {projeto_id}"
            )
        )

    return True


def listar_integrantes(projeto_id: int, usuario: UsuarioAutenticado) -> list[dict]:

    projeto = _buscar_projeto(projeto_id)

    if usuario.perfil == "coordenador":
        return integrante_repository.listar_integrantes(projeto_id)

    if usuario.perfil == "professor":
        professor_orientador = (
            projeto["professor_orientador_id"]
            == usuario.id
        )

        if professor_orientador:
            return integrante_repository.listar_integrantes(projeto_id)

        permitido = (
            projeto_repository.pode_visualizar_projeto(
                projeto_id,
                usuario.id,
                usuario.perfil
            )
        )

        if permitido:
            return integrante_repository.listar_integrantes(projeto_id)

    if usuario.perfil == "aluno":
        responsavel = (
            projeto["aluno_responsavel_id"]
            == usuario.id
        )

        integrante = (
            integrante_repository.buscar_por_projeto_e_aluno(
                projeto_id=projeto_id,
                aluno_id=usuario.id
            )
        )

        if responsavel or integrante:
            return integrante_repository.listar_integrantes(projeto_id)

    raise ValueError(
        "Você não tem permissão para visualizar "
        "os integrantes deste projeto"
    )


def remover_integrante(projeto_id: int, aluno_id: int, usuario: UsuarioAutenticado) -> bool:

    projeto = _buscar_projeto(projeto_id)

    _validar_permissao_para_remocao(
        projeto,
        usuario
    )

    _validar_status_para_alterar_integrantes(
    projeto,
    usuario
    )

    if projeto["aluno_responsavel_id"] == aluno_id:
        raise ValueError(
            "O aluno responsável não pode ser removido"
        )

    integrante = (
        integrante_repository.buscar_por_projeto_e_aluno(
            projeto_id=projeto_id,
            aluno_id=aluno_id
        )
    )

    if not integrante:
        raise ValueError(
            "O aluno não faz parte deste projeto"
        )

    sucesso = (
    integrante_repository.remover_integrante(
        projeto_id=projeto_id,
        aluno_id=aluno_id
    )
)

    if not sucesso:
        raise ValueError(
            "Não foi possível remover o integrante"
        )

    if usuario.perfil == "coordenador":

        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="DELETE",
            entidade="projeto_integrantes",
            registro_id=projeto_id,
            detalhes=(
                f"Aluno {aluno_id} removido "
                f"do projeto {projeto_id}"
            )
        )

    return True
