from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.auth_core import (
    exigir_coordenador,
    obter_usuario_logado
)
from app.models.auth import UsuarioAutenticado
from app.models.empresa import (
    EmpresaCreate,
    EmpresaCreateResponse,
    EmpresaResponse,
    EmpresaUpdate
)
import app.services.empresa_service as empresa_service


router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.post(
    "/",
    response_model=EmpresaCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_empresa(
    empresa: EmpresaCreate
):

    try:
        id_empresa = empresa_service.cadastrar_empresa(
            empresa
        )

        return {
            "message": "Empresa cadastrada com sucesso",
            "id": id_empresa
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[EmpresaResponse],
    status_code=status.HTTP_200_OK
)
def listar_empresas(
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):
    exigir_coordenador(usuario)

    return empresa_service.listar_empresas()


@router.get(
    "/{id_empresa}",
    response_model=EmpresaResponse,
    status_code=status.HTTP_200_OK
)
def buscar_empresa_por_id(
    id_empresa: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    try:
        return empresa_service.buscar_empresa_por_id(
            id_empresa=id_empresa,
            usuario=usuario
        )

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Empresa não encontrada":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )


@router.put(
    "/{id_empresa}",
    status_code=status.HTTP_200_OK
)
def atualizar_empresa(
    id_empresa: int,
    empresa: EmpresaUpdate,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    try:
        empresa_service.atualizar_empresa(
            id_empresa=id_empresa,
            empresa=empresa,
            usuario=usuario
        )

        return {
            "message": "Empresa atualizada com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Empresa não encontrada":
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
            "Este email já está cadastrado no Scripta",
            "Este CNPJ já está cadastrado no Scripta"
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
    "/{id_empresa}",
    status_code=status.HTTP_200_OK
)
def deletar_empresa(
    id_empresa: int,
    usuario: UsuarioAutenticado = Depends(
        obter_usuario_logado
    )
):

    exigir_coordenador(usuario)

    try:
        empresa_service.deletar_empresa(
            id_empresa=id_empresa,
            coordenador_id=usuario.id
        )

        return {
            "message": "Empresa removida com sucesso"
        }

    except ValueError as e:
        mensagem = str(e)

        if mensagem == "Empresa não encontrada":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensagem
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )
