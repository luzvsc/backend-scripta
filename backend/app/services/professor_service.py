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

        campos_permitidos = {
            "area_atuacao",
            "senha",
            "confirmar_senha"
        }

    elif usuario.perfil == "coordenador":
        campos_permitidos = {
            "nome",
            "email",
            "area_atuacao",
            "senha",
            "confirmar_senha"
        }

    else:
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

    novo_email = dados.get("email")

    if novo_email is not None:
        novo_email = str(
            novo_email
        ).strip().lower()

        professor_email = (
            professor_repository
            .buscar_por_email(
                novo_email
            )
        )

        if (
            professor_email
            and professor_email["id"]
            != id_professor
        ):
            raise ValueError(
                "Este email já está cadastrado no Scripta"
            )

        dados["email"] = novo_email

    dados_alterados = {
        campo: valor
        for campo, valor in dados.items()
        if (
            campo == "senha"
            or valor
            != professor_existente.get(campo)
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
        professor_repository
        .atualizar_professor(
            id_professor=id_professor,
            dados=dados_alterados
        )
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar o professor"
        )

    if usuario.perfil == "coordenador":
        campos = ", ".join(
            dados_alterados.keys()
        )

        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="UPDATE",
            entidade="professores",
            registro_id=id_professor,
            detalhes=(
                "Cadastro do professor atualizado. "
                f"Campos alterados: {campos}"
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