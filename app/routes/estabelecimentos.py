from app import app

from datetime import datetime

from app.servicos.read_db import read_empresa

from typing import Literal


@app.get("/api/v1/empresas/")
async def consultar_estabelecimentos(tipopesquisa: str,
                                     busca: str,
                                     matriz: Literal['1', '2', None] = None,
                                     cep: str = None,
                                     pagina: int = 0,
                                     uf: str = None):

    mensagem = read_empresa(tipo_busca=tipopesquisa,
                                busca=busca,
                                matriz=matriz,
                                cep=cep,
                                pagina=pagina,
                                uf=uf)
    
    return {"datetime": datetime.now(),
            "message": mensagem,
            "status": 200}
