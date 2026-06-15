from app.database.database import get_connection
from typing import Optional, Any


def buscar_por_email(email: str) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenadores WHERE email = %s", (email,))
        coordenador = cursor.fetchone()
        return coordenador
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_por_id(id_coordenador: int) -> Optional[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenadores WHERE id = %s", (id_coordenador,))
        coordenador = cursor.fetchone()
        return coordenador
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def listar_coordenadores() -> list[dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenadores")
        coordenadores = list(cursor.fetchall())
        return coordenadores
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualizar_coordenador(id_coordenador: int, dados: dict) -> bool:
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

        valores.append(id_coordenador)
        sql = f"UPDATE coordenadores SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        coordenador_atualizado = cursor.rowcount > 0
        return coordenador_atualizado
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

