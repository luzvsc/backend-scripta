from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (obter_usuario_logado, exigir_aluno)
from app.models.auth import UsuarioAutenticado
from app.models.link_projeto import (
    LinkProjetoCreate,
    LinkProjetoCreateResponse,
    LinkProjetoResponse,
    LinkProjetoUpdate
)
import app.services.link_projeto_service as link_service


router = APIRouter(prefix="/projetos/{id_projeto}/links", tags=["Links Projeto"])


@router.post(
    "/",
    response_model=LinkProjetoCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_link(
    id_projeto: int,
    link: LinkProjetoCreate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        id_link = link_service.criar_link(
            projeto_id=id_projeto,
            link=link,
            aluno_id=usuario.id
        )

        return {
            "message": "Link adicionado com sucesso",
            "id": id_link
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

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.get(
    "/",
    response_model=list[LinkProjetoResponse],
    status_code=status.HTTP_200_OK
)
def listar_links(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return link_service.listar_links(
            projeto_id=id_projeto,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Projeto não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.patch(
    "/{id_link}",
    status_code=status.HTTP_200_OK
)
def atualizar_link(
    id_projeto: int,
    id_link: int,
    link: LinkProjetoUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        link_service.atualizar_link(
            projeto_id=id_projeto,
            id_link=id_link,
            link_update=link,
            aluno_id=usuario.id
        )

        return {
            "message": "Link atualizado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Projeto não encontrado",
            "Link não encontrado neste projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == "Você não faz parte deste projeto":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )


@router.delete(
    "/{id_link}",
    status_code=status.HTTP_200_OK
)
def deletar_link(
    id_projeto: int,
    id_link: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    try:
        link_service.deletar_link(
            projeto_id=id_projeto,
            id_link=id_link,
            aluno_id=usuario.id
        )

        return {
            "message": "Link removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Projeto não encontrado",
            "Link não encontrado neste projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == "Você não faz parte deste projeto":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )