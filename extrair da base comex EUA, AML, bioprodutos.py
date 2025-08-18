import pandas as pd
import os

# Caminho da pasta com os arquivos CSV
pasta = r'C:\Users\Saulo Vale\Desktop\IPAM\abdi\comex\anual'

# Estados da Amazônia Legal
estados_aml = ['PA', 'MA', 'AM', 'AC', 'AP', 'RO', 'RR', 'TO', 'MT']

# Lista de códigos CO_NCM permitidos (convertidos para string para evitar problemas com zeros à esquerda)
co_ncm_desejados = [
    '3011190', '3048930', '15119000', '3038932', '3048990', '3028990',
    '20089900', '21069090', '8134090', '62069000', '33074900', '3038920',
    '3038990', '7133590', '20089100', '20089710', '21069030', '7061000',
    '15152100', '8119000', '20098990', '21069010', '61082900', '35030019',
    '21050090', '9041100', '62046200', '33021000', '11063000', '12122900',
    '13021999', '3035400', '3024600', '3028922', '4090000', '33049910',
    '23099090', '12051090', '23099010', '42022220', '9012100', '3048910',
    '15159090', '61034900', '3055390', '20079921', '12129100', '3044920',
    '3061190', '22030000', '7133399', '18069000', '71179000', '15132120',
    '3038964', '3039990', '7070000', '7032010', '11062000', '13023990',
    '7096000', '7041000', '15081000', '13021400', '20079100', '17031000',
    '61044900', '71171900', '7089000', '61069000', '12129990', '12119090',
    '20081100', '7093000', '9011110', '18063210', '19059020', '3028910',
    '19021900', '8135000', '3044990', '9101100', '21041011', '7020000',
    '3032300', '61091000', '3038953', '3049900', '12074090', '3028938',
    '44041000', '34024200', '19022000', '20057000', '20021000', '33011990',
    '6029089', '20052000', '7051900', '3048600', '19041000', '7099300',
    '21012010', '61130000', '33011300', '21039099', '7133190', '22085000',
    '19019090', '7129090', '12079990', '63079090', '20079990', '96020090',
    '8031000', '8013100', '61045100', '8083000', '7133990'
]

# Lista para armazenar os DataFrames filtrados e log dos arquivos processados
dfs_filtrados = []
log_arquivos = []

# Percorrer todos os arquivos .csv na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(pasta, arquivo)
        
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
        
        # Verifica se as colunas necessárias existem
        if {'SG_UF_NCM', 'CO_PAIS', 'CO_NCM'}.issubset(df.columns):
            # Garante que CO_NCM está como string
            df['CO_NCM'] = df['CO_NCM'].astype(str).str.strip()
            
            df_filtrado = df[
                (df['SG_UF_NCM'].isin(estados_aml)) &
                (df['CO_PAIS'] == 249) &
                (df['CO_NCM'].isin(co_ncm_desejados))
            ]
            
            dfs_filtrados.append(df_filtrado)
            log_arquivos.append(arquivo)

# Concatenar todos os dados filtrados
df_final = pd.concat(dfs_filtrados, ignore_index=True)

# Salvar o resultado filtrado
df_final.to_csv('comex_filtrado_AML_EUA_NCM.csv', index=False, sep=';', encoding='utf-8')

# Salvar log dos arquivos processados
with open('log_arquivos_processados.txt', 'w', encoding='utf-8') as log:
    for nome in log_arquivos:
        log.write(nome + '\n')
