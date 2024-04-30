from app.bd.conexao_bd import create_session

from app.models.cnpj_base_model import Estabelecimentos, Fiscal, Empresas, Nm_Estab_Empresas
from app.models.dominios_model import Cnaes, Tipos

from sqlalchemy.dialects.mysql import match

from sqlalchemy import and_, text

from math import ceil

from typing import Literal

from datetime import datetime, date


def read_empresa(cnpj: str = None,
                 nome: str = None,
                 matriz: str = None,
                 uf: str = None,
                 cep: str = None,
                 pagina: int = 0,
                 capital_social_minimo: float = 0,
                 capital_social_maximo: float = 9_000_000_000_000_000_000,
                 abertura_de: date = date(1850, 1, 1),
                 abertura_ate: date = date.today(),
                 porte_empresa = None) -> dict:

    lista = [matriz, uf, cep, porte_empresa]

    pesquisa1 = [Estabelecimentos.ID_MATRIZ_FILIAL,
                 Estabelecimentos.UF,
                 Estabelecimentos.CEP,
                 Empresas.PORTE_EMPRESA]

    pesquisa2 =[Estabelecimentos.CNPJ.like(f'{cnpj}%'),
                match(Nm_Estab_Empresas.NM_FANTASIA, Nm_Estab_Empresas.RAZAO_SOCIAL_NOME_EMPRESARIAL, against=f'{nome}').in_natural_language_mode(),
                Empresas.CAPITAL_SOCIAL_DA_EMPRESA.between(cleft=capital_social_minimo, cright=capital_social_maximo),
                Estabelecimentos.DT_INICIO_ATIV.between(cleft=abertura_de, cright=abertura_ate)]

    pesquisar = [(coluna == parametro) for parametro, coluna in zip(lista, pesquisa1) if parametro]

    for i, parametro in enumerate([cnpj, nome, capital_social_minimo, abertura_de]):
        if parametro:
            pesquisar.append(pesquisa2[i])

    resultado = {}
    

    with create_session() as session:
        
        query = session.query(Estabelecimentos) \
            .join(Nm_Estab_Empresas, Nm_Estab_Empresas.CNPJ_BASE == Estabelecimentos.CNPJ_BASICO) \
            .join(Empresas, Estabelecimentos.CNPJ_BASICO == Empresas.CNPJ_BASE) \
            .filter(and_(*pesquisar))
    
        quantidade = query.count()
        minimo = 50 * pagina
        maximo = 50 * (pagina + 1)
        resultados = query.slice(minimo, maximo)

    for estabelecimentos in resultados:

        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == estabelecimentos.CNPJ).all()

        cnae_fiscal_principal = [str(item.CNAES) for item in fiscal if item.PRINCIPAL == 1]

        cnae_fiscal_secundaria = [str(item.CNAES) for item in fiscal if item.PRINCIPAL == 0]


        estabelecimento = {"id": estabelecimentos.ID,
                            "cnpj": estabelecimentos.CNPJ,
                            "cnpj_basico": estabelecimentos.CNPJ_BASICO,
                            "cnpj_ordem": estabelecimentos.CNPJ_ORDEM, 
                            "cnpj_dv": estabelecimentos.CNPJ_DV,
                            "identificador_matriz_filial": estabelecimentos.ID_MATRIZ_FILIAL,
                            "nome_fantasia": estabelecimentos.NM_FANTASIA,
                            "situacao_cadastral": estabelecimentos.SITU_CADASTRAL,
                            "data_situacao_cadastral": str(estabelecimentos.DT_SITU_CADASTRAL) if estabelecimentos.DT_SITU_CADASTRAL else None,
                            "motivo_situacao_cadastral": estabelecimentos.MT_SITU_CADASTRAL,
                            "nome_da_cidade_no_exterior": estabelecimentos.CIDADE_EXTERIOR,
                            "pais": estabelecimentos.PAIS,
                            "data_de_inicio_atividade": str(estabelecimentos.DT_INICIO_ATIV) if estabelecimentos.DT_INICIO_ATIV else None,
                            "cnae_fiscal_principal": cnae_fiscal_principal,
                            "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
                            "tipo_de_logradouro": estabelecimentos.TP_LOGRADOURO,
                            "logradouro": estabelecimentos.LOGRADOURO,
                            "numero": estabelecimentos.NUMERO,
                            "complemento": estabelecimentos.COMPLEMENTO,
                            "bairro": estabelecimentos.BAIRRO,
                            "cep": estabelecimentos.CEP,
                            "uf": estabelecimentos.UF,
                            "municipio": estabelecimentos.MUNICIPIO,
                            "ddd1": estabelecimentos.DDD1,
                            "telefone1": estabelecimentos.TELEFONE1,
                            "ddd2": estabelecimentos.DDD2,
                            "telefone2": estabelecimentos.TELEFONE2,
                            "ddd_do_fax": estabelecimentos.DDD_FAX,
                            "fax": estabelecimentos.FAX,
                            "correio_eletronico": estabelecimentos.CORREIO_ELETRONICO,
                            "situacao_especial": estabelecimentos.SITUACAO_ESPECIAL,
                            "data_da_situacao_especial": str(estabelecimentos.DT_SITU_ESPECIAL) if estabelecimentos.DT_SITU_ESPECIAL else None}
        
        empresa = {"cnpj_base": estabelecimentos.EMPRESAS.CNPJ_BASE,
                    "razao_social_nome_empresarial": estabelecimentos.EMPRESAS.RAZAO_SOCIAL_NOME_EMPRESARIAL,
                    "natureza_juridica": estabelecimentos.EMPRESAS.NATUREZA_JURIDICA,
                    "qualificacao_responsavel": estabelecimentos.EMPRESAS.QUALIFICACAO_DO_RESPONSAVEL,
                    "capital_social": estabelecimentos.EMPRESAS.CAPITAL_SOCIAL_DA_EMPRESA,
                    "porte_empresa": estabelecimentos.EMPRESAS.PORTE_EMPRESA,
                    "ente_federativo_responsavel": estabelecimentos.EMPRESAS.ENTE_FEDERATIVO_RESPONSAVEL}
        
        try:
            resultado[estabelecimentos.EMPRESAS.CNPJ_BASE]['filial'].append(estabelecimento)
        except KeyError:
            empresa['filial'] = [estabelecimento]
            resultado[estabelecimentos.EMPRESAS.CNPJ_BASE] = empresa


    return {"resposta": [valor for _, valor in resultado.items()],
            "total_registros": quantidade,
            "pagina": pagina + 1,
            "max_paginas": ceil(quantidade / 50)}


