from app.database.database import get_connection
from typing import Any

def buscar_por_id(id_projeto: int) -> dict | None:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                p.*,
                a.nome AS aluno_responsavel,
                prof.nome AS professor_orientador
            FROM projetos p
            JOIN alunos a
                ON p.aluno_responsavel_id = a.id
            JOIN professores prof
                ON p.professor_orientador_id = prof.id
            WHERE p.id = %s
            """,
            (id_projeto,)
        )
        projeto = cursor.fetchone()
        return projeto
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_projeto(
    titulo: str,
    descricao: str,
    curso: str,
    turma: str,
    semestre: str,
    area_conhecimento: str,
    aluno_responsavel_id: int,
    professor_orientador_id: int
) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projetos (titulo, descricao, curso, turma, semestre, area_conhecimento, aluno_responsavel_id, professor_orientador_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (titulo, descricao, curso, turma, semestre,
             area_conhecimento, aluno_responsavel_id, professor_orientador_id)
        )
        conn.commit()
        id_projeto = cursor.lastrowid
        return id_projeto
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_projetos() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
        """
        SELECT
            p.id,
            p.titulo,
            p.status,
            a.nome AS aluno_responsavel,
            prof.nome AS professor_orientador
        FROM projetos p
        JOIN alunos a
            ON p.aluno_responsavel_id = a.id
        JOIN professores prof
            ON p.professor_orientador_id = prof.id
        """
)
        projetos = list(cursor.fetchall())
        return projetos
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_projeto(id_projeto: int, dados: dict[str, Any]) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for chave, valor in dados.items():
            campos.append(f"{chave} = %s")
            valores.append(valor)

        if not campos:
            return False

        valores.append(id_projeto)
        sql = f"UPDATE projetos SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        projeto_atualizado = cursor.rowcount > 0
        return projeto_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def deletar_projeto(id_projeto: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projetos WHERE id = %s", (id_projeto,))
        conn.commit()
        projeto_deletado = cursor.rowcount > 0
        return projeto_deletado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_titulo_turma_semestre(titulo: str, turma: str, semestre: str) -> dict | None:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id
            FROM projetos
            WHERE titulo = %s
            AND turma = %s
            AND semestre = %s
            LIMIT 1
            """,
            (titulo, turma, semestre)
        )
        projeto = cursor.fetchone()
        return projeto
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_status_projeto(projeto_id: int, status: str) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE projetos SET status = %s WHERE id = %s", (status, projeto_id))
        conn.commit()
        projeto_atualizado = cursor.rowcount > 0
        return projeto_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_projetos_por_perfil(usuario_id: int, perfil: str) -> list[dict]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if perfil == "coordenador":
            cursor.execute(
                """
                SELECT
                    p.*,
                    a.nome AS aluno_responsavel,
                    prof.nome AS professor_orientador
                FROM projetos p
                JOIN alunos a
                    ON p.aluno_responsavel_id = a.id
                JOIN professores prof
                    ON p.professor_orientador_id = prof.id
                ORDER BY p.id DESC
                """
            )

        elif perfil == "professor":
            cursor.execute(
                """
                SELECT
                    p.*,
                    a.nome AS aluno_responsavel,
                    prof.nome AS professor_orientador
                FROM projetos p
                JOIN alunos a
                    ON p.aluno_responsavel_id = a.id
                JOIN professores prof
                    ON p.professor_orientador_id = prof.id
                WHERE p.status IN (
                    'submetido',
                    'em_avaliacao',
                    'aprovado',
                    'reprovado'
                )
                ORDER BY p.id DESC
                """
            )

        elif perfil == "empresa":
            cursor.execute(
                """
                SELECT
                    p.*,
                    a.nome AS aluno_responsavel,
                    prof.nome AS professor_orientador
                FROM projetos p
                JOIN alunos a
                    ON p.aluno_responsavel_id = a.id
                JOIN professores prof
                    ON p.professor_orientador_id = prof.id
                WHERE p.status = 'aprovado'
                AND EXISTS (
                    SELECT 1
                    FROM portfolios pf
                    WHERE pf.projeto_id = p.id
                        AND pf.visibilidade = 'publico'
                ORDER BY p.id DESC
                """
            )

        elif perfil == "aluno":
            cursor.execute(
                """
                SELECT DISTINCT
                    p.*,
                    a.nome AS aluno_responsavel,
                    prof.nome AS professor_orientador
                FROM projetos p
                JOIN alunos a
                    ON p.aluno_responsavel_id = a.id
                JOIN professores prof
                    ON p.professor_orientador_id = prof.id
                WHERE p.aluno_responsavel_id = %s
                   OR EXISTS (
                        SELECT 1
                        FROM projeto_integrantes pi
                        WHERE pi.projeto_id = p.id
                          AND pi.aluno_id = %s
                   )
                ORDER BY p.id DESC
                """,
                (
                    usuario_id,
                    usuario_id
                )
            )

        else:
            return []

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def pode_visualizar_projeto(
    projeto_id: int,
    usuario_id: int,
    perfil: str
) -> bool:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if perfil == "coordenador":
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM projetos
                    WHERE id = %s
                ) AS permitido
                """,
                (projeto_id,)
            )

        elif perfil == "professor":
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM projetos
                    WHERE id = %s
                      AND status IN (
                          'submetido',
                          'em_avaliacao',
                          'aprovado',
                          'reprovado'
                      )
                ) AS permitido
                """,
                (projeto_id,)
            )

        elif perfil == "empresa":
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM projetos p
                    WHERE p.id = %s
                    AND p.status = 'aprovado'
                    AND EXISTS (
                        SELECT 1
                        FROM portfolios pf
                        WHERE pf.projeto_id = p.id
                            AND pf.visibilidade = 'publico'
                    )
                ) AS permitido
                """,
                (projeto_id,)
            )

        elif perfil == "aluno":
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM projetos p
                    WHERE p.id = %s
                      AND (
                          EXISTS (
                              SELECT 1
                              FROM projeto_integrantes pi
                              WHERE pi.projeto_id = p.id
                                AND pi.aluno_id = %s
                          )
                          OR (
                              p.status = 'aprovado'
                                AND EXISTS (
                                    SELECT 1
                                    FROM portfolios pf
                                    WHERE pf.projeto_id = p.id
                                    AND pf.visibilidade IN (
                                        'publico',
                                        'apenas_senac'
                                    )
                                )
                          )
                      )
                ) AS permitido
                """,
                (
                    projeto_id,
                    usuario_id
                )
            )

        else:
            return False

        resultado = cursor.fetchone()

        return bool(
            resultado
            and resultado["permitido"]
        )

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def listar_projetos_exploraveis() -> list[dict[str, Any]]:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT
                p.id,
                p.titulo,
                p.curso,
                p.turma,
                p.semestre,
                p.area_conhecimento,
                p.status,
                a.nome AS aluno_responsavel,
                prof.nome AS professor_orientador
            FROM projetos p
            JOIN alunos a
                ON a.id = p.aluno_responsavel_id
            JOIN professores prof
                ON prof.id = p.professor_orientador_id
            WHERE p.status = 'aprovado'
              AND EXISTS (
                  SELECT 1
                  FROM portfolios pf
                  WHERE pf.projeto_id = p.id
                    AND pf.visibilidade IN (
                        'publico',
                        'apenas_senac'
                    )
              )
            ORDER BY p.id DESC
            """
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
