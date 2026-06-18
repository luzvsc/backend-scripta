from app.database.database import get_connection


def buscar_por_id(id_versao: int) -> dict | None:
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            vp.*,
            p.titulo AS projeto_titulo
        FROM versoes_projeto vp
        JOIN projetos p
            ON vp.projeto_id = p.id
        WHERE vp.id = %s
            """,
            (id_versao,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_versao(
    projeto_id: int,
    titulo_na_epoca: str,
    descricao_na_epoca: str,
    quem_alterou_tipo: str,
    quem_alterou_id: int
) -> int:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO versoes_projeto
            (
                projeto_id,
                titulo_na_epoca,
                descricao_na_epoca,
                quem_alterou_tipo,
                quem_alterou_id
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                projeto_id,
                titulo_na_epoca,
                descricao_na_epoca,
                quem_alterou_tipo,
                quem_alterou_id
            )
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_versoes() -> list[dict]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                vp.*,
                p.titulo AS projeto_titulo
            FROM versoes_projeto vp
            JOIN projetos p
                ON vp.projeto_id = p.id
            ORDER BY vp.data_alteracao DESC
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_por_projeto(projeto_id: int) -> list[dict]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            vp.*,
            p.titulo AS projeto_titulo
        FROM versoes_projeto vp
        JOIN projetos p
            ON vp.projeto_id = p.id
        WHERE vp.projeto_id = %s
        ORDER BY vp.data_alteracao DESC
            """,
            (projeto_id,)
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()