from app.database.database import get_connection
from typing import Any
from pymysql.err import IntegrityError

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

def listar_integrantes(projeto_id: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                pi.projeto_id,
                a.id AS aluno_id,
                a.nome
            FROM projeto_integrantes pi
            JOIN alunos a
                ON pi.aluno_id = a.id
            WHERE pi.projeto_id = %s
            """,
            (projeto_id,)
        )

        integrantes = list(cursor.fetchall())
        return integrantes
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_projeto_e_aluno(projeto_id: int, aluno_id: int) -> dict | None:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
            projeto_id,
            aluno_id
            FROM projeto_integrantes
            WHERE projeto_id = %s
            AND aluno_id = %s
            """,
            (projeto_id, aluno_id)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def remover_integrante(projeto_id: int, aluno_id: int) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM projeto_integrantes
            WHERE projeto_id = %s
              AND aluno_id = %s
            """,
            (
                projeto_id,
                aluno_id
            )
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()