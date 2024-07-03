from app import app

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse

from pydantic import BaseModel

from app.servicos.read_db import procurar_lugar, read_clusters

import pandas as pd

import folium

from datetime import datetime

import re


class PesquisarLocalEmpresa(BaseModel):
    estado: str
    cidade: str
    tipo_empresa: str
    componentes: bool = False


@app.get('/api/v1/sugerir-local-empresa')
def segerir_abertura_empresa(parametros: PesquisarLocalEmpresa = Depends()):
    
    clusters = procurar_lugar(
        estado=parametros.estado,
        cidade=parametros.cidade
    )

    if clusters == []:
        return HTTPException(
            status_code=404,
            detail={
                "datetime": datetime.now(),
                "messagem": "Os parâmetros solicitados não foram encontrados no banco de dados."
            }
        )
    

    clusters = pd.DataFrame(clusters, columns=['cluster', 'tipo', 'quantidade'])
    cluster_com_tipo = clusters.loc[(clusters['tipo'].notnull()) & (clusters['tipo'] == parametros.tipo_empresa), 'cluster'].unique()
    pontuacao = clusters.loc[clusters['cluster'].isin(cluster_com_tipo), ['tipo', 'quantidade']].groupby('tipo').mean('quantidade')
    pontuacao_dict = pontuacao['quantidade'].to_dict()

    # Excluir clusters que já possuem aquele tipo
    cluster = clusters[~clusters['cluster'].isin(cluster_com_tipo.tolist())]

    ranking_cluster = {}

    for cluster_id in cluster['cluster'].unique():
        pontuacao_cluster = 0
        
        # Split the 'tipo' string into a list of types
        tipos = cluster.loc[cluster['cluster'] == cluster_id]
        

        for tipo in tipos['tipo']:
            try:
                pontuacao_cluster += pontuacao_dict[tipo]
            except KeyError:
                pass

        ranking_cluster[cluster_id] = pontuacao_cluster

    ranking_cluster_df = pd.DataFrame.from_dict(ranking_cluster, orient='index', columns=['pontuacao']).reset_index()
    ranking_cluster_df.rename(columns={'index':'cluster'}, inplace=True)
    ranking_cluster_df = ranking_cluster_df.nlargest(10, columns='pontuacao')

    cluster_ids = ranking_cluster_df['cluster'].to_list()

    resultado_clusters = read_clusters(clusters=cluster_ids)
    resultado_clusters = pd.DataFrame(resultado_clusters, columns=['cluster', 'lat', 'lon', 'bairro', 'uf', 'localidade'])

    resultado_clusters['cluster'] = resultado_clusters['cluster'].astype(int)
    ranking_cluster_df['cluster'] = ranking_cluster_df['cluster'].astype(float).astype(int)

    resultado_clusters['lat'] = resultado_clusters['lat'].astype(float)
    resultado_clusters['lon'] = resultado_clusters['lon'].astype(float)

    resultado_final = resultado_clusters.merge(ranking_cluster_df, on='cluster')
    resultado_final = resultado_final.groupby('cluster').mean(['lon', 'lat']).reset_index()

    resultado_clusters = resultado_clusters.drop_duplicates(subset='cluster', keep='first')

    resultado_final = resultado_final.merge(resultado_clusters[['cluster', 'bairro', 'uf', 'localidade']], how='left', on='cluster').nlargest(10, columns='pontuacao').reset_index()

    if parametros.componentes:
        m = folium.Map(location=[resultado_final.lat.mean(), resultado_final.lon.mean()], zoom_start=10, tiles='OpenStreetMap', width=800, height=600)

        for i, row in resultado_final.iterrows():
            descricao = f"Posição: {1+i}° lugar, UF: {row.uf}, Cidade: {row.localidade}, Bairro: {row.bairro}"
            folium.CircleMarker(
                location=[row.lat, row.lon],
                radius=15,
                tooltip=f'{i + 1}° lugar',
                popup=descricao, #re.sub(r'[^a-zA-Z ]+', '', row.cluster),
                color='#1787FE',
                fill=True,
                fill_colour='#1787FE'
            ).add_to(m)

        m.get_root().render()
        header = re.sub('\n', '', m.get_root().header.render())
        body_html = re.sub('\n', '', m.get_root().html.render())
        script = re.sub('\n', '', m.get_root().script.render())

        return JSONResponse(
            content={
                "datetime": str(datetime.now()),
                "resultado": {
                    "header": header,
                    "body_html": body_html,
                    "script": script
                } 
            },
            status_code=201
        )
    
    info_resultado = {
        "localizacao": [resultado_final.lat.mean(), resultado_final.lon.mean()],
        "locais": []
    }

    for i, row in resultado_final.iterrows():
        descricao = {"posicao": i+1, "uf": row.uf, "cidade": row.localidade, "bairro": row.bairro}
        
        resultado = {
            "descricao": descricao,
            "localizacao": [row.lat, row.lon]
        }

        info_resultado['locais'].append(resultado)

    return JSONResponse(
        content={
            "datetime": str(datetime.now()),
            "resultado": info_resultado
        },
        status_code=201
    )
