from app.models.auth import UsuarioAutenticado
from app.models.versao_projeto import VersaoProjetoCreate
import app.repositories.projeto_integrante_repository as integrante_repository
import app.repositories.projeto_repository as projeto_repository
import app.repositories.versao_projeto_repository as repository


def _buscar_projeto(projeto_id: int) -> dict:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    return projeto


def _validar_acesso_ao_projeto(projeto: dict, usuario: UsuarioAutenticado) -> None:
    
    if usuario.perfil == "coordenador":
        return

    if usuario.perfil == "empresa":
        raise ValueError(
            "Você não tem permissão para visualizar "
            "o histórico deste projeto"
        )

    if usuario.perfil == "professor":
        if (
            projeto["professor_orientador_id"]
            == usuario.id
        ):
            return

        raise ValueError(
            "Você não tem permissão para visualizar "
            "o histórico deste projeto"
        )

    if usuario.perfil == "aluno":
        responsavel = (
            projeto["aluno_responsavel_id"]
            == usuario.id
        )

        integrante = (
            integrante_repository.buscar_por_projeto_e_aluno(
                projeto_id=projeto["id"],
                aluno_id=usuario.id
            )
        )

        if responsavel or integrante:
            return

    raise ValueError(
        "Você não tem permissão para visualizar "
        "o histórico deste projeto"
    )


def criar_versao(versao: VersaoProjetoCreate) -> int:
    
    projeto = _buscar_projeto(versao.projeto_id)

    return repository.criar_versao(
        projeto_id=versao.projeto_id,
        titulo_na_epoca=projeto["titulo"],
        descricao_na_epoca=projeto["descricao"],
        quem_alterou_tipo=versao.quem_alterou_tipo,
        quem_alterou_id=versao.quem_alterou_id
    )


def buscar_versao_por_id(id_versao: int, usuario: UsuarioAutenticado) -> dict:

    versao = repository.buscar_por_id(id_versao)

    if not versao:
        raise ValueError(
            "Versão não encontrada"
        )

    projeto = _buscar_projeto(
        versao["projeto_id"]
    )

    _validar_acesso_ao_projeto(
        projeto=projeto,
        usuario=usuario
    )

    return versao


def listar_versoes(usuario: UsuarioAutenticado) -> list[dict]:

    if usuario.perfil != "coordenador":
        raise ValueError(
            "Apenas a coordenação pode listar "
            "todas as versões"
        )

    return repository.listar_versoes()


def listar_por_projeto(projeto_id: int, usuario: UsuarioAutenticado) -> list[dict]:
    
    projeto = _buscar_projeto(projeto_id)

    _validar_acesso_ao_projeto(
        projeto=projeto,
        usuario=usuario
    )

    return repository.listar_por_projeto(projeto_id)