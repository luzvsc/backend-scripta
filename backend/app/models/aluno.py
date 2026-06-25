from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator
)


class AlunoBase(BaseModel):
    nome: str = Field(
        ...,
        min_length=3,
        max_length=150
    )
    email: EmailStr
    curso: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class AlunoCreate(AlunoBase):
    senha: str = Field(
        ...,
        min_length=6
    )
    confirmar_senha: str = Field(
        ...,
        min_length=6
    )

    @model_validator(mode="after")
    def verificar_senhas(
        self
    ) -> "AlunoCreate":
        if self.senha != self.confirmar_senha:
            raise ValueError(
                "A senha e a confirmação da senha "
                "não coincidem"
            )

        return self


class AlunoResponse(AlunoBase):
    id: int
    matricula: Optional[str] = None
    turma: Optional[str] = None
    semestre_ingresso: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    competencias: Optional[str] = None


class AlunoLogin(BaseModel):
    email: EmailStr
    senha: str = Field(
        ...,
        min_length=6
    )


class AlunoUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    senha: Optional[str] = Field(
        default=None,
        min_length=6
    )

    confirmar_senha: Optional[str] = Field(
        default=None,
        min_length=6
    )

    linkedin_url: Optional[str] = Field(
        default=None,
        max_length=255
    )

    github_url: Optional[str] = Field(
        default=None,
        max_length=255
    )

    competencias: Optional[str] = Field(
        default=None,
        max_length=255
    )

    @model_validator(mode="after")
    def verificar_nova_senha(
        self
    ) -> "AlunoUpdate":
        senha_informada = self.senha is not None
        confirmacao_informada = (
            self.confirmar_senha is not None
        )

        if senha_informada != confirmacao_informada:
            raise ValueError(
                "Informe a senha e a confirmação da senha"
            )

        if (
            senha_informada
            and self.senha != self.confirmar_senha
        ):
            raise ValueError(
                "A senha e a confirmação da senha "
                "não coincidem"
            )

        return self


class AlunoCreateResponse(BaseModel):
    message: str
    id: int