def read_estabelecimentos_por_tipo(busca_tipo: str):


    with create_session() as session:
        tipos = session.query(Tipos).filter(Tipos.tipo == busca_tipo)

    lista_cnaes = [cnae.cnaes for tipo in tipos for cnae in tipo.Tipos_Cnaes]

    return lista_cnaes

        

            
                

        #     fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

        #     cnae_fiscal_principal = None


        #     for item in fiscal:
        #         if item.PRINCIPAL == 1:
        #             cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
        #             break

        #     cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

        #     estabelecimento = {"cnpj": cnpj.CNPJ,
        #                     "cnpj_basico": cnpj.CNPJ_BASICO,
        #                     "cnpj_ordem": cnpj.CNPJ_ORDEM, 
        #                     "cnpj_dv": cnpj.CNPJ_DV,
        #                     "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
        #                     "nome_fantasia": cnpj.NM_FANTASIA,
        #                     "situacao_cadastral": cnpj.SITU_CADASTRAL,
        #                     "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
        #                     "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
        #                     "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
        #                     "pais": cnpj.PAIS,
        #                     "data_de_inicio_atividade": cnpj.DT_INICIO_ATIV,
        #                     "cnae_fiscal_principal": cnae_fiscal_principal,
        #                     "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
        #                     "tipo_de_logradouro": cnpj.TP_LOGRADOURO,
        #                     "logradouro": cnpj.LOGRADOURO,
        #                     "numero": cnpj.NUMERO,
        #                     "complemento": cnpj.COMPLEMENTO,
        #                     "bairro": cnpj.BAIRRO,
        #                     "cep": cnpj.CEP,
        #                     "uf": cnpj.UF,
        #                     "municipio": cnpj.MUNICIPIO,
        #                     "ddd1": cnpj.DDD1,
        #                     "telefone1": cnpj.TELEFONE1,
        #                     "ddd2": cnpj.DDD2,
        #                     "telefone2": cnpj.TELEFONE2,
        #                     "ddd_do_fax": cnpj.DDD_FAX,
        #                     "fax": cnpj.FAX,
        #                     "correio_eletronico": cnpj.CORREIO_ELETRONICO,
        #                     "situacao_especial": cnpj.SITUACAO_ESPECIAL,
        #                     "data_da_situacao_especial": cnpj.DT_SITU_ESPECIAL,
        #                     "razao_social_nome_empresarial": cnpj.ESTABELECIMENTOS_EMPRESAS_FK.RAZAO_SOCIAL_NOME_EMPRESARIAL}
            
        #     resultado.append(estabelecimento)

        # return resultado


