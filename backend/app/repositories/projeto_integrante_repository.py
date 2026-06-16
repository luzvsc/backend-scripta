from app.database.database import get_connection
from typing import Any

def adicionar_integrante(projeto_id: int, aluno_id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projeto_integrantes (projeto_id, aluno_id) VALUES (%s, %s)", 
            (projeto_id, aluno_id)
        )
        conn.commit()
        return True
    except Exception as e:
        # Pega a exceção se der erro de UNIQUE ou FK (ex: aluno já no projeto)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def listar_integrantes(projeto_id: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projeto_integrantes WHERE projeto_id = %s", (projeto_id,))
        integrantes = list(cursor.fetchall())
        return integrantes
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
