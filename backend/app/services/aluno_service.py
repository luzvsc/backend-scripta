from app.models.aluno import AlunoCreate
import app.repositories.aluno_repository as aluno_repository
from app.core.security import gerar_hash


def cadastrar_aluno(aluno: AlunoCreate):
    aluno_existente = aluno_repository.buscar_por_email(aluno.email)
    if aluno_existente:
        raise ValueError("Aluno com este email já está cadastrado")
    
    senha_hash = gerar_hash(aluno.senha)

    id_aluno = aluno_repository.criar_aluno(nome=aluno.nome,
                                            email=aluno.email,
                                            senha=senha_hash,
                                            curso=aluno.curso)
    return id_aluno

