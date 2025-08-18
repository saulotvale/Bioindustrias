import pandas as pd
import os

# Caminho da pasta com os arquivos CSV
pasta = r'C:\Users\Saulo Vale\Desktop\IPAM\abdi\comex\anual'

# Estados da Amazônia Legal
estados_aml = ['PA', 'MA', 'AM', 'AC', 'AP', 'RO', 'RR', 'TO', 'MT']

# Lista para armazenar DataFrames e log
dfs_filtrados = []
log_arquivos = []

# Percorrer os arquivos da pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
        
        # Verifica se colunas necessárias existem
        if {'SG_UF_NCM', 'CO_PAIS', 'CO_ANO', 'KG_LIQUIDO', 'VL_FOB'}.issubset(df.columns):
            df_filtrado = df[
                (df['SG_UF_NCM'].isin(estados_aml)) &
                (df['CO_PAIS'] == 249)
            ]
            dfs_filtrados.append(df_filtrado)
            log_arquivos.append(arquivo)

# Concatenar todos os dados filtrados
df_final = pd.concat(dfs_filtrados, ignore_index=True)

# Agrupar por ano e somar KG_LIQUIDO e VL_FOB
df_agrupado = df_final.groupby('CO_ANO')[['KG_LIQUIDO', 'VL_FOB']].sum().reset_index()

# Salvar resultado
df_agrupado.to_csv('soma_export_AML_EUA_por_ano.csv', index=False, sep=';', encoding='utf-8')

# Salvar log dos arquivos processados
with open('log_arquivos_processados_total_por_ano.txt', 'w', encoding='utf-8') as log:
    for nome in log_arquivos:
        log.write(nome + '\n')
