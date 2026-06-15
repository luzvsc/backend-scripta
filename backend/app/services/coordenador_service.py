from app.models.coordenador import CoordenadorUpdate, CoordenadorLogin
import app.repositories.coordenador_repository as coordenador_repository
from app.core.security import verificar_senha
from app.core.jwt_handler import criar_access_token


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

    return coordenador_repository.atualizar_coordenador(id_coordenador, dados)


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
