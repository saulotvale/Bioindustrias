import pandas as pd

# 1. Carrega o Excel (CNPJs estão na coluna 0)
df_bio = pd.read_excel('base_2.3 maio 2025.xlsx', header=None, dtype={0: str})
df_bio[0] = df_bio[0].str.strip('"')

# 2. Carrega o CSV com os dados adicionais (usando colunas específicas)
df_empre = pd.read_csv('estab_merged.csv', encoding="utf-8", sep=";", usecols=[0, 1, 2], header=None, dtype={0: str})
df_empre[0] = df_empre[0].str.strip('"')

# 3. Cria um DataFrame auxiliar com apenas a primeira ocorrência de cada CNPJ no CSV
df_empre_first = df_empre.drop_duplicates(subset=0, keep='first').set_index(0)

# 4. Mapeia as colunas adicionais diretamente na base do Excel, mantendo o mesmo número de linhas
df_bio[100] = df_bio[0].map(df_empre_first[1])  # Coluna telefone (por ex)
df_bio[101] = df_bio[0].map(df_empre_first[2])


# 5. Salva no Excel sem cabeçalhos e sem alterar a ordem
df_bio.to_excel('base_com_merge_correto_3.xlsx', index=False, header=False)

print("Arquivo 'base_com_merge_correto_3.xlsx' criado com sucesso!")



