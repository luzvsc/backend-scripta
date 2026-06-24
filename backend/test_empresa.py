import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT email_contato, senha FROM empresas LIMIT 1")
    empresa = cursor.fetchone()
    print(f"Empresa no banco: {empresa}")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
