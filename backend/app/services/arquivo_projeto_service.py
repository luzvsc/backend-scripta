from uuid import uuid4
from app.models.arquivo_projeto import (
    ArquivoProjetoCreate,
    ArquivoProjetoMetadataCreate,
    ArquivoProjetoUpdate
)
from app.models.auth import UsuarioAutenticado
from app.models.versao_projeto import (VersaoProjetoCreate)
from app.repositories import (arquivo_projeto_repository as repository)
import app.repositories.projeto_repository as projeto_repository
import app.repositories.projeto_integrante_repository as integrante_repository
from app.services import versao_projeto_service
import app.services.logs_sistema_service as logs_sistema_service


LIMITE_ARQUIVO_MB = 50


def criar_arquivo(arquivo: ArquivoProjetoCreate, aluno_id: int) -> int:

    projeto = projeto_repository.buscar_por_id(arquivo.projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    integrante = (
        integrante_repository.buscar_por_projeto_e_aluno(
            arquivo.projeto_id,
            aluno_id
        )
    )

    if not integrante:
        raise ValueError(
            "Você não faz parte deste projeto"
        )

    status_projeto = projeto["status"]

    if status_projeto not in (
        "rascunho",
        "submetido"
    ):
        raise ValueError(
            "Não é permitido adicionar arquivos "
            "a projetos em avaliação, aprovados "
            "ou reprovados"
        )

    if arquivo.tamanho_mb <= 0:
        raise ValueError(
            "Tamanho do arquivo inválido"
        )

    if arquivo.tamanho_mb > LIMITE_ARQUIVO_MB:
        raise ValueError(
            "O arquivo não pode ultrapassar 50 MB"
        )

    arquivo_id = repository.criar_arquivo(
        projeto_id=arquivo.projeto_id,
        nome_original=arquivo.nome_original,
        caminho_servidor=arquivo.caminho_servidor,
        tamanho_mb=arquivo.tamanho_mb
    )

    if status_projeto == "submetido":
        versao_projeto_service.criar_versao(
            VersaoProjetoCreate(
                projeto_id=arquivo.projeto_id,
                quem_alterou_tipo="aluno",
                quem_alterou_id=aluno_id
            )
        )

    return arquivo_id


def buscar_arquivo_por_id(id_arquivo: int, usuario: UsuarioAutenticado) -> dict:

    arquivo = repository.buscar_por_id(id_arquivo)

    if not arquivo:
        raise ValueError(
            "Arquivo não encontrado"
        )

    permitido = (
        projeto_repository.pode_visualizar_projeto(
            arquivo["projeto_id"],
            usuario.id,
            usuario.perfil
        )
    )

    if not permitido:
        raise ValueError(
            "Você não tem permissão para "
            "visualizar este arquivo"
        )

    return arquivo


def listar_arquivos() -> list[dict]:

    return repository.listar_arquivos()


def listar_por_projeto(projeto_id: int, usuario: UsuarioAutenticado) -> list[dict]:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    permitido = (
        projeto_repository.pode_visualizar_projeto(
            projeto_id,
            usuario.id,
            usuario.perfil
        )
    )

    if not permitido:
        raise ValueError(
            "Você não tem permissão para "
            "visualizar os arquivos deste projeto"
        )

    return repository.listar_por_projeto(projeto_id)


def buscar_ultimo_arquivo(projeto_id: int, usuario: UsuarioAutenticado) -> dict:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    permitido = (
        projeto_repository.pode_visualizar_projeto(
            projeto_id,
            usuario.id,
            usuario.perfil
        )
    )

    if not permitido:
        raise ValueError(
            "Você não tem permissão para "
            "visualizar os arquivos deste projeto"
        )

    arquivo = repository.buscar_ultima_versao(projeto_id)

    if not arquivo:
        raise ValueError(
            "Nenhum arquivo encontrado para este projeto"
        )

    return arquivo


def criar_metadado_arquivo(arquivo: ArquivoProjetoMetadataCreate, coordenador_id: int) -> int:

    projeto = projeto_repository.buscar_por_id(arquivo.projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    identificador = uuid4().hex

    caminho_metadado = (
        "metadata-only://"
        f"projetos/{arquivo.projeto_id}/"
        f"{identificador}"
    )

    arquivo_id = repository.criar_arquivo(
        projeto_id=arquivo.projeto_id,
        nome_original=arquivo.nome_original,
        caminho_servidor=caminho_metadado,
        tamanho_mb=arquivo.tamanho_mb
    )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="CREATE",
        entidade="arquivos_projeto",
        registro_id=arquivo_id,
        detalhes=(
            f"Metadado do arquivo "
            f"'{arquivo.nome_original}' "
            f"cadastrado no projeto "
            f"{arquivo.projeto_id}"
        )
    )

    return arquivo_id


def atualizar_arquivo(
    id_arquivo: int,
    arquivo: ArquivoProjetoUpdate,
    coordenador_id: int
) -> bool:

    arquivo_existente = (
        repository.buscar_por_id(id_arquivo)
    )

    if not arquivo_existente:
        raise ValueError(
            "Arquivo não encontrado"
        )

    dados_recebidos = (
        arquivo.model_dump(
            exclude_unset=True
        )
    )

    if not dados_recebidos:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    dados_alterados = {
        campo: valor
        for campo, valor
        in dados_recebidos.items()
        if valor
        != arquivo_existente.get(campo)
    }

    if not dados_alterados:
        raise ValueError(
            "Nenhuma alteração identificada"
        )

    atualizado = (
        repository.atualizar_arquivo(
            id_arquivo=id_arquivo,
            dados=dados_alterados
        )
    )

    if not atualizado:
        raise ValueError(
            "Não foi possível atualizar o arquivo"
        )

    campos_alterados = ", ".join(
        dados_alterados.keys()
    )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="UPDATE",
        entidade="arquivos_projeto",
        registro_id=id_arquivo,
        detalhes=(
            f"Metadados do arquivo "
            f"'{arquivo_existente['nome_original']}' "
            f"atualizados. Campos: "
            f"{campos_alterados}"
        )
    )

    return True


def deletar_arquivo(id_arquivo: int, coordenador_id: int) -> bool:

    arquivo = repository.buscar_por_id(id_arquivo)

    if not arquivo:
        raise ValueError(
            "Arquivo não encontrado"
        )

    resultado = repository.deletar_arquivo(id_arquivo)

    if not resultado:
        raise ValueError(
            "Não foi possível remover o arquivo"
        )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="DELETE",
        entidade="arquivos_projeto",
        registro_id=id_arquivo,
        detalhes=(
            f"Arquivo '{arquivo['nome_original']}' "
            f"removido do projeto "
            f"{arquivo['projeto_id']}"
        )
    )

    return True
