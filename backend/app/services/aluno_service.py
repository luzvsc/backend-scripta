from app.models.aluno import AlunoCreate, AlunoUpdate, AlunoLogin
import app.repositories.aluno_repository as aluno_repository
from app.core.security import gerar_hash, verificar_senha
from app.core.jwt_handler import criar_access_token
import app.services.logs_sistema_service as logs_sistema_service


def cadastrar_aluno(aluno: AlunoCreate):
    aluno_existente = aluno_repository.buscar_por_email(aluno.email)
    if aluno_existente:
        raise ValueError("Este email já está cadastrado no Scripta")
    
    senha_hash = gerar_hash(aluno.senha)

    id_aluno = aluno_repository.criar_aluno(nome=aluno.nome,
                                            email=aluno.email,
                                            senha=senha_hash,
                                            curso=aluno.curso)
    return id_aluno


def buscar_aluno_por_email(email: str) -> dict:
    aluno = aluno_repository.buscar_por_email(email)
    if not aluno:
        raise ValueError("Aluno não encontrado")
    return aluno


def buscar_aluno_por_id(id_aluno: int) -> dict:
    aluno = aluno_repository.buscar_por_id(id_aluno)
    if not aluno:
        raise ValueError("Aluno não encontrado")
    return aluno


def listar_alunos() -> list[dict]:
    alunos = aluno_repository.listar_alunos()
    return alunos


def deletar_aluno(id_aluno: int) -> bool:
    deleted = aluno_repository.deletar_aluno(id_aluno)
    if not deleted:
        raise ValueError("Aluno não encontrado")
 
    # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="DELETE",
        entidade="alunos",
        registro_id=id_aluno,
        detalhes="Aluno removido"
    )
 
    return True


def atualizar_aluno(id_aluno: int, aluno: AlunoUpdate) -> bool:
    aluno_existente = aluno_repository.buscar_por_id(id_aluno)
    if not aluno_existente:
        raise ValueError("Aluno não encontrado")
    
    dados = aluno.model_dump(exclude_unset=True)
    if not dados:
        raise ValueError("Nenhum dado informado para atualização")
    
    resultado = aluno_repository.atualizar_aluno(id_aluno, dados)
 
    # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="UPDATE",
        entidade="alunos",
        registro_id=id_aluno,
        detalhes="Aluno atualizado"
    )
 
    return resultado


def login_aluno(login: AlunoLogin) -> str:
    aluno = aluno_repository.buscar_por_email(login.email)

    if not aluno:
        raise ValueError("Email ou senha inválidos")
    
    senha_valida = verificar_senha(
        login.senha,
        aluno["senha"]
    )

    if not senha_valida:
        raise ValueError("Email ou senha inválidos")

    token = criar_access_token(
        {
            "sub": str(aluno["id"]),
            "tipo": "aluno"
        }
    )

    return token