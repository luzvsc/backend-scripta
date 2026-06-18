from app.models.arquivo_projeto import ArquivoProjetoCreate
from app.repositories import arquivo_projeto_repository as repository
from app.services import projeto_service
from app.services import versao_projeto_service
from app.models.versao_projeto import VersaoProjetoCreate


def criar_arquivo(arquivo: ArquivoProjetoCreate) -> int:

    projeto = projeto_service.buscar_projeto_por_id(arquivo.projeto_id)

    status = projeto["status"]

    if status not in ["rascunho", "submetido"]:
        raise ValueError(
            "Não é permitido alterar arquivos de projetos em avaliação, aprovados ou reprovados"
        )

    if arquivo.tamanho_mb <= 0:
        raise ValueError(
            "Tamanho do arquivo inválido"
        )

    arquivo_id = repository.criar_arquivo(
        projeto_id=arquivo.projeto_id,
        nome_original=arquivo.nome_original,
        caminho_servidor=arquivo.caminho_servidor,
        tamanho_mb=arquivo.tamanho_mb
    )

    versao_projeto_service.criar_versao(
    VersaoProjetoCreate(
        projeto_id=arquivo.projeto_id,
        quem_alterou_tipo="aluno",
        quem_alterou_id=0
        )
    )

    return arquivo_id


def buscar_arquivo_por_id(id_arquivo: int) -> dict:

    arquivo = repository.buscar_por_id(id_arquivo)

    if not arquivo:
        raise ValueError(
        "Arquivo não encontrado"
    )
    
    return arquivo


def listar_arquivos() -> list[dict]:

    return repository.listar_arquivos()


def listar_por_projeto(projeto_id: int) -> list[dict]:

    projeto_service.buscar_projeto_por_id(projeto_id)

    return repository.listar_por_projeto(projeto_id)


def buscar_ultimo_arquivo(projeto_id: int) -> dict:

    projeto_service.buscar_projeto_por_id(projeto_id)

    arquivo = repository.buscar_ultima_versao(projeto_id)

    if not arquivo:
        raise ValueError(
        "Nenhum arquivo encontrado para este projeto"
        )

    return arquivo


def deletar_arquivo(id_arquivo: int) -> bool:

    arquivo = repository.buscar_por_id(id_arquivo)

    if not arquivo:
        raise ValueError(
        "Arquivo não encontrado"
    )

    projeto = projeto_service.buscar_projeto_por_id(
    arquivo["projeto_id"]
)
    
    if projeto["status"] not in [
    "rascunho",
    "submetido"
]:
        raise ValueError(
        "Arquivos não podem ser removidos após o início da avaliação"
        )
    
    versao_projeto_service.criar_versao(
    VersaoProjetoCreate(
        projeto_id=arquivo["projeto_id"],
        quem_alterou_tipo="aluno",
        quem_alterou_id=0
        )
    )

    return repository.deletar_arquivo(id_arquivo)