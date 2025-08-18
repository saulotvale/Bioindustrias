import pandas as pd

# Ler o novo arquivo CSV
df_novo = pd.read_csv('EXP_2024.csv', sep=';', encoding='utf-8')

# Substitua 'valor_desejado' pelo valor que você está procurando na coluna 'SG_UF'
#valores_desejados = ['PA', 'MA']
valor_desejado = ['PA','MA','AM','AC','AP','RO','RR','TO','MT']

# Selecionar linhas com base nos valores desejados na coluna 'SG_UF'
df_selecionado = df_novo[df_novo['SG_UF_NCM'].isin(valor_desejado)]

# Selecionar linhas com base no valor desejado na coluna 'SG_UF'
#df_selecionado = df_novo[df_novo['nomeUF'] == valor_desejado]

# Exibir o DataFrame resultante
df_selecionado.to_csv('comex ncm só AML.csv', index=False, sep=';', encoding='utf-8')