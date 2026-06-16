from app.database.database import get_connection
from typing import Optional, Any

def criar_contato(empresa_id: int, aluno_id: int, assunto: str, mensagem: str) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contatos_empresa (empresa_id, aluno_id, assunto, mensagem) VALUES (%s, %s, %s, %s)", 
            (empresa_id, aluno_id, assunto, mensagem)
        )
        conn.commit()
        id_contato = cursor.lastrowid
        return id_contato
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_por_id(id_contato: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contatos_empresa WHERE id = %s", (id_contato,))
        contato = cursor.fetchone()
        return contato
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_por_aluno_id(aluno_id: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contatos_empresa WHERE aluno_id = %s ORDER BY data_envio DESC", (aluno_id,))
        contatos = list(cursor.fetchall())
        return contatos
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
