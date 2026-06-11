from app.core.security import (
    gerar_hash,
    verificar_senha
)

senha = "123456"

hash_senha = gerar_hash(senha)

print(hash_senha)

print(verificar_senha("123456", hash_senha))
print(verificar_senha("abcdef", hash_senha))