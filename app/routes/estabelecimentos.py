from app import app

from datetime import datetime

from app.servicos.read_db import read_estabelecimento_nome, read_estabelecimento_cnpj


@app.get("/api/v1/estabelecimentos/{cnpj}")
async def consultar_estabelecimentos_nome(cnpj):

    teste = {
    '1':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "12345678",
        "cnpj_ordem": "9101",
        "cnpj_dv": "11",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "teste",
        "situacao_cadastral": "Teste",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "1",
        "nome_da_cidade_no_exterior": "Brasilia",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "11",
        "telefone1": "987654321",
        "ddd2": "22",
        "telefone2": "987654321",
        "ddd_do_fax": "33",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    },
    '2':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "87654321",
        "cnpj_ordem": "1098",
        "cnpj_dv": "22",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "exemplo",
        "situacao_cadastral": "Exemplo",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "2",
        "nome_da_cidade_no_exterior": "Rio de Janeiro",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "44",
        "telefone1": "987654321",
        "ddd2": "55",
        "telefone2": "987654321",
        "ddd_do_fax": "66",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    },
    '3':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "98765432",
        "cnpj_ordem": "2109",
        "cnpj_dv": "33",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "exemplo2",
        "situacao_cadastral": "Exemplo2",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "3",
        "nome_da_cidade_no_exterior": "São Paulo",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "77",
        "telefone1": "987654321",
        "ddd2": "88",
        "telefone2": "987654321",
        "ddd_do_fax": "99",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    },
    '4':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "56781234",
        "cnpj_ordem": "3456",
        "cnpj_dv": "44",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "exemplo3",
        "situacao_cadastral": "Exemplo3",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "4",
        "nome_da_cidade_no_exterior": "Porto Alegre",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "111",
        "telefone1": "987654321",
        "ddd2": "222",
        "telefone2": "987654321",
        "ddd_do_fax": "333",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    },
    '5':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "65432100",
        "cnpj_ordem": "6789",
        "cnpj_dv": "55",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "exemplo4",
        "situacao_cadastral": "Exemplo4",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "5",
        "nome_da_cidade_no_exterior": "Recife",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "444",
        "telefone1": "987654321",
        "ddd2": "555",
        "telefone2": "987654321",
        "ddd_do_fax": "666",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    },
    '5':{
        "datetime": "2023-10-24T18:02:23.857996",
        "message": {
        "cnpj_basico": "11223344",
        "cnpj_ordem": "5566",
        "cnpj_dv": "66",
        "identificador_matriz_filial": "#######",
        "nome_fantasia": "exemplo5",
        "situacao_cadastral": "Exemplo5",
        "data_situacao_cadastral": None,
        "motivo_situacao_cadastral": "6",
        "nome_da_cidade_no_exterior": "Salvador",
        "pais": "Brasil",
        "data_de_inicio_atividade": "2023-10-24",
        "cnae_fiscal_principal": None,
        "cnae_fiscal_secundaria": [],
        "tipo_de_logradouro": None,
        "logradouro": None,
        "numero": None,
        "complemento": None,
        "bairro": None,
        "cep": None,
        "uf": None,
        "municipio": None,
        "ddd1": "777",
        "telefone1": "987654321",
        "ddd2": "888",
        "telefone2": "987654321",
        "ddd_do_fax": "999",
        "fax": "987654321",
        "correio_eletronico": None,
        "situacao_especial": None,
        "data_da_situacao_especial": "2023-10-24"
        },
        "status": 200
    }
    }

    retorno = {"datetime": datetime.now(),
            "message": {},
            "status": 200}
    
    return teste.get(cnpj, retorno)


@app.get("/api/v1/estabelecimentos/cnpj/{estabelecimentos_cnpj}")
async def consultar_estabelecimentos(estabelecimentos_cnpj: str):
    """
    Consultar estabelecimentos cnpj
    """
    

    return {"datetime": datetime.now(),
            "message": read_estabelecimento_cnpj(estabelecimentos_cnpj),
            "status": 200}


"""
    Razao social - empresas
    endereços - estabelecimentos
    por tipo - 
"""