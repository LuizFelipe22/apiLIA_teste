from app.bd.conexao_bd import create_session

from app.models.cnpj_base_model import Estabelecimentos, Fiscal, Empresas, Nm_Estab_Empresas
from app.models.dominios_model import TiposCnaes, Tipos, Cluster

from sqlalchemy.dialects.mysql import match

from sqlalchemy import and_, func

from math import ceil

from typing import Literal

from datetime import datetime, date


def read_empresa(cnpj: str = None,
                 nome: str = None,
                 matriz: str = None,
                 uf: str = None,
                 cep: str = None,
                 pagina: int = 0,
                 tamanho: int = 50,
                 capital_min: float = 0,
                 capital_max: float = 9_000_000_000_000_000_000,
                 abertura_de: date = date(1850, 1, 1),
                 abertura_ate: date = date.today(),
                 porte_empresa = None) -> dict:

    lista = [matriz, uf, cep, porte_empresa]

    pesquisa1 = [Estabelecimentos.id_matriz_filial,
                 Estabelecimentos.uf,
                 Estabelecimentos.cep,
                 Empresas.porte_empresa]

    pesquisa2 =[Estabelecimentos.cnpj.like(f'{cnpj}%'),
                match(Nm_Estab_Empresas.nm_fantasia, Nm_Estab_Empresas.razao_social_nome_empresarial, against=f'{nome}').in_natural_language_mode(),
                Empresas.capital_social_da_empresa.between(cleft=capital_min, cright=capital_max),
                Estabelecimentos.dt_inicio_ativ.between(cleft=abertura_de, cright=abertura_ate)]

    pesquisar = [(coluna == parametro) for parametro, coluna in zip(lista, pesquisa1) if parametro]

    for i, parametro in enumerate([cnpj, nome, capital_min, abertura_de]):
        if parametro:
            pesquisar.append(pesquisa2[i])

    resultado = []

    with create_session() as session:
        
        query = session.query(Estabelecimentos) \
            .join(Nm_Estab_Empresas, Nm_Estab_Empresas.cnpj_base == Estabelecimentos.cnpj_base) \
            .join(Empresas, Estabelecimentos.cnpj_base == Empresas.cnpj_base) \
            .filter(and_(*pesquisar))
    
        quantidade = query.count()
        minimo = tamanho * pagina
        maximo = tamanho * (pagina + 1)
        resultados = query.slice(minimo, maximo)
        
    for estabelecimentos in resultados:

        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == estabelecimentos.CNPJ).all()

        cnae_fiscal_principal = [{item.CNAE: item.CNAES.DESCRICAO} for item in fiscal if item.PRINCIPAL == 1]
        cnae_fiscal_secundaria = [{item.CNAE: item.CNAES.DESCRICAO} for item in fiscal if item.PRINCIPAL == 0]


        estabelecimento = {"cnpj": estabelecimentos.cnpj,
                           "cnpj_base": estabelecimentos.empresas.cnpj_base,
                           "razao_social_nome_empresarial": estabelecimentos.empresas.razao_social_nome_empresarial,
                           "natureza_juridica": estabelecimentos.empresas.natureza_juridica,
                           "qualificacao_responsavel": estabelecimentos.empresas.qualificacao_do_responsavel,
                           "capital_social": estabelecimentos.empresas.capital_social_da_empresa,
                           "porte_empresa": estabelecimentos.empresas.porte_empresa,
                           "ente_federativo_responsavel": estabelecimentos.empresas.ente_federativo_responsavel,
                        #    "cnpj_base": estabelecimentos.cnpj_base,
                           "cnpj_ordem": estabelecimentos.cnpj_ordem, 
                           "cnpj_dv": estabelecimentos.cnpj_dv,
                           "identificador_matriz_filial": estabelecimentos.id_matriz_filial,
                           "nome_fantasia": estabelecimentos.nm_fantasia,
                           "situacao_cadastral": estabelecimentos.situ_cadastral,
                           "data_situacao_cadastral": str(estabelecimentos.dt_situ_cadastral) if estabelecimentos.dt_situ_cadastral else None,
                           "motivo_situacao_cadastral": estabelecimentos.mt_situ_cadastral,
                           "nome_da_cidade_no_exterior": estabelecimentos.cidade_exterior,
                           "pais": estabelecimentos.pais,
                           "data_de_inicio_atividade": str(estabelecimentos.dt_inicio_ativ) if estabelecimentos.dt_inicio_ativ else None,
                           "cnae_fiscal_principal": cnae_fiscal_principal[0],
                           "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
                           "tipo_de_logradouro": estabelecimentos.tp_logradouro,
                           "logradouro": estabelecimentos.logradouro,
                           "numero": estabelecimentos.numero,
                           "complemento": estabelecimentos.complemento,
                           "bairro": estabelecimentos.bairro,
                           "cep": estabelecimentos.cep,
                           "uf": estabelecimentos.uf,
                           "municipio": estabelecimentos.municipio,
                           "ddd1": estabelecimentos.ddd1,
                           "telefone1": estabelecimentos.telefone1,
                           "ddd2": estabelecimentos.ddd2,
                           "telefone2": estabelecimentos.telefone2,
                           "ddd_do_fax": estabelecimentos.ddd_fax,
                           "fax": estabelecimentos.fax,
                           "correio_eletronico": estabelecimentos.correio_eletronico,
                           "situacao_especial": estabelecimentos.situacao_especial,
                           "data_da_situacao_especial": str(estabelecimentos.dt_situ_especial) if estabelecimentos.dt_situ_especial else None}
        
        # empresa = {"cnpj_base": estabelecimentos.EMPRESAS.cnpj_base,
        #             "razao_social_nome_empresarial": estabelecimentos.EMPRESAS.RAZAO_SOCIAL_NOME_EMPRESARIAL,
        #             "natureza_juridica": estabelecimentos.EMPRESAS.NATUREZA_JURIDICA,
        #             "qualificacao_responsavel": estabelecimentos.EMPRESAS.QUALIFICACAO_DO_RESPONSAVEL,
        #             "capital_social": estabelecimentos.EMPRESAS.CAPITAL_SOCIAL_DA_EMPRESA,
        #             "porte_empresa": estabelecimentos.EMPRESAS.PORTE_EMPRESA,
        #             "ente_federativo_responsavel": estabelecimentos.EMPRESAS.ENTE_FEDERATIVO_RESPONSAVEL}
        
        # try:
        #     resultado[estabelecimentos.EMPRESAS.cnpj_base]['filial'].append(estabelecimento)
        # except KeyError:
        #     empresa['filial'] = [estabelecimento]
        #     resultado[estabelecimentos.EMPRESAS.cnpj_base] = empresa
        resultado.append(estabelecimento)


    return {"resposta": resultado, # [valor for _, valor in resultado.items()],
            "total_registros": quantidade,
            "pagina": pagina,
            "max_paginas": ceil(quantidade / 50)}


