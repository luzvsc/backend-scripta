from app.models.aluno import AlunoCreate
import app.repositories.aluno_repository as aluno_repository
from app.core.security import gerar_hash
from typing import Optional
from fastapi import HTTPException


def cadastrar_aluno(aluno: AlunoCreate):
    aluno_existente = aluno_repository.buscar_por_email(aluno.email)
    if aluno_existente:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado no Scripta")
    
    senha_hash = gerar_hash(aluno.senha)

    id_aluno = aluno_repository.criar_aluno(nome=aluno.nome,
                                            email=aluno.email,
                                            senha=senha_hash,
                                            curso=aluno.curso)
    return id_aluno


def buscar_aluno_por_email(email: str) -> dict:
    aluno = aluno_repository.buscar_por_email(email)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def buscar_aluno_por_id(id_aluno: int) -> dict:
    aluno = aluno_repository.buscar_por_id(id_aluno)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def listar_alunos() -> list:
    alunos = aluno_repository.listar_alunos()
    return alunos


def deletar_aluno(id_aluno: int) -> bool:
    deleted = aluno_repository.deletar_aluno(id_aluno)
    if not deleted:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return True