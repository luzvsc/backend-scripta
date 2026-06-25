from app.core.security import gerar_hash
from app.models.auth import UsuarioAutenticado
from app.models.professor import (
    ProfessorCreate,
    ProfessorUpdate
)
import app.repositories.professor_repository as professor_repository
import app.services.logs_sistema_service as logs_sistema_service


def cadastrar_professor(professor: ProfessorCreate) -> int:

    professor_existente = (
        professor_repository.buscar_por_email(
            str(professor.email)
        )
    )

    if professor_existente:
        raise ValueError(
            "Este email já está cadastrado no Scripta"
        )

    senha_hash = gerar_hash(professor.senha)

    return professor_repository.criar_professor(
        nome=professor.nome,
        email=str(professor.email),
        senha=senha_hash,
        area_atuacao=professor.area_atuacao
    )


def buscar_professor_por_email(email: str) -> dict:

    professor = professor_repository.buscar_por_email(email)

    if not professor:
        raise ValueError(
            "Professor não encontrado"
        )

    return professor


def buscar_professor_por_id(id_professor: int, usuario: UsuarioAutenticado) -> dict:
    
    professor = professor_repository.buscar_por_id(id_professor)

    if not professor:
        raise ValueError(
            "Professor não encontrado"
        )

    if usuario.perfil == "coordenador":
        return professor

    if (
        usuario.perfil == "professor"
        and usuario.id == id_professor
    ):
        return professor

    raise ValueError(
        "Você não tem permissão para visualizar "
        "este cadastro"
    )


def listar_professores() -> list[dict]:

    return professor_repository.listar_professores()


def listar_opcoes_orientadores() -> list[dict]:

    return professor_repository.listar_opcoes_orientadores()


def atualizar_professor(
    id_professor: int,
    professor: ProfessorUpdate,
    usuario: UsuarioAutenticado
) -> bool:
    
    professor_existente = (
        professor_repository.buscar_por_id(
            id_professor
        )
    )

    if not professor_existente:
        raise ValueError(
            "Professor não encontrado"
        )

    if usuario.perfil == "professor":
        if usuario.id != id_professor:
            raise ValueError(
                "Você só pode alterar o próprio cadastro"
            )

    elif usuario.perfil != "coordenador":
        raise ValueError(
            "Você não tem permissão para alterar "
            "este cadastro"
        )

    dados = professor.model_dump(
        exclude_unset=True
    )

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    dados.pop(
        "confirmar_senha",
        None
    )

    nova_senha = dados.get("senha")

    if not nova_senha:
        raise ValueError(
            "Nenhuma senha informada para atualização"
        )

    senha_hash = gerar_hash(nova_senha)

    resultado = professor_repository.atualizar_senha(
        id_professor=id_professor,
        senha=senha_hash
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar a senha "
            "do professor"
        )

    if usuario.perfil == "coordenador":
        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="UPDATE",
            entidade="professores",
            registro_id=id_professor,
            detalhes=(
                "Senha do professor atualizada "
                "pela coordenação"
            )
        )

    return True


def deletar_professor(id_professor: int, coordenador_id: int) -> bool:

    professor = professor_repository.buscar_por_id(id_professor)

    if not professor:
        raise ValueError(
            "Professor não encontrado"
        )

    resultado = professor_repository.deletar_professor(id_professor)

    if not resultado:
        raise ValueError(
            "Não foi possível remover o professor. "
            "Verifique se ele possui projetos ou "
            "avaliações vinculadas."
        )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="DELETE",
        entidade="professores",
        registro_id=id_professor,
        detalhes=(
            f"Professor '{professor['nome']}' removido"
        )
    )

    return True