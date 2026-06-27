from typing import Any

from pymysql.err import IntegrityError

from app.database.database import get_connection


def buscar_por_email(email: str) -> dict[str, Any] | None:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # A senha é necessária nesta consulta para o login.
        cursor.execute(
            """
            SELECT *
            FROM alunos
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


def buscar_por_matricula(matricula: str) -> dict[str, Any] | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                matricula
            FROM alunos
            WHERE matricula = %s
            """,
            (matricula,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_id(id_aluno: int) -> dict[str, Any] | None:

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
                matricula,
                curso,
                turma,
                semestre_ingresso,
                linkedin_url,
                github_url,
                competencias
            FROM alunos
            WHERE id = %s
            """,
            (id_aluno,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def criar_aluno(
    nome: str,
    email: str,
    senha: str,
    curso: str
) -> int:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO alunos (
                nome,
                email,
                senha,
                curso
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                nome,
                email,
                senha,
                curso
            )
        )

        conn.commit()

        id_aluno = cursor.lastrowid

        if id_aluno is None:
            raise RuntimeError(
                "Não foi possível obter o ID do aluno"
            )

        return int(id_aluno)

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

        cursor.execute(
            """
            SELECT
                id,
                nome,
                email,
                matricula,
                curso,
                turma,
                semestre_ingresso,
                linkedin_url,
                github_url,
                competencias
            FROM alunos
            ORDER BY nome
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_aluno(id_aluno: int, dados: dict[str, Any]) -> bool:

    campos_permitidos = {
    "nome",
    "email",
    "senha",
    "matricula",
    "curso",
    "turma",
    "semestre_ingresso",
    "linkedin_url",
    "github_url",
    "competencias"
    }

    campos: list[str] = []
    valores: list[Any] = []

    for chave, valor in dados.items():
        if chave in campos_permitidos:
            campos.append(
                f"{chave} = %s"
            )
            valores.append(valor)

    if not campos:
        return False

    valores.append(id_aluno)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = f"""
            UPDATE alunos
            SET {", ".join(campos)}
            WHERE id = %s
        """

        cursor.execute(
            sql,
            tuple(valores)
        )

        conn.commit()

        # O MySQL pode retornar rowcount 0 quando o valor
        # informado já era igual ao valor armazenado.
        return True

    except IntegrityError:
        if conn:
            conn.rollback()

        return False

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

        cursor.execute(
            """
            DELETE FROM alunos
            WHERE id = %s
            """,
            (id_aluno,)
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