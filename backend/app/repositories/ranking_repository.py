from typing import Any
from app.database.database import get_connection


def buscar_ranking(
    curso: str | None = None,
    turma: str | None = None,
    semestre: str | None = None,
    somente_publicos: bool = False
) -> list[dict[str, Any]]:
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                p.id AS projeto_id,
                p.titulo,
                p.curso,
                p.turma,
                p.semestre,
                p.area_conhecimento,
                al.nome AS aluno_responsavel,
                prof.nome AS professor_orientador,
                COUNT(av.id) AS total_avaliacoes,
                ROUND(
                    AVG(av.media_geral),
                    2
                ) AS media_geral
            FROM projetos p
            JOIN alunos al
                ON al.id = p.aluno_responsavel_id
            JOIN professores prof
                ON prof.id = p.professor_orientador_id
            JOIN avaliacoes av
                ON av.projeto_id = p.id
            WHERE p.status = 'aprovado'
        """

        condicoes: list[str] = []
        valores: list[Any] = []

        if curso:
            condicoes.append(
                "p.curso = %s"
            )
            valores.append(curso)

        if turma:
            condicoes.append(
                "p.turma = %s"
            )
            valores.append(turma)

        if semestre:
            condicoes.append(
                "p.semestre = %s"
            )
            valores.append(semestre)

        if somente_publicos:
            condicoes.append(
                """
                EXISTS (
                    SELECT 1
                    FROM portfolios pf
                    WHERE pf.projeto_id = p.id
                      AND pf.visibilidade = 'publico'
                )
                """
            )

        if condicoes:
            sql += " AND " + " AND ".join(
                condicoes
            )

        sql += """
            GROUP BY
                p.id,
                p.titulo,
                p.curso,
                p.turma,
                p.semestre,
                p.area_conhecimento,
                al.nome,
                prof.nome
            ORDER BY
                media_geral DESC,
                total_avaliacoes DESC,
                p.titulo ASC,
                p.id ASC
        """

        cursor.execute(
            sql,
            tuple(valores)
        )

        return list(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()