from app.models.contato_empresa import ContatoEmpresaCreate
import app.repositories.contato_empresa_repository as contato_repository
import app.services.aluno_service as aluno_service
import app.services.empresa_service as empresa_service


def cadastrar_contato(contato: ContatoEmpresaCreate) -> int:
    empresa_service.buscar_empresa_por_id(contato.empresa_id)
    aluno_service.buscar_aluno_por_id(contato.aluno_id)

    id_contato = contato_repository.criar_contato(
        empresa_id=contato.empresa_id,
        aluno_id=contato.aluno_id,
        assunto=contato.assunto,
        mensagem=contato.mensagem
    )
    return id_contato

def buscar_contato_por_id(id_contato: int) -> dict:
    contato = contato_repository.buscar_por_id(id_contato)
    if not contato:
        raise ValueError("Contato não encontrado")
    return contato

def buscar_contatos_por_aluno(aluno_id: int) -> list[dict]:
    contatos = contato_repository.buscar_por_aluno_id(aluno_id)
    return contatos
