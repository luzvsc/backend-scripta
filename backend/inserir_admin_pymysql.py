import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_connection
from app.core.security import gerar_hash

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT id FROM coordenadores WHERE email = 'coordenacao@example.com'")
    if cursor.fetchone():
        print("Coordenador já existe no banco de dados!")
    else:
        hash_senha = gerar_hash("123456")
        cursor.execute(
            "INSERT INTO coordenadores (nome, email, senha) VALUES (%s, %s, %s)",
            ('Coordenação TI', 'coordenacao@example.com', hash_senha)
        )
        conn.commit()
        print("Coordenador inserido no banco de dados com sucesso!")
except Exception as e:
    print(f"Erro: {e}")
finally:
    cursor.close()
    conn.close()
