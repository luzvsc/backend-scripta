from app.core.security import gerar_hash
from app.models.auth import UsuarioAutenticado
from app.models.empresa import (
    EmpresaCreate,
    EmpresaUpdate
)
import app.repositories.empresa_repository as empresa_repository
import app.services.logs_sistema_service as logs_sistema_service


def cadastrar_empresa(empresa: EmpresaCreate) -> int:
    
    empresa_email = empresa_repository.buscar_por_email(str(empresa.email_contato))

    if empresa_email:
        raise ValueError(
            "Este email já está cadastrado no Scripta"
        )

    empresa_cnpj = empresa_repository.buscar_por_cnpj(empresa.cnpj)

    if empresa_cnpj:
        raise ValueError(
            "Este CNPJ já está cadastrado no Scripta"
        )

    senha_hash = gerar_hash(empresa.senha)

    return empresa_repository.criar_empresa(
        nome_empresa=empresa.nome_empresa,
        email_contato=str(empresa.email_contato),
        senha=senha_hash,
        cnpj=empresa.cnpj,
        setor=empresa.setor
    )


def buscar_empresa_por_email(email_contato: str) -> dict:
    
    empresa = empresa_repository.buscar_por_email(email_contato)

    if not empresa:
        raise ValueError(
            "Empresa não encontrada"
        )

    return empresa


def buscar_empresa_por_id(id_empresa: int, usuario: UsuarioAutenticado) -> dict:

    empresa = empresa_repository.buscar_por_id(id_empresa)

    if not empresa:
        raise ValueError(
            "Empresa não encontrada"
        )

    if usuario.perfil == "coordenador":
        return empresa

    if (
        usuario.perfil == "empresa"
        and usuario.id == id_empresa
    ):
        return empresa

    raise ValueError(
        "Você não tem permissão para visualizar "
        "este cadastro"
    )


def listar_empresas() -> list[dict]:

    return empresa_repository.listar_empresas()


def atualizar_empresa(
    id_empresa: int,
    empresa: EmpresaUpdate,
    usuario: UsuarioAutenticado
) -> bool:

    empresa_existente = (
        empresa_repository.buscar_por_id(
            id_empresa
        )
    )

    if not empresa_existente:
        raise ValueError(
            "Empresa não encontrada"
        )

    if usuario.perfil == "empresa":
        if usuario.id != id_empresa:
            raise ValueError(
                "Você só pode alterar o próprio cadastro"
            )

        campos_permitidos = {
            "email_contato",
            "setor",
            "senha",
            "confirmar_senha"
        }

    elif usuario.perfil == "coordenador":
        campos_permitidos = {
            "nome_empresa",
            "cnpj",
            "email_contato",
            "setor",
            "senha",
            "confirmar_senha"
        }

    else:
        raise ValueError(
            "Você não tem permissão para alterar "
            "este cadastro"
        )

    dados = empresa.model_dump(
        exclude_unset=True
    )

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    campos_nao_permitidos = (
        set(dados)
        - campos_permitidos
    )

    if campos_nao_permitidos:
        raise ValueError(
            "Você não tem permissão para alterar "
            "estes campos"
        )

    dados.pop(
        "confirmar_senha",
        None
    )

    novo_email = dados.get(
        "email_contato"
    )

    if novo_email is not None:
        novo_email = str(
            novo_email
        ).strip().lower()

        empresa_email = (
            empresa_repository.buscar_por_email(
                novo_email
            )
        )

        if (
            empresa_email
            and empresa_email["id"]
            != id_empresa
        ):
            raise ValueError(
                "Este email já está cadastrado no Scripta"
            )

        dados["email_contato"] = (
            novo_email
        )

    novo_cnpj = dados.get("cnpj")

    if novo_cnpj:
        empresa_cnpj = (
            empresa_repository.buscar_por_cnpj(
                novo_cnpj
            )
        )

        if (
            empresa_cnpj
            and empresa_cnpj["id"]
            != id_empresa
        ):
            raise ValueError(
                "Este CNPJ já está cadastrado no Scripta"
            )

    dados_alterados = {
        campo: valor
        for campo, valor in dados.items()
        if (
            campo == "senha"
            or valor
            != empresa_existente.get(campo)
        )
    }

    if not dados_alterados:
        raise ValueError(
            "Nenhuma alteração identificada"
        )

    nova_senha = dados_alterados.get(
        "senha"
    )

    if nova_senha:
        dados_alterados["senha"] = (
            gerar_hash(nova_senha)
        )

    resultado = (
        empresa_repository.atualizar_empresa(
            id_empresa=id_empresa,
            dados=dados_alterados
        )
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar a empresa"
        )

    if usuario.perfil == "coordenador":
        campos = ", ".join(
            dados_alterados.keys()
        )

        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="UPDATE",
            entidade="empresas",
            registro_id=id_empresa,
            detalhes=(
                "Cadastro da empresa atualizado. "
                f"Campos alterados: {campos}"
            )
        )

    return True


def deletar_empresa(id_empresa: int, coordenador_id: int) -> bool:

    empresa = empresa_repository.buscar_por_id(id_empresa)

    if not empresa:
        raise ValueError(
            "Empresa não encontrada"
        )

    resultado = empresa_repository.deletar_empresa(id_empresa)

    if not resultado:
        raise ValueError(
            "Não foi possível remover a empresa. "
            "Verifique se existem registros vinculados."
        )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="DELETE",
        entidade="empresas",
        registro_id=id_empresa,
        detalhes=(
            f"Empresa '{empresa['nome_empresa']}' removida"
        )
    )

    return True