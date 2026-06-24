from app.database.connection import get_db
from app.models.coordenador import Coordenador
from app.core.security import gerar_hash

db = next(get_db())

existente = db.query(Coordenador).filter(Coordenador.email == 'coordenacao@example.com').first()
if existente:
    print("Coordenador já existe na tabela coordenadores!")
else:
    novo = Coordenador(
        nome="Coordenação TI",
        email="coordenacao@example.com",
        senha=gerar_hash("123456")
    )
    db.add(novo)
    db.commit()
    print("Coordenador inserido no banco de dados REAL do MySQL com sucesso!")

db.close()
