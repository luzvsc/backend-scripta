from app.database.database import get_connection
from typing import Optional, Any


def buscar_relatorio_projetos(curso: Optional[str] = None,
                               turma: Optional[str] = None,
                               semestre: Optional[str] = None,
                               status: Optional[str] = None) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                p.id,
                p.titulo,
                p.curso,
                p.turma,
                p.semestre,
                p.status,
                p.area_conhecimento,
                al.nome AS aluno_responsavel,
                pr.nome AS professor_orientador,
                COUNT(a.id) AS total_avaliacoes,
                AVG(a.media_geral) AS media_geral
            FROM projetos p
            JOIN alunos al ON al.id = p.aluno_responsavel_id
            JOIN professores pr ON pr.id = p.professor_orientador_id
            LEFT JOIN avaliacoes a ON a.projeto_id = p.id
        """

        condicoes = []
        valores: list[Any] = []

        if curso:
            condicoes.append("p.curso = %s")
            valores.append(curso)
        if turma:
            condicoes.append("p.turma = %s")
            valores.append(turma)
        if semestre:
            condicoes.append("p.semestre = %s")
            valores.append(semestre)
        if status:
            condicoes.append("p.status = %s")
            valores.append(status)

        if condicoes:
            sql += " WHERE " + " AND ".join(condicoes)

        sql += """
            GROUP BY p.id, p.titulo, p.curso, p.turma, p.semestre, p.status,
                     p.area_conhecimento, al.nome, pr.nome
            ORDER BY p.curso, p.turma, p.semestre, p.titulo
        """

        cursor.execute(sql, tuple(valores))
        projetos = list(cursor.fetchall())
        return projetos
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_indicadores_academicos(curso: Optional[str] = None,
                                   turma: Optional[str] = None,
                                   semestre: Optional[str] = None) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                p.curso,
                p.turma,
                p.semestre,
                COUNT(DISTINCT p.id) AS total_projetos,
                COUNT(a.id) AS total_avaliacoes,
                AVG(a.nota_inovacao) AS media_inovacao,
                AVG(a.nota_tecnica) AS media_tecnica,
                AVG(a.nota_aplicabilidade) AS media_aplicabilidade,
                AVG(a.nota_clareza) AS media_clareza,
                AVG(a.media_geral) AS media_geral
            FROM projetos p
            LEFT JOIN avaliacoes a ON a.projeto_id = p.id
        """

        condicoes = []
        valores: list[Any] = []

        if curso:
            condicoes.append("p.curso = %s")
            valores.append(curso)
        if turma:
            condicoes.append("p.turma = %s")
            valores.append(turma)
        if semestre:
            condicoes.append("p.semestre = %s")
            valores.append(semestre)

        if condicoes:
            sql += " WHERE " + " AND ".join(condicoes)

        sql += """
            GROUP BY p.curso, p.turma, p.semestre
            ORDER BY p.curso, p.turma, p.semestre
        """

        cursor.execute(sql, tuple(valores))
        indicadores = list(cursor.fetchall())
        return indicadores
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
