import sqlalchemy as sa

from .model_base import ModelBase

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import ForeignKey

from typing import List


class Natureza(ModelBase):
    __tablename__: str = 'naturezas_juridicas'

    ID: str = sa.Column(sa.CHAR(4), primary_key=True, index=True)
    DESCRICAO: str = sa.Column(sa.String(90), nullable=False)

    def __repr__(self) -> str:
        return f'<Natureza>'
    

class Qualificacao(ModelBase):
    __tablename__: str = 'qualificacoes_socios'

    ID: str = sa.Column(sa.CHAR(2), primary_key=True, index=True)
    DESCRICAO: str = sa.Column(sa.String(90), nullable=False)

    def __repr__(self) -> str:
        return f'<Qualificacao>'
    

class Cnaes(ModelBase):
    __tablename__: str = 'cnaes'

    ID: str = sa.Column(sa.CHAR(7), primary_key=True, index=True)
    DESCRICAO: str = sa.Column(sa.String(150), nullable=False)

    FISCAL: Mapped[List['Fiscal']] = relationship(
        back_populates="CNAES"
    )

    Tipos_Cnaes: Mapped[List['TiposCnaes']] = relationship(
        back_populates="CNAES"
    )

    def __repr__(self) -> str:
        return f'<Cnaes>'
    

class Motivos(ModelBase):
    __tablename__: str = 'motivos_situacao_empresa'

    ID: str = sa.Column(sa.CHAR(2), primary_key=True, index=True)
    DESCRICAO: str = sa.Column(sa.String(40), nullable=False)

    def __repr__(self) -> str:
        return f'<Motivos>'
    

class Tipos(ModelBase):
    __tablename__: str = 'tipos'

    id: str = sa.Column(sa.Integer, primary_key=True, index=True)
    tipo: str = sa.Column(sa.String(60))

    Tipos_Cnaes: Mapped[List['TiposCnaes']] = relationship(
        back_populates="TIPOS"
    )

    def __repr__(self) -> str:
        return f'<Tipos>'
    

class TiposCnaes(ModelBase):
    __tablename__: str = 'tipos_cnaes'

    id_tipos: str = sa.Column(sa.Integer, ForeignKey('tipos.id'), primary_key=True)
    cnaes: str = sa.Column(sa.CHAR(7), ForeignKey('cnaes.ID'), primary_key=True)

    CNAES: Mapped['Cnaes'] = relationship(
        back_populates="Tipos_Cnaes"
    )

    TIPOS: Mapped['Tipos'] = relationship(
        back_populates="Tipos_Cnaes"
    )

    def __repr__(self) -> str:
        return f'<TiposCnaes>'