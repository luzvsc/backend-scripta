from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (
    exigir_aluno,
    exigir_coordenador,
    obter_usuario_logado
)
from app.models.auth import UsuarioAutenticado
from app.models.professor import (
    ProfessorCreate,
    ProfessorCreateResponse,
    ProfessorOrientadorResponse,
    ProfessorResponse,
    ProfessorUpdate
)
import app.services.professor_service as professor_service


router = APIRouter(prefix="/professores", tags=["Professores"])


@router.post(
    "/",
    response_model=ProfessorCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_professor(
    professor: ProfessorCreate
):
    
    try:
        id_professor = professor_service.cadastrar_professor(professor)

        return {
            "message": "Professor cadastrado com sucesso",
            "id": id_professor
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get(
    "/opcoes-orientadores",
    response_model=list[ProfessorOrientadorResponse],
    status_code=status.HTTP_200_OK
)
def listar_opcoes_orientadores(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_aluno(usuario)

    return professor_service.listar_opcoes_orientadores()


@router.get(
    "/",
    response_model=list[ProfessorResponse],
    status_code=status.HTTP_200_OK
)
def listar_professores(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_coordenador(usuario)

    return professor_service.listar_professores()


@router.get(
    "/{id_professor}",
    response_model=ProfessorResponse,
    status_code=status.HTTP_200_OK
)
def buscar_professor_por_id(
    id_professor: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        return professor_service.buscar_professor_por_id(
            id_professor=id_professor,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Professor não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.put(
    "/{id_professor}",
    status_code=status.HTTP_200_OK
)
def atualizar_professor(
    id_professor: int,
    professor: ProfessorUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    try:
        professor_service.atualizar_professor(
            id_professor=id_professor,
            professor=professor,
            usuario=usuario
        )

        return {
            "message": "Senha do professor atualizada "
            "com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Professor não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem in (
            "Você só pode alterar o próprio cadastro",
            "Você não tem permissão para alterar "
            "este cadastro"
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
    "/{id_professor}",
    status_code=status.HTTP_200_OK
)
def deletar_professor(
    id_professor: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    
    exigir_coordenador(usuario)

    try:
        professor_service.deletar_professor(
            id_professor=id_professor,
            coordenador_id=usuario.id
        )

        return {
            "message": "Professor removido com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Professor não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )