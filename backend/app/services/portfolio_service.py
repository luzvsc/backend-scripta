from app.models.auth import UsuarioAutenticado
from app.models.portfolio import (PortfolioCreate, PortfolioUpdate)
import app.repositories.aluno_repository as aluno_repository
import app.repositories.portfolio_repository as portfolio_repository
import app.repositories.projeto_integrante_repository as integrante_repository
import app.repositories.projeto_repository as projeto_repository


def cadastrar_portfolio(portfolio: PortfolioCreate, aluno_id: int) -> int:

    projeto = projeto_repository.buscar_por_id(portfolio.projeto_id)

    if not projeto:
        raise ValueError(
            "Projeto não encontrado"
        )

    if projeto["status"] != "aprovado":
        raise ValueError(
            "Somente projetos aprovados podem ser "
            "adicionados ao portfólio"
        )

    responsavel = (
        projeto["aluno_responsavel_id"]
        == aluno_id
    )

    integrante = (
        integrante_repository.buscar_por_projeto_e_aluno(
            projeto_id=portfolio.projeto_id,
            aluno_id=aluno_id
        )
    )

    if not responsavel and not integrante:
        raise ValueError(
            "Você não faz parte deste projeto"
        )

    portfolio_existente = (
        portfolio_repository.buscar_por_aluno_e_projeto(
            aluno_id=aluno_id,
            projeto_id=portfolio.projeto_id
        )
    )

    if portfolio_existente:
        raise ValueError(
            "Este projeto já está no seu portfólio"
        )

    id_portfolio = portfolio_repository.criar_portfolio(
        aluno_id=aluno_id,
        projeto_id=portfolio.projeto_id,
        visibilidade=portfolio.visibilidade.value
    )

    if id_portfolio is None:
        raise ValueError(
            "Não foi possível adicionar o projeto "
            "ao portfólio"
        )

    return id_portfolio


def buscar_portfolio_por_id(id_portfolio: int, usuario: UsuarioAutenticado) -> dict:

    portfolio = portfolio_repository.buscar_por_id(id_portfolio)

    if not portfolio:
        raise ValueError(
            "Portfólio não encontrado"
        )

    if (
        usuario.perfil == "aluno"
        and portfolio["aluno_id"] == usuario.id
    ):
        return portfolio

    visibilidade = portfolio["visibilidade"]

    if (
        usuario.perfil == "empresa"
        and visibilidade == "publico"
    ):
        return portfolio

    if (
        usuario.perfil in (
            "aluno",
            "professor",
            "coordenador"
        )
        and visibilidade in (
            "publico",
            "apenas_senac"
        )
    ):
        return portfolio

    raise ValueError(
        "Você não tem permissão para visualizar "
        "este portfólio"
    )


def listar_meus_portfolios(aluno_id: int) -> list[dict]:

    return portfolio_repository.listar_por_aluno(aluno_id=aluno_id)


def listar_portfolios_do_aluno(id_aluno: int, usuario: UsuarioAutenticado) -> list[dict]:

    aluno = aluno_repository.buscar_por_id(id_aluno)

    if not aluno:
        raise ValueError(
            "Aluno não encontrado"
        )

    if (
        usuario.perfil == "aluno"
        and usuario.id == id_aluno
    ):
        visibilidades = None

    elif usuario.perfil == "empresa":
        visibilidades = (
            "publico",
        )

    else:
        visibilidades = (
            "publico",
            "apenas_senac"
        )

    return portfolio_repository.listar_por_aluno(
        aluno_id=id_aluno,
        visibilidades=visibilidades
    )


def atualizar_portfolio(
    id_portfolio: int,
    portfolio_update: PortfolioUpdate,
    aluno_id: int
) -> bool:
    
    portfolio = portfolio_repository.buscar_por_id(id_portfolio)

    if not portfolio:
        raise ValueError(
            "Portfólio não encontrado"
        )

    if portfolio["aluno_id"] != aluno_id:
        raise ValueError(
            "Você só pode alterar o próprio portfólio"
        )

    resultado = portfolio_repository.atualizar_portfolio(
        id_portfolio=id_portfolio,
        visibilidade=portfolio_update.visibilidade.value
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar o portfólio"
        )

    return True


def deletar_portfolio(id_portfolio: int, aluno_id: int) -> bool:

    portfolio = portfolio_repository.buscar_por_id(id_portfolio)

    if not portfolio:
        raise ValueError(
            "Portfólio não encontrado"
        )

    if portfolio["aluno_id"] != aluno_id:
        raise ValueError(
            "Você só pode remover projetos do "
            "próprio portfólio"
        )

    resultado = portfolio_repository.deletar_portfolio(
        id_portfolio
    )

    if not resultado:
        raise ValueError(
            "Não foi possível remover o portfólio"
        )

    return True