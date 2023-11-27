import sqlalchemy as sa

from .model_base import ModelBase


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

    def __repr__(self) -> str:
        return f'<Cnaes>'
    

class Motivos(ModelBase):
    __tablename__: str = 'motivos_situacao_empresa'

    ID: str = sa.Column(sa.CHAR(2), primary_key=True, index=True)
    DESCRICAO: str = sa.Column(sa.String(40), nullable=False)

    def __repr__(self) -> str:
        return f'<Motivos>'
    

# class Paises(ModelBase):
#     __tablename__: str = ''

#     ID: str = sa.Column(sa.CHAR(3), primary_key=True, index=True)
#     DESCRICAO: str = sa.Column(sa.String(30), nullable=False)

#     def __repr__(self) -> str:
#         return f'<Paises>'