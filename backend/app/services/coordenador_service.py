from app.models.coordenador import CoordenadorUpdate, CoordenadorLogin
from app.models.projeto import ProjetoStatusUpdate
import app.repositories.coordenador_repository as coordenador_repository
from app.core.security import verificar_senha
from app.core.jwt_handler import criar_access_token
import app.services.projeto_service as projeto_service
import app.services.certificado_service as certificado_service
import app.services.logs_sistema_service as logs_sistema_service


def buscar_coordenador_por_id(id_coordenador: int) -> dict:
    coordenador = coordenador_repository.buscar_por_id(id_coordenador)
    if not coordenador:
        raise ValueError("Coordenador não encontrado")
    return coordenador


def listar_coordenadores() -> list[dict]:
    coordenadores = coordenador_repository.listar_coordenadores()
    return coordenadores



def atualizar_coordenador(id_coordenador: int, coordenador: CoordenadorUpdate) -> bool:
    coordenador_existente = coordenador_repository.buscar_por_id(id_coordenador)
    if not coordenador_existente:
        raise ValueError("Coordenador não encontrado")
 
    dados = coordenador.model_dump(exclude_unset=True)
    if not dados:
        raise ValueError("Nenhum dado informado para atualização")
 
    resultado = coordenador_repository.atualizar_coordenador(id_coordenador, dados)
 
    # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="UPDATE",
        entidade="coordenadores",
        registro_id=id_coordenador,
        detalhes="Coordenador atualizado"
    )
 
    return resultado

def login_coordenador(login: CoordenadorLogin) -> str:
    coordenador = coordenador_repository.buscar_por_email(login.email)

    if not coordenador:
        raise ValueError("Email ou senha inválidos")

    senha_valida = verificar_senha(
        login.senha,
        coordenador["senha"]
    )

    if not senha_valida:
        raise ValueError("Email ou senha inválidos")

    token = criar_access_token(
        {
            "sub": str(coordenador["id"]),
            "tipo": "coordenador"
        }
    )

    return token

def aprovar_projeto(coordenador_id: int, id_projeto: int) -> bool:

    status_update = ProjetoStatusUpdate(status="aprovado")
    projeto_service.atualizar_status_projeto(id_projeto, status_update)

    certificado_service.emitir_certificados_por_projeto(id_projeto)

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="UPDATE",
        entidade="projetos",
        registro_id=id_projeto,
        detalhes="Projeto aprovado e certificados emitidos automaticamente"
    )

    return True