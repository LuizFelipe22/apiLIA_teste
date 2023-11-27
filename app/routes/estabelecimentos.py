from app import app

from datetime import datetime

from app.servicos.read_db import read_estabelecimento_nome, read_estabelecimento_cnpj


@app.get("/api/v1/estabelecimentos/{tipopesquisa}/{busca}")
async def consultar_estabelecimentos_nome(tipopesquisa, busca):


    tipos_pesquisas = {"cnpj": read_estabelecimento_cnpj(busca),
                       "nome": read_estabelecimento_nome(busca)}
    
    resposta = tipos_pesquisas.get(tipopesquisa, "Tipo de pesquisa não disponível")
    
    return {"datetime": datetime.now(),
            "message": resposta,
            "status": 200}


"""
    Razao social - empresas
    endereços - estabelecimentos
    por tipo - 
"""