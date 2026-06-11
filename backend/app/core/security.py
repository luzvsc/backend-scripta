import bcrypt

def gerar_hash(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")

    salt = bcrypt.gensalt()

    hash_senha = bcrypt.hashpw(
        senha_bytes,
        salt
    )

    return hash_senha.decode("utf-8")


def verificar_senha(
    senha_digitada: str,
    hash_armazenado: str
) -> bool:

    return bcrypt.checkpw(
        senha_digitada.encode("utf-8"),
        hash_armazenado.encode("utf-8")
    )