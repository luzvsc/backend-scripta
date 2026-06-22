from app.models.empresa import EmpresaCreate, EmpresaUpdate
import app.repositories.empresa_repository as empresa_repository
from app.core.security import gerar_hash
import app.services.logs_sistema_service as logs_sistema_service


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


def atualizar_empresa(id_empresa: int, empresa: EmpresaUpdate) -> bool:
    empresa_existente = empresa_repository.buscar_por_id(id_empresa)
    if not empresa_existente:
        raise ValueError("Empresa não encontrada")
    
    dados = empresa.model_dump(exclude_unset=True)
    if not dados:
        raise ValueError("Nenhum dado informado para atualização")
    
    resultado = empresa_repository.atualizar_empresa(id_empresa, dados)
 
    # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="UPDATE",
        entidade="empresas",
        registro_id=id_empresa,
        detalhes="Empresa atualizada"
    )
 
    return resultado
