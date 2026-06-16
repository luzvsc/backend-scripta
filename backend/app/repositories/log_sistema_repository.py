from app.database.database import get_connection
from typing import Optional, Any


def registrar_log(
    id_coordenador: int,
    acao: str,
    entidade: str,
    id_entidade: Optional[int] = None,
    descricao: Optional[str] = None
) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO log_sistema (id_coordenador, acao, entidade, id_entidade, descricao, data_hora)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """,
            (id_coordenador, acao, entidade, id_entidade, descricao)
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
        cursor.execute(
            """
            SELECT l.*, c.nome AS nome_coordenador
            FROM log_sistema l
            JOIN coordenadores c ON l.id_coordenador = c.id
            ORDER BY l.data_hora DESC
            """
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_logs_por_coordenador(id_coordenador: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT l.*, c.nome AS nome_coordenador
            FROM log_sistema l
            JOIN coordenadores c ON l.id_coordenador = c.id
            WHERE l.id_coordenador = %s
            ORDER BY l.data_hora DESC
            """,
            (id_coordenador,)
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
            """
            SELECT l.*, c.nome AS nome_coordenador
            FROM log_sistema l
            JOIN coordenadores c ON l.id_coordenador = c.id
            WHERE l.entidade = %s
            ORDER BY l.data_hora DESC
            """,
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
            """
            SELECT l.*, c.nome AS nome_coordenador
            FROM log_sistema l
            JOIN coordenadores c ON l.id_coordenador = c.id
            WHERE l.id = %s
            """,
            (id_log,)
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
