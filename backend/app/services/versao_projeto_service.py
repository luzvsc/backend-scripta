from app.models.versao_projeto import VersaoProjetoCreate
from app.repositories import versao_projeto_repository as repository
from app.services import projeto_service


def criar_versao(versao: VersaoProjetoCreate) -> int:

    projeto = projeto_service.buscar_projeto_por_id(versao.projeto_id)

    versao_id = repository.criar_versao(
        projeto_id=versao.projeto_id,
        titulo_na_epoca=projeto["titulo"],
        descricao_na_epoca=projeto["descricao"],
        quem_alterou_tipo=versao.quem_alterou_tipo,
        quem_alterou_id=versao.quem_alterou_id
    )

    return versao_id


def buscar_versao_por_id(id_versao: int) -> dict:

    versao = repository.buscar_por_id(id_versao)

    if not versao:
        raise ValueError(
            "Versão não encontrada"
        )

    return versao


def listar_versoes() -> list[dict]:

    return repository.listar_versoes()


def listar_por_projeto(projeto_id: int) -> list[dict]:

    projeto_service.buscar_projeto_por_id(projeto_id)

    return repository.listar_por_projeto(projeto_id)