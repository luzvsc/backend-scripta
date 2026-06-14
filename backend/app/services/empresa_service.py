from app.models.empresa import EmpresaCreate, EmpresaUpdate, EmpresaLogin
import app.repositories.empresa_repository as empresa_repository
from app.core.security import gerar_hash, verificar_senha
from app.core.jwt_handler import criar_access_token


def cadastrar_empresa(empresa: EmpresaCreate):
    empresa_existente = empresa_repository.buscar_por_email(empresa.email_contato)
    if empresa_existente:
        raise ValueError("Este email já está cadastrado no Scripta")
    
    senha_hash = gerar_hash(empresa.senha)

    id_empresa = empresa_repository.criar_empresa(nome_empresa=empresa.nome_empresa,
                                            email_contato=empresa.email_contato,
                                            senha=senha_hash,
                                            cnpj=empresa.cnpj,
                                            setor=empresa.setor)
    return id_empresa


def buscar_empresa_por_email(email_contato: str) -> dict:
    empresa = empresa_repository.buscar_por_email(email_contato)
    if not empresa:
        raise ValueError("Empresa não encontrada")
    return empresa


def buscar_empresa_por_id(id_empresa: int) -> dict:
    empresa = empresa_repository.buscar_por_id(id_empresa)
    if not empresa:
        raise ValueError("Empresa não encontrada")
    return empresa


def listar_empresas() -> list[dict]:
    empresas = empresa_repository.listar_empresas()
    return empresas


def deletar_empresa(id_empresa: int) -> bool:
    deleted = empresa_repository.deletar_empresa(id_empresa)
    if not deleted:
        raise ValueError("Empresa não encontrada")
    return True


def atualizar_empresa(id_empresa: int, empresa: EmpresaUpdate) -> bool:
    empresa_existente = empresa_repository.buscar_por_id(id_empresa)
    if not empresa_existente:
        raise ValueError("Empresa não encontrada")
    
    dados = empresa.model_dump(exclude_unset=True)
    if not dados:
        raise ValueError("Nenhum dado informado para atualização")
    
    return empresa_repository.atualizar_empresa(id_empresa, dados)


def login_empresa(login: EmpresaLogin) -> str:
    empresa = empresa_repository.buscar_por_email(login.email_contato)

    if not empresa:
        raise ValueError("Email ou senha inválidos")
    
    senha_valida = verificar_senha(
        login.senha,
        empresa["senha"]
    )

    if not senha_valida:
        raise ValueError("Email ou senha inválidos")

    token = criar_access_token(
        {
            "sub": str(empresa["id"]),
            "tipo": "empresa"
        }
    )

    return token
