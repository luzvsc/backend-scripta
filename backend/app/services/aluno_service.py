from app.core.security import gerar_hash
from app.models.aluno import (
    AlunoCreate,
    AlunoUpdate
)
from app.models.auth import UsuarioAutenticado
import app.repositories.aluno_repository as aluno_repository
import app.services.logs_sistema_service as logs_sistema_service


def cadastrar_aluno(aluno: AlunoCreate) -> int:
    
    aluno_existente = aluno_repository.buscar_por_email(str(aluno.email))

    if aluno_existente:
        raise ValueError(
            "Este email já está cadastrado no Scripta"
        )

    senha_hash = gerar_hash(aluno.senha)

    return aluno_repository.criar_aluno(
        nome=aluno.nome,
        email=str(aluno.email),
        senha=senha_hash,
        curso=aluno.curso
    )


def buscar_aluno_por_email(email: str) -> dict:

    aluno = aluno_repository.buscar_por_email(email)

    if not aluno:
        raise ValueError(
            "Aluno não encontrado"
        )

    return aluno


def buscar_aluno_por_id(id_aluno: int, usuario: UsuarioAutenticado) -> dict:
        
    aluno = aluno_repository.buscar_por_id(id_aluno)

    if not aluno:
        raise ValueError(
            "Aluno não encontrado"
        )

    if usuario.perfil == "coordenador":
        return aluno

    if (
        usuario.perfil == "aluno"
        and usuario.id == id_aluno
    ):
        return aluno

    raise ValueError(
        "Você não tem permissão para visualizar "
        "este cadastro"
    )


def listar_alunos() -> list[dict]:

    return aluno_repository.listar_alunos()


def atualizar_aluno(
    id_aluno: int,
    aluno: AlunoUpdate,
    usuario: UsuarioAutenticado
) -> bool:

    aluno_existente = (
        aluno_repository.buscar_por_id(
            id_aluno
        )
    )

    if not aluno_existente:
        raise ValueError(
            "Aluno não encontrado"
        )

    if usuario.perfil == "aluno":
        if usuario.id != id_aluno:
            raise ValueError(
                "Você só pode alterar o próprio cadastro"
            )

        campos_permitidos = {
            "senha",
            "confirmar_senha",
            "linkedin_url",
            "github_url",
            "competencias"
        }

    elif usuario.perfil == "coordenador":
        campos_permitidos = {
            "nome",
            "email",
            "matricula",
            "curso",
            "turma",
            "semestre_ingresso",
            "linkedin_url",
            "github_url",
            "competencias",
            "senha",
            "confirmar_senha"
        }

    else:
        raise ValueError(
            "Você não tem permissão para alterar "
            "este cadastro"
        )

    dados = aluno.model_dump(
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

        aluno_email = (
            aluno_repository.buscar_por_email(
                novo_email
            )
        )

        if (
            aluno_email
            and aluno_email["id"]
            != id_aluno
        ):
            raise ValueError(
                "Este email já está cadastrado no Scripta"
            )

        dados["email"] = novo_email

    nova_matricula = dados.get(
        "matricula"
    )

    if nova_matricula:
        aluno_matricula = (
            aluno_repository
            .buscar_por_matricula(
                nova_matricula
            )
        )

        if (
            aluno_matricula
            and aluno_matricula["id"]
            != id_aluno
        ):
            raise ValueError(
                "Esta matrícula já está cadastrada"
            )

    dados_alterados = {
        campo: valor
        for campo, valor in dados.items()
        if (
            campo == "senha"
            or valor
            != aluno_existente.get(campo)
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
        aluno_repository.atualizar_aluno(
            id_aluno=id_aluno,
            dados=dados_alterados
        )
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar o aluno"
        )

    if usuario.perfil == "coordenador":
        campos = ", ".join(
            dados_alterados.keys()
        )

        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="UPDATE",
            entidade="alunos",
            registro_id=id_aluno,
            detalhes=(
                "Cadastro do aluno atualizado. "
                f"Campos alterados: {campos}"
            )
        )

    return True


def deletar_aluno(id_aluno: int, coordenador_id: int) -> bool:

    aluno = aluno_repository.buscar_por_id(id_aluno)

    if not aluno:
        raise ValueError(
            "Aluno não encontrado"
        )

    resultado = aluno_repository.deletar_aluno(id_aluno)

    if not resultado:
        raise ValueError(
            "Não foi possível remover o aluno. "
            "Verifique se ele possui projetos vinculados."
        )

    logs_sistema_service.registrar_acao(
        coordenador_id=coordenador_id,
        acao="DELETE",
        entidade="alunos",
        registro_id=id_aluno,
        detalhes=(
            f"Aluno '{aluno['nome']}' removido"
        )
    )

    return True