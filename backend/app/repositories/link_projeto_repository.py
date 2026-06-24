from typing import Any
from app.database.database import get_connection


def criar_link(
    projeto_id: int,
    url: str,
    descricao: str | None
) -> int:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO links_projeto (
                projeto_id,
                url,
                descricao
            )
            VALUES (%s, %s, %s)
            """,
            (
                projeto_id,
                url,
                descricao
            )
        )

        conn.commit()

        id_link = cursor.lastrowid

        if id_link is None:
            raise RuntimeError(
                "Não foi possível obter o ID do link"
            )

        return int(id_link)

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def buscar_por_id(id_link: int) -> dict[str, Any] | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                projeto_id,
                url,
                descricao
            FROM links_projeto
            WHERE id = %s
            """,
            (id_link,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_por_projeto(projeto_id: int) -> list[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                projeto_id,
                url,
                descricao
            FROM links_projeto
            WHERE projeto_id = %s
            ORDER BY id DESC
            """,
            (projeto_id,)
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def atualizar_link(id_link: int, dados: dict[str, Any]) -> bool:

    campos_permitidos = {
        "url",
        "descricao"
    }

    campos: list[str] = []
    valores: list[Any] = []

    for campo, valor in dados.items():
        if campo in campos_permitidos:
            campos.append(f"{campo} = %s")
            valores.append(valor)

    if not campos:
        return False

    valores.append(id_link)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            UPDATE links_projeto
            SET {", ".join(campos)}
            WHERE id = %s
            """,
            tuple(valores)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def deletar_link(id_link: int) -> bool:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM links_projeto
            WHERE id = %s
            """,
            (id_link,)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()