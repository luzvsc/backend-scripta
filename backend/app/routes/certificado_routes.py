from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (
    obter_usuario_logado,
    exigir_aluno,
    exigir_coordenador
)
from app.models.auth import UsuarioAutenticado
from app.models.certificado import (
    CertificadoResponse,
    CertificadoEmitirRequest,
    CertificadoCreateResponse
)
import app.services.certificado_service as certificado_service


router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.post(
    "/emitir",
    response_model=CertificadoCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def emitir_certificados(
    payload: CertificadoEmitirRequest,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    try:
        ids = (
            certificado_service.emitir_certificados_por_projeto(
                projeto_id=payload.projeto_id,
                coordenador_id=usuario.id
            )
        )

        return {
            "message": "Certificados emitidos com sucesso",
            "ids_certificados": ids
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem in (
            "Projeto não encontrado",
            "Nenhum integrante encontrado para este projeto"
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem in (
            "Certificados só podem ser emitidos "
            "para projetos aprovados",
            "Todos os integrantes já possuem certificado"
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
    "/",
    response_model=list[CertificadoResponse],
    status_code=status.HTTP_200_OK
)
def listar_todos_certificados(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    return certificado_service.listar_todos_certificados()


@router.get(
    "/meus",
    response_model=list[CertificadoResponse],
    status_code=status.HTTP_200_OK
)
def listar_meus_certificados(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_aluno(usuario)

    return certificado_service.listar_meus_certificados(
        aluno_id=usuario.id
    )


@router.get(
    "/aluno/{id_aluno}",
    response_model=list[CertificadoResponse],
    status_code=status.HTTP_200_OK
)
def listar_certificados_do_aluno(
    id_aluno: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    return certificado_service.listar_certificados_do_aluno(
        id_aluno=id_aluno
    )


@router.get(
    "/projeto/{id_projeto}",
    response_model=list[CertificadoResponse],
    status_code=status.HTTP_200_OK
)
def listar_certificados_do_projeto(
    id_projeto: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    try:
        return (
            certificado_service.listar_certificados_do_projeto(
                id_projeto=id_projeto
            )
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{id_certificado}",
    response_model=CertificadoResponse,
    status_code=status.HTTP_200_OK
)
def buscar_certificado_por_id(
    id_certificado: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    try:
        return certificado_service.buscar_certificado_por_id(
            id_certificado=id_certificado,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Certificado não encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        if mensagem == (
            "Você não tem permissão para visualizar "
            "este certificado"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )