from app.database.database import get_connection
from typing import Optional, Any
import uuid


def buscar_por_id(id_certificado: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.*, a.nome AS nome_aluno, a.curso,
                   p.titulo AS titulo_projeto, p.semestre,
                   pr.nome AS nome_professor
            FROM certificados c
            JOIN alunos a ON c.aluno_id = a.id
            JOIN projetos p ON c.projeto_id = p.id
            LEFT JOIN professores pr ON p.professor_orientador_id = pr.id
            WHERE c.id = %s
            """,
            (id_certificado,)
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_aluno(id_aluno: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.*, a.nome AS nome_aluno, a.curso,
                   p.titulo AS titulo_projeto, p.semestre,
                   pr.nome AS nome_professor
            FROM certificados c
            JOIN alunos a ON c.aluno_id = a.id
            JOIN projetos p ON c.projeto_id = p.id
            LEFT JOIN professores pr ON p.professor_orientador_id = pr.id
            WHERE c.aluno_id = %s
            ORDER BY c.data_emissao DESC
            """,
            (id_aluno,)
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_projeto(id_projeto: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.*, a.nome AS nome_aluno, a.curso,
                   p.titulo AS titulo_projeto, p.semestre,
                   pr.nome AS nome_professor
            FROM certificados c
            JOIN alunos a ON c.aluno_id = a.id
            JOIN projetos p ON c.projeto_id = p.id
            LEFT JOIN professores pr ON p.professor_orientador_id = pr.id
            WHERE c.projeto_id = %s
            """,
            (id_projeto,)
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def certificado_ja_existe(id_projeto: int, id_aluno: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
             """
            SELECT id
            FROM certificados
            WHERE projeto_id = %s
            AND aluno_id = %s
            """,
            (id_projeto, id_aluno)
        )
        return cursor.fetchone() is not None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_integrantes_do_projeto(projeto_id: int) -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT
                pi.projeto_id,
                pi.aluno_id,
                a.nome
            FROM projeto_integrantes pi
            JOIN alunos a
                ON pi.aluno_id = a.id
            WHERE pi.projeto_id = %s
            """,
            (projeto_id,)
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

            
def criar_certificado(projeto_id: int, aluno_id: int) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        codigo = str(uuid.uuid4()).replace("-", "").upper()[:16]
        cursor.execute(
            """
            INSERT INTO certificados
            (
                projeto_id,
                aluno_id,
                codigo_autenticidade
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (projeto_id, aluno_id, codigo)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_certificados() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.*, a.nome AS nome_aluno, a.curso,
                   p.titulo AS titulo_projeto, p.semestre,
                   pr.nome AS nome_professor
            FROM certificados c
            JOIN alunos a ON c.aluno_id = a.id
            JOIN projetos p ON c.projeto_id = p.id
            LEFT JOIN professores pr ON p.professor_orientador_id = pr.id
            ORDER BY c.data_emissao DESC
            """
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
