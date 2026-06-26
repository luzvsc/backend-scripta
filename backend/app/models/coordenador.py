from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator
)


class CoordenadorBase(BaseModel):

    nome: str = Field(
        ...,
        min_length=3,
        max_length=150
    )
    email: EmailStr


class CoordenadorResponse(CoordenadorBase):

    id: int


class CoordenadorLogin(BaseModel):

    email: EmailStr
    senha: str = Field(
        ...,
        min_length=6
    )


class CoordenadorUpdate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    senha: Optional[str] = Field(
        default=None,
        min_length=6
    )

    confirmar_senha: Optional[str] = Field(
        default=None,
        min_length=6
    )

    @model_validator(mode="after")
    def verificar_nova_senha(
        self
    ) -> "CoordenadorUpdate":
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