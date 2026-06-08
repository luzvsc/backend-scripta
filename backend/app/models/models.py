from __future__ import annotations
from typing import Optional
import datetime
import decimal
import enum
from app.database.database import Base
from sqlalchemy import Column, DECIMAL, DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, UniqueConstraint, Text, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship


class AvaliacoesConceito(str, enum.Enum):
    EXCELENTE = 'Excelente'
    OTIMO = 'Ótimo'
    BOM = 'Bom'
    AINDA_NAO_SUFICIENTE = 'Ainda não suficiente'
    INSUFICIENTE = 'Insuficiente'


class ProjetosStatus(str, enum.Enum):
    RASCUNHO = 'rascunho'
    SUBMETIDO = 'submetido'
    EM_AVALIACAO = 'em_avaliacao'
    APROVADO = 'aprovado'
    REPROVADO = 'reprovado'


class ProjetosVisibilidade(str, enum.Enum):
    PUBLICO = 'publico'
    APENAS_SENAC = 'apenas_senac'
    PRIVADO = 'privado'


class VersoesProjetoQuemAlterouTipo(str, enum.Enum):
    ALUNO = 'aluno'
    PROFESSOR = 'professor'
    COORDENADOR = 'coordenador'


# --- 1. Classes Principais (Independentes) ---

