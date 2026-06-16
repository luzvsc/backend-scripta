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
            JOIN alunos a ON c.id_aluno = a.id
            JOIN projetos p ON c.id_projeto = p.id
            LEFT JOIN professores pr ON p.id_professor = pr.id
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
            JOIN alunos a ON c.id_aluno = a.id
            JOIN projetos p ON c.id_projeto = p.id
            LEFT JOIN professores pr ON p.id_professor = pr.id
            WHERE c.id_aluno = %s
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
            JOIN alunos a ON c.id_aluno = a.id
            JOIN projetos p ON c.id_projeto = p.id
            LEFT JOIN professores pr ON p.id_professor = pr.id
            WHERE c.id_projeto = %s
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
            "SELECT id FROM certificados WHERE id_projeto = %s AND id_aluno = %s",
            (id_projeto, id_aluno)
        )
        return cursor.fetchone() is not None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_certificado(id_projeto: int, id_aluno: int) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        codigo_verificacao = str(uuid.uuid4()).replace("-", "").upper()[:16]
        cursor.execute(
            """
            INSERT INTO certificados (id_projeto, id_aluno, data_emissao, codigo_verificacao)
            VALUES (%s, %s, CURDATE(), %s)
            """,
            (id_projeto, id_aluno, codigo_verificacao)
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
            JOIN alunos a ON c.id_aluno = a.id
            JOIN projetos p ON c.id_projeto = p.id
            LEFT JOIN professores pr ON p.id_professor = pr.id
            ORDER BY c.data_emissao DESC
            """
        )
        return list(cursor.fetchall())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
