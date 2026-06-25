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
    
    aluno_existente = aluno_repository.buscar_por_id(id_aluno)

    if not aluno_existente:
        raise ValueError(
            "Aluno não encontrado"
        )

    if usuario.perfil == "aluno":
        if usuario.id != id_aluno:
            raise ValueError(
                "Você só pode alterar o próprio cadastro"
            )

    elif usuario.perfil != "coordenador":
        raise ValueError(
            "Você não tem permissão para alterar "
            "este cadastro"
        )

    dados = aluno.model_dump(exclude_unset=True)

    if not dados:
        raise ValueError(
            "Nenhum dado informado para atualização"
        )

    dados.pop(
        "confirmar_senha",
        None
    )

    nova_senha = dados.get(
        "senha"
    )

    if nova_senha:
        dados["senha"] = gerar_hash(
            nova_senha
        )

    resultado = aluno_repository.atualizar_aluno(
        id_aluno=id_aluno,
        dados=dados
    )

    if not resultado:
        raise ValueError(
            "Não foi possível atualizar o aluno"
        )

    if usuario.perfil == "coordenador":
        logs_sistema_service.registrar_acao(
            coordenador_id=usuario.id,
            acao="UPDATE",
            entidade="alunos",
            registro_id=id_aluno,
            detalhes=(
                "Dados profissionais ou senha "
                "do aluno atualizados"
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