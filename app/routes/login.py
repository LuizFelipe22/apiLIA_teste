from app import app

from app.servicos.insert_db import create_usuario

from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import status


class Usuario(BaseModel):

    login: str
    email: str
    nome_completo: str
    inativo: bool
    senha_hash: str


@app.post("/registrar")
def registrar_user(user: Usuario):
    
    create_usuario(login=user.login,
                   email=user.email,
                   nome_completo=user.nome_completo,
                   inativo=user.inativo,
                   senha_hash=user.senha_hash)
    
    return JSONResponse(
        content={"msg": "usuario criado"},
        status_code=status.HTTP_201_CREATED
        )