#%%
import pandas as pd
import requests
from config import api_key
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq


def extrair_dados():
    link_api = "https://api.football-data.org/v4/competitions/CL/matches"



    headers = {
        "X-Auth-Token": api_key
    }

    resposta_api = requests.get(link_api,headers=headers)

    

    if resposta_api.status_code == 200:
        dict_dados_api = resposta_api.json()
    else:
        raise Exception(f"Erro na API: {resposta_api.status_code}")



    #guardar dados nos dicionarios json respectivos 

    partidas = dict_dados_api["matches"]

    competition = dict_dados_api["competition"]

    resultados = dict_dados_api["resultSet"]

    filtros = dict_dados_api["filters"]



    #transformar os dicionarios json em dfs e salvar na raw

    caminho_raw = Path("../data/raw")
    caminho_raw.mkdir(parents=True , exist_ok=True)



    df_partidas = pd.json_normalize(partidas)

    df_competicao = pd.json_normalize(competition)


    df_resumo_competicao = pd.json_normalize(resultados)


    df_ano_da_competicao = pd.json_normalize(filtros)




    #transformar os dicionarios json em dfs e salvar na raw

    caminho_raw = Path("../data/raw")



    #passar os dfs para tabela parquet pelo pyarrow 

    tabela_partida = pa.Table.from_pandas(df_partidas)

    tabela_competicao = pa.Table.from_pandas(df_competicao)

    tabela_resumo_competicao = pa.Table.from_pandas(df_resumo_competicao)

    tabela_ano_da_competicao = pa.Table.from_pandas(df_ano_da_competicao)



    pq.write_table(tabela_partida,  caminho_raw / "partidas.parquet")

    pq.write_table(tabela_competicao, caminho_raw / "dados_competicao.parquet")

    pq.write_table(tabela_resumo_competicao , caminho_raw /"resumo_competicao.parquet")

    pq.write_table(tabela_ano_da_competicao , caminho_raw /"ano_da_competicao.parquet")


