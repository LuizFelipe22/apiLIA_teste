import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column, Double, Date, BOOLEAN, BIGINT

from datetime import datetime

from typing import Optional, List

from .model_base import ModelBase
from .dominios_model import Natureza, Qualificacao, Cnaes


class Empresas(ModelBase):
    __tablename__: str = 'empresas'

    CNPJ_BASE: Mapped[str] = mapped_column(String(8), primary_key=True, index=True)
    RAZAO_SOCIAL_NOME_EMPRESARIAL: Mapped[Optional[str]] = mapped_column(String(200))
    NATUREZA_JURIDICA: Mapped[Optional[str]] = mapped_column(String(4), ForeignKey('naturezas_juridicas.ID'))
    QUALIFICACAO_DO_RESPONSAVEL: Mapped[Optional[str]] = mapped_column(String(2), ForeignKey('qualificacoes_socios.ID'))
    CAPITAL_SOCIAL_DA_EMPRESA: Mapped[float] = mapped_column(Double)
    PORTE_EMPRESA: Mapped[Optional[str]] = mapped_column(String(30))
    ENTE_FEDERATIVO_RESPONSAVEL: Mapped[Optional[str]] = mapped_column(String(50))
    # HASH: Mapped[Optional[str]] = mapped_column(String(40))

    NATUREZA: Mapped[Natureza] = relationship('Natureza', lazy='joined')
    QUALIFICACAO: Mapped[Qualificacao] = relationship('Qualificacao', lazy='joined')
    ESTABELECIMENTOS: Mapped[List['Estabelecimentos']] = relationship(
        back_populates="EMPRESAS"
    )

    def __repr__(self) -> str:
        return f'<Empresas>'


class Estabelecimentos(ModelBase):
    __tablename__: str = 'estabelecimentos'

    ID: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    CNPJ: Mapped[str] = mapped_column(String(14), index=True, primary_key=True)
    CNPJ_BASICO: Mapped[str] = mapped_column(String(8), ForeignKey('empresas.CNPJ_BASE'))
    CNPJ_ORDEM: Mapped[Optional[str]] = mapped_column(String(4))
    CNPJ_DV: Mapped[Optional[str]] = mapped_column(String(2))
    ID_MATRIZ_FILIAL: Mapped[Optional[str]] = mapped_column(String(1))
    NM_FANTASIA:  Mapped[Optional[str]] = mapped_column(String(60))
    SITU_CADASTRAL: Mapped[Optional[str]] = mapped_column(String(1))
    DT_SITU_CADASTRAL: Mapped[Optional[datetime]] = mapped_column(Date)
    MT_SITU_CADASTRAL: Mapped[Optional[str]] = mapped_column(String(4))
    CIDADE_EXTERIOR: Mapped[Optional[str]] = mapped_column(String(60))
    PAIS: Mapped[Optional[str]] = mapped_column(String(45))
    DT_INICIO_ATIV: Mapped[Optional[datetime]] = mapped_column(Date)
    TP_LOGRADOURO: Mapped[Optional[str]] = mapped_column(String(20))
    LOGRADOURO: Mapped[Optional[str]] = mapped_column(String(100))
    NUMERO: Mapped[Optional[str]] = mapped_column(String(10))
    COMPLEMENTO: Mapped[Optional[str]] = mapped_column(String(200))
    BAIRRO: Mapped[Optional[str]] = mapped_column(String(60))
    CEP: Mapped[Optional[str]] = mapped_column(String(8))
    UF: Mapped[Optional[str]] = mapped_column(String(2))
    MUNICIPIO: Mapped[Optional[str]] = mapped_column(String(4))
    DDD1: Mapped[Optional[str]] = mapped_column(String(4))
    TELEFONE1: Mapped[Optional[str]] = mapped_column(String(8))
    DDD2: Mapped[Optional[str]] = mapped_column(String(4))
    TELEFONE2: Mapped[Optional[str]] = mapped_column(String(8))
    DDD_FAX: Mapped[Optional[str]] = mapped_column(String(4))
    FAX: Mapped[Optional[str]] = mapped_column(String(8))
    CORREIO_ELETRONICO: Mapped[Optional[str]] = mapped_column(String(150))
    SITUACAO_ESPECIAL: Mapped[Optional[str]] = mapped_column(String(50))
    DT_SITU_ESPECIAL: Mapped[Optional[datetime]] = mapped_column(Date)

    EMPRESAS: Mapped['Empresas'] = relationship(
        back_populates="ESTABELECIMENTOS"
    )

    FISCAL: Mapped[List['Fiscal']] = relationship(
        back_populates='ESTABELECIMENTOS'
    )

    def __repr__(self) -> str:
        return f'<Estabelecimentos>'


class Fiscal(ModelBase):
    __tablename__: str = 'estabelecimento_cnaes'

    ID: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    CNPJ: Mapped[Optional[str]] = mapped_column(String(14), ForeignKey('estabelecimentos.CNPJ'))
    CNAE: Mapped[Optional[str]] = mapped_column(String(7), ForeignKey('cnaes.ID'))
    PRINCIPAL: Mapped[Optional[int]] = mapped_column(BOOLEAN)

    ESTABELECIMENTOS: Mapped['Estabelecimentos'] = relationship(
        back_populates="FISCAL"
    )

    CNAES: Mapped[Cnaes] = relationship(
        back_populates="FISCAL"
    )

    def __repr__(self) -> str:
        return f'<Fiscal>'


class Socios(ModelBase):
    __tablename__: str = 'socios'

    ID: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True, autoincrement=True)

    CNPJ_BASICO: Mapped[Optional[str]] = mapped_column(String(8), ForeignKey('empresas.CNPJ_BASE'))
    IDENTIFICADOR_SOCIO: Mapped[Optional[str]] = mapped_column(String(20))
    NOME_SOCIO_OU_RAZAO_SOCIAL:Mapped[Optional[str]] = mapped_column(String(150))
    CNPJ_CPF_SOCIO: Mapped[Optional[str]] = mapped_column(String(14))
    QUALIFICACAO_SOCIO: Mapped[Optional[str]] = mapped_column(String(100))
    DT_ENTRADA_SOCIEDADE: Mapped[Optional[datetime]] = mapped_column(Date)
    PAIS: Mapped[Optional[str]] = mapped_column(String(40))
    REPRESENTANTEA_LEGAL: Mapped[Optional[str]] = mapped_column(String(11))
    NOME_REPRESENTANTE: Mapped[Optional[str]] = mapped_column(String(100))
    QUALIFICACAO_REPRESENTANTE_LEGAL: Mapped[Optional[str]] = mapped_column(String(2), ForeignKey('qualificacoes_socios.ID'))
    FAIXA_ETARIA: Mapped[Optional[str]] = mapped_column(String(20))
    HASH: Mapped[Optional[str]] = mapped_column(String(40))

    EMPRESAS_FK: Mapped[Empresas] = relationship('Empresas', lazy='joined')
    SOCIOS_QUALIFICACAO_FK: Mapped[Qualificacao] = relationship('Qualificacao', lazy='joined')

    def __repr__(self) -> str:
        return f'<Socios>'


class Nm_Estab_Empresas(ModelBase):
    __tablename__: str = 'nm_estabele_empresas'

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CNPJ_BASE: Mapped[str] = mapped_column(String(8))
    RAZAO_SOCIAL_NOME_EMPRESARIAL: Mapped[Optional[str]] = mapped_column(String(200))
    NM_FANTASIA:  Mapped[Optional[str]] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f'<Nm_Estab_Empresas>'