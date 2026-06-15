from app.database.database import get_connection
from typing import Optional, Any

def criar_portfolio(aluno_id: int, projeto_id: int, visibilidade: str) -> int:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO portfolios (aluno_id, projeto_id, visibilidade) VALUES (%s, %s, %s)", 
            (aluno_id, projeto_id, visibilidade)
        )
        conn.commit()
        id_portfolio = cursor.lastrowid
        return id_portfolio
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_por_id(id_portfolio: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolios WHERE id = %s", (id_portfolio,))
        portfolio = cursor.fetchone()
        return portfolio
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def atualizar_portfolio(id_portfolio: int, visibilidade: str) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE portfolios SET visibilidade = %s WHERE id = %s", (visibilidade, id_portfolio))
        conn.commit()
        portfolio_atualizado = cursor.rowcount > 0
        return portfolio_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deletar_portfolio(id_portfolio: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM portfolios WHERE id = %s", (id_portfolio,))
        conn.commit()
        portfolio_deletado = cursor.rowcount > 0
        return portfolio_deletado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
