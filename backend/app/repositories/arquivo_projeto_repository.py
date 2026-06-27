from app.database.database import get_connection


def buscar_por_id(id_arquivo: int) -> dict | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM arquivos_projeto
            WHERE id = %s
            """,
            (id_arquivo,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_arquivo(projeto_id: int, nome_original: str, caminho_servidor: str, tamanho_mb: float) -> int:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO arquivos_projeto
            (
                projeto_id,
                nome_original,
                caminho_servidor,
                tamanho_mb
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                projeto_id,
                nome_original,
                caminho_servidor,
                tamanho_mb
            )
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_arquivos() -> list[dict]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            a.*,
            p.titulo AS projeto_titulo
        FROM arquivos_projeto a
        JOIN projetos p
            ON a.projeto_id = p.id
        ORDER BY a.id DESC
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
            a.*,
            p.titulo AS projeto_titulo
        FROM arquivos_projeto a
        JOIN projetos p
            ON a.projeto_id = p.id
        WHERE a.projeto_id = %s
        ORDER BY a.id DESC
            """,
            (projeto_id,)
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def deletar_arquivo(id_arquivo: int) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM arquivos_projeto
            WHERE id = %s
            """,
            (id_arquivo,)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_ultima_versao(projeto_id: int) -> dict | None:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM arquivos_projeto
            WHERE projeto_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (projeto_id,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_arquivo(id_arquivo: int, dados: dict) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if not dados:
            return False

        campos = []
        valores = []

        for campo, valor in dados.items():
            campos.append(
                f"{campo} = %s"
            )
            valores.append(valor)

        valores.append(id_arquivo)

        sql = (
            "UPDATE arquivos_projeto "
            f"SET {', '.join(campos)} "
            "WHERE id = %s"
        )

        cursor.execute(
            sql,
            tuple(valores)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()