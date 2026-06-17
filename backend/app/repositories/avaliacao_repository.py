from app.database.database import get_connection
from typing import Optional, Any


def buscar_por_id(id_avaliacao: int) -> dict | None:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
            a.*,
            p.titulo AS projeto_titulo,
            prof.nome AS professor_nome
        FROM avaliacoes a
        JOIN projetos p
            ON a.projeto_id = p.id
        JOIN professores prof
            ON a.professor_id = prof.id
        WHERE a.id = %s
            """, (id_avaliacao,))
        avaliacao = cursor.fetchone()
        return avaliacao
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_projeto_professor(projeto_id: int, professor_id: int) -> dict | None:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id
        FROM avaliacoes
        WHERE projeto_id = %s
        AND professor_id = %s
        LIMIT 1
            """, (projeto_id, professor_id))
        avaliacao = cursor.fetchone()
        return avaliacao
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_avaliacao(
    projeto_id: int,
    professor_id: int,
    nota_inovacao: float,
    nota_tecnica: float,
    nota_aplicabilidade: float,
    nota_clareza: float,
    media_geral: float,
    conceito: str,
    parecer_descritivo: str
) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO avaliacoes
            (
                projeto_id,
                professor_id,
                nota_inovacao,
                nota_tecnica,
                nota_aplicabilidade,
                nota_clareza,
                media_geral,
                conceito,
                parecer_descritivo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                projeto_id,
                professor_id,
                nota_inovacao,
                nota_tecnica,
                nota_aplicabilidade,
                nota_clareza,
                media_geral,
                conceito,
                parecer_descritivo
            ),
        )

        conn.commit()
        return cursor.lastrowid
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_avaliacoes() -> list[dict]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
            a.id,
            a.projeto_id,
            a.professor_id,
            a.media_geral,
            a.conceito,
            p.titulo AS projeto_titulo,
            prof.nome AS professor_nome
        FROM avaliacoes a
        JOIN projetos p
            ON a.projeto_id = p.id
        JOIN professores prof
            ON a.professor_id = prof.id
        ORDER BY a.data_avaliacao DESC
            """)
        avaliacoes = list(cursor.fetchall())
        return avaliacoes
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
            prof.nome AS professor_nome,
            p.titulo AS projeto_titulo
        FROM avaliacoes a
        JOIN professores prof
            ON a.professor_id = prof.id
        JOIN projetos p
            ON a.projeto_id = p.id
        WHERE a.projeto_id = %s
        ORDER BY a.data_avaliacao DESC
            """, (projeto_id,))
        avaliacoes = list(cursor.fetchall())
        return avaliacoes
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_avaliacao(id_avaliacao: int, dados: dict) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if not dados:
            return False

        campos = []
        valores = []
        for chave, valor in dados.items():
            campos.append(f"{chave} = %s")
            valores.append(valor)
        valores.append(id_avaliacao)

        sql = f"UPDATE avaliacoes SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()