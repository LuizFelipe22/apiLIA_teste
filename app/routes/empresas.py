from app import app

from datetime import datetime, date

from app.servicos.read_db import read_empresa, read_estabelecimentos_por_tipo

from typing import Literal, Optional

from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import Depends


class PesquisaEmpresa(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    matriz: Optional[Literal['1', '2']] = None
    cep: Optional[str] = None
    pagina: int = 0
    tamanho: int = 50
    uf: Optional[str] = None
    capital_min: float = 0
    capital_max: float = 9_000_000_000_000_000_000
    porte_empresa: Optional[Literal['Micro Empresa', 'Empresa de Pequeno Porte', 'Demais', 'Não Informado']] = None
    abertura_de: date = date(year=1850, month=1, day=1)
    abertura_ate: date = date(year=datetime.now().year, month=datetime.now().month, day=1)


@app.get("/api/v1/empresas/")
async def consultar_empresas(parametros: PesquisaEmpresa = Depends()):

    mensagem = read_empresa(
        cnpj=         parametros.cnpj,
        nome=         parametros.nome,
        matriz=       parametros.matriz,
        cep=          parametros.cep,
        pagina=       parametros.pagina,
        tamanho=      parametros.tamanho,
        uf=           parametros.uf,
        capital_min=  parametros.capital_min,
        capital_max=  parametros.capital_max,
        porte_empresa=parametros.porte_empresa,
        abertura_de=  parametros.abertura_de,
        abertura_ate= parametros.abertura_ate
    )
    
    return JSONResponse(
        content={
            "datetime": str(datetime.now()),
            "message": mensagem
        },
        status_code=200
    )
