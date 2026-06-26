from typing import Any, Optional
from app.database.database import get_connection


def buscar_por_email(email: str) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # O hash da senha é necessário para autenticação.
        cursor.execute(
            """
            SELECT *
            FROM coordenadores
            WHERE email = %s
            """,
            (email,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_id(id_coordenador: int) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nome,
                email
            FROM coordenadores
            WHERE id = %s
            """,
            (id_coordenador,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_senha(id_coordenador: int, senha: str) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE coordenadores
            SET senha = %s
            WHERE id = %s
            """,
            (
                senha,
                id_coordenador
            )
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()