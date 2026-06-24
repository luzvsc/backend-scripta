import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM coordenadores")
    coordenadores = cursor.fetchall()
    print("Coordenadores no banco de dados:")
    for c in coordenadores:
        print(c)
except Exception as e:
    print(f"Erro: {e}")
finally:
    cursor.close()
    conn.close()
