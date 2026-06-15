from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.portfolio import (
    PortfolioCreate,
    PortfolioCreateResponse,
    PortfolioResponse,
    PortfolioUpdate
)
import app.services.portfolio_service as portfolio_service

router = APIRouter(prefix="/portfolios", tags=["Portfólios"])

@router.post("/", response_model=PortfolioCreateResponse, responses={409: {"description": "Conflito ao cadastrar"}}, status_code=status.HTTP_201_CREATED)
def cadastrar_portfolio(portfolio: PortfolioCreate):
    try:
        id_portfolio = portfolio_service.cadastrar_portfolio(portfolio)
        return {
            "message": "Portfólio cadastrado com sucesso",
            "id": id_portfolio
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/{id_portfolio}", response_model=PortfolioResponse, responses={404: {"description": "Portfólio não encontrado"}})
def buscar_portfolio_por_id(id_portfolio: int):
    try:
        portfolio = portfolio_service.buscar_portfolio_por_id(id_portfolio)
        return portfolio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id_portfolio}", responses={404: {"description": "Portfólio não encontrado"}})
def atualizar_portfolio(id_portfolio: int, portfolio: PortfolioUpdate):
    try:
        portfolio_service.atualizar_portfolio(id_portfolio, portfolio)
        return {
            "message": "Portfólio atualizado com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{id_portfolio}", status_code=status.HTTP_200_OK, responses={404: {"description": "Portfólio não encontrado"}})
def deletar_portfolio(id_portfolio: int):
    try:
        portfolio_service.deletar_portfolio(id_portfolio)
        return {
            "message": "Portfólio removido com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
