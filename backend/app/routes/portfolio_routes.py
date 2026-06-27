from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (obter_usuario_logado, exigir_aluno)
from app.models.auth import UsuarioAutenticado
from app.models.portfolio import (
    PortfolioCreate,
    PortfolioCreateResponse,
    PortfolioResponse,
    PortfolioUpdate
)
import app.services.portfolio_service as portfolio_service


router = APIRouter(prefix="/portfolios", tags=["Portfólios"])


@router.post(
    "/",
    response_model=PortfolioCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_portfolio(
    portfolio: PortfolioCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        id_portfolio = (
            portfolio_service.cadastrar_portfolio(
                portfolio=portfolio,
                aluno_id=usuario.id
            )
        )

        return {
            "message": "Projeto adicionado ao portfólio",
            "id": id_portfolio
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == "Você não faz parte deste projeto":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        if mensagem in (
            "Somente projetos aprovados podem ser "
            "adicionados ao portfólio",
            "Este projeto já está no seu portfólio"
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.get(
    "/meus",
    response_model=list[PortfolioResponse],
    status_code=status.HTTP_200_OK
)
def listar_meus_portfolios(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    return portfolio_service.listar_meus_portfolios(
        aluno_id=usuario.id
    )


@router.get(
    "/aluno/{id_aluno}",
    response_model=list[PortfolioResponse],
    status_code=status.HTTP_200_OK
)
def listar_portfolios_do_aluno(
    id_aluno: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return portfolio_service.listar_portfolios_do_aluno(
            id_aluno=id_aluno,
            usuario=usuario
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/publicos",
    response_model=list[PortfolioResponse],
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Acesso negado"
        }
    }
)
def listar_portfolios_publicos(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    if usuario.perfil != "empresa":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Apenas empresas podem acessar "
                "os portfólios públicos"
            )
        )

    return (
        portfolio_service
        .listar_portfolios_publicos()
    )


@router.get(
    "/{id_portfolio}",
    response_model=PortfolioResponse,
    status_code=status.HTTP_200_OK
)
def buscar_portfolio_por_id(
    id_portfolio: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return portfolio_service.buscar_portfolio_por_id(
            id_portfolio=id_portfolio,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Portfólio não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.put(
    "/{id_portfolio}",
    status_code=status.HTTP_200_OK
)
def atualizar_portfolio(
    id_portfolio: int,
    portfolio: PortfolioUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        portfolio_service.atualizar_portfolio(
            id_portfolio=id_portfolio,
            portfolio_update=portfolio,
            aluno_id=usuario.id
        )

        return {
            "message": "Portfólio atualizado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Portfólio não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você só pode alterar o próprio portfólio"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.delete(
    "/{id_portfolio}",
    status_code=status.HTTP_200_OK
)
def deletar_portfolio(
    id_portfolio: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        portfolio_service.deletar_portfolio(
            id_portfolio=id_portfolio,
            aluno_id=usuario.id
        )

        return {
            "message": "Projeto removido do portfólio"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Portfólio não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você só pode remover projetos do "
            "próprio portfólio"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )