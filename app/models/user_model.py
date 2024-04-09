import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column, Double, Date, BOOLEAN, BIGINT

from datetime import datetime

from typing import Optional

from .model_base import ModelBase
from .dominios_model import Natureza, Qualificacao, Cnaes


class Usuario(ModelBase):
    __tablename__ = 'auth_usuario'

    id: Mapped[int]  = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(70), unique=True, index=True)
    nome_completo: Mapped[str] = mapped_column(String(100), index=True)
    inativo: Mapped[int] = mapped_column(Boolean, default=False)
    senha_hash: Mapped[str] = mapped_column(String(60))


    def __repr__(self) -> str:
        return f'<Usuario>'