class Coordenadores(Base):
    __tablename__ = 'coordenadores'
    __table_args__ = (
        Index('email', 'email', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    logs: Mapped[list["LogsSistema"]] = relationship(
        back_populates="coordenador"
    )

class Empresas(Base):
    __tablename__ = 'empresas'
    __table_args__ = (
        Index('cnpj', 'cnpj', unique=True),
        Index('email_contato', 'email_contato', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_empresa: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), nullable=False)
    email_contato: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    setor: Mapped[Optional[str]] = mapped_column(String(100))

    contatos_empresa: Mapped[list['ContatosEmpresa']] = relationship('ContatosEmpresa', back_populates='empresa')


class Professores(Base):
    __tablename__ = 'professores'
    __table_args__ = (
        Index('email', 'email', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    area_atuacao: Mapped[Optional[str]] = mapped_column(String(100))

    projetos: Mapped[list['Projetos']] = relationship('Projetos', back_populates='professor_orientador')
    avaliacoes: Mapped[list['Avaliacoes']] = relationship('Avaliacoes', back_populates='professor')


class Alunos(Base):
    __tablename__ = 'alunos'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('matricula', 'matricula', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    matricula: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    curso: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    turma: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    semestre_ingresso: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    projetos_como_integrante: Mapped[list['Projetos']] = relationship('Projetos', secondary='projeto_integrantes', back_populates='integrantes')
    contatos_empresa: Mapped[list['ContatosEmpresa']] = relationship('ContatosEmpresa', back_populates='aluno')
    portfolio: Mapped[Optional['Portfolios']] = relationship(
    'Portfolios',
    back_populates='aluno',
    uselist=False
)
    projetos_criados: Mapped[list['Projetos']] = relationship('Projetos', back_populates='aluno_responsavel')
    certificados: Mapped[list['Certificados']] = relationship('Certificados', back_populates='aluno')


# --- 2. Classes Dependentes (Conectadas) ---

class Portfolios(Base):
    __tablename__ = 'portfolios'
    __table_args__ = (
        ForeignKeyConstraint(['aluno_id'], ['alunos.id'], ondelete='CASCADE'),
        Index('aluno_id', 'aluno_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aluno_id: Mapped[int] = mapped_column(Integer, nullable=False)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255))
    github_url: Mapped[Optional[str]] = mapped_column(String(255))
    habilidades: Mapped[Optional[str]] = mapped_column(String(255))

    aluno: Mapped['Alunos'] = relationship(
    'Alunos',
    back_populates='portfolio'
)


class ContatosEmpresa(Base):
    __tablename__ = 'contatos_empresa'
    __table_args__ = (
        ForeignKeyConstraint(['aluno_id'], ['alunos.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ondelete='CASCADE'),
        Index('aluno_id', 'aluno_id'),
        Index('empresa_id', 'empresa_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(Integer, nullable=False)
    aluno_id: Mapped[int] = mapped_column(Integer, nullable=False)
    assunto: Mapped[str] = mapped_column(String(150), nullable=False)
    mensagem: Mapped[str] = mapped_column(Text, nullable=False)
    data_envio: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    aluno: Mapped['Alunos'] = relationship('Alunos', back_populates='contatos_empresa')
    empresa: Mapped['Empresas'] = relationship('Empresas', back_populates='contatos_empresa')


class Projetos(Base):
    __tablename__ = 'projetos'
    __table_args__ = (
        ForeignKeyConstraint(['aluno_responsavel_id'], ['alunos.id'], ondelete='RESTRICT'),
        ForeignKeyConstraint(['professor_orientador_id'], ['professores.id'], ondelete='RESTRICT'),
        Index('aluno_responsavel_id', 'aluno_responsavel_id'),
        Index('professor_orientador_id', 'professor_orientador_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    curso: Mapped[str] = mapped_column(String(100), nullable=False)
    turma: Mapped[str] = mapped_column(String(50), nullable=False)
    semestre: Mapped[str] = mapped_column(String(10), nullable=False)
    aluno_responsavel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_orientador_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[Optional[ProjetosStatus]] = mapped_column(Enum(ProjetosStatus), server_default=text("'rascunho'"))
    visibilidade: Mapped[Optional[ProjetosVisibilidade]] = mapped_column(Enum(ProjetosVisibilidade), server_default=text("'privado'"))

    integrantes: Mapped[list['Alunos']] = relationship('Alunos', secondary='projeto_integrantes', back_populates='projetos_como_integrante')
    aluno_responsavel: Mapped['Alunos'] = relationship('Alunos', back_populates='projetos_criados')
    professor_orientador: Mapped['Professores'] = relationship('Professores', back_populates='projetos')
    arquivos_projeto: Mapped[list['ArquivosProjeto']] = relationship('ArquivosProjeto', back_populates='projeto')
    avaliacoes: Mapped[list['Avaliacoes']] = relationship('Avaliacoes', back_populates='projeto')
    certificados: Mapped[list['Certificados']] = relationship('Certificados', back_populates='projeto')
    versoes_projeto: Mapped[list['VersoesProjeto']] = relationship('VersoesProjeto', back_populates='projeto')


class ProjetoIntegrantes(Base):
    __tablename__ = 'projeto_integrantes'
    __table_args__ = (
        ForeignKeyConstraint(['aluno_id'], ['alunos.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ondelete='CASCADE'),
    )
    projeto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aluno_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ArquivosProjeto(Base):
    __tablename__ = 'arquivos_projeto'
    __table_args__ = (
        ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ondelete='CASCADE'),
        Index('projeto_id', 'projeto_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nome_original: Mapped[str] = mapped_column(String(255), nullable=False)
    caminho_servidor: Mapped[str] = mapped_column(String(255), nullable=False)
    tamanho_mb: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)

    projeto: Mapped['Projetos'] = relationship('Projetos', back_populates='arquivos_projeto')


class VersoesProjeto(Base):
    __tablename__ = 'versoes_projeto'
    __table_args__ = (
        ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ondelete='CASCADE'),
        Index('projeto_id', 'projeto_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    titulo_na_epoca: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao_na_epoca: Mapped[str] = mapped_column(Text, nullable=False)
    quem_alterou_tipo: Mapped[VersoesProjetoQuemAlterouTipo] = mapped_column(Enum(VersoesProjetoQuemAlterouTipo), nullable=False)
    quem_alterou_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data_alteracao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    projeto: Mapped['Projetos'] = relationship('Projetos', back_populates='versoes_projeto')

class Avaliacoes(Base):
    __tablename__ = 'avaliacoes'
    __table_args__ = (
    ForeignKeyConstraint(['professor_id'], ['professores.id'], ondelete='RESTRICT'),
    ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ondelete='CASCADE'),
    Index('projeto_id', 'projeto_id'),
    Index('professor_id', 'professor_id'),
    UniqueConstraint(
        'projeto_id',
        'professor_id',
        name='uq_avaliacao_professor_projeto'
    )
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nota_inovacao: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    nota_tecnica: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    nota_aplicabilidade: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    nota_clareza: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    media_geral: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    conceito: Mapped[AvaliacoesConceito] = mapped_column(Enum(AvaliacoesConceito), nullable=False)
    parecer_descritivo: Mapped[Optional[str]] = mapped_column(Text)
    data_avaliacao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    professor: Mapped['Professores'] = relationship('Professores', back_populates='avaliacoes')
    projeto: Mapped['Projetos'] = relationship('Projetos', back_populates='avaliacoes')

class Certificados(Base):
    __tablename__ = 'certificados'
    __table_args__ = (
            ForeignKeyConstraint(['aluno_id'], ['alunos.id'], ondelete='CASCADE'),
            ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ondelete='CASCADE'),
            Index('aluno_id', 'aluno_id'),
            Index('projeto_id', 'projeto_id'),
            UniqueConstraint(
                'projeto_id',
                'aluno_id',
                name='uq_certificado_aluno_projeto'
            )
        )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    aluno_id: Mapped[int] = mapped_column(Integer, nullable=False)
    codigo_autenticidade: Mapped[str] = mapped_column(String(100), nullable=False)
    data_emissao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    aluno: Mapped['Alunos'] = relationship('Alunos', back_populates='certificados')
    projeto: Mapped['Projetos'] = relationship('Projetos', back_populates='certificados')

class LogsSistema(Base):
    __tablename__ = 'logs_sistema'

    __table_args__ = (
        ForeignKeyConstraint(
            ['coordenador_id'],
            ['coordenadores.id'],
            ondelete='RESTRICT'
        ),
        Index('coordenador_id', 'coordenador_id'),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    coordenador_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    entidade: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    acao: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    registro_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    detalhes: Mapped[Optional[str]] = mapped_column(
        Text
    )

    data_hora: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    coordenador: Mapped["Coordenadores"] = relationship(
    back_populates="logs"
)