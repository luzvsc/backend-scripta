from app.database.database import get_connection


def buscar_por_email(email: str) -> dict | None:

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Alunos
        cursor.execute(
            """
            SELECT
                id,
                email,
                senha
            FROM alunos
            WHERE email = %s
            """,
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario:
            usuario["perfil"] = "aluno"
            return usuario

        # Professores
        cursor.execute(
            """
            SELECT
                id,
                email,
                senha
            FROM professores
            WHERE email = %s
            """,
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario:
            usuario["perfil"] = "professor"
            return usuario

        # Coordenadores
        cursor.execute(
            """
            SELECT
                id,
                email,
                senha
            FROM coordenadores
            WHERE email = %s
            """,
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario:
            usuario["perfil"] = "coordenador"
            return usuario

        # Empresas
        cursor.execute(
            """
            SELECT
                id,
                email_contato AS email,
                senha
            FROM empresas
            WHERE email_contato = %s
            """,
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario:
            usuario["perfil"] = "empresa"

            return usuario

        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()