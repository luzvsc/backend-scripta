from app.models.projeto import (
    ProjetoCreate,
    ProjetoUpdate,
    ProjetoStatusUpdate
)
import app.repositories.projeto_repository as projeto_repository
import app.repositories.aluno_repository as aluno_repository
import app.repositories.professor_repository as professor_repository
import app.repositories.projeto_integrante_repository as integrante_repository
from app.services import versao_projeto_service
from app.models.versao_projeto import VersaoProjetoCreate
import app.services.logs_sistema_service as logs_sistema_service
from typing import Literal

PerfilAlterador = Literal[ "aluno", "professor", "coordenador" ]

PerfilAutenticado = Literal[ "aluno", "professor", "coordenador", "empresa" ]

def cadastrar_projeto(
    projeto: ProjetoCreate,
    aluno_responsavel_id: int
) -> int:
    aluno = aluno_repository.buscar_por_id(
        aluno_responsavel_id
    )

    if not aluno:
        raise ValueError(
            "Aluno responsável não encontrado"
        )

    professor = professor_repository.buscar_por_id(
        projeto.professor_orientador_id
    )

    if not professor:
        raise ValueError(
            "Professor orientador não encontrado"
        )

    projeto_existente = (
        projeto_repository.buscar_por_titulo_turma_semestre(
            projeto.titulo,
            projeto.turma,
            projeto.semestre
        )
    )

    if projeto_existente:
        raise ValueError(
            "Já existe um projeto com este título "
            "nesta turma e semestre"
        )

    id_projeto = projeto_repository.criar_projeto(
        titulo=projeto.titulo,
        descricao=projeto.descricao,
        curso=projeto.curso,
        turma=projeto.turma,
        semestre=projeto.semestre,
        area_conhecimento=projeto.area_conhecimento,
        aluno_responsavel_id=aluno_responsavel_id,
        professor_orientador_id=(
            projeto.professor_orientador_id
        )
    )

    integrante_repository.adicionar_integrante(
        projeto_id=id_projeto,
        aluno_id=aluno_responsavel_id
    )

    return id_projeto


def buscar_projeto_por_id(id_projeto: int) -> dict:

    projeto = projeto_repository.buscar_por_id(id_projeto)

    if not projeto:
        raise ValueError("Projeto não encontrado")

    return projeto


def listar_projetos() -> list[dict]:

    return projeto_repository.listar_projetos()


def atualizar_projeto(
    id_projeto: int,
    projeto: ProjetoUpdate,
    quem_alterou_id: int,
    quem_alterou_tipo: PerfilAlterador
) -> bool:
    projeto_existente = projeto_repository.buscar_por_id(
        id_projeto
    )

    if not projeto_existente:
        raise ValueError(
            "Projeto não encontrado"
        )

    integrante = (
        integrante_repository.buscar_por_projeto_e_aluno(
            projeto_id=id_projeto,
            aluno_id=quem_alterou_id
        )
    )

    if not integrante:
        raise ValueError(
            "Você não faz parte deste projeto"
        )

    status_atual = projeto_existente["status"]

    if status_atual in (
        "em_avaliacao",
        "aprovado",
        "reprovado"
    ):
        raise ValueError(
            "Este projeto não pode mais ser editado"
        )

    dados = projeto.model_dump(
        exclude_unset=True
    )

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    titulo = dados.get(
        "titulo",
        projeto_existente["titulo"]
    )

    turma = dados.get(
        "turma",
        projeto_existente["turma"]
    )

    semestre = dados.get(
        "semestre",
        projeto_existente["semestre"]
    )

    projeto_duplicado = (
        projeto_repository.buscar_por_titulo_turma_semestre(
            titulo,
            turma,
            semestre
        )
    )

    if (
        projeto_duplicado
        and projeto_duplicado["id"] != id_projeto
    ):
        raise ValueError(
            "Já existe um projeto com este título "
            "nesta turma e semestre"
        )

    versao_projeto_service.criar_versao(
        VersaoProjetoCreate(
            projeto_id=id_projeto,
            quem_alterou_tipo=quem_alterou_tipo,
            quem_alterou_id=quem_alterou_id
        )
    )

    return projeto_repository.atualizar_projeto(
        id_projeto,
        dados
    )



def atualizar_status_projeto(
    id_projeto: int,
    status_update: ProjetoStatusUpdate,
    usuario_id: int | None = None,
    usuario_perfil: PerfilAutenticado | None = None
) -> bool:
    projeto = projeto_repository.buscar_por_id(
        id_projeto
    )

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    status_atual = projeto["status"]
    novo_status = status_update.status

    transicoes = {
        "rascunho": ["submetido"],
        "submetido": ["em_avaliacao"],
        "em_avaliacao": [
            "aprovado",
            "reprovado"
        ],
        "aprovado": [],
        "reprovado": []
    }

    if novo_status not in transicoes[status_atual]:
        raise ValueError(
            f"Não é permitido alterar status de "
            f"'{status_atual}' para '{novo_status}'"
        )

    coordenador_id: int | None = None

    if novo_status == "submetido":
        if usuario_perfil != "aluno":
            raise ValueError(
                "Apenas alunos podem submeter projetos"
            )

        if usuario_id is None:
            raise ValueError(
                "Aluno autenticado não identificado"
            )

        integrante = (
            integrante_repository.buscar_por_projeto_e_aluno(
                projeto_id=id_projeto,
                aluno_id=usuario_id
            )
        )

        if not integrante:
            raise ValueError(
                "Você não faz parte deste projeto"
            )

    elif novo_status == "em_avaliacao":
        if (
            usuario_id is not None
            or usuario_perfil is not None
        ):
            raise ValueError(
                "O status 'em_avaliacao' é definido "
                "automaticamente pelo sistema"
            )

    elif novo_status in (
        "aprovado",
        "reprovado"
    ):
        if usuario_perfil != "coordenador":
            raise ValueError(
                "Apenas coordenadores podem aprovar "
                "ou reprovar projetos"
            )

        if usuario_id is None:
            raise ValueError(
                "Coordenador autenticado não identificado"
            )

        coordenador_id = usuario_id

    resultado = (
        projeto_repository.atualizar_status_projeto(
            projeto_id=id_projeto,
            status=novo_status
        )
    )

    if novo_status in (
        "aprovado",
        "reprovado"
    ):
        if coordenador_id is None:
            raise ValueError(
                "Coordenador não identificado"
            )

        logs_sistema_service.registrar_acao(
            coordenador_id=coordenador_id,
            acao="UPDATE",
            entidade="projetos",
            registro_id=id_projeto,
            detalhes=(
                f"Status do projeto alterado "
                f"para '{novo_status}'"
            )
        )

    return resultado



def deletar_projeto(
    id_projeto: int,
    coordenador_id: int
) -> bool:
    projeto = projeto_repository.buscar_por_id(
        id_projeto
    )

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    status_atual = projeto["status"]

    if status_atual in (
        "em_avaliacao",
        "aprovado",
        "reprovado"
    ):
        raise ValueError(
            "Este projeto não pode ser removido"
        )

    resultado = projeto_repository.deletar_projeto(
        id_projeto
    )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="DELETE",
        entidade="projetos",
        registro_id=id_projeto,
        detalhes="Projeto removido"
    )

    return resultado
