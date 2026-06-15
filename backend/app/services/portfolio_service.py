from app.models.portfolio import PortfolioCreate, PortfolioUpdate
import app.repositories.portfolio_repository as portfolio_repository
import app.services.projeto_service as projeto_service
import app.services.aluno_service as aluno_service


def cadastrar_portfolio(portfolio: PortfolioCreate) -> int:
    aluno_service.buscar_aluno_por_id(portfolio.aluno_id)
    projeto_service.buscar_projeto_por_id(portfolio.projeto_id)
    
    try:
        id_portfolio = portfolio_repository.criar_portfolio(
            aluno_id=portfolio.aluno_id,
            projeto_id=portfolio.projeto_id,
            visibilidade=portfolio.visibilidade.value
        )
        return id_portfolio
    except Exception as e:
        # Assuming duplicate entry will throw a db exception (uq_aluno_projeto)
        raise ValueError("Erro ao cadastrar portfólio. Verifique se a combinação de aluno e projeto já existe.")


def buscar_portfolio_por_id(id_portfolio: int) -> dict:
    portfolio = portfolio_repository.buscar_por_id(id_portfolio)
    if not portfolio:
        raise ValueError("Portfólio não encontrado")
    return portfolio


def atualizar_portfolio(id_portfolio: int, portfolio: PortfolioUpdate) -> bool:
    portfolio_existente = portfolio_repository.buscar_por_id(id_portfolio)
    if not portfolio_existente:
        raise ValueError("Portfólio não encontrado")
    
    return portfolio_repository.atualizar_portfolio(id_portfolio, portfolio.visibilidade.value)


def deletar_portfolio(id_portfolio: int) -> bool:
    deleted = portfolio_repository.deletar_portfolio(id_portfolio)
    if not deleted:
        raise ValueError("Portfólio não encontrado")
    return True
