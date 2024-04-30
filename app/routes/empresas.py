from app import app

from datetime import datetime, date

from app.servicos.read_db import read_empresa, read_estabelecimentos_por_tipo

from typing import Literal

from pydantic import BaseModel

from fastapi.responses import JSONResponse


class PesquisaEmpresa(BaseModel):
    nome_empresa: str
    cnpj: str
    matriz: Literal['1', '2']
    cep: str
    pagina: int
    uf: str
    capital_social_minimo: float
    capital_social_maximo: float
    porte_empresa: Literal['Micro Empresa', 'Empresa de Pequeno Porte', 'Demais', 'Não Informado']
    dt_abertura_de: date
    dt_abertura_ate: date


@app.get("/api/v1/empresas/")
async def consultar_empresas(nome_empresa: str = None,
                                    cnpj: str = None,
                                    matriz: Literal['1', '2'] = None,
                                    cep: str = None,
                                    pagina: int = 0,
                                    uf: str = None,
                                    capital_social_minimo: float = None,
                                    capital_social_maximo: float = None,
                                    porte_empresa: Literal['Micro Empresa', 'Empresa de Pequeno Porte', 'Demais', 'Não Informado'] = None,
                                    dt_abertura_de: date = date(year=1850, month=1, day=1),
                                    dt_abertura_ate: date = date(year=datetime.now().year, month=datetime.now().month, day=1)):


    mensagem = read_empresa(cnpj=cnpj,
                            nome=nome_empresa,
                            matriz=matriz,
                            cep=cep,
                            pagina=pagina,
                            uf=uf,
                            capital_social_minimo=capital_social_minimo,
                            capital_social_maximo=capital_social_maximo,
                            porte_empresa=porte_empresa,
                            abertura_de=dt_abertura_de,
                            abertura_ate=dt_abertura_ate)
    
    return JSONResponse(
        content={
            "datetime": str(datetime.now()),
            "message": mensagem
        },
        status_code=200
    )
