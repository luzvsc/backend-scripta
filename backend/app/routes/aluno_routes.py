from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (obter_usuario_logado, exigir_coordenador)
from app.models.aluno import (
    AlunoCreate,
    AlunoCreateResponse,
    AlunoResponse,
    AlunoUpdate
)
from app.models.auth import UsuarioAutenticado
import app.services.aluno_service as aluno_service


router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.post(
    "/",
    response_model=AlunoCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_aluno(
    aluno: AlunoCreate
):

    try:
        id_aluno = aluno_service.cadastrar_aluno(
            aluno
        )

        return {
            "message": "Aluno cadastrado com sucesso",
            "id": id_aluno
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[AlunoResponse],
    status_code=status.HTTP_200_OK
)
def listar_alunos(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    exigir_coordenador(usuario)

    return aluno_service.listar_alunos()


@router.get(
    "/{id_aluno}",
    response_model=AlunoResponse,
    status_code=status.HTTP_200_OK
)
def buscar_aluno_por_id(
    id_aluno: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    try:
        return aluno_service.buscar_aluno_por_id(
            id_aluno=id_aluno,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Aluno não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.put(
    "/{id_aluno}",
    status_code=status.HTTP_200_OK
)
def atualizar_aluno(
    id_aluno: int,
    aluno: AlunoUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    try:
        aluno_service.atualizar_aluno(
            id_aluno=id_aluno,
            aluno=aluno,
            usuario=usuario
        )

        return {
            "message": "Aluno atualizado com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Aluno não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem in (
            "Você só pode alterar o próprio cadastro",
            "Você não tem permissão para alterar este cadastro",
            "Você não tem permissão para alterar estes campos"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        if mensagem == (
            "Este email já está cadastrado no Scripta"
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensagem
            )

        if mensagem == (
            "Esta matrícula já está cadastrada"
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )



@router.delete(
    "/{id_aluno}",
    status_code=status.HTTP_200_OK
)
def deletar_aluno(
    id_aluno: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    exigir_coordenador(usuario)

    try:
        aluno_service.deletar_aluno(
            id_aluno=id_aluno,
            coordenador_id=usuario.id
        )

        return {
            "message": "Aluno removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Aluno não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )
