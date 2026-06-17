from app.models.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from app.repositories import avaliacao_repository as repository
import app.services.projeto_service as projeto_service
from app.models.projeto import ProjetoStatusUpdate


def calcular_media(
    nota_inovacao: float,
    nota_tecnica: float,
    nota_aplicabilidade: float,
    nota_clareza: float
) -> float:

    return round(
        (
            nota_inovacao +
            nota_tecnica +
            nota_aplicabilidade +
            nota_clareza
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


def validar_status_para_avaliacao(status: str) -> None:

    status_bloqueados = [
        "rascunho",
        "aprovado",
        "reprovado"
    ]

    if status in status_bloqueados:
        raise ValueError(
            f"Não é permitido avaliar projetos com status '{status}'"
        )


def criar_avaliacao(avaliacao: AvaliacaoCreate) -> int:

    avaliacao_existente = repository.buscar_por_projeto_professor(
    avaliacao.projeto_id,
    avaliacao.professor_id
)

    if avaliacao_existente:
        raise ValueError("Avaliação já existe para este projeto e professor.")
    
    projeto = projeto_service.buscar_projeto_por_id(
    avaliacao.projeto_id
    )

    validar_status_para_avaliacao(projeto["status"])
    
    media = calcular_media(
        nota_inovacao=avaliacao.nota_inovacao,
        nota_tecnica=avaliacao.nota_tecnica,
        nota_aplicabilidade=avaliacao.nota_aplicabilidade,
        nota_clareza=avaliacao.nota_clareza
    )

    conceito = calcular_conceito(media)

    avaliacao_id = repository.criar_avaliacao(
    projeto_id=avaliacao.projeto_id,
    professor_id=avaliacao.professor_id,
    nota_inovacao=avaliacao.nota_inovacao,
    nota_tecnica=avaliacao.nota_tecnica,
    nota_aplicabilidade=avaliacao.nota_aplicabilidade,
    nota_clareza=avaliacao.nota_clareza,
    media_geral=media,
    conceito=conceito,
    parecer_descritivo=avaliacao.parecer_descritivo
)
    projeto = projeto_service.buscar_projeto_por_id(
    avaliacao.projeto_id
)

    if projeto["status"] == "submetido":
        projeto_service.atualizar_status_projeto(avaliacao.projeto_id, ProjetoStatusUpdate(status="em_avaliacao"))

    return avaliacao_id


def buscar_avaliacao_por_id(id_avaliacao: int) -> dict:
    
    avaliacao = repository.buscar_por_id(id_avaliacao)

    if not avaliacao:
        raise ValueError("Avaliação não encontrada")
    return avaliacao


def listar_avaliacoes() -> list[dict]:

    return repository.listar_avaliacoes()


def listar_avaliacoes_por_projeto(projeto_id: int) -> list[dict]:

    return repository.listar_por_projeto(projeto_id)


def atualizar_avaliacao(id_avaliacao: int, avaliacao: AvaliacaoUpdate) -> bool:

    avaliacao_existente = repository.buscar_por_id(id_avaliacao)

    if not avaliacao_existente:
        raise ValueError("Avaliação não encontrada")
    
    projeto = projeto_service.buscar_projeto_por_id(
    avaliacao.projeto_id
    )

    validar_status_para_avaliacao(projeto["status"])

    dados = avaliacao.model_dump(exclude_unset=True)

    if not dados:
        raise ValueError("Nenhum dado informado para atualização")

    notas = {
        "nota_inovacao": dados.get(
            "nota_inovacao",
            avaliacao_existente["nota_inovacao"]
        ),
        "nota_tecnica": dados.get(
            "nota_tecnica",
            avaliacao_existente["nota_tecnica"]
        ),
        "nota_aplicabilidade": dados.get(
            "nota_aplicabilidade",
            avaliacao_existente["nota_aplicabilidade"]
        ),
        "nota_clareza": dados.get(
            "nota_clareza",
            avaliacao_existente["nota_clareza"]
        ),
    }

    media = calcular_media(**notas)
    conceito = calcular_conceito(media)

    dados["media_geral"] = media
    dados["conceito"] = conceito

    sucesso = repository.atualizar_avaliacao(
        id_avaliacao=id_avaliacao,
        dados=dados
    )

    return sucesso