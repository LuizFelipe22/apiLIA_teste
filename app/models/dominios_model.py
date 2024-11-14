import sqlalchemy as sa

from .model_base import ModelBase

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import ForeignKey

from typing import List


class Natureza(ModelBase):
    __tablename__: str = 'naturezas_juridicas'

    id: str = sa.Column(sa.CHAR(4), primary_key=True, index=True)
    descricao: str = sa.Column(sa.String(90), nullable=False)

    def __repr__(self) -> str:
        return f'<Natureza>'
    

class Qualificacao(ModelBase):
    __tablename__: str = 'qualificacoes_socios'

    id: str = sa.Column(sa.CHAR(2), primary_key=True, index=True)
    descricao: str = sa.Column(sa.String(90), nullable=False)

    def __repr__(self) -> str:
        return f'<Qualificacao>'
    

class Cnaes(ModelBase):
    __tablename__: str = 'cnaes'

    id: str = sa.Column(sa.CHAR(7), primary_key=True, index=True)
    descricao: str = sa.Column(sa.String(150), nullable=False)

    fiscal: Mapped[List['Fiscal']] = relationship(
        back_populates="cnaes"
    )

    tipos_cnaes: Mapped[List['TiposCnaes']] = relationship(
        back_populates="cnaes"
    )

    def __repr__(self) -> str:
        return f'<Cnaes>'
    

class Motivos(ModelBase):
    __tablename__: str = 'motivos_situacao_empresa'

    id: str = sa.Column(sa.CHAR(2), primary_key=True, index=True)
    descricao: str = sa.Column(sa.String(40), nullable=False)

    def __repr__(self) -> str:
        return f'<Motivos>'
    

class Tipos(ModelBase):
    __tablename__: str = 'tipos'

    id: str = sa.Column(sa.Integer, primary_key=True, index=True)
    tipo: str = sa.Column(sa.String(60))

    tipos_cnaes: Mapped[List['TiposCnaes']] = relationship(
        back_populates="tipos"
    )

    def __repr__(self) -> str:
        return f'<Tipos>'
    

class TiposCnaes(ModelBase):
    __tablename__: str = 'tipos_cnaes'

    id_tipos: str = sa.Column(sa.Integer, ForeignKey('tipos.id'), primary_key=True)
    cnaes: str = sa.Column(sa.CHAR(7), ForeignKey('cnaes.id'), primary_key=True)

    cnaes: Mapped['Cnaes'] = relationship(
        back_populates="tipos_cnaes"
    )

    tipos: Mapped['Tipos'] = relationship(
        back_populates="tipos_cnaes"
    )

    def __repr__(self) -> str:
        return f'<TiposCnaes>'
    

class Cluster(ModelBase):
    __tablename__: str = 'cluster'

    index: int = sa.Column(sa.Integer, primary_key=True)
    uf: str = sa.Column(sa.CHAR(2))
    localidade: str = sa.Column(sa.VARCHAR(50))
    logradouroDNEC: str = sa.Column(sa.Text)
    bairro: str = sa.Column(sa.VARCHAR(75))
    cep: str = sa.Column(sa.CHAR(8))
    lat: float = sa.Column(sa.DOUBLE)
    lon: float = sa.Column(sa.DOUBLE)
    cluster: int = sa.Column(sa.Integer)

    def __repr__(self) -> str:
        return f'<Cluster>'
