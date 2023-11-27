from app.models.cnpj_base_model import Estabelecimentos, Empresas, Fiscal
from app.models.dominios_model import Motivos, Cnaes, Qualificacao, Natureza

from app.bd.conexao_bd import create_session



def create_estabelecimentos(CNPJ,
    CNPJ_BASICO,    
    CNPJ_ORDEM,
    CNPJ_DV,
    ID_MATRIZ_FILIAL,
    NM_FANTASIA,
    SITU_CADASTRAL,
    MT_SITU_CADASTRAL, 
    CIDADE_EXTERIOR,
    PAIS,
    DT_INICIO_ATIV,
    DT_SITU_ESPECIAL,
    HASH):

    estabelecimentos: Estabelecimentos = Estabelecimentos(CNPJ = CNPJ,
    CNPJ_BASICO = CNPJ_BASICO,    
    CNPJ_ORDEM = CNPJ_ORDEM,
    CNPJ_DV = CNPJ_DV,
    ID_MATRIZ_FILIAL = ID_MATRIZ_FILIAL,
    NM_FANTASIA = NM_FANTASIA,
    SITU_CADASTRAL = SITU_CADASTRAL,
    MT_SITU_CADASTRAL = MT_SITU_CADASTRAL, 
    CIDADE_EXTERIOR = CIDADE_EXTERIOR,
    PAIS = PAIS,
    DT_INICIO_ATIV = DT_INICIO_ATIV,
    DT_SITU_ESPECIAL = DT_SITU_ESPECIAL,
    HASH = HASH)

    with create_session() as session:
        session.add(estabelecimentos)
        session.commit()


def create_motivos(ID, DESCRICAO):

    motivos: Motivos = Motivos(ID = ID, DESCRICAO = DESCRICAO)

    with create_session() as session:
        session.add(motivos)
        session.commit()


def create_empresas(CNPJ_BASE):

    empresa: Empresas = Empresas(CNPJ_BASE = CNPJ_BASE, QUALIFICACAO_DO_RESPONSAVEL = "1", NATUREZA_JURIDICA="1")

    with create_session() as session:
        session.add(empresa)
        session.commit()