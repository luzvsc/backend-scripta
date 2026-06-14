from app.models.coordenador import CoordenadorCreate, CoordenadorUpdate, CoordenadorLogin
import app.repositories.coordenador_repository as coordenador_repository
from app.core.security import gerar_hash, verificar_senha
from app.core.jwt_handler import criar_access_token


def cadastrar_coordenador(coordenador: CoordenadorCreate):
    coordenador_existente = coordenador_repository.buscar_por_email(coordenador.email)
    if coordenador_existente:
        raise ValueError("Este email já está cadastrado no Scripta")

    senha_hash = gerar_hash(coordenador.senha)

    id_coordenador = coordenador_repository.criar_coordenador(
        nome=coordenador.nome,
        email=coordenador.email,
        senha=senha_hash,
        departamento=coordenador.departamento
    )
    return id_coordenador


def buscar_coordenador_por_id(id_coordenador: int) -> dict:
    coordenador = coordenador_repository.buscar_por_id(id_coordenador)
    if not coordenador:
        raise ValueError("Coordenador não encontrado")
    return coordenador


def listar_coordenadores() -> list[dict]:
    coordenadores = coordenador_repository.listar_coordenadores()
    return coordenadores


def deletar_coordenador(id_coordenador: int) -> bool:
    deleted = coordenador_repository.deletar_coordenador(id_coordenador)
    if not deleted:
        raise ValueError("Coordenador não encontrado")
    return True


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
