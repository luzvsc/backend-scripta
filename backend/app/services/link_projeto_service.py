from app.models.auth import UsuarioAutenticado
from app.models.link_projeto import (
    LinkProjetoCreate,
    LinkProjetoUpdate
)
from app.models.versao_projeto import (
    VersaoProjetoCreate
)
import app.repositories.link_projeto_repository as link_repository
import app.repositories.projeto_integrante_repository as integrante_repository
import app.repositories.projeto_repository as projeto_repository
from app.services import versao_projeto_service


STATUS_EDITAVEIS = (
    "rascunho",
    "submetido"
)


def _buscar_projeto(projeto_id: int) -> dict:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    return projeto


def _buscar_link_do_projeto(projeto_id: int, id_link: int) -> dict:

    link = link_repository.buscar_por_id(id_link)

    if (
        not link
        or link["projeto_id"] != projeto_id
    ):
        raise ValueError(
            "Link não encontrado neste projeto"
        )

    return link


def _validar_integrante(projeto: dict, aluno_id: int) -> None:

    responsavel = (
        projeto["aluno_responsavel_id"]
        == aluno_id
    )

    integrante = (
        integrante_repository.buscar_por_projeto_e_aluno(
            projeto_id=projeto["id"],
            aluno_id=aluno_id
        )
    )

    if not responsavel and not integrante:
        raise ValueError(
            "Você não faz parte deste projeto"
        )


def _validar_status_edicao(projeto: dict) -> None:

    if projeto["status"] not in STATUS_EDITAVEIS:
        raise ValueError(
            "Os links não podem ser alterados "
            "após o início da avaliação"
        )


def _registrar_versao_se_submetido(projeto: dict, aluno_id: int) -> None:

    if projeto["status"] == "submetido":
        versao_projeto_service.criar_versao(
            VersaoProjetoCreate(
                projeto_id=projeto["id"],
                quem_alterou_tipo="aluno",
                quem_alterou_id=aluno_id
            )
        )


def criar_link(
    projeto_id: int,
    link: LinkProjetoCreate,
    aluno_id: int
) -> int:
    
    projeto = _buscar_projeto(projeto_id)

    _validar_integrante(
        projeto,
        aluno_id
    )

    _validar_status_edicao(projeto)

    id_link = link_repository.criar_link(
        projeto_id=projeto_id,
        url=link.url,
        descricao=link.descricao
    )

    _registrar_versao_se_submetido(
        projeto,
        aluno_id
    )

    return id_link


def listar_links(projeto_id: int, usuario: UsuarioAutenticado) -> list[dict]:

    _buscar_projeto(projeto_id)

    permitido = (
        projeto_repository.pode_visualizar_projeto(
            projeto_id=projeto_id,
            usuario_id=usuario.id,
            perfil=usuario.perfil
        )
    )

    if not permitido:
        raise ValueError(
            "Você não tem permissão para visualizar "
            "os links deste projeto"
        )

    return link_repository.listar_por_projeto(
        projeto_id
    )


def atualizar_link(
    projeto_id: int,
    id_link: int,
    link_update: LinkProjetoUpdate,
    aluno_id: int
) -> bool:
    
    projeto = _buscar_projeto(projeto_id)

    _validar_integrante(
        projeto,
        aluno_id
    )

    _validar_status_edicao(projeto)

    _buscar_link_do_projeto(
        projeto_id,
        id_link
    )

    dados = link_update.model_dump(exclude_unset=True)

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    resultado = link_repository.atualizar_link(
        id_link=id_link,
        dados=dados
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar o link"
        )

    _registrar_versao_se_submetido(
        projeto,
        aluno_id
    )

    return True


def deletar_link(
    projeto_id: int,
    id_link: int,
    aluno_id: int
) -> bool:
    
    projeto = _buscar_projeto(projeto_id)

    _validar_integrante(
        projeto,
        aluno_id
    )

    _validar_status_edicao(projeto)

    _buscar_link_do_projeto(
        projeto_id,
        id_link
    )

    resultado = link_repository.deletar_link(id_link)

    if not resultado:
        raise ValueError(
            "Não foi possível remover o link"
        )

    _registrar_versao_se_submetido(
        projeto,
        aluno_id
    )

    return True