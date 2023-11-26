from app.bd.conexao_bd import create_session

from app.models.cnpj_base_model import Estabelecimentos, Fiscal, Empresas

from sqlalchemy.dialects.mysql import match



def read_empresa_filiais(razao_social: str):

    with create_session() as session:
        cnpjs = session.query(Empresas).filter(Empresas.RAZAO_SOCIAL_NOME_EMPRESARIAL.match(razao_social)).limit(100)

        resultado = []

    for cnpj in cnpjs:
    
        estabelecimento = session.query(Estabelecimentos).filter(Estabelecimentos.CNPJ == cnpj.CNPJ_BASE).all()

        todos_estabelecimentos = [item.CNPJ for item in estabelecimento]

        estabelecimento = {"cnpj_basico": cnpj.CNPJ_BASICO,
                           "razao_social_nome_empresarial": cnpj.RAZAO_SOCIAL_NOME_EMPRESARIAL,
                           "natureza_juridica": cnpj.NATUREZA.DESCRICAO,
                           "qualificacao_responsavel": cnpj.QUALIFICACAO.DESCRICAO,
                           "capital_social": cnpj.CAPITAL_SOCIAL_DA_EMPRESA,
                           "porte_empresa": cnpj.PORTE_EMPRESA,
                           "ente_federativo": cnpj.ENTE_FEDERATIVO_RESPONSAVEL,
                           "filiais": todos_estabelecimentos}
        
        resultado.append(estabelecimento)

    return resultado



def read_estabelecimento_nome(nome_fantasia: str):

    # match_expr = match(Estabelecimentos.CNPJ, Estabelecimentos.NM_FANTASIA, against=correspondencia)

    resultado = []

    with create_session() as session:
        # cnpjs = session.query(Estabelecimentos).filter(match_expr.in_boolean_mode())
        cnpjs = session.query(Estabelecimentos).filter(Estabelecimentos.NM_FANTASIA.match(nome_fantasia))

    for cnpj in cnpjs:
    
        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

        cnae_fiscal_principal = None


        for item in fiscal:
            if item.PRINCIPAL == 1:
                cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
                break

        cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

        estabelecimento = {"cnpj": cnpj.CNPJ,
                           "cnpj_basico": cnpj.CNPJ_BASICO,
                           "cnpj_ordem": cnpj.CNPJ_ORDEM, 
                           "cnpj_dv": cnpj.CNPJ_DV,
                           "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
                           "nome_fantasia": cnpj.NM_FANTASIA,
                           "situacao_cadastral": cnpj.SITU_CADASTRAL,
                           "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
                           "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
                           "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
                           "pais": cnpj.PAIS,
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


def read_estabelecimento_cnpj(cnpj: str):

    # match_expr = match(Estabelecimentos.CNPJ, Estabelecimentos.NM_FANTASIA, against=correspondencia)

    resultado = []

    with create_session() as session:
        # cnpjs = session.query(Estabelecimentos).filter(match_expr.in_boolean_mode())
        cnpjs = session.query(Estabelecimentos).filter(Estabelecimentos.CNPJ == cnpj)

    for cnpj in cnpjs:
    
        fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

        cnae_fiscal_principal = None


        for item in fiscal:
            if item.PRINCIPAL == 1:
                cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
                break

        cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

        estabelecimento = {"cnpj": cnpj.CNPJ,
                           "cnpj_basico": cnpj.CNPJ_BASICO,
                           "cnpj_ordem": cnpj.CNPJ_ORDEM, 
                           "cnpj_dv": cnpj.CNPJ_DV,
                           "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
                           "nome_fantasia": cnpj.NM_FANTASIA,
                           "situacao_cadastral": cnpj.SITU_CADASTRAL,
                           "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
                           "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
                           "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
                           "pais": cnpj.PAIS,
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


def read_estabelecimentos_por_tipo(tipo):

    with create_session() as session:

        tipos = session.query(Tipo).filter(Tipo.tipo == tipo).first()

        conjunto_cnaes = tipos.cnaes.split()

        cnpj_correspondentes = session.query(Fiscal).filter(Fiscal.CNAES_FK.in_(conjunto_cnaes))


        for fiscal in cnpj_correspondentes:
    
            fiscal = session.query(Fiscal).filter(Fiscal.CNPJ == cnpj.CNPJ).all()

            cnae_fiscal_principal = None


            for item in fiscal:
                if item.PRINCIPAL == 1:
                    cnae_fiscal_principal = item.CNAES_FK.DESCRICAO
                    break

            cnae_fiscal_secundaria = [item.CNAES_FK.DESCRICAO for item in fiscal if item.PRINCIPAL == 0]

            estabelecimento = {"cnpj": cnpj.CNPJ,
                            "cnpj_basico": cnpj.CNPJ_BASICO,
                            "cnpj_ordem": cnpj.CNPJ_ORDEM, 
                            "cnpj_dv": cnpj.CNPJ_DV,
                            "identificador_matriz_filial": cnpj.ID_MATRIZ_FILIAL,
                            "nome_fantasia": cnpj.NM_FANTASIA,
                            "situacao_cadastral": cnpj.SITU_CADASTRAL,
                            "data_situacao_cadastral": cnpj.DT_SITU_CADASTRAL,
                            "motivo_situacao_cadastral": cnpj.MT_SITU_CADASTRAL,
                            "nome_da_cidade_no_exterior": cnpj.CIDADE_EXTERIOR,
                            "pais": cnpj.PAIS,
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

        
