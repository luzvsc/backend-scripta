from app.database.database import get_connection
from typing import Optional, Any


def registrar_log(
    coordenador_id: int,
    acao: str,
    entidade: str,
    registro_id: int,
    detalhes: Optional[str] = None
) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs_sistema (coordenador_id, acao, entidade, registro_id, detalhes) VALUES (%s, %s, %s, %s, %s)",
            (coordenador_id, acao, entidade, registro_id, detalhes)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_logs() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs_sistema")
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_logs_por_coordenador(coordenador_id: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM logs_sistema WHERE coordenador_id = %s",
            (coordenador_id,)
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_logs_por_entidade(entidade: str) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM logs_sistema WHERE entidade = %s",
            (entidade,)
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_log_por_id(id_log: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM logs_sistema WHERE id = %s",
            (id_log,)
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
