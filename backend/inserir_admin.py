import mysql.connector
import bcrypt

senha_bytes = "123456".encode("utf-8")
salt = bcrypt.gensalt()
hash_senha = bcrypt.hashpw(senha_bytes, salt).decode("utf-8")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="scripta"
)

cursor = db.cursor()
cursor.execute("SELECT id FROM coordenadores WHERE email = 'coordenacao@example.com'")
if cursor.fetchone():
    print("Coordenador já existe no MySQL!")
else:
    cursor.execute("INSERT INTO coordenadores (nome, email, senha) VALUES (%s, %s, %s)", ('Coordenação TI', 'coordenacao@example.com', hash_senha))
    db.commit()
    print("Coordenador inserido no MySQL com sucesso!")

cursor.close()
db.close()
