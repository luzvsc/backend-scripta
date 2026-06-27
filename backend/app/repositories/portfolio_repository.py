from typing import Any
from pymysql.err import IntegrityError
from app.database.database import get_connection


def criar_portfolio(
    aluno_id: int,
    projeto_id: int,
    visibilidade: str
) -> int | None:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO portfolios (
                aluno_id,
                projeto_id,
                visibilidade
            )
            VALUES (%s, %s, %s)
            """,
            (
                aluno_id,
                projeto_id,
                visibilidade
            )
        )

        conn.commit()

        id_portfolio = cursor.lastrowid

        if id_portfolio is None:
            return None

        return int(id_portfolio)

    except IntegrityError:
        if conn:
            conn.rollback()

        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_id(id_portfolio: int) -> dict[str, Any] | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                pf.id,
                pf.aluno_id,
                pf.projeto_id,
                pf.visibilidade,
                a.nome AS nome_aluno,
                p.titulo AS titulo_projeto,
                p.curso,
                p.semestre
            FROM portfolios pf
            JOIN alunos a
                ON a.id = pf.aluno_id
            JOIN projetos p
                ON p.id = pf.projeto_id
            WHERE pf.id = %s
            """,
            (id_portfolio,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_aluno_e_projeto(aluno_id: int, projeto_id: int) -> dict[str, Any] | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                aluno_id,
                projeto_id,
                visibilidade
            FROM portfolios
            WHERE aluno_id = %s
              AND projeto_id = %s
            """,
            (
                aluno_id,
                projeto_id
            )
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_por_aluno(aluno_id: int, visibilidades: tuple[str, ...] | None = None) -> list[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        consulta = """
            SELECT
                pf.id,
                pf.aluno_id,
                pf.projeto_id,
                pf.visibilidade,
                a.nome AS nome_aluno,
                p.titulo AS titulo_projeto,
                p.curso,
                p.semestre
            FROM portfolios pf
            JOIN alunos a
                ON a.id = pf.aluno_id
            JOIN projetos p
                ON p.id = pf.projeto_id
            WHERE pf.aluno_id = %s
              AND p.status = 'aprovado'
        """

        parametros: list[Any] = [aluno_id]

        if visibilidades:
            placeholders = ", ".join(
                ["%s"] * len(visibilidades)
            )

            consulta += (
                f" AND pf.visibilidade IN "
                f"({placeholders})"
            )

            parametros.extend(visibilidades)

        consulta += " ORDER BY pf.id DESC"

        cursor.execute(
            consulta,
            tuple(parametros)
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_portfolio(id_portfolio: int, visibilidade: str) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE portfolios
            SET visibilidade = %s
            WHERE id = %s
            """,
            (
                visibilidade,
                id_portfolio
            )
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def deletar_portfolio(id_portfolio: int) -> bool:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM portfolios
            WHERE id = %s
            """,
            (id_portfolio,)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_publicos() -> list[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                pf.id,
                pf.aluno_id,
                pf.projeto_id,
                pf.visibilidade,
                a.nome AS nome_aluno,
                p.titulo AS titulo_projeto,
                p.curso,
                p.semestre
            FROM portfolios pf
            JOIN alunos a
                ON a.id = pf.aluno_id
            JOIN projetos p
                ON p.id = pf.projeto_id
            WHERE pf.visibilidade = 'publico'
              AND p.status = 'aprovado'
            ORDER BY pf.id DESC
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()