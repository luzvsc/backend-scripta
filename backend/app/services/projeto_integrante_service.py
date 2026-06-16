from app.models.projeto_integrante import ProjetoIntegranteCreate
import app.repositories.projeto_integrante_repository as integrante_repository
import app.services.projeto_service as projeto_service
import app.services.aluno_service as aluno_service

def adicionar_integrante(projeto_id: int, integrante: ProjetoIntegranteCreate) -> bool:
    projeto_service.buscar_projeto_por_id(projeto_id)
    aluno_service.buscar_aluno_por_id(integrante.aluno_id)

    sucesso = integrante_repository.adicionar_integrante(
        projeto_id=projeto_id,
        aluno_id=integrante.aluno_id
    )

    if not sucesso:
        raise ValueError("Não foi possível adicionar o integrante. Verifique se o aluno já faz parte do projeto.")
    
    return True

def listar_integrantes(projeto_id: int) -> list[dict]:
    projeto_service.buscar_projeto_por_id(projeto_id)
    integrantes = integrante_repository.listar_integrantes(projeto_id)
    return integrantes
