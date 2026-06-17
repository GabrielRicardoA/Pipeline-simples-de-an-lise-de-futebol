#%%
import os
from transform import transformar_dados
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

def carregar_dados():

    (           df_partidas,
                df_ano_da_competicao,
                df_resumo_competicao,
                df_competicao,
                df_resultados_partida,
                df_partidas_info,
                df_times
    ) = transformar_dados()


    #os para criar a pasta caso nao exista
    os.makedirs("../data/processed",exist_ok=True)

    #transformar de dataframe para pyarrow parquet

    partidas = pa.Table.from_pandas(df_partidas)

    ano_da_competicao = pa.Table.from_pandas(df_ano_da_competicao)

    resumo_competicao = pa.Table.from_pandas(df_resumo_competicao)

    competicao = pa.Table.from_pandas(df_competicao)

    resultados_partida = pa.Table.from_pandas(df_resultados_partida)

    partidas_info = pa.Table.from_pandas(df_partidas_info)

    times = pa.Table.from_pandas(df_times)


    caminho_processed = Path("../data/processed")

    pq.write_table(partidas,caminho_processed /"partidas.parquet" )

    pq.write_table(ano_da_competicao, caminho_processed /"ano_da_competicao.parquet")

    pq.write_table(resumo_competicao , caminho_processed / "resumo_competicao.parquet")

    pq.write_table(competicao,caminho_processed / "competicao.parquet")

    pq.write_table(resultados_partida, caminho_processed / "resultados_partida.parquet")

    pq.write_table(partidas_info , caminho_processed / "partidas_info.parquet")

    pq.write_table(times, caminho_processed / "times.parquet")


# %%
