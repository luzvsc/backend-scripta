import sys
import os

# Garante que o Python encontre a pasta 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database.database import SessionLocal
from app.models.models import Alunos

def testar_conexao_e_modelos():
    print("🔄 Iniciando teste de conexão e modelos...")
    session = SessionLocal()
    try:
        # Tenta fazer uma consulta simples na tabela de alunos
        quantidade_alunos = session.query(Alunos).count()
        print("✅ Sucesso! O FastAPI conseguiu ler os modelos e acessar o MySQL.")
        print(f"📊 Quantidade de alunos cadastrados no banco: {quantidade_alunos}")
    except Exception as error:
        print("❌ Erro encontrado! Algo deu errado na conexão ou nos modelos:")
        print(error)
    finally:
        session.close()

if __name__ == "__main__":
    testar_conexao_e_modelos()