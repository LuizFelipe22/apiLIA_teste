
from os import getenv

from dotenv import load_dotenv

import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from app.models.model_base import ModelBase

__engine: Optional[Engine] = None


load_dotenv('dev.env')


def create_engine(host: str = getenv('HOST'), user: str = getenv('USUARIO'), \
                  password: str = getenv('PASSWORD'), database: str = getenv('DATABASE')) -> Engine:
    global __engine
        

    conn_str = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
    
    __engine = sa.create_engine(url=conn_str, echo=False)

    return __engine


def create_session() -> Session:
    global __engine
        
    Session = sessionmaker(bind=create_engine())
    session = Session()
    
    return session


# def create_tables() -> None:
#     global __engine 
    
#     if not __engine:
#         create_engine(sqlite=True)
        
#     import app.models.__all_models
#     ModelBase.metadata.drop_all(__engine)
#     ModelBase.metadata.create_all(__engine)