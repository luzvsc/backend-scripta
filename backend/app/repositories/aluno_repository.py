from app.database.database import get_connection
from typing import Optional, Any

def buscar_por_email(email: str) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE email = %s", (email,))
        aluno = cursor.fetchone()
        return aluno
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_id(id_aluno: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE id = %s", (id_aluno,))
        aluno = cursor.fetchone()
        return aluno
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_aluno(nome: str, email: str, senha: str, curso: str) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, email, senha, curso) VALUES (%s, %s, %s, %s)", (nome, email, senha, curso))
        conn.commit()
        id_aluno = cursor.lastrowid
        return id_aluno
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_alunos() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        alunos = list(cursor.fetchall())
        return alunos
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_aluno(id_aluno: int, dados: dict) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        campos = []
        valores = []
        for chave, valor in dados.items():
            campos.append(f"{chave} = %s")
            valores.append(valor)
        
        if not campos:
            return False

        valores.append(id_aluno)
        sql = f"UPDATE alunos SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        aluno_atualizado = cursor.rowcount > 0
        return aluno_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deletar_aluno(id_aluno: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
        conn.commit()
        aluno_deletado = cursor.rowcount > 0
        return aluno_deletado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()