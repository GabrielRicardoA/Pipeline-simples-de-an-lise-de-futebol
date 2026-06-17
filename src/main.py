#%%
from extract import extrair_dados
from transform import transformar_dados
from load import carregar_dados
from analysis import analisar_dados_e_criar_graficos


def main():

    print("Iniciando extração...")
    extrair_dados()

    print("Iniciando transformação...")
    transformar_dados()

    print("Iniciando carga...")
    carregar_dados()

    print("Iniciando análise...")
    analisar_dados_e_criar_graficos()

    print("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
# %%
