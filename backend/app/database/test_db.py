from app.database.database import get_connection

try:
    print("🔄 Testando conexão com o MySQL...")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM alunos")

    resultado = cursor.fetchone()

    if resultado is not None:
        print("✅ Conexão realizada com sucesso!")
        print(f"📊 Quantidade de alunos cadastrados: {resultado['total']}")
    else:
        print("⚠️ Nenhum resultado retornado.")

except Exception as e:
    print(f"❌ Erro ao conectar ao banco: {e}")

finally:
    if 'conn' in locals():
        conn.close()
        print("🔒 Conexão encerrada.")