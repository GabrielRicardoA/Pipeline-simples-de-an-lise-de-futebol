#%%
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

#%%

def transformar_dados() -> tuple[pd.DataFrame, ...]:

    caminho_raw = Path("../data/raw/")

    tabela_ano_da_competicao = pq.read_table(caminho_raw / "ano_da_competicao.parquet")

    df_ano_da_competicao = tabela_ano_da_competicao.to_pandas()


    tabela_dados_competicao = pq.read_table(caminho_raw / "dados_competicao.parquet")

    df_competicao = tabela_dados_competicao.to_pandas() 



    tabela_partidas = pq.read_table( caminho_raw / "partidas.parquet")

    df_partidas = tabela_partidas.to_pandas()



    tabela_resumo_competicao = pq.read_table(caminho_raw / "resumo_competicao.parquet")

    df_resumo_competicao = tabela_resumo_competicao.to_pandas()


    df_partidas.columns = [
        "ID_da_partida",
        "Data_UTC",
        "Status",
        "Rodada",
        "Fase",
        "Grupo",
        "Ultima_atualizacao",
        
        "Arbitros",
        
        "ID_da_area",
        "Nome_da_area",
        "Codigo_da_area",
        "Bandeira_da_area",
        
        "ID_da_competicao",
        "Nome_da_competicao",
        "Codigo_da_competicao",
        "Tipo_da_competicao",
        "Emblema_da_competicao",
        
        "ID_da_temporada",
        "Inicio_da_temporada",
        "Fim_da_temporada",
        "Rodada_atual_da_temporada",
        "Vencedor_da_temporada",
        
        "ID_time_casa",
        "Nome_time_casa",
        "Nome_curto_time_casa",
        "Sigla_time_casa",
        "Escudo_time_casa",
        
        "ID_time_fora",
        "Nome_time_fora",
        "Nome_curto_time_fora",
        "Sigla_time_fora",
        "Escudo_time_fora",
        
        "Vencedor_da_partida",
        "Duracao_da_partida",
        
        "Gols_casa_tempo_completo",
        "Gols_fora_tempo_completo",
        
        "Gols_casa_primeiro_tempo",
        "Gols_fora_primeiro_tempo",
        
        "Mensagem_odds",
        
        "Gols_casa_tempo_normal",
        "Gols_fora_tempo_normal",
        
        "Gols_casa_prorrogacao",
        "Gols_fora_prorrogacao",
        
        "Gols_casa_penaltis",
        "Gols_fora_penaltis"
    ]

    
    df_partidas_info = df_partidas[[
        "ID_da_partida",
        "Data_UTC",
        "Status",
        "Rodada",
        "ID_time_casa",
        "Nome_time_casa",
        "ID_time_fora",
        "Nome_time_fora",
        "Fase",
        "Grupo",
        "Ultima_atualizacao",
    ]].copy()

   
    df_times_casa = df_partidas[[
        "ID_time_casa",
        "Nome_time_casa",
        "Nome_curto_time_casa",
        "Sigla_time_casa",
        "Escudo_time_casa"
    ]].copy()

    df_times_casa.columns = [
        "ID_time",
        "Nome_time",
        "Nome_curto_time",
        "Sigla_time",
        "Escudo_time"
    ]


    df_times_fora = df_partidas[[
        "ID_time_fora",
        "Nome_time_fora",
        "Nome_curto_time_fora",
        "Sigla_time_fora",
        "Escudo_time_fora"
    ]].copy()

    df_times_fora.columns = [
        "ID_time",
        "Nome_time",
        "Nome_curto_time",
        "Sigla_time",
        "Escudo_time"
    ]


    df_times = pd.concat([df_times_casa, df_times_fora], ignore_index=True)

    df_times = df_times.drop_duplicates(subset="ID_time").reset_index(drop=True)

   
    df_resultados_partida  = df_partidas[[
        "ID_da_partida",
        "Vencedor_da_partida",
        "Duracao_da_partida",

        "ID_time_casa",
        "Nome_time_casa",
        "ID_time_fora",
        "Nome_time_fora",
        
        "Gols_casa_tempo_completo",
        "Gols_fora_tempo_completo",
        
        "Gols_casa_primeiro_tempo",
        "Gols_fora_primeiro_tempo",
        
        "Gols_casa_tempo_normal",
        "Gols_fora_tempo_normal",
        
        "Gols_casa_prorrogacao",
        "Gols_fora_prorrogacao",
        
        "Gols_casa_penaltis",
        "Gols_fora_penaltis"
    
    ]].copy()
   
    df_competicao.columns = [
        "ID_da_competicao",
        "Nome_da_competicao",
        "Codigo_da_competicao",
        "Tipo_da_competicao",
        "Escudo_da_competicao"
    ]


    df_resumo_competicao.columns = [
        "Quantidade_de_partidas",
        "Primeira_partida",
        "Ultima_partida",
        "Partidas_jogadas"
    ]
 

    df_ano_da_competicao.columns = [
        "Temporada"
    ]

    return (df_partidas,
            df_ano_da_competicao,
            df_resumo_competicao,
            df_competicao,
            df_resultados_partida,
            df_partidas_info,
            df_times)