def read_estabelecimentos_por_tipo(busca_tipo: str):

    with create_session() as session:
        tipos = session.query(Tipos).filter(Tipos.tipo == busca_tipo)

    lista_cnaes = [cnae.cnaes for tipo in tipos for cnae in tipo.Tipos_Cnaes]

    return lista_cnaes


def procurar_lugar(estado: str, cidade: str) -> list:
    with create_session() as session:
        consulta = session.query(Cluster.cluster, Tipos.tipo, func.count().label('quantidade')) \
                .join(Estabelecimentos, Estabelecimentos.cep == Cluster.cep) \
                .join(Fiscal, Estabelecimentos.cnpj == Fiscal.cnpj) \
                .join(TiposCnaes, TiposCnaes.cnaes == Fiscal.cnae) \
                .join(Tipos, Tipos.id == TiposCnaes.id_tipos) \
                .filter(Estabelecimentos.UF == estado, Estabelecimentos.municipio == cidade, Fiscal.principal == 1) \
                .group_by(Cluster.cluster, Tipos.tipo) \
                .order_by(func.count().desc()) \
                .distinct()
    
    return consulta.all()


def read_clusters(clusters: list):
    with create_session() as session:
        consulta = session.query(Cluster.cluster, Cluster.lat, Cluster.lon, Cluster.bairro, Cluster.uf, Cluster.localidade) \
                   .filter(Cluster.cluster.in_(clusters)).distinct()
        
    return consulta.all()

        
    # 1 - Consultar no banco na tabela de cluster o estado e a cidade que desejamos colocar o estabelecimento
    #   - Retornar todos os cluster ques estão naquela cidade
    #   - Fazer um JOIN usando o campo 'cep' na tabela estabelecimentos para pegar as empresas que estão naquele local, outro JOIN na tabela tipos para saber que tipo é essa empresa

    # - Consulta reversa para pegar alguns exemplos de cluster que possue atributos parecidos
     
    # 2 - Fazer um groupby nas colunas cluster e tipos

            
                

        #     fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

        #     cnae_fiscal_principal = None


        #     for item in fiscal:
        #         if item.PRINCIPAL == 1:
        #             cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
        #             break

        #     cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

        #     estabelecimento = {"cnpj": cnpj.CNPJ,
        #                     "cnpj_base": cnpj.cnpj_base,
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
        cnpjs = session.query(Estabelecimentos).filter(Estabelecimentos.nm_fantasia.match(nome_fantasia))
        
    for cnpj in cnpjs:

        fiscal = session.query(Fiscal).filter(Fiscal.cnpj == cnpj.cnpj).all()
        
        cnae_fiscal_principal = [item.CNAES for item in fiscal if item.principal == 1]

        cnae_fiscal_secundaria = [item.CNAES for item in fiscal if item.principal == 0]

        estabelecimento = {"cnpj": cnpj.cnpj,
                           "cnpj_base": cnpj.cnpj_base,
                           "cnpj_ordem": cnpj.cnpj_ordem, 
                           "cnpj_dv": cnpj.cnpj_dv,
                           "identificador_matriz_filial": cnpj.id_matriz_filial,
                           "nome_fantasia": cnpj.nm_fantasia,
                           "situacao_cadastral": cnpj.situ_cadastral,
                           "data_situacao_cadastral": cnpj.dt_situ_cadastral,
                           "motivo_situacao_cadastral": cnpj.mt_situ_cadastral,
                           "nome_da_cidade_no_exterior": cnpj.cidade_exterior,
                           "pais": cnpj.pais,
                           "data_de_inicio_atividade": cnpj.dt_inicio_ativ,
                           "cnae_fiscal_principal": cnae_fiscal_principal,
                           "cnae_fiscal_secundaria": cnae_fiscal_secundaria,
                           "tipo_de_logradouro": cnpj.tp_logradouro,
                           "logradouro": cnpj.logradouro,
                           "numero": cnpj.numero,
                           "complemento": cnpj.complemento,
                           "bairro": cnpj.bairro,
                           "cep": cnpj.cep,
                           "uf": cnpj.uf,
                           "municipio": cnpj.municipio,
                           "ddd1": cnpj.ddd1,
                           "telefone1": cnpj.telefone1,
                           "ddd2": cnpj.ddd2,
                           "telefone2": cnpj.telefone2,
                           "ddd_do_fax": cnpj.ddd_fax,
                           "fax": cnpj.fax,
                           "correio_eletronico": cnpj.correio_eletronico,
                           "situacao_especial": cnpj.situacao_especial,
                           "data_da_situacao_especial": cnpj.dt_situ_especial}
        
        resultado.append(estabelecimento)

    return resultado


def read_empresa_filiais(razao_social: str):

    with create_session() as session:
        cnpjs = session.query(Empresas).filter(Empresas.RAZAO_SOCIAL_NOME_EMPRESARIAL.match(razao_social)).limit(100)

        resultado = []

    for cnpj in cnpjs:
    
        estabelecimento = session.query(Estabelecimentos).filter(Estabelecimentos.CNPJ == cnpj.cnpj_base).all()

        todos_estabelecimentos = [item.CNPJ for item in estabelecimento]

        estabelecimento = {"cnpj_base": cnpj.cnpj_base,
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
                           "cnpj_base": cnpj.cnpj_base,
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
