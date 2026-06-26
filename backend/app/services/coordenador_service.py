from app.core.security import gerar_hash
from app.models.auth import UsuarioAutenticado
from app.models.coordenador import CoordenadorUpdate
import app.repositories.coordenador_repository as coordenador_repository
import app.services.logs_sistema_service as logs_sistema_service


def buscar_coordenador_por_id(id_coordenador: int, usuario: UsuarioAutenticado) -> dict:
    
    coordenador = coordenador_repository.buscar_por_id(id_coordenador)

    if not coordenador:
        raise ValueError(
            "Coordenador não encontrado"
        )

    if (
        usuario.perfil != "coordenador"
        or usuario.id != id_coordenador
    ):
        raise ValueError(
            "Você só pode visualizar o próprio cadastro"
        )

    return coordenador


def atualizar_coordenador(
    id_coordenador: int,
    coordenador: CoordenadorUpdate,
    usuario: UsuarioAutenticado
) -> bool:
    
    coordenador_existente = (coordenador_repository.buscar_por_id(id_coordenador))

    if not coordenador_existente:
        raise ValueError(
            "Coordenador não encontrado"
        )

    if (
        usuario.perfil != "coordenador"
        or usuario.id != id_coordenador
    ):
        raise ValueError(
            "Você só pode alterar o próprio cadastro"
        )

    dados = coordenador.model_dump(exclude_unset=True)

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    nova_senha = dados.get("senha")

    if not nova_senha:
        raise ValueError(
            "Nenhuma senha informada para atualização"
        )

    senha_hash = gerar_hash(
        nova_senha
    )

    resultado = coordenador_repository.atualizar_senha(
        id_coordenador=id_coordenador,
        senha=senha_hash
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar a senha "
            "do coordenador"
        )

    logs_sistema_service.registrar_acao(
        coordenador_id=usuario.id,
        acao="UPDATE",
        entidade="coordenadores",
        registro_id=id_coordenador,
        detalhes=(
            "Coordenador alterou a própria senha"
        )
    )

    return True