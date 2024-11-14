import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column, Double, Date, BOOLEAN, BIGINT

from datetime import datetime

from typing import Optional, List

from .model_base import ModelBase
from .dominios_model import Natureza, Qualificacao, Cnaes


class Empresas(ModelBase):
    __tablename__: str = 'empresas'

    cnpj_base: Mapped[str] = mapped_column(String(8), primary_key=True, index=True)
    razao_social_nome_empresarial: Mapped[Optional[str]] = mapped_column(String(255))
    natureza_juridica: Mapped[Optional[str]] = mapped_column(String(4), ForeignKey('naturezas_juridicas.id'))
    qualificacao_do_responsavel: Mapped[Optional[str]] = mapped_column(String(2), ForeignKey('qualificacoes_socios.id'))
    capital_social_da_empresa: Mapped[float] = mapped_column(Double)
    porte_empresa: Mapped[Optional[str]] = mapped_column(String(30))
    ente_federativo_responsavel: Mapped[Optional[str]] = mapped_column(String(50))
    hash: Mapped[Optional[str]] = mapped_column(String(40))

    NATUREZA: Mapped[Natureza] = relationship('Natureza', lazy='joined')
    QUALIFICACAO: Mapped[Qualificacao] = relationship('Qualificacao', lazy='joined')
    ESTABELECIMENTOS: Mapped[List['Estabelecimentos']] = relationship(
        back_populates="empresas"
    )

    def __repr__(self) -> str:
        return f'<Empresas>'


class Estabelecimentos(ModelBase):
    __tablename__: str = 'estabelecimentos'

    cnpj: Mapped[str] = mapped_column(String(14), index=True, primary_key=True)
    cnpj_base: Mapped[str] = mapped_column(String(8), ForeignKey('empresas.cnpj_base'))
    cnpj_ordem: Mapped[Optional[str]] = mapped_column(String(4))
    cnpj_dv: Mapped[Optional[str]] = mapped_column(String(2))
    id_matriz_filial: Mapped[Optional[str]] = mapped_column(String(1))
    nm_fantasia:  Mapped[Optional[str]] = mapped_column(String(150))
    situ_cadastral: Mapped[Optional[str]] = mapped_column(String(10))
    dt_situ_cadastral: Mapped[Optional[datetime]] = mapped_column(Date)
    mt_situ_cadastral: Mapped[Optional[str]] = mapped_column(String(2))
    cidade_exterior: Mapped[Optional[str]] = mapped_column(String(90))
    pais: Mapped[Optional[str]] = mapped_column(String(100))
    dt_inicio_ativ: Mapped[Optional[datetime]] = mapped_column(Date)
    tp_logradouro: Mapped[Optional[str]] = mapped_column(String(30))
    logradouro: Mapped[Optional[str]] = mapped_column(String(255))
    numero: Mapped[Optional[str]] = mapped_column(String(20))
    complemento: Mapped[Optional[str]] = mapped_column(String(250))
    bairro: Mapped[Optional[str]] = mapped_column(String(80))
    cep: Mapped[Optional[str]] = mapped_column(String(8))
    uf: Mapped[Optional[str]] = mapped_column(String(2))
    municipio: Mapped[Optional[str]] = mapped_column(String(100))
    ddd1: Mapped[Optional[str]] = mapped_column(String(4))
    telefone1: Mapped[Optional[str]] = mapped_column(String(9))
    ddd2: Mapped[Optional[str]] = mapped_column(String(4))
    telefone2: Mapped[Optional[str]] = mapped_column(String(9))
    ddd_fax: Mapped[Optional[str]] = mapped_column(String(4))
    fax: Mapped[Optional[str]] = mapped_column(String(9))
    correio_eletronico: Mapped[Optional[str]] = mapped_column(String(150))
    situacao_especial: Mapped[Optional[str]] = mapped_column(String(100))
    dt_situ_especial: Mapped[Optional[datetime]] = mapped_column(Date)
    hash: Mapped[Optional[str]] = mapped_column(String(40))

    empresas: Mapped['Empresas'] = relationship(
        back_populates="estabelecimentos"
    )

    fiscal: Mapped[List['Fiscal']] = relationship(
        back_populates='estabelecimentos'
    )

    def __repr__(self) -> str:
        return f'<Estabelecimentos>'


class Fiscal(ModelBase):
    __tablename__: str = 'cnpj_cnaes'

    cnpj: Mapped[Optional[str]] = mapped_column(String(14), ForeignKey('estabelecimentos.cnpj'))
    cnae: Mapped[Optional[str]] = mapped_column(String(7), ForeignKey('cnaes.id'))
    principal: Mapped[Optional[int]] = mapped_column(BOOLEAN)

    ESTABELECIMENTOS: Mapped['Estabelecimentos'] = relationship(
        back_populates="fiscal"
    )

    CNAES: Mapped[Cnaes] = relationship(
        back_populates="fiscal"
    )

    def __repr__(self) -> str:
        return f'<Fiscal>'


class Socios(ModelBase):
    __tablename__: str = 'socios'

    cnpj_cpf_socio: Mapped[Optional[str]] = mapped_column(String(14))
    cnpj_basico: Mapped[Optional[str]] = mapped_column(String(8), ForeignKey('empresas.CNPJ_BASE'))
    identificador_socio: Mapped[Optional[str]] = mapped_column(String(20))
    nome_socio_ou_razao_social:Mapped[Optional[str]] = mapped_column(String)
    qualificacao_socio: Mapped[Optional[str]] = mapped_column(String(70))
    dt_entrada_sociedade: Mapped[Optional[datetime]] = mapped_column(Date)
    pais: Mapped[Optional[str]] = mapped_column(String(100))
    representantea_legal: Mapped[Optional[str]] = mapped_column(String(11))
    nome_representante: Mapped[Optional[str]] = mapped_column(String(100))
    qualificacao_representante_legal: Mapped[Optional[str]] = mapped_column(String(2), ForeignKey('qualificacoes_socios.ID'))
    faixa_etaria: Mapped[Optional[str]] = mapped_column(String(25))
    hash: Mapped[Optional[str]] = mapped_column(String(40))

    empresas_fk: Mapped[Empresas] = relationship('Empresas', lazy='joined')
    socios_qualificacao_fk: Mapped[Qualificacao] = relationship('Qualificacao', lazy='joined')

    def __repr__(self) -> str:
        return f'<Socios>'


class Nm_Estab_Empresas(ModelBase):
    __tablename__: str = 'nm_estabele_empresas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj_base: Mapped[str] = mapped_column(String(8))
    razao_social_nome_empresarial: Mapped[Optional[str]] = mapped_column(String(200))
    nm_fantasia:  Mapped[Optional[str]] = mapped_column(String(150))

    def __repr__(self) -> str:
        return f'<Nm_Estab_Empresas>'