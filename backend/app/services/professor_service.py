from app.models.professor import ProfessorCreate, ProfessorUpdate
import app.repositories.professor_repository as professor_repository
from app.core.security import gerar_hash
import app.services.logs_sistema_service as logs_sistema_service


def cadastrar_professor(professor: ProfessorCreate):
    professor_existente = professor_repository.buscar_por_email(professor.email)
    if professor_existente:
        raise ValueError("Este email já está cadastrado no Scripta")
    
    senha_hash = gerar_hash(professor.senha)

    id_professor = professor_repository.criar_professor(nome=professor.nome,
                                                        email=professor.email,
                                                        senha=senha_hash,
                                                        area_atuacao=professor.area_atuacao)
    return id_professor


def buscar_professor_por_email(email: str) -> dict:
    professor = professor_repository.buscar_por_email(email)
    if not professor:
        raise ValueError("Professor não encontrado")
    return professor


def buscar_professor_por_id(id_professor: int) -> dict:
    professor = professor_repository.buscar_por_id(id_professor)
    if not professor:
        raise ValueError("Professor não encontrado")
    return professor


def listar_professores() -> list[dict]:
    professores = professor_repository.listar_professores()
    return professores


def deletar_professor(id_professor: int) -> bool:
    deleted = professor_repository.deletar_professor(id_professor)
    if not deleted:
        raise ValueError("Professor não encontrado")
 
    # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="DELETE",
        entidade="professores",
        registro_id=id_professor,
        detalhes="Professor removido"
    )
 
    return True


def atualizar_professor(id_professor: int, professor: ProfessorUpdate) -> bool:
    professor_existente = professor_repository.buscar_por_id(id_professor)
    if not professor_existente:
        raise ValueError("Professor não encontrado")
 
    dados = professor.model_dump(exclude_unset=True)
    if not dados:
        raise ValueError("Nenhum dado informado para atualização")
    
    resultado = professor_repository.atualizar_professor(id_professor, dados)

     # TODO: substituir coordenador_id=1 quando a autenticação existir
    logs_sistema_service.registrar_acao(
        coordenador_id=1,
        acao="UPDATE",
        entidade="professores",
        registro_id=id_professor,
        detalhes="Professor atualizado"
    )

    return resultado