def read_estabelecimento_nome(nome_fantasia: str):

    resultado = []

    with create_session() as session:
        # cnpjs = session.query(Estabelecimentos).filter(match_expr.in_boolean_mode())
        cnpjs = session.query(Estabelecimentos).filter(Estabelecimentos.NM_FANTASIA.match(nome_fantasia))
        
    for cnpj in cnpjs:

        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()
        
        cnae_fiscal_principal = [item.CNAES for item in fiscal if item.PRINCIPAL == 1]

        cnae_fiscal_secundaria = [item.CNAES for item in fiscal if item.PRINCIPAL == 0]

        estabelecimento = {"id": cnpj.ID,
                           "cnpj": cnpj.CNPJ,
                           "cnpj_basico": cnpj.CNPJ_BASICO,
                           "cnpj_ordem": cnpj.CNPJ_ORDEM, 
                           "cnpj_dv": cnpj.CNPJ_DV,
                           "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
                           "nome_fantasia": cnpj.NM_FANTASIA,
                           "situacao_cadastral": cnpj.SITU_CADASTRAL,
                           "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
                           "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
                           "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
                           "pais": cnpj.PAIZES,
                           "data_de_inicio_atividade": cnpj.DT_INICIO_ATIV,
                           "cnae_fiscal_principal": cnae_fiscal_principal,
                           "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
                           "tipo_de_logradouro": cnpj.TP_LOGRADOURO,
                           "logradouro": cnpj.LOGRADOURO,
                           "numero": cnpj.NUMERO,
                           "complemento": cnpj.COMPLEMENTO,
                           "bairro": cnpj.BAIRRO,
                           "cep": cnpj.CEP,
                           "uf": cnpj.UF,
                           "municipio": cnpj.MUNICIPIO,
                           "ddd1": cnpj.DDD1,
                           "telefone1": cnpj.TELEFONE1,
                           "ddd2": cnpj.DDD2,
                           "telefone2": cnpj.TELEFONE2,
                           "ddd_do_fax": cnpj.DDD_FAX,
                           "fax": cnpj.FAX,
                           "correio_eletronico": cnpj.CORREIO_ELETRONICO,
                           "situacao_especial": cnpj.SITUACAO_ESPECIAL,
                           "data_da_situacao_especial": cnpj.DT_SITU_ESPECIAL}
        
        resultado.append(estabelecimento)

    return resultado


def read_empresa_filiais(razao_social: str):

    with create_session() as session:
        cnpjs = session.query(Empresas).filter(Empresas.RAZAO_SOCIAL_NOME_EMPRESARIAL.match(razao_social)).limit(100)

        resultado = []

    for cnpj in cnpjs:
    
        estabelecimento = session.query(Estabelecimentos).filter(Estabelecimentos.CNPJ == cnpj.CNPJ_BASE).all()

        todos_estabelecimentos = [item.CNPJ for item in estabelecimento]

        estabelecimento = {"cnpj_basico": cnpj.CNPJ_BASE,
                           "razao_social_nome_empresarial": cnpj.RAZAO_SOCIAL_NOME_EMPRESARIAL,
                           "natureza_juridica": cnpj.NATUREZA.DESCRICAO,
                           "qualificacao_responsavel": cnpj.QUALIFICACAO.DESCRICAO,
                           "capital_social": cnpj.CAPITAL_SOCIAL_DA_EMPRESA,
                           "porte_empresa": cnpj.PORTE_EMPRESA,
                           "ente_federativo": cnpj.ENTE_FEDERATIVO_RESPONSAVEL,
                           "filiais": todos_estabelecimentos}
        
        resultado.append(estabelecimento)

    return resultado


def read_estabelecimento_cnpj(cnpj: str):

    # match_expr = match(Estabelecimentos.CNPJ, Estabelecimentos.NM_FANTASIA, against=correspondencia)

    resultado = []

    with create_session() as session:
        cnpjs = session.query(Estabelecimentos).filter(Estabelecimentos.CNPJ == cnpj)

    for cnpj in cnpjs:
    
        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

        cnae_fiscal_principal = None

        for item in fiscal:
            if item.PRINCIPAL == 1:
                cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
                break

        cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

        estabelecimento = {"id": cnpj.ID,
                           "cnpj": cnpj.CNPJ,
                           "cnpj_basico": cnpj.CNPJ_BASICO,
                           "cnpj_ordem": cnpj.CNPJ_ORDEM, 
                           "cnpj_dv": cnpj.CNPJ_DV,
                           "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
                           "nome_fantasia": cnpj.NM_FANTASIA,
                           "situacao_cadastral": cnpj.SITU_CADASTRAL,
                           "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
                           "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
                           "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
                           "pais": cnpj.PAIZES,
                           "data_de_inicio_atividade": cnpj.DT_INICIO_ATIV,
                           "cnae_fiscal_principal": cnae_fiscal_principal,
                           "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
                           "tipo_de_logradouro": cnpj.TP_LOGRADOURO,
                           "logradouro": cnpj.LOGRADOURO,
                           "numero": cnpj.NUMERO,
                           "complemento": cnpj.COMPLEMENTO,
                           "bairro": cnpj.BAIRRO,
                           "cep": cnpj.CEP,
                           "uf": cnpj.UF,
                           "municipio": cnpj.MUNICIPIO,
                           "ddd1": cnpj.DDD1,
                           "telefone1": cnpj.TELEFONE1,
                           "ddd2": cnpj.DDD2,
                           "telefone2": cnpj.TELEFONE2,
                           "ddd_do_fax": cnpj.DDD_FAX,
                           "fax": cnpj.FAX,
                           "correio_eletronico": cnpj.CORREIO_ELETRONICO,
                           "situacao_especial": cnpj.SITUACAO_ESPECIAL,
                           "data_da_situacao_especial": cnpj.DT_SITU_ESPECIAL,
                           "razao_social_nome_empresarial": cnpj.ESTABELECIMENTOS_EMPRESAS_FK.RAZAO_SOCIAL_NOME_EMPRESARIAL}
        
        resultado.append(estabelecimento)

    return resultado        
