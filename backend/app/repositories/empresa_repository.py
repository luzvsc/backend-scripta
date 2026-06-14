from app.database.database import get_connection
from typing import Optional, Any

def buscar_por_email(email_contato: str) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empresas WHERE email_contato = %s", (email_contato,))
        empresa = cursor.fetchone()
        return empresa
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
        cursor.execute("SELECT * FROM empresas WHERE id = %s", (id_empresa,))
        empresa = cursor.fetchone()
        return empresa
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def criar_empresa(nome_empresa: str, email_contato: str, senha: str, cnpj: str, setor: str) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO empresas (nome_empresa, email_contato, senha, cnpj, setor) VALUES (%s, %s, %s, %s, %s)", 
            (nome_empresa, email_contato, senha, cnpj, setor)
        )
        conn.commit()
        id_empresa = cursor.lastrowid
        return id_empresa
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
        cursor.execute("SELECT * FROM empresas")
        empresas = list(cursor.fetchall())
        return empresas
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_empresa(id_empresa: int, dados: dict) -> bool:
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

        valores.append(id_empresa)
        sql = f"UPDATE empresas SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        empresa_atualizada = cursor.rowcount > 0
        return empresa_atualizada
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
        cursor.execute("DELETE FROM empresas WHERE id = %s", (id_empresa,))
        conn.commit()
        empresa_deletada = cursor.rowcount > 0
        return empresa_deletada
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
