from fastapi import FastAPI
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from app.bd.conexao_bd import create_tables

app = FastAPI()

# create_tables()

# auth = OAuth2PasswordBearer(tokenUrl="token")




from app.routes.estabelecimentos import *
from app.routes.login import *
