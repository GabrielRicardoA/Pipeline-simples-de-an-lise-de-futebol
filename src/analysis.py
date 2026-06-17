#%%
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from pathlib import Path

def analisar_dados_e_criar_graficos():
    # pegar os dados procesados em pyarrow.parquet em tranformar em dataframes e criar pasta analitics
    caminho_processed = Path("../data/processed")
    caminho_analitcs = Path("../data/analitics")
    caminho_analitcs.mkdir(parents=True, exist_ok=True)

    # leitura dos pyarrow.parquet
    ano_da_competicao = pq.read_table(caminho_processed / "ano_da_competicao.parquet")
    competicao = pq.read_table(caminho_processed / "competicao.parquet")
    partidas_info = pq.read_table(caminho_processed / "partidas_info.parquet")
    partidas = pq.read_table(caminho_processed / "partidas.parquet")
    resultados_partidas = pq.read_table(caminho_processed / "resultados_partida.parquet")
    resumo_competicao = pq.read_table(caminho_processed / "resumo_competicao.parquet")
    times = pq.read_table(caminho_processed / "times.parquet")

    # conversao para dataframe pandas novamente para ajudar o vscode
    df_ano_da_competicao : pd.DataFrame = ano_da_competicao.to_pandas()
    df_competicao : pd.DataFrame = competicao.to_pandas()
    df_partidas_info : pd.DataFrame = partidas_info.to_pandas()
    df_partidas : pd.DataFrame = partidas.to_pandas()
    df_resultados_partidas : pd.DataFrame = resultados_partidas.to_pandas()
    df_resumo_competicao : pd.DataFrame = resumo_competicao.to_pandas()
    df_times : pd.DataFrame = times.to_pandas()


    # Filtros de Zona Neutra (Campo Neutro)
    filtro_partidas_sem_zona_neutra = (df_partidas["Fase"] != "FINAL")
    df_partidas_sem_zona_neutra = df_partidas[filtro_partidas_sem_zona_neutra]

    filtro_partidas_info_sem_zona_neutra = (df_partidas_info["Fase"] != "FINAL")
    df_partidas_info_sem_zona_neutra = df_partidas_info[filtro_partidas_info_sem_zona_neutra]

    # Filtro para os resultados baseado nas partidas sem zona neutra
    ids_sem_zona_neutra = df_partidas_info_sem_zona_neutra["ID_da_partida"]
    df_resultados_sem_zona = df_resultados_partidas[df_resultados_partidas["ID_da_partida"].isin(ids_sem_zona_neutra)]


    # quantidade de partidas 
    quantidade_de_partidas = df_resumo_competicao[["Quantidade_de_partidas"]]
    tabela_quantidade_de_partidas = pa.Table.from_pandas(quantidade_de_partidas)
    pq.write_table(tabela_quantidade_de_partidas, caminho_analitcs / "quantidade_de_partidas.parquet")


    # quantidades de partidas por fases
    quantidade_de_partidas_por_fase = df_partidas_info["Fase"].value_counts()
    partidas_por_fase_array = pa.array(quantidade_de_partidas_por_fase)


    # media de gols por partida
    df_resultados_partidas["gols_na_partida"] = (df_resultados_partidas["Gols_casa_tempo_completo"].fillna(0) + df_resultados_partidas["Gols_fora_tempo_completo"].fillna(0))
    gols_total_da_competicao = df_resultados_partidas["gols_na_partida"].sum()
    media_de_gols_por_partida = gols_total_da_competicao / df_resultados_partidas.shape[0]


    # time com mais vitorias fora de casa 
    df_mais_vitorias_fora = df_resultados_sem_zona["Vencedor_da_partida"] == "AWAY_TEAM"
    mais_venceram_fora = df_resultados_sem_zona[df_mais_vitorias_fora]["Nome_time_fora"].value_counts()
    mais_venceram_fora_array = pa.array(mais_venceram_fora)


    # time com mais vitorias dentro de casa 
    df_mais_vitorias_casa = df_resultados_sem_zona["Vencedor_da_partida"] == "HOME_TEAM"
    mais_venceram_casa = df_resultados_sem_zona[df_mais_vitorias_casa]["Nome_time_casa"].value_counts()
    mais_venceram_casa_array = pa.array(mais_venceram_casa) 


    # times que mais venceram
    times_que_mais_venceram = mais_venceram_fora.add(mais_venceram_casa, fill_value=0).sort_values(ascending=False)
    times_que_mais_venceram_array = pa.array(times_que_mais_venceram)


    # Times com mais gols marcados em casa vs fora
    gols_marcados_fora = df_resultados_sem_zona.groupby(by="Nome_time_fora")["Gols_fora_tempo_completo"].sum().sort_values(ascending=False)
    ordem_gols_marcados_fora = gols_marcados_fora.head(10)
    ordem_gols_marcados_fora_array = pa.array(ordem_gols_marcados_fora)

    gols_marcados_casa = df_resultados_sem_zona.groupby(by="Nome_time_casa")["Gols_casa_tempo_completo"].sum().sort_values(ascending=False)
    ordem_gols_marcados_casa = gols_marcados_casa.head(10)
    ordem_gols_marcados_casa_array = pa.array(ordem_gols_marcados_casa)

    # Times com mais gols marcados no total
    gols_por_time = gols_marcados_fora.add(gols_marcados_casa, fill_value=0).sort_values(ascending=False).head(10)
    gols_por_time_array = pa.array(gols_por_time)


    # Partidas em casa vs fora 
    partidas_em_casa = df_partidas_info_sem_zona_neutra["Nome_time_casa"].value_counts()
    partidas_em_fora = df_partidas_info_sem_zona_neutra["Nome_time_fora"].value_counts()
    partidas_total = partidas_em_casa.add(partidas_em_fora, fill_value=0).sort_values(ascending=False)

    partidas_em_casa_array = pa.array(partidas_em_casa)
    partidas_em_fora_array = pa.array(partidas_em_fora)
    partidas_total_array = pa.array(partidas_total)


    # Média de gols casa vs fora
    media_de_gols_fora_por_time = gols_marcados_fora / partidas_em_fora
    media_de_gols_em_casa_por_time = gols_marcados_casa / partidas_em_casa
    
    df_casa_vs_fora = df_times[["Nome_time","Nome_curto_time","Sigla_time"]]
    df_casa_vs_fora = df_casa_vs_fora.set_index("Nome_time")
    df_casa_vs_fora["media_de_gols_fora"] = media_de_gols_fora_por_time
    df_casa_vs_fora["media_de_gols_casa"] = media_de_gols_em_casa_por_time

    tabela_casa_vs_fora = pa.Table.from_pandas(df_casa_vs_fora)
    pq.write_table(tabela_casa_vs_fora, caminho_analitcs / "casa_vs_fora.parquet")


    # Quantidade de empates
    filtro_empate = df_resultados_partidas["Vencedor_da_partida"] == "DRAW"
    numero_de_empates = df_resultados_partidas[filtro_empate].shape[0]


    # Jogos com mais gols
    jogos_com_mais_gols = df_resultados_partidas[["Nome_time_casa", "Nome_time_fora", "gols_na_partida"]].sort_values(by="gols_na_partida", ascending=False).head(10)
    tabela_jogos_coma_mais_gols = pa.Table.from_pandas(jogos_com_mais_gols)
    pq.write_table(tabela_jogos_coma_mais_gols, caminho_analitcs / "jogos_com_mais_gols.parquet")


    # Jogos decididos nos pênaltis
    filtro_penaltis = (df_resultados_partidas["Gols_casa_penaltis"].fillna(0) > 0) | (df_resultados_partidas["Gols_fora_penaltis"].fillna(0) > 0)
    jogos_decididos_penaltis = df_resultados_partidas[filtro_penaltis].shape[0]


    # Estruturação dos DataFrames finais para exportação limpa em Parquet
    df_analytics_partidas = pd.DataFrame({
        'partidas_em_casa': partidas_em_casa,
        'partidas_em_fora': partidas_em_fora,
        'partidas_total': partidas_total
    }).fillna(0).astype(int).reset_index()
    df_analytics_partidas.rename(columns={'index': 'time'}, inplace=True)
    tabela_partidas = pa.Table.from_pandas(df_analytics_partidas)

    df_analytics_gols = pd.DataFrame({
        'ordem_gols_marcados_casa': gols_marcados_casa, 
        'ordem_gols_marcados_fora': gols_marcados_fora,
        'gols_por_time': gols_por_time
    }).fillna(0).astype(int).reset_index()
    df_analytics_gols.rename(columns={'index': 'time'}, inplace=True)
    tabela_gols = pa.Table.from_pandas(df_analytics_gols)

    tabela_quantidade_de_partidas_por_fase = pa.Table.from_arrays(
        [partidas_por_fase_array],
        names=['partidas_por_fase']
    )

    df_analytics_times = pd.DataFrame({
        'total_vitorias': times_que_mais_venceram,    
        'vitorias_casa': mais_venceram_casa,       
        'vitorias_fora': mais_venceram_fora           
    }).fillna(0).astype(int).reset_index()
    df_analytics_times.rename(columns={'index': 'time'}, inplace=True)
    tabela_times = pa.Table.from_pandas(df_analytics_times)

    df_kpis_gerais = pd.DataFrame({
        'media_de_gols_por_partida': [media_de_gols_por_partida],
        'gols_total_da_competicao': [gols_total_da_competicao],
        'numero_de_empates': [numero_de_empates],
        'jogos_decididos_nos_penaltis': [jogos_decididos_penaltis]
    })
    tabela_kpis_gerais = pa.Table.from_pandas(df_kpis_gerais)

    # Salvando tabelas Parquet
    pq.write_table(tabela_times, caminho_analitcs / "analytics_times.parquet")
    pq.write_table(tabela_partidas, caminho_analitcs / "tabela_partidas.parquet")
    pq.write_table(tabela_gols, caminho_analitcs / "tabela_gols.parquet")
    pq.write_table(tabela_quantidade_de_partidas_por_fase, caminho_analitcs / "tabela_quantidade_de_partidas_por_fase.parquet")
    pq.write_table(tabela_kpis_gerais, caminho_analitcs / "kpis_gerais.parquet")


    #Criando pasta images
    caminho_images = Path("../data/analitics/images")

    # Grafico 1: Quantidade de Partidas por Fase
    plt.figure(figsize=(10, 5))
    quantidade_de_partidas_por_fase.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Quantidade de Partidas por Fase')
    plt.xlabel('Fases')
    plt.ylabel('Número de Partidas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(caminho_images / "grafico_partidas_por_fase.png")
    plt.show()

    # Grafico 2: Top 10 Times com Mais Vitórias (Barras Empilhadas)
    top_10_vitorias = df_analytics_times.sort_values(by='total_vitorias', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_vitorias['time'], top_10_vitorias['vitorias_casa'], label='Vitórias em Casa', color='royalblue')
    plt.bar(top_10_vitorias['time'], top_10_vitorias['vitorias_fora'], bottom=top_10_vitorias['vitorias_casa'], label='Vitórias Fora', color='orange')
    plt.title('Top 10 Times com Mais Vitórias (Casa vs Fora)')
    plt.xlabel('Times')
    plt.ylabel('Quantidade de Vitórias')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho_images / "grafico_top_10_vitorias.png")
    plt.show()

    # Grafico 3: Top 10 Times com Mais Gols na Competição
    top_10_gols = df_analytics_gols.sort_values(by='gols_por_time', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_gols['time'], top_10_gols['gols_por_time'], color='forestgreen', edgecolor='black')
    plt.title('Top 10 Times com Mais Gols na Competição')
    plt.xlabel('Times')
    plt.ylabel('Total de Gols')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(caminho_images / "grafico_top_10_gols.png")
    plt.show()
# %%
