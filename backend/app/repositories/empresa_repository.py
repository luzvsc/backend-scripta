from typing import Any, Optional
from pymysql.err import IntegrityError
from app.database.database import get_connection


def buscar_por_email(email_contato: str) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # A senha é necessária nesta consulta para o login.
        cursor.execute(
            """
            SELECT *
            FROM empresas
            WHERE email_contato = %s
            """,
            (email_contato,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_cnpj(cnpj: str) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                cnpj
            FROM empresas
            WHERE cnpj = %s
            """,
            (cnpj,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_id(id_empresa: int) -> Optional[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nome_empresa,
                cnpj,
                email_contato,
                setor
            FROM empresas
            WHERE id = %s
            """,
            (id_empresa,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def criar_empresa(
    nome_empresa: str,
    email_contato: str,
    senha: str,
    cnpj: str,
    setor: Optional[str]
) -> int:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO empresas (
                nome_empresa,
                email_contato,
                senha,
                cnpj,
                setor
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                nome_empresa,
                email_contato,
                senha,
                cnpj,
                setor
            )
        )

        conn.commit()

        id_empresa = cursor.lastrowid

        if id_empresa is None:
            raise RuntimeError(
                "Não foi possível obter o ID da empresa"
            )

        return int(id_empresa)

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_empresas() -> list[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nome_empresa,
                cnpj,
                email_contato,
                setor
            FROM empresas
            ORDER BY nome_empresa
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_empresa(id_empresa: int, dados: dict[str, Any]) -> bool:

    campos_permitidos = {
        "email_contato",
        "setor",
        "senha"
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

    valores.append(id_empresa)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = f"""
            UPDATE empresas
            SET {", ".join(campos)}
            WHERE id = %s
        """

        cursor.execute(
            sql,
            tuple(valores)
        )

        conn.commit()

        # Considera a operação válida mesmo quando o novo
        # valor já é igual ao armazenado.
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


def deletar_empresa(id_empresa: int) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM empresas
            WHERE id = %s
            """,
            (id_empresa,)
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