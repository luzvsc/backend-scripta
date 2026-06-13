from app.database.database import get_connection
from typing import Optional, Any

def buscar_por_email(email: str) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professores WHERE email = %s", (email,))
        professores = cursor.fetchone()
        return professores
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_id(id_professor: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professores WHERE id = %s", (id_professor,))
        professor = cursor.fetchone()
        return professor
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_professor(nome: str, email: str, senha: str, area_atuacao: Optional[str]) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO professores (nome, email, senha, area_atuacao) VALUES (%s, %s, %s, %s)", (nome, email, senha, area_atuacao))
        conn.commit()
        id_professor = cursor.lastrowid
        return id_professor
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_professores() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professores")
        professores = list(cursor.fetchall())
        return professores
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_professor(id_professor: int, dados: dict[str, Any]) -> bool:
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

        valores.append(id_professor)
        sql = f"UPDATE professores SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        professor_atualizado = cursor.rowcount > 0
        return professor_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deletar_professor(id_professor: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professores WHERE id = %s", (id_professor,))
        conn.commit()
        professor_deletado = cursor.rowcount > 0
        return professor_deletado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()