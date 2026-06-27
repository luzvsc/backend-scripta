from app.models.avaliacao import (AvaliacaoCreate, AvaliacaoUpdate)
from app.models.auth import UsuarioAutenticado
from app.repositories import (avaliacao_repository as repository)
import app.repositories.projeto_repository as projeto_repository
import app.repositories.projeto_integrante_repository as integrante_repository


def calcular_media(
    nota_inovacao: float,
    nota_tecnica: float,
    nota_aplicabilidade: float,
    nota_clareza: float
) -> float:
    
    return round(
        (
            nota_inovacao
            + nota_tecnica
            + nota_aplicabilidade
            + nota_clareza
        ) / 4,
        2
    )


def calcular_conceito(media: float) -> str:

    if media >= 95:
        return "Excelente"

    if media >= 85:
        return "Ótimo"

    if media >= 70:
        return "Bom"

    if media >= 50:
        return "Ainda não suficiente"

    return "Insuficiente"


def validar_status_para_avaliacao(status_projeto: str) -> None:
    
    status_permitidos = [
        "submetido",
        "em_avaliacao"
    ]

    if status_projeto not in status_permitidos:
        raise ValueError(
            f"Não é permitido avaliar projetos "
            f"com status '{status_projeto}'"
        )


def criar_avaliacao(avaliacao: AvaliacaoCreate, professor_id: int) -> int:

    projeto = projeto_repository.buscar_por_id(avaliacao.projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    validar_status_para_avaliacao(
        projeto["status"]
    )

    avaliacao_existente = (
        repository.buscar_por_projeto_professor(
            avaliacao.projeto_id,
            professor_id
        )
    )

    if avaliacao_existente:
        raise ValueError(
            "Avaliação já existe para este "
            "projeto e professor"
        )

    media = calcular_media(
        nota_inovacao=avaliacao.nota_inovacao,
        nota_tecnica=avaliacao.nota_tecnica,
        nota_aplicabilidade=(
            avaliacao.nota_aplicabilidade
        ),
        nota_clareza=avaliacao.nota_clareza
    )

    conceito = calcular_conceito(media)

    id_avaliacao = repository.criar_avaliacao(
        projeto_id=avaliacao.projeto_id,
        professor_id=professor_id,
        nota_inovacao=avaliacao.nota_inovacao,
        nota_tecnica=avaliacao.nota_tecnica,
        nota_aplicabilidade=(
            avaliacao.nota_aplicabilidade
        ),
        nota_clareza=avaliacao.nota_clareza,
        media_geral=media,
        conceito=conceito,
        parecer_descritivo=(
            avaliacao.parecer_descritivo
        )
    )

    if projeto["status"] == "submetido":
        projeto_repository.atualizar_status_projeto(
            projeto_id=avaliacao.projeto_id,
            status="em_avaliacao"
    )

    return id_avaliacao


def buscar_avaliacao_por_id(id_avaliacao: int, usuario: UsuarioAutenticado) -> dict:
    
    avaliacao = repository.buscar_por_id(id_avaliacao)

    if not avaliacao:
        raise ValueError(
            "Avaliação não encontrada"
        )

    if usuario.perfil == "coordenador":
        return avaliacao

    if usuario.perfil == "professor":
        if avaliacao["professor_id"] == usuario.id:
            return avaliacao

        raise ValueError(
            "Você não tem permissão para "
            "visualizar esta avaliação"
        )

    if usuario.perfil == "aluno":
        integrante = (
            integrante_repository.buscar_por_projeto_e_aluno(
                avaliacao["projeto_id"],
                usuario.id
            )
        )

        if integrante:
            return avaliacao

    raise ValueError(
        "Você não tem permissão para "
        "visualizar esta avaliação"
    )


def listar_avaliacoes(usuario: UsuarioAutenticado) -> list[dict]:

    if usuario.perfil == "coordenador":
        return repository.listar_avaliacoes()

    if usuario.perfil == "professor":
        return repository.listar_por_professor(usuario.id)

    raise ValueError(
        "A listagem geral de avaliações é permitida "
        "apenas para professores e coordenadores"
    )


def listar_avaliacoes_por_projeto(projeto_id: int, usuario: UsuarioAutenticado) -> list[dict]:

    projeto = projeto_repository.buscar_por_id(projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    if usuario.perfil in (
        "professor",
        "coordenador"
    ):
        return repository.listar_por_projeto(
            projeto_id
        )

    if usuario.perfil == "aluno":
        integrante = (
            integrante_repository.buscar_por_projeto_e_aluno(
                projeto_id,
                usuario.id
            )
        )

        if integrante:
            return repository.listar_por_projeto(projeto_id)

    raise ValueError(
        "Você não tem permissão para visualizar "
        "as avaliações deste projeto"
    )


def atualizar_avaliacao(
    id_avaliacao: int,
    avaliacao: AvaliacaoUpdate,
    professor_id: int
) -> bool:
    
    avaliacao_existente = repository.buscar_por_id(id_avaliacao)

    if not avaliacao_existente:
        raise ValueError(
            "Avaliação não encontrada"
        )

    if (
        avaliacao_existente["professor_id"]
        != professor_id
    ):
        raise ValueError(
            "Você só pode alterar avaliações "
            "criadas por você"
        )

    projeto = projeto_repository.buscar_por_id(
        avaliacao_existente["projeto_id"]
    )

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    validar_status_para_avaliacao(projeto["status"])

    dados = avaliacao.model_dump(exclude_unset=True)

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    nota_inovacao = float(
        dados.get(
            "nota_inovacao",
            avaliacao_existente["nota_inovacao"]
        )
    )

    nota_tecnica = float(
        dados.get(
            "nota_tecnica",
            avaliacao_existente["nota_tecnica"]
        )
    )

    nota_aplicabilidade = float(
        dados.get(
            "nota_aplicabilidade",
            avaliacao_existente[
                "nota_aplicabilidade"
            ]
        )
    )

    nota_clareza = float(
        dados.get(
            "nota_clareza",
            avaliacao_existente["nota_clareza"]
        )
    )

    media = calcular_media(
        nota_inovacao=nota_inovacao,
        nota_tecnica=nota_tecnica,
        nota_aplicabilidade=nota_aplicabilidade,
        nota_clareza=nota_clareza
    )

    conceito = calcular_conceito(
        media
    )

    dados["media_geral"] = media
    dados["conceito"] = conceito

    return repository.atualizar_avaliacao(
        id_avaliacao=id_avaliacao,
        dados=dados
    )