from typing import Any, Optional
from pymysql.err import IntegrityError
from app.database.database import get_connection


def buscar_por_email(email: str) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # O hash da senha é necessário para a autenticação.
        cursor.execute(
            """
            SELECT *
            FROM professores
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


def buscar_por_id(id_professor: int) -> Optional[dict[str, Any]]:

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
                email,
                area_atuacao
            FROM professores
            WHERE id = %s
            """,
            (id_professor,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def criar_professor(
    nome: str,
    email: str,
    senha: str,
    area_atuacao: Optional[str]
) -> int:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO professores (
                nome,
                email,
                senha,
                area_atuacao
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                nome,
                email,
                senha,
                area_atuacao
            )
        )

        conn.commit()

        id_professor = cursor.lastrowid

        if id_professor is None:
            raise RuntimeError(
                "Não foi possível obter o ID do professor"
            )

        return int(id_professor)

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

        cursor.execute(
            """
            SELECT
                id,
                nome,
                email,
                area_atuacao
            FROM professores
            ORDER BY nome
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_opcoes_orientadores() -> list[dict[str, Any]]:

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
                area_atuacao
            FROM professores
            ORDER BY nome
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_senha(id_professor: int, senha: str) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE professores
            SET senha = %s
            WHERE id = %s
            """,
            (
                senha,
                id_professor
            )
        )

        conn.commit()

        return cursor.rowcount > 0

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

        cursor.execute(
            """
            DELETE FROM professores
            WHERE id = %s
            """,
            (id_professor,)
        )

        conn.commit()

        return cursor.rowcount > 0

    except IntegrityError:
        if conn:
            conn.rollback()

        return False

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()