from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator
)


class EmpresaBase(BaseModel):
    nome_empresa: str = Field(
        ...,
        min_length=2,
        max_length=150
    )
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=18
    )
    email_contato: EmailStr
    setor: Optional[str] = Field(
        default=None,
        max_length=100
    )


class EmpresaCreate(EmpresaBase):
    
    senha: str = Field(
        ...,
        min_length=6
    )
    confirmar_senha: str = Field(
        ...,
        min_length=6
    )

    @model_validator(mode="after")
    def verificar_senhas(self) -> "EmpresaCreate":

        if self.senha != self.confirmar_senha:
            raise ValueError(
                "A senha e a confirmação da senha "
                "não coincidem"
            )

        return self


class EmpresaResponse(EmpresaBase):

    id: int


class EmpresaLogin(BaseModel):

    email_contato: EmailStr
    senha: str = Field(
        ...,
        min_length=6
    )


class EmpresaUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    nome_empresa: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    cnpj: Optional[str] = Field(
        default=None,
        min_length=14,
        max_length=18
    )

    email_contato: Optional[EmailStr] = None

    setor: Optional[str] = Field(
        default=None,
        max_length=100
    )

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
    ) -> "EmpresaUpdate":
        senha_informada = (
            self.senha is not None
        )

        confirmacao_informada = (
            self.confirmar_senha is not None
        )

        if senha_informada != confirmacao_informada:
            raise ValueError(
                "Informe a senha e a confirmação da senha"
            )

        if (
            senha_informada
            and self.senha
            != self.confirmar_senha
        ):
            raise ValueError(
                "A senha e a confirmação da senha "
                "não coincidem"
            )

        return self


class EmpresaCreateResponse(BaseModel):

    message: str
    id